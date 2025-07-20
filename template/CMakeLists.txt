message(STATUS "test-project by cadonslab - 1.0.0")
cmake_minimum_required(VERSION 3.23)

project(test-project
    VERSION 1.0.0
    DESCRIPTION "A monorepo project"
    LANGUAGES CXX
)

# Organization info
set(PROJECT_ORG_NAME "cadonslab")
set(PROJECT_ORG_URL "https://example.com")

# Prefer Ninja if not explicitly specified

if(NOT CMAKE_GENERATOR)
    message(STATUS "No generator specified. Consider using Ninja for faster builds.")
endif()


# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Default build type
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the build type." FORCE)
endif()

# Enable IDE folder grouping
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Add extra cmake modules (optional)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
include(common OPTIONAL)

# Compiler warnings
if(MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -pedantic -Werror)
endif()

# Testing
include(CTest)
enable_testing()

# Version header generation
configure_file(
    ${CMAKE_SOURCE_DIR}/cmake/version.h.in
    ${CMAKE_BINARY_DIR}/generated/version.h
    @ONLY
)

# === Add subdirectories ===

add_subdirectory(app)

add_subdirectory(lib)
