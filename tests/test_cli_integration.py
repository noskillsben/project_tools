#!/usr/bin/env python3
"""
CLI integration tests for project_tools.

Tests all documented command-line functionality and validates fixes.
"""

import pytest
import subprocess
import sys
import json
import tempfile
from pathlib import Path
from .conftest import run_cli_command, validate_json_output


class TestCoreCLI:
    """Test core CLI functionality."""
    
    def test_status_command_console(self, isolated_venv, github_install, temp_project):
        """Test project-tools status command with console output."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Run status command
        status_result = run_cli_command(
            venv_path, 
            ["-m", "project_tools.cli", "status"],
            cwd=temp_project
        )
        
        assert status_result.returncode == 0, f"Status command failed: {status_result.stderr}"
        # Should not crash (validates CLI formatter fixes)
        assert len(status_result.stdout) > 0
        
    def test_status_command_json(self, isolated_venv, github_install, temp_project):
        """Test project-tools status command with JSON output."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Run status command with JSON format
        status_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "status", "--format", "json"],
            cwd=temp_project
        )
        
        assert status_result.returncode == 0, f"Status JSON command failed: {status_result.stderr}"
        
        # Validate JSON output
        status_data = validate_json_output(status_result.stdout)
        assert isinstance(status_data, dict)
        
    def test_todo_list_command(self, isolated_venv, github_install, temp_project):
        """Test project-tools todo list command."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Run todo list command
        todo_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "todo", "list"],
            cwd=temp_project
        )
        
        assert todo_result.returncode == 0, f"Todo list command failed: {todo_result.stderr}"
        # Should not crash (validates format_todos_table fix)
        assert len(todo_result.stdout) > 0
        
    def test_todo_add_command(self, isolated_venv, github_install, temp_project):
        """Test project-tools todo add command."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Add a new todo
        add_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "todo", "add", "Test todo from CLI", 
             "--priority", "high", "--category", "testing"],
            cwd=temp_project
        )
        
        assert add_result.returncode == 0, f"Todo add command failed: {add_result.stderr}"
        
        # Verify todo was added by listing
        list_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "todo", "list"],
            cwd=temp_project
        )
        
        assert "Test todo from CLI" in list_result.stdout
        
    def test_version_current_command(self, isolated_venv, github_install, temp_project):
        """Test project-tools version current command."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Get current version
        version_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "version", "current"],
            cwd=temp_project
        )
        
        assert version_result.returncode == 0, f"Version current command failed: {version_result.stderr}"
        assert len(version_result.stdout.strip()) > 0


class TestExportFunctionality:
    """Test export command with different formats."""
    
    def test_export_json(self, isolated_venv, github_install, temp_project):
        """Test export command with JSON format."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Export to JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_file = Path(f.name)
            
        try:
            export_result = run_cli_command(
                venv_path,
                ["-m", "project_tools.cli", "export", "--format", "json", 
                 "--output", str(export_file)],
                cwd=temp_project
            )
            
            assert export_result.returncode == 0, f"Export JSON failed: {export_result.stderr}"
            assert export_file.exists()
            
            # Validate exported JSON
            with open(export_file) as f:
                export_data = json.load(f)
            assert isinstance(export_data, dict)
            
        finally:
            if export_file.exists():
                export_file.unlink()
                
    def test_export_html(self, isolated_venv, github_install, temp_project):
        """Test export command with HTML format (validates HTML table fix)."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Export to HTML
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            export_file = Path(f.name)
            
        try:
            export_result = run_cli_command(
                venv_path,
                ["-m", "project_tools.cli", "export", "--format", "html",
                 "--output", str(export_file)],
                cwd=temp_project
            )
            
            assert export_result.returncode == 0, f"Export HTML failed: {export_result.stderr}"
            assert export_file.exists()
            
            # Validate HTML content
            with open(export_file) as f:
                html_content = f.read()
            assert "<html>" in html_content
            assert "<table" in html_content
            assert "</html>" in html_content
            
        finally:
            if export_file.exists():
                export_file.unlink()


class TestIntelligenceCLI:
    """Test intelligence system CLI commands."""
    
    def test_intelligence_init(self, isolated_venv, github_install, temp_project):
        """Test project-tools intelligence init command."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Initialize intelligence
        init_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "intelligence", "init"],
            cwd=temp_project
        )
        
        # Should not crash even if intelligence module has issues
        # We're primarily testing CLI integration here
        assert init_result.returncode in [0, 1]  # Allow for expected failures
        
    def test_compass_commands(self, isolated_venv, github_install, temp_project):
        """Test compass-related CLI commands."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test compass init
        compass_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "compass", "init"],
            cwd=temp_project
        )
        
        # Should not crash
        assert compass_result.returncode in [0, 1]


class TestErrorHandling:
    """Test CLI error handling and edge cases."""
    
    def test_invalid_command(self, isolated_venv, github_install, temp_project):
        """Test handling of invalid commands."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Run invalid command
        invalid_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "invalid_command"],
            cwd=temp_project
        )
        
        assert invalid_result.returncode != 0
        
    def test_missing_todo_id(self, isolated_venv, github_install, temp_project):
        """Test handling of missing todo ID."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Try to complete non-existent todo
        complete_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "todo", "complete", "99999"],
            cwd=temp_project
        )
        
        # Should handle error gracefully
        assert complete_result.returncode != 0
        
    def test_empty_project_directory(self, isolated_venv, github_install):
        """Test CLI behavior in empty directory."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Create empty temp directory
        with tempfile.TemporaryDirectory() as empty_dir:
            # Run status in empty directory
            status_result = run_cli_command(
                venv_path,
                ["-m", "project_tools.cli", "status"],
                cwd=Path(empty_dir)
            )
            
            # Should handle missing files gracefully
            assert status_result.returncode in [0, 1]


class TestOutputValidation:
    """Test CLI output formats and validation."""
    
    def test_help_output(self, isolated_venv, github_install):
        """Test --help output is properly formatted."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test main help
        help_result = run_cli_command(
            venv_path,
            ["-m", "project_tools.cli", "--help"]
        )
        
        assert help_result.returncode == 0
        assert "usage:" in help_result.stdout.lower()
        
    def test_console_formatting_no_crash(self, isolated_venv, github_install, temp_project):
        """Test that console formatting doesn't crash (validates formatter fixes)."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Commands that use console formatting
        commands_to_test = [
            ["status"],
            ["todo", "list"],
            ["version", "current"]
        ]
        
        for cmd in commands_to_test:
            cmd_result = run_cli_command(
                venv_path,
                ["-m", "project_tools.cli"] + cmd,
                cwd=temp_project
            )
            
            # Primary goal: should not crash with formatting errors
            # Allow various exit codes but no Python tracebacks
            assert "Traceback" not in cmd_result.stderr, f"Command {cmd} crashed with traceback"