#!/usr/bin/env python3
"""
Project Tools Web GUI Startup Script

This script provides an easy way to start the Flask web interface for Project Tools.
It handles dependency installation, frontend building, and server startup.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json

def check_python_version():
    """Ensure Python 3.7+ is being used."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)

def install_dependencies():
    """Install Python dependencies for web GUI."""
    print("Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True)
        print("✓ Python dependencies installed")
    except subprocess.CalledProcessError:
        print("Error: Failed to install Python dependencies")
        sys.exit(1)

def setup_frontend():
    """Set up and build the React frontend."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("Error: Frontend directory not found")
        sys.exit(1)
    
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Installing Node.js dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✓ Node.js dependencies installed")
        except subprocess.CalledProcessError:
            print("Error: Failed to install Node.js dependencies")
            print("Make sure Node.js and npm are installed")
            sys.exit(1)
    
    # Build frontend for production
    print("Building frontend...")
    try:
        subprocess.run(["npm", "run", "build"], check=True)
        print("✓ Frontend built successfully")
    except subprocess.CalledProcessError:
        print("Error: Failed to build frontend")
        sys.exit(1)

def start_development_servers(args):
    """Start both Flask backend and React development server."""
    import threading
    import time
    
    # Start Flask server in background
    def start_flask():
        os.chdir(Path(__file__).parent)
        from project_tools.web_gui.app import run_server
        run_server(
            host=args.host,
            port=args.port,
            project_root=args.project_root,
            debug=args.debug
        )
    
    # Start React dev server in background
    def start_react():
        os.chdir(Path(__file__).parent / "frontend")
        subprocess.run(["npm", "run", "dev"])
    
    print(f"Starting development servers...")
    print(f"Flask API: http://{args.host}:{args.port}")
    print(f"React Dev: http://{args.host}:3000")
    print("Press Ctrl+C to stop servers")
    
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    react_thread = threading.Thread(target=start_react, daemon=True)
    
    flask_thread.start()
    time.sleep(2)  # Give Flask time to start
    react_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")

def start_production_server(args):
    """Start Flask server with built frontend."""
    os.chdir(Path(__file__).parent)
    from project_tools.web_gui.app import run_server
    
    print(f"Starting production server at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop")
    
    run_server(
        host=args.host,
        port=args.port,
        project_root=args.project_root,
        debug=False
    )

def main():
    parser = argparse.ArgumentParser(description="Start Project Tools Web GUI")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--project-root", help="Project root directory")
    parser.add_argument("--dev", action="store_true", help="Run in development mode with hot reload")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies before starting")
    parser.add_argument("--build-frontend", action="store_true", help="Build frontend before starting")
    
    args = parser.parse_args()
    
    check_python_version()
    
    # Install dependencies if requested
    if args.install_deps:
        install_dependencies()
    
    # Set up frontend if requested or in production mode
    if args.build_frontend or not args.dev:
        setup_frontend()
    
    try:
        if args.dev:
            start_development_servers(args)
        else:
            start_production_server(args)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()