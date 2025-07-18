# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.2] - 2025-01-18 - Packaging and Integration Fixes

### Fixed
- Fixed setup.py version reading mechanism that was always defaulting to "1.0.0"
  - Changed version file path from `Path(__file__).parent / "__init__.py"` to `Path(__file__).parent / "project_tools" / "__init__.py"`
  - Version is now correctly read from the actual package __init__.py file
- Added missing CLI dependencies (colorama, tabulate) to setup.py install_requires
  - CLI functionality now works correctly after installation via setup.py
  - Prevents ImportError when using console formatting features
- Added missing subpackages (intelligence, web_gui) to pyproject.toml packages list
  - `project_tools.intelligence` module now included in built packages
  - `project_tools.web_gui` and `project_tools.web_gui.api` modules now included
  - Prevents ModuleNotFoundError when accessing intelligence or web GUI features
- Fixed CLI method signature mismatches causing runtime errors
  - Fixed `format_todos_table()` calls to pass `(todo_manager, status)` instead of `(todos_list)`
  - Fixed `format_combined_status()` calls to pass manager instances instead of properties
  - Fixed HTML export in CLI to use simple table generation instead of calling formatter with wrong signature
- Resolved runtime errors in CLI formatter integration

### Added
- Comprehensive test suite for package installation, CLI commands, and Python API
  - `tests/conftest.py` - Pytest configuration and shared fixtures for isolated testing
  - `tests/test_packaging.py` - Package installation and import validation tests
  - `tests/test_cli_integration.py` - CLI command integration and error handling tests
  - `tests/test_api_integration.py` - Python API functionality and workflow tests
  - `tests/test_web_gui.py` - Web GUI smoke tests and Flask app validation
  - `tests/test_cleanup.py` - Complete cleanup and uninstall validation
  - `tests/fixtures/` - Sample data for testing (todo.json, changelog.json)
  - `tests/utils/` - Test utilities and helper functions
- Hermetic testing with virtual environment isolation
  - Each test runs in isolated virtual environment to prevent cross-contamination
  - Complete install → test → uninstall cycle validation
  - Tests validate that no traces remain after uninstall
- GitHub Actions workflow for automated testing across Python versions
  - `.github/workflows/test.yml` - Comprehensive CI/CD pipeline
  - Tests across Python 3.8-3.12 on Ubuntu, Windows, and macOS
  - Separate jobs for packaging, CLI, API, web GUI, and cleanup testing
  - Full workflow validation from installation to uninstall
- Tox configuration for local multi-environment testing
  - `tox.ini` - Support for testing across multiple Python versions locally
  - Separate environments for different test types (packaging, cli, api, web, cleanup)
  - Linting and formatting environments for code quality
  - Development environment with all dependencies

### Improved
- Package installation reliability across different methods (pip, wheel, GitHub)
  - Installation now works consistently via `pip install -e .`, wheel files, and GitHub URLs
  - All required dependencies are properly declared and installed
  - Console script entry points are correctly configured
- CLI error handling and output formatting
  - Console formatting no longer crashes with method signature errors
  - Improved error messages for invalid commands and missing files
  - Better handling of edge cases in CLI workflows
- Documentation alignment with actual implementation
  - All documented API methods and CLI commands now work as advertised
  - Test suite validates that every documented feature is functional
  - Comprehensive validation prevents documentation drift
- Development workflow with automated testing
  - Developers can now run `tox` to test across multiple Python versions locally
  - GitHub Actions provide automated validation for all pull requests
  - Comprehensive test coverage ensures reliability

### Breaking Changes
None - all changes are backward compatible fixes.

### Technical Details
This release focuses on fixing critical packaging and integration issues that prevented proper installation and testing of the project_tools package. The changes ensure that:

1. **Version Reading Works**: The package version is correctly read from the project_tools/__init__.py file instead of looking for a non-existent root __init__.py
2. **Dependencies Are Complete**: All required dependencies (colorama, tabulate) are included in both setup.py and pyproject.toml
3. **Packages Are Complete**: All submodules (intelligence, web_gui) are included in the built package
4. **CLI Functions Correctly**: Method signature mismatches that caused runtime errors have been resolved
5. **Testing Is Comprehensive**: Full test suite validates installation, functionality, and cleanup across multiple environments

The test suite provides hermetic validation that installs the package from GitHub, tests all interfaces (CLI, Python API, Web GUI), and ensures complete cleanup with no system pollution.

---

## [1.2.1] - 2023-XX-XX (Previous Release)

### Fixed
- Various bug fixes and improvements (details from git history)

### Added  
- Web GUI front-end implementation
- Flask dependencies and web console script

---

*Note: This changelog documents the comprehensive cleanup and testing improvements. Previous release history can be found in git commit messages.*