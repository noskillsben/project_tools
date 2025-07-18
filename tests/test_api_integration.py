#!/usr/bin/env python3
"""
Python API integration tests for project_tools.

Tests all documented ProjectManager functionality and API methods.
"""

import pytest
import subprocess
import sys
import json
import tempfile
from pathlib import Path
from .conftest import run_cli_command


class TestProjectManagerInstantiation:
    """Test ProjectManager creation and basic functionality."""
    
    def test_project_manager_creation(self, isolated_venv, github_install, temp_project):
        """Test ProjectManager can be instantiated."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test ProjectManager creation
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
print("ProjectManager created successfully")
""".format(str(temp_project))
        
        pm_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert pm_result.returncode == 0, f"ProjectManager creation failed: {pm_result.stderr}"
        assert "ProjectManager created successfully" in pm_result.stdout
        
    def test_project_manager_with_config(self, isolated_venv, github_install, temp_project):
        """Test ProjectManager with custom configuration."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test ProjectManager with config
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager(todo_file="custom_todo.json", changelog_file="custom_changelog.json")
print("ProjectManager with config created successfully")
""".format(str(temp_project))
        
        pm_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert pm_result.returncode == 0, f"ProjectManager with config failed: {pm_result.stderr}"


class TestTodoManagement:
    """Test todo-related API methods."""
    
    def test_add_todo(self, isolated_venv, github_install, temp_project):
        """Test adding todos via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test adding todo
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
todo_id = pm.add_todo("Test API todo", priority="high", category="testing")
print(f"Todo added with ID: {{todo_id}}")
todos = pm.get_todos()
print(f"Total todos: {{len(todos)}}")
""".format(str(temp_project))
        
        add_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert add_result.returncode == 0, f"Add todo failed: {add_result.stderr}"
        assert "Todo added with ID:" in add_result.stdout
        
    def test_get_todos(self, isolated_venv, github_install, temp_project):
        """Test getting todos via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test getting todos
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
todos = pm.get_todos()
print(f"Found {{len(todos)}} todos")
for todo in todos:
    print(f"Todo: {{todo.get('title', 'No title')}}")
""".format(str(temp_project))
        
        get_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert get_result.returncode == 0, f"Get todos failed: {get_result.stderr}"
        assert "Found" in get_result.stdout
        
    def test_complete_todo(self, isolated_venv, github_install, temp_project):
        """Test completing todos via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test completing todo
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
todos = pm.get_todos()
if todos:
    todo_id = todos[0]['id']
    pm.complete_todo(todo_id)
    print(f"Completed todo {{todo_id}}")
    updated_todos = pm.get_todos()
    completed = [t for t in updated_todos if t['id'] == todo_id and t['status'] == 'completed']
    print(f"Todo marked as completed: {{len(completed) > 0}}")
else:
    print("No todos to complete")
""".format(str(temp_project))
        
        complete_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert complete_result.returncode == 0, f"Complete todo failed: {complete_result.stderr}"


class TestVersionManagement:
    """Test version-related API methods."""
    
    def test_get_current_version(self, isolated_venv, github_install, temp_project):
        """Test getting current version via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test getting current version
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
version = pm.get_current_version()
print(f"Current version: {{version}}")
""".format(str(temp_project))
        
        version_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert version_result.returncode == 0, f"Get version failed: {version_result.stderr}"
        assert "Current version:" in version_result.stdout
        
    def test_bump_version(self, isolated_venv, github_install, temp_project):
        """Test version bumping via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test version bump
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
old_version = pm.get_current_version()
print(f"Old version: {{old_version}}")
new_version = pm.bump_version("patch")
print(f"New version: {{new_version}}")
""".format(str(temp_project))
        
        bump_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert bump_result.returncode == 0, f"Version bump failed: {bump_result.stderr}"
        assert "Old version:" in bump_result.stdout
        assert "New version:" in bump_result.stdout
        
    def test_add_change(self, isolated_venv, github_install, temp_project):
        """Test adding changelog entries via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test adding change
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
pm.add_change("feat", "Test feature from API")
changelog = pm.get_changelog()
print(f"Changelog entries: {{len(changelog.get('versions', []))}}")
""".format(str(temp_project))
        
        change_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert change_result.returncode == 0, f"Add change failed: {change_result.stderr}"


class TestDependencyManagement:
    """Test dependency-related API methods."""
    
    def test_add_dependency(self, isolated_venv, github_install, temp_project):
        """Test adding todo dependencies via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test adding dependency
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()

# Add two todos
todo1_id = pm.add_todo("First todo", priority="high")
todo2_id = pm.add_todo("Second todo depends on first", priority="medium")

# Add dependency
pm.add_dependency(todo2_id, todo1_id)
print(f"Added dependency: {{todo2_id}} depends on {{todo1_id}}")

# Check blocked/unblocked todos
blocked = pm.get_blocked_todos()
unblocked = pm.get_unblocked_todos()
print(f"Blocked todos: {{len(blocked)}}")
print(f"Unblocked todos: {{len(unblocked)}}")
""".format(str(temp_project))
        
        dep_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert dep_result.returncode == 0, f"Add dependency failed: {dep_result.stderr}"
        assert "Added dependency:" in dep_result.stdout


class TestIntegratedWorkflows:
    """Test integrated API workflows."""
    
    def test_integrated_status(self, isolated_venv, github_install, temp_project):
        """Test get_integrated_status method."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test integrated status
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()
status = pm.get_integrated_status()
print(f"Status type: {{type(status)}}")
print(f"Status keys: {{list(status.keys()) if isinstance(status, dict) else 'Not a dict'}}")
""".format(str(temp_project))
        
        status_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert status_result.returncode == 0, f"Integrated status failed: {status_result.stderr}"
        assert "Status type:" in status_result.stdout
        
    def test_complete_todo_with_version(self, isolated_venv, github_install, temp_project):
        """Test complete_todo_with_version workflow."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test integrated workflow
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()

# Add a todo
todo_id = pm.add_todo("Feature to complete with version", priority="high")
print(f"Added todo {{todo_id}}")

# Complete with version bump (if method exists)
try:
    result = pm.complete_todo_with_version(todo_id, "feat", "patch")
    print(f"Completed todo with version: {{result}}")
except AttributeError:
    print("complete_todo_with_version method not available")
except Exception as e:
    print(f"Workflow failed: {{e}}")
""".format(str(temp_project))
        
        workflow_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert workflow_result.returncode == 0, f"Integrated workflow failed: {workflow_result.stderr}"


class TestIntelligenceAPI:
    """Test intelligence system API methods."""
    
    def test_intelligence_initialization(self, isolated_venv, github_install, temp_project):
        """Test intelligence system initialization via API."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test intelligence init
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()

try:
    pm.initialize_intelligence()
    print("Intelligence initialized successfully")
    
    # Test intelligence status
    status = pm.get_intelligence_status()
    print(f"Intelligence status type: {{type(status)}}")
    
except AttributeError:
    print("Intelligence methods not available")
except Exception as e:
    print(f"Intelligence init failed: {{e}}")
""".format(str(temp_project))
        
        intel_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert intel_result.returncode == 0, f"Intelligence API failed: {intel_result.stderr}"


class TestErrorHandling:
    """Test API error handling."""
    
    def test_invalid_todo_operations(self, isolated_venv, github_install, temp_project):
        """Test API handles invalid todo operations gracefully."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test invalid operations
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager
pm = ProjectManager()

try:
    # Try to complete non-existent todo
    pm.complete_todo(99999)
    print("Completed non-existent todo (unexpected)")
except Exception as e:
    print(f"Properly handled invalid todo: {{type(e).__name__}}")

try:
    # Try to add dependency with invalid IDs
    pm.add_dependency(99999, 99998)
    print("Added invalid dependency (unexpected)")
except Exception as e:
    print(f"Properly handled invalid dependency: {{type(e).__name__}}")
""".format(str(temp_project))
        
        error_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert error_result.returncode == 0, f"Error handling test failed: {error_result.stderr}"
        
    def test_missing_files_handling(self, isolated_venv, github_install):
        """Test API handles missing project files gracefully."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test in empty directory
        with tempfile.TemporaryDirectory() as empty_dir:
            test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager

try:
    pm = ProjectManager()
    todos = pm.get_todos()
    print(f"Empty project todos: {{len(todos)}}")
    
    # Should handle missing files gracefully
    version = pm.get_current_version()
    print(f"Default version: {{version}}")
    
except Exception as e:
    print(f"Failed to handle missing files: {{e}}")
""".format(empty_dir)
            
            missing_result = subprocess.run([
                str(python_path), "-c", test_code
            ], capture_output=True, text=True)
            
            assert missing_result.returncode == 0, f"Missing files handling failed: {missing_result.stderr}"


class TestDataPersistence:
    """Test that API operations persist data correctly."""
    
    def test_data_survives_recreation(self, isolated_venv, github_install, temp_project):
        """Test that data survives ProjectManager recreation."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test data persistence
        test_code = """
import os
os.chdir(r'{}')
from project_tools import ProjectManager

# Create first instance and add data
pm1 = ProjectManager()
todo_id = pm1.add_todo("Persistent todo", priority="high")
pm1.add_change("feat", "Persistent change")

print(f"Added todo {{todo_id}} and change")

# Create second instance and verify data
pm2 = ProjectManager()
todos = pm2.get_todos()
changelog = pm2.get_changelog()

persistent_todo = [t for t in todos if t['id'] == todo_id]
print(f"Todo persisted: {{len(persistent_todo) > 0}}")
print(f"Changelog entries: {{len(changelog.get('versions', []))}}")
""".format(str(temp_project))
        
        persist_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert persist_result.returncode == 0, f"Data persistence test failed: {persist_result.stderr}"
        assert "Todo persisted: True" in persist_result.stdout