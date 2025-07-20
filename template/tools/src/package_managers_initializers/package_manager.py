import os
import re
import subprocess
from abc import ABC, abstractmethod

from rich.console import Console
from rich.prompt import IntPrompt

console = Console()

class PackageManager(ABC):
    """
    Base class for package managers.
    """

    def __init__(self, name: str):
        self.name = name
        self.vcpkg_location = "${VCPKG_ROOT}"
        if os.name != 'nt':
            vcpkg_path = os.popen("which vcpkg").read().strip()
            if vcpkg_path:
                self.find_vcpkg_root(vcpkg_path)
            else:
                console.print("[bold red]VCPKG not found. Please ensure vcpkg is installed and configured correctly.[/bold red]")
                exit(1)

    def find_vcpkg_root(self, vcpkg_path):
        if vcpkg_path:
            vcpkg_dir = os.path.dirname(os.path.abspath(vcpkg_path))
            self.vcpkg_location = vcpkg_dir
            return self.vcpkg_location
        return None

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def configure_cmake_presets(self):
        pass

    @staticmethod
    def list_generators():
        """
        Get list of available CMake generators, excluding specific IDE generators.

        Returns:
            list: List of available CMake generator names
        """
        output = PackageManager._get_cmake_help_output()
        if not output:
            return []

        return PackageManager._parse_generators(output)

    @staticmethod
    def _get_cmake_help_output():
        """
        Execute cmake --help command and return its output.

        Returns:
            str: Command output or empty string on error
        """
        try:
            return subprocess.check_output(
                ['cmake', '--help'],
                universal_newlines=True
            )
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def _parse_generators(cmake_output):
        """
        Parse cmake help output to extract generator names.

        Args:
            cmake_output (str): Output from cmake --help command

        Returns:
            list: List of generator names
        """
        generators = []

        # Find the generators section
        lines = cmake_output.splitlines()
        try:
            generators_start = next(
                i for i, line in enumerate(lines)
                if "Generators" in line
            )
            # Skip the header line
            generators_start += 2
        except StopIteration:
            return []

        # Parse generator entries
        for line in lines[generators_start:]:
            if not line.strip():
                break

            match = re.match(r'^\s*(\S.+?)\s+=', line)
            if not match:
                continue

            generator = match.group(1).replace("*", "").strip()
            generators.append(generator)

        return generators

    def generate_cmake_user_presets(self, inherit_from):
        generators = PackageManager.list_generators()
        if not generators:
            console.print("[bold red]No CMake generators found.[/bold red]")
            return

        cmake_presets_json = {
            "version": 3,
            "configurePresets": [],
            "buildPresets": [],
        }
        cpus = os.cpu_count() or 4

        console.print("[bold green]Available CMake Generators:[/bold green]")
        for idx, generator in enumerate(generators, 1):
            console.print(f"[cyan]{idx}[/cyan]. {generator}")

        console.print("[yellow]Warning: Be sure that the selected generator is available on your machine[/yellow]")

        selected_preset = None
        while selected_preset is None:
            try:
                selected_idx = IntPrompt.ask("Select generator number", choices=[str(i) for i in range(1, len(generators) + 1)])
                selected_preset = generators[selected_idx - 1]
            except (ValueError, IndexError):
                console.print("[red]Invalid selection. Please choose a valid number.[/red]")

        for generator in generators:
            cmake_presets_json["configurePresets"].append({
                "name": generator,
                "hidden": selected_preset != generator,
                "generator": generator,
                "inherits": inherit_from,
                "cacheVariables": {
                    "CMAKE_TOOLCHAIN_FILE": f"{self.vcpkg_location}/scripts/buildsystems/vcpkg.cmake",
                }
            })
            cmake_presets_json["buildPresets"].append({
                "name": f"{generator} Debug",
                "hidden": selected_preset != generator,
                "configurePreset": generator,
                "configuration": "Debug",
                "jobs": cpus,
            })
            cmake_presets_json["buildPresets"].append({
                "name": f"{generator} Release",
                "hidden": selected_preset != generator,
                "configurePreset": generator,
                "configuration": "Release",
                "jobs": cpus,
            })

        cmake_user_presets_path = os.path.join(os.getcwd(), "CMakeUserPresets.json")
        import json
        with open(cmake_user_presets_path, 'w') as f:
            json.dump(cmake_presets_json, f, indent=2)

        console.print(f"[bold green]CMake user presets generated at[/bold green] {cmake_user_presets_path}")
