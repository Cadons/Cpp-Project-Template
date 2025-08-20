# C++ Project Template

Welcome to the **C++ Template** — a flexible and extensible starting point for developing modern C++ applications. This template streamlines project organization, dependency management, and build configuration, following a modular and maintainable structure.

---

## 🔧 Features

* **Project Structure**

    * `app/`: Contains executable targets.
    * `lib/`: Contains libraries (static or shared).
    * Each module includes a `test/` folder with unit tests (built as executables, but not part of `app/`).

* **Package Management**

    * Currently supports **vcpkg**.
    * Future support planned for **Conan** and others.

* **Tooling**

    * Built-in toolset to:

        * Create new modules
        * Add new source files
        * Synchronize with Git (using subtrees)

* **Build System**

    * CMake-based
    * Source list synchronization (no globbing)
    * Optional support for Qt and Vcpkg integrations

---

## 🚀 Getting Started

### 1. Configure the Project

Run the configuration script based on your OS:

* **Windows**: `configure.bat`
* **Linux/macOS**: `configure.sh`

Follow the interactive prompts to fill out project metadata. This information is stored in the `project.json` file in the root directory.

The configuration process generates:

* Initial `app/` and `lib/` structures
* Boilerplate files like `CMakeLists.txt`, `project.json`, etc.

---

### 2. Using the Toolset

The `tools/dev_tools.py` script provides interactive commands for managing your project.

To launch:

```bash
python tools/dev_tools.py
```

Use the help menu for available commands and usage instructions.

You can:

* Create modules
* Add new files
* Synchronize Git subtrees

For projects with shared libraries across repositories, we recommend using **Git subtrees** over submodules for better integration.

---

### 3. Adding Source Files

Instead of relying on CMake source globbing, this template maintains a curated list of source files per module.

To update this list, use the `fast_sources` script located at:

* **Windows**: `tools/cli/windows/fast_sources.bat`
* **Unix/Linux/macOS**: `tools/cli/unix/fast_sources.sh`

Run it after adding or removing files to ensure CMake files stay in sync.

---

## 🛠 Versioning

Versions are managed in:

* `project.json` – project-level version
* `module.json` – individual module versions

CMake reads these values during the build process to apply the correct versioning.

---

## ✏️ Customization

You are encouraged to tailor the template to your specific needs:

* Modify templates in the `.resources/templates` folder.
* Extend the tools or add new features.

If your changes could benefit others, feel free to open a **merge request** to the template repository.

---

## 📁 Folder Structure

```
.
├── app/                # Executables
│       ├── src/
│       ├── include/
│       ├── resources/
│       ├── test/
│       └── module.json
│       └── CMakeLists.json
├── lib/                # Libraries
│   └── module/         
│       ├── src/
│       ├── include/
│       ├── resources/
│       ├── test/
│       └── module.json
│       └── CMakeLists.json
├── cmake/              # CMake utilities and helpers
├── tools/              # Tooling scripts and CLI utilities
├── resources/          # File and template resources
├── configure.sh/bat    # Initial project setup
├── project.json        # Project metadata
└── CMakeLists.txt
```

---

## 📌 Notes

* This template enforces a consistent structure — please follow it for compatibility.
* Utility functions in `cmake/` provide extended support for Qt, Vcpkg, and modular builds.
