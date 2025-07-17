#!/usr/bin/env python3
"""
Flask Web GUI Application for Project Tools

Main Flask application providing web interface for project management tools.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from pathlib import Path
import logging

from project_tools import ProjectManager
from project_tools.web_gui.api.todos import todos_bp
from project_tools.web_gui.api.versions import versions_bp
from project_tools.web_gui.api.intelligence import intelligence_bp

def create_app(project_root=None, debug=True):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'project-tools-web-gui-secret-key'
    app.config['DEBUG'] = debug
    
    # Initialize CORS for all routes
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Initialize Project Manager
    try:
        project_manager = ProjectManager(project_root=project_root)
        app.project_manager = project_manager
    except Exception as e:
        logging.error(f"Failed to initialize ProjectManager: {e}")
        raise
    
    # Register blueprints
    app.register_blueprint(todos_bp, url_prefix='/api/todos')
    app.register_blueprint(versions_bp, url_prefix='/api/versions')
    app.register_blueprint(intelligence_bp, url_prefix='/api/intelligence')
    
    @app.route('/')
    def index():
        """Serve React app or basic info page."""
        static_dir = Path(__file__).parent / 'static'
        if (static_dir / 'index.html').exists():
            return send_from_directory(static_dir, 'index.html')
        else:
            return jsonify({
                'message': 'Project Tools Web GUI API',
                'version': '1.0.0',
                'endpoints': [
                    '/api/todos',
                    '/api/versions', 
                    '/api/intelligence'
                ]
            })
    
    @app.route('/api/status')
    def status():
        """Get overall project status."""
        try:
            status_data = app.project_manager.get_integrated_status()
            return jsonify(status_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/health')
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    
    # WebSocket events
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        emit('status', {'message': 'Connected to Project Tools'})
        
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        print('Client disconnected')
    
    @socketio.on('join_project')
    def handle_join_project(data):
        """Join a project room for real-time updates."""
        project_id = data.get('project_id', 'default')
        join_room(project_id)
        emit('joined', {'project_id': project_id})
    
    @socketio.on('leave_project')
    def handle_leave_project(data):
        """Leave a project room."""
        project_id = data.get('project_id', 'default')
        leave_room(project_id)
        emit('left', {'project_id': project_id})
    
    app.socketio = socketio
    return app, socketio

def run_server(host='127.0.0.1', port=5000, project_root=None, debug=True):
    """Run the Flask development server."""
    app, socketio = create_app(project_root=project_root, debug=debug)
    
    print(f"Starting Project Tools Web GUI...")
    print(f"Server: http://{host}:{port}")
    print(f"Project Root: {app.project_manager.todos.project_root}")
    print(f"Todo File: {app.project_manager.todos.todo_path}")
    
    socketio.run(app, host=host, port=port, debug=debug)

def main():
    """Main entry point for console script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Project Tools Web GUI")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to (default: 5000)")
    parser.add_argument("--project-root", help="Project root directory (auto-detected if not specified)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print("Starting Project Tools Web GUI...")
    print(f"Access the web interface at: http://{args.host}:{args.port}")
    print("Note: This starts only the Flask backend. For full development with React hot-reload,")
    print("use the start_web_gui.py script with --dev flag instead.")
    print()
    
    try:
        run_server(
            host=args.host, 
            port=args.port, 
            project_root=args.project_root, 
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())