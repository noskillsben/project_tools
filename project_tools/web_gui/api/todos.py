"""
Todo API endpoints for Project Tools Web GUI
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/', methods=['GET'])
def get_todos():
    """Get todos with optional filtering."""
    try:
        # Get query parameters
        status = request.args.get('status')
        category = request.args.get('category')
        min_priority = request.args.get('min_priority', type=int)
        max_priority = request.args.get('max_priority', type=int)
        sort_by = request.args.get('sort_by', 'priority')
        
        # Get todos from project manager
        todos = current_app.project_manager.get_todos(
            status=status,
            category=category,
            min_priority=min_priority,
            max_priority=max_priority,
            sort_by=sort_by
        )
        
        return jsonify({
            'success': True,
            'todos': todos,
            'count': len(todos)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/', methods=['POST'])
def create_todo():
    """Create a new todo."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('title'):
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # Create todo
        todo_id = current_app.project_manager.add_todo(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 5),
            category=data.get('category', 'general'),
            target_date=data.get('target_date'),
            notes=data.get('notes'),
            custom_fields=data.get('custom_fields')
        )
        
        if todo_id == -1:
            return jsonify({
                'success': False,
                'error': 'Failed to create todo'
            }), 500
        
        # Get the created todo
        todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        
        # Emit real-time update if SocketIO is available
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('todo_created', {
                'todo': todo
            }, room='default')
        
        return jsonify({
            'success': True,
            'todo': todo,
            'id': todo_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID."""
    try:
        todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        return jsonify({
            'success': True,
            'todo': todo
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Check if todo exists
        todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        # Update todo
        success = current_app.project_manager.todos.update_todo(todo_id, **data)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to update todo'
            }), 500
        
        # Get updated todo
        updated_todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('todo_updated', {
                'todo': updated_todo
            }, room='default')
        
        return jsonify({
            'success': True,
            'todo': updated_todo
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo."""
    try:
        # Check if todo exists
        todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        # Delete todo
        success = current_app.project_manager.todos.delete_todo(todo_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to delete todo'
            }), 500
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('todo_deleted', {
                'todo_id': todo_id
            }, room='default')
        
        return jsonify({
            'success': True,
            'message': 'Todo deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/<int:todo_id>/complete', methods=['POST'])
def complete_todo(todo_id):
    """Complete a todo."""
    try:
        data = request.get_json() or {}
        
        # Check if todo exists
        todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        # Complete todo
        if data.get('with_changelog', False):
            # Complete with changelog integration
            success = current_app.project_manager.complete_todo_with_version(
                todo_id=todo_id,
                change_type=data.get('change_type', 'general'),
                change_description=data.get('change_description'),
                auto_version_bump=data.get('auto_version_bump', False)
            )
        else:
            # Simple completion
            success = current_app.project_manager.complete_todo(todo_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to complete todo'
            }), 500
        
        # Get updated todo
        completed_todo = current_app.project_manager.todos.get_todo_by_id(todo_id)
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('todo_completed', {
                'todo': completed_todo
            }, room='default')
        
        return jsonify({
            'success': True,
            'todo': completed_todo
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get todo summary statistics."""
    try:
        summary = current_app.project_manager.todos.get_summary()
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/dependencies', methods=['GET'])
def get_dependencies():
    """Get all todo dependencies."""
    try:
        blocked_todos = current_app.project_manager.get_blocked_todos()
        unblocked_todos = current_app.project_manager.get_unblocked_todos()
        
        return jsonify({
            'success': True,
            'dependencies': {
                'blocked': blocked_todos,
                'unblocked': unblocked_todos,
                'blocked_count': len(blocked_todos),
                'unblocked_count': len(unblocked_todos)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/<int:todo_id>/dependencies', methods=['POST'])
def add_dependency(todo_id):
    """Add a dependency to a todo."""
    try:
        data = request.get_json()
        
        if not data or 'depends_on_id' not in data:
            return jsonify({
                'success': False,
                'error': 'depends_on_id is required'
            }), 400
        
        depends_on_id = data['depends_on_id']
        
        # Add dependency
        success = current_app.project_manager.add_dependency(todo_id, depends_on_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to add dependency (check for circular dependencies)'
            }), 400
        
        # Get dependency chain
        chain = current_app.project_manager.todos.get_dependency_chain(todo_id)
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('dependency_added', {
                'todo_id': todo_id,
                'depends_on_id': depends_on_id,
                'chain': chain
            }, room='default')
        
        return jsonify({
            'success': True,
            'dependency_chain': chain
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/<int:todo_id>/dependencies/<int:depends_on_id>', methods=['DELETE'])
def remove_dependency(todo_id, depends_on_id):
    """Remove a dependency from a todo."""
    try:
        # Remove dependency
        success = current_app.project_manager.todos.remove_dependency(todo_id, depends_on_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to remove dependency'
            }), 400
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('dependency_removed', {
                'todo_id': todo_id,
                'depends_on_id': depends_on_id
            }, room='default')
        
        return jsonify({
            'success': True,
            'message': 'Dependency removed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@todos_bp.route('/export', methods=['GET'])
def export_todos():
    """Export todos in various formats."""
    try:
        format_type = request.args.get('format', 'json')
        
        if format_type not in ['json', 'csv', 'markdown']:
            return jsonify({
                'success': False,
                'error': 'Invalid format. Supported: json, csv, markdown'
            }), 400
        
        exported_data = current_app.project_manager.todos.export_todos(format_type)
        
        return jsonify({
            'success': True,
            'format': format_type,
            'data': exported_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500