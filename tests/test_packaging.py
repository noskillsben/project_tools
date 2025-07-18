#!/usr/bin/env python3
"""
Comprehensive packaging tests for project_tools.

Tests installation, imports, version consistency, and dependencies.
"""

import pytest
import subprocess
import sys
from pathlib import Path
from .conftest import validate_package_structure, run_cli_command


class TestPackageInstallation:
    """Test package installation from various sources."""
    
    def test_editable_install(self, isolated_venv, temp_project):
        """Test pip install -e . installation."""
        venv_path = isolated_venv
        
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
            python_path = venv_path / "bin" / "python"
            
        # Install in editable mode
        repo_root = Path(__file__).parent.parent
        result = subprocess.run([
            str(pip_path), "install", "-e", str(repo_root)
        ], capture_output=True, text=True)
        
        assert result.returncode == 0, f"Editable install failed: {result.stderr}"
        
        # Validate installation
        validation = validate_package_structure(venv_path)
        assert validation["main_import"], "Main import failed"
        assert validation["version"] != "1.0.0", "Version still defaulting to 1.0.0"
        
    def test_wheel_install(self, isolated_venv):
        """Test wheel building and installation."""
        venv_path = isolated_venv
        
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
            python_path = venv_path / "bin" / "python"
            
        # Install build dependencies
        subprocess.run([
            str(pip_path), "install", "build"
        ], check=True)
        
        # Build wheel
        repo_root = Path(__file__).parent.parent
        build_result = subprocess.run([
            str(python_path), "-m", "build", "--wheel", str(repo_root)
        ], capture_output=True, text=True, cwd=repo_root)
        
        assert build_result.returncode == 0, f"Wheel build failed: {build_result.stderr}"
        
        # Find wheel file
        dist_dir = repo_root / "dist"
        wheel_files = list(dist_dir.glob("*.whl"))
        assert len(wheel_files) > 0, "No wheel files found"
        
        # Install wheel
        install_result = subprocess.run([
            str(pip_path), "install", str(wheel_files[0])
        ], capture_output=True, text=True)
        
        assert install_result.returncode == 0, f"Wheel install failed: {install_result.stderr}"
        
        # Validate installation
        validation = validate_package_structure(venv_path)
        assert validation["main_import"], "Main import failed"


class TestImports:
    """Test all module imports work correctly."""
    
    def test_main_import(self, isolated_venv, github_install):
        """Test main project_tools import."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available, using local install")
            
        # Test main import
        import_result = subprocess.run([
            str(python_path), "-c", 
            "import project_tools; print('Import successful')"
        ], capture_output=True, text=True)
        
        assert import_result.returncode == 0, f"Main import failed: {import_result.stderr}"
        assert "Import successful" in import_result.stdout
        
    def test_project_manager_import(self, isolated_venv, github_install):
        """Test ProjectManager import."""
        venv_path = isolated_venv
        
        # Install package (skip if GitHub not available)
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test ProjectManager import
        import_result = subprocess.run([
            str(python_path), "-c",
            "from project_tools import ProjectManager; print('ProjectManager imported')"
        ], capture_output=True, text=True)
        
        assert import_result.returncode == 0, f"ProjectManager import failed: {import_result.stderr}"
        
    def test_submodule_imports(self, isolated_venv, github_install):
        """Test all submodule imports."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        submodules = [
            "project_tools.intelligence",
            "project_tools.web_gui", 
            "project_tools.formatters"
        ]
        
        for module in submodules:
            import_result = subprocess.run([
                str(python_path), "-c", f"import {module}; print('{module} imported')"
            ], capture_output=True, text=True)
            
            assert import_result.returncode == 0, f"{module} import failed: {import_result.stderr}"


class TestVersionConsistency:
    """Test version reading and consistency."""
    
    def test_version_not_default(self, isolated_venv, github_install):
        """Test that version is not the default 1.0.0."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Check version
        version_result = subprocess.run([
            str(python_path), "-c", 
            "import project_tools; print(project_tools.__version__)"
        ], capture_output=True, text=True)
        
        assert version_result.returncode == 0, f"Version check failed: {version_result.stderr}"
        version = version_result.stdout.strip()
        assert version != "1.0.0", f"Version still defaulting to 1.0.0, got: {version}"


class TestDependencies:
    """Test that all required dependencies are installed."""
    
    def test_cli_dependencies(self, isolated_venv, github_install):
        """Test colorama and tabulate are available."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test colorama
        colorama_result = subprocess.run([
            str(python_path), "-c", "import colorama; print('colorama available')"
        ], capture_output=True, text=True)
        
        assert colorama_result.returncode == 0, "colorama not available"
        
        # Test tabulate
        tabulate_result = subprocess.run([
            str(python_path), "-c", "import tabulate; print('tabulate available')"
        ], capture_output=True, text=True)
        
        assert tabulate_result.returncode == 0, "tabulate not available"
        
    def test_web_dependencies(self, isolated_venv, github_install):
        """Test Flask and related dependencies are available."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        web_deps = ["Flask", "flask_cors", "flask_socketio"]
        
        for dep in web_deps:
            dep_result = subprocess.run([
                str(python_path), "-c", f"import {dep}; print('{dep} available')"
            ], capture_output=True, text=True)
            
            assert dep_result.returncode == 0, f"{dep} not available"


class TestConsoleScripts:
    """Test console script entry points."""
    
    def test_project_tools_command(self, isolated_venv, github_install):
        """Test project-tools command is available."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test project-tools --help
        if sys.platform == "win32":
            cmd_path = venv_path / "Scripts" / "project-tools.exe"
        else:
            cmd_path = venv_path / "bin" / "project-tools"
            
        help_result = subprocess.run([
            str(cmd_path), "--help"
        ], capture_output=True, text=True)
        
        assert help_result.returncode == 0, f"project-tools command failed: {help_result.stderr}"
        assert "project-tools" in help_result.stdout.lower()
        
    def test_project_tools_web_command(self, isolated_venv, github_install):
        """Test project-tools-web command is available."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test project-tools-web --help
        if sys.platform == "win32":
            cmd_path = venv_path / "Scripts" / "project-tools-web.exe"
        else:
            cmd_path = venv_path / "bin" / "project-tools-web"
            
        help_result = subprocess.run([
            str(cmd_path), "--help"
        ], capture_output=True, text=True)
        
        assert help_result.returncode == 0, f"project-tools-web command failed: {help_result.stderr}"