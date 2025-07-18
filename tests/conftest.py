#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures for project_tools testing.

Provides isolated virtual environments and test utilities for hermetic testing.
"""

import pytest
import tempfile
import shutil
import subprocess
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, Generator


@pytest.fixture
def isolated_venv():
    """
    Create an isolated virtual environment for testing package installation.
    
    Yields:
        Path to the virtual environment directory
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / "test_venv"
        
        # Create virtual environment
        subprocess.run([
            sys.executable, "-m", "venv", str(venv_path)
        ], check=True)
        
        yield venv_path
        
        # Cleanup is automatic with tempfile.TemporaryDirectory


@pytest.fixture
def temp_project():
    """
    Create a temporary project directory with sample todo.json and changelog.json.
    
    Yields:
        Path to the temporary project directory
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / "test_project"
        project_path.mkdir()
        
        # Create sample todo.json
        todo_data = {
            "todos": [
                {
                    "id": 1,
                    "title": "Test todo 1",
                    "status": "pending",
                    "priority": "high",
                    "category": "development"
                },
                {
                    "id": 2,
                    "title": "Test todo 2", 
                    "status": "completed",
                    "priority": "medium",
                    "category": "testing"
                }
            ]
        }
        
        with open(project_path / "todo.json", "w") as f:
            json.dump(todo_data, f, indent=2)
            
        # Create sample changelog.json
        changelog_data = {
            "versions": [
                {
                    "version": "1.0.0",
                    "date": "2023-01-01",
                    "changes": [
                        {
                            "type": "feat",
                            "description": "Initial release"
                        }
                    ]
                }
            ]
        }
        
        with open(project_path / "changelog.json", "w") as f:
            json.dump(changelog_data, f, indent=2)
            
        yield project_path


@pytest.fixture
def github_install():
    """
    Fixture for testing GitHub installation in isolated environment.
    
    Returns:
        Function that performs GitHub installation in given venv
    """
    def install_from_github(venv_path: Path, repo_url: str = None):
        """Install package from GitHub in the given virtual environment."""
        if repo_url is None:
            # Default to current repository
            repo_url = "git+https://github.com/yourusername/project-tools.git"
            
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
            python_path = venv_path / "bin" / "python"
            
        # Install package from GitHub
        result = subprocess.run([
            str(pip_path), "install", repo_url
        ], capture_output=True, text=True)
        
        return result, python_path, pip_path
        
    return install_from_github


@pytest.fixture 
def package_cleanup():
    """
    Fixture for ensuring complete package cleanup and uninstall.
    
    Returns:
        Function that performs complete cleanup
    """
    def cleanup(venv_path: Path, package_name: str = "project-tools"):
        """Uninstall package and validate complete removal."""
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            pip_path = venv_path / "bin" / "pip" 
            python_path = venv_path / "bin" / "python"
            
        # Uninstall package
        uninstall_result = subprocess.run([
            str(pip_path), "uninstall", "-y", package_name
        ], capture_output=True, text=True)
        
        # Test that import fails
        import_test = subprocess.run([
            str(python_path), "-c", "import project_tools"
        ], capture_output=True, text=True)
        
        return uninstall_result, import_test
        
    return cleanup


@pytest.fixture
def sample_intelligence_data():
    """
    Provide sample intelligence system data for testing.
    
    Returns:
        Dictionary containing sample intelligence data
    """
    return {
        "compass": {
            "vision": "Test project vision",
            "mission": "Test project mission", 
            "values": ["test", "quality", "reliability"]
        },
        "direction": {
            "current_direction": "Testing implementation",
            "assumptions": ["Tests will pass", "Code is correct"],
            "pivots": []
        },
        "reflection": {
            "lessons_learned": ["Testing is important"],
            "energy_levels": {"high": 0.8, "medium": 0.2, "low": 0.0}
        }
    }


def run_cli_command(venv_path: Path, command: list, cwd: Path = None):
    """
    Utility function to run CLI commands in isolated environment.
    
    Args:
        venv_path: Path to virtual environment
        command: Command list to execute
        cwd: Working directory for command
        
    Returns:
        subprocess.CompletedProcess result
    """
    if sys.platform == "win32":
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        python_path = venv_path / "bin" / "python"
        
    full_command = [str(python_path)] + command
    
    return subprocess.run(
        full_command,
        capture_output=True,
        text=True,
        cwd=cwd
    )


def validate_json_output(output: str) -> Dict[Any, Any]:
    """
    Validate and parse JSON output from CLI commands.
    
    Args:
        output: JSON string output
        
    Returns:
        Parsed JSON data
        
    Raises:
        ValueError: If output is not valid JSON
    """
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON output: {e}")


def validate_package_structure(venv_path: Path):
    """
    Validate that all expected package components are installed.
    
    Args:
        venv_path: Path to virtual environment
        
    Returns:
        Dictionary with validation results
    """
    if sys.platform == "win32":
        python_path = venv_path / "Scripts" / "python.exe"
        site_packages = venv_path / "Lib" / "site-packages"
    else:
        python_path = venv_path / "bin" / "python"
        site_packages = venv_path / "lib" / "python*/site-packages"
        
    results = {}
    
    # Test main import
    main_import = subprocess.run([
        str(python_path), "-c", "import project_tools; print(project_tools.__version__)"
    ], capture_output=True, text=True)
    results["main_import"] = main_import.returncode == 0
    results["version"] = main_import.stdout.strip() if main_import.returncode == 0 else None
    
    # Test submodule imports
    submodules = [
        "project_tools.formatters",
        "project_tools.intelligence", 
        "project_tools.web_gui"
    ]
    
    for module in submodules:
        import_test = subprocess.run([
            str(python_path), "-c", f"import {module}"
        ], capture_output=True, text=True)
        results[f"{module}_import"] = import_test.returncode == 0
        
    return results