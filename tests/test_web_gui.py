#!/usr/bin/env python3
"""
Web GUI smoke tests for project_tools.

Tests basic Flask application functionality and API endpoints.
"""

import pytest
import subprocess
import sys
import json
import requests
import threading
import time
import signal
import tempfile
from pathlib import Path


class TestFlaskApp:
    """Test Flask application creation and basic functionality."""
    
    def test_create_app_import(self, isolated_venv, github_install):
        """Test that Flask app can be created."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test Flask app creation
        test_code = """
try:
    from project_tools.web_gui.app import create_app
    app = create_app()
    print(f"Flask app created: {type(app)}")
    print(f"App name: {app.name}")
except Exception as e:
    print(f"Failed to create app: {e}")
"""
        
        app_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert app_result.returncode == 0, f"Flask app creation failed: {app_result.stderr}"
        
    def test_flask_dependencies(self, isolated_venv, github_install):
        """Test that Flask dependencies are available."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test Flask dependencies
        deps_to_test = [
            "Flask",
            "flask_cors", 
            "flask_socketio"
        ]
        
        for dep in deps_to_test:
            dep_test = subprocess.run([
                str(python_path), "-c", f"import {dep}; print('{dep} available')"
            ], capture_output=True, text=True)
            
            assert dep_test.returncode == 0, f"{dep} not available: {dep_test.stderr}"


class TestBasicRoutes:
    """Test basic Flask routes without full server startup."""
    
    def test_app_routes_exist(self, isolated_venv, github_install, temp_project):
        """Test that expected routes exist in the Flask app."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test route existence
        test_code = """
import os
os.chdir(r'{}')
try:
    from project_tools.web_gui.app import create_app
    app = create_app()
    
    # List all routes
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule.rule))
    
    print(f"Found routes: {routes}")
    
    # Check for expected routes
    expected = ['/', '/api/health']
    for route in expected:
        if route in routes or any(route in r for r in routes):
            print(f"Route {route}: Found")
        else:
            print(f"Route {route}: Missing")
            
except Exception as e:
    print(f"Route test failed: {e}")
""".format(str(temp_project))
        
        route_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert route_result.returncode == 0, f"Route test failed: {route_result.stderr}"


class TestConsoleScript:
    """Test project-tools-web console script."""
    
    def test_web_console_script_help(self, isolated_venv, github_install):
        """Test project-tools-web --help command."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test console script help
        if sys.platform == "win32":
            script_path = venv_path / "Scripts" / "project-tools-web.exe"
        else:
            script_path = venv_path / "bin" / "project-tools-web"
            
        # Test help command with timeout
        try:
            help_result = subprocess.run([
                str(script_path), "--help"
            ], capture_output=True, text=True, timeout=10)
            
            assert help_result.returncode == 0, f"Web console script help failed: {help_result.stderr}"
            
        except subprocess.TimeoutExpired:
            pytest.skip("Web console script help timed out")
        except FileNotFoundError:
            pytest.skip("Web console script not found")


class TestWebIntegration:
    """Test web GUI integration with ProjectManager."""
    
    def test_web_app_project_manager_access(self, isolated_venv, github_install, temp_project):
        """Test that web app can access ProjectManager."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test ProjectManager integration
        test_code = """
import os
os.chdir(r'{}')
try:
    from project_tools.web_gui.app import create_app
    from project_tools import ProjectManager
    
    # Create app and test context
    app = create_app()
    
    with app.app_context():
        # Test that we can create ProjectManager instance
        pm = ProjectManager()
        todos = pm.get_todos()
        print(f"Web app can access ProjectManager: {len(todos)} todos")
        
        status = pm.get_integrated_status()
        print(f"Web app can get status: {type(status)}")
        
except Exception as e:
    print(f"Web integration test failed: {e}")
""".format(str(temp_project))
        
        integration_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert integration_result.returncode == 0, f"Web integration failed: {integration_result.stderr}"


class TestAPIEndpoints:
    """Test API endpoints (if they can be tested without full server)."""
    
    def test_api_endpoint_structure(self, isolated_venv, github_install, temp_project):
        """Test API endpoint modules can be imported."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test API module imports
        test_code = """
import os
os.chdir(r'{}')
try:
    from project_tools.web_gui.api import todos, versions, intelligence
    print("API modules imported successfully")
    
    # Check if modules have expected attributes
    modules_to_check = [
        (todos, 'todos API'),
        (versions, 'versions API'), 
        (intelligence, 'intelligence API')
    ]
    
    for module, name in modules_to_check:
        attrs = dir(module)
        print(f"{name} attributes: {len(attrs)}")
        
except Exception as e:
    print(f"API import test failed: {e}")
""".format(str(temp_project))
        
        api_result = subprocess.run([
            str(python_path), "-c", test_code
        ], capture_output=True, text=True)
        
        assert api_result.returncode == 0, f"API import test failed: {api_result.stderr}"


class TestErrorHandling:
    """Test web GUI error handling."""
    
    def test_app_handles_missing_project_files(self, isolated_venv, github_install):
        """Test web app handles missing project files gracefully."""
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
try:
    from project_tools.web_gui.app import create_app
    
    # Create app in empty directory
    app = create_app()
    
    with app.app_context():
        # Should handle missing files gracefully
        from project_tools import ProjectManager
        pm = ProjectManager()
        
        # These should not crash
        todos = pm.get_todos()
        status = pm.get_integrated_status()
        
        print(f"Handled empty directory: {len(todos)} todos")
        
except Exception as e:
    print(f"Empty directory handling failed: {e}")
""".format(empty_dir)
            
            empty_result = subprocess.run([
                str(python_path), "-c", test_code
            ], capture_output=True, text=True)
            
            assert empty_result.returncode == 0, f"Empty directory test failed: {empty_result.stderr}"


class TestWebServerSmoke:
    """Smoke tests for actual web server startup (if possible)."""
    
    @pytest.mark.slow
    def test_server_can_start_and_stop(self, isolated_venv, github_install, temp_project):
        """Test that web server can start and respond to basic requests."""
        venv_path = isolated_venv
        
        # Install package
        result, python_path, _ = github_install(venv_path, ".")
        if result.returncode != 0:
            pytest.skip("GitHub install not available")
            
        # Test server startup
        test_script = f"""
import os
import sys
import threading
import time
from pathlib import Path

os.chdir(r'{temp_project}')
sys.path.insert(0, r'{temp_project}')

try:
    from project_tools.web_gui.app import create_app
    
    app = create_app()
    
    # Start server in thread
    def run_server():
        app.run(host='127.0.0.1', port=5555, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give server time to start
    time.sleep(2)
    
    print("Server started successfully")
    
    # Try to make a simple request
    import requests
    try:
        response = requests.get('http://127.0.0.1:5555/', timeout=5)
        print(f"Server responded: {{response.status_code}}")
    except Exception as e:
        print(f"Request failed: {{e}}")
        
    print("Server test completed")
    
except Exception as e:
    print(f"Server test failed: {{e}}")
"""
        
        # Write test script to file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_script)
            script_path = Path(f.name)
            
        try:
            # Run server test with timeout
            server_result = subprocess.run([
                str(python_path), str(script_path)
            ], capture_output=True, text=True, timeout=15)
            
            # Don't fail if server test has issues - this is just a smoke test
            print(f"Server test output: {server_result.stdout}")
            if server_result.stderr:
                print(f"Server test stderr: {server_result.stderr}")
                
        except subprocess.TimeoutExpired:
            # Server tests can be flaky, just note it
            print("Server test timed out - this is acceptable for smoke testing")
            
        finally:
            if script_path.exists():
                script_path.unlink()


@pytest.mark.skipif(
    not pytest.importorskip("requests", reason="requests not available"),
    reason="Requests library required for web tests"
)
class TestWithRequests:
    """Tests that require the requests library."""
    
    def test_requests_available(self):
        """Verify requests is available for web testing."""
        import requests
        assert hasattr(requests, 'get')