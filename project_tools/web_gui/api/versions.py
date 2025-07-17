"""
Version Management API endpoints for Project Tools Web GUI
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

versions_bp = Blueprint('versions', __name__)

@versions_bp.route('/', methods=['GET'])
def get_versions():
    """Get version information and recent changes."""
    try:
        # Get query parameters
        days = request.args.get('days', default=30, type=int)
        
        # Get version data
        current_version = current_app.project_manager.get_current_version()
        recent_changes = current_app.project_manager.get_recent_changes(days)
        version_summary = current_app.project_manager.versions.get_version_summary()
        
        return jsonify({
            'success': True,
            'current_version': current_version,
            'recent_changes': recent_changes,
            'summary': version_summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/current', methods=['GET'])
def get_current_version():
    """Get current version information."""
    try:
        current_version = current_app.project_manager.get_current_version()
        version_summary = current_app.project_manager.versions.get_version_summary()
        
        return jsonify({
            'success': True,
            'version': current_version,
            'version_date': version_summary.get('version_date'),
            'git_status': version_summary.get('git_status')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/changes', methods=['GET'])
def get_changes():
    """Get recent changes with filtering."""
    try:
        # Get query parameters
        days = request.args.get('days', default=7, type=int)
        change_type = request.args.get('type')
        
        # Get changes
        changes = current_app.project_manager.get_recent_changes(days)
        
        # Filter by type if specified
        if change_type:
            changes = [c for c in changes if c.get('type') == change_type]
        
        return jsonify({
            'success': True,
            'changes': changes,
            'count': len(changes),
            'days': days
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/changes', methods=['POST'])
def add_change():
    """Add a new change to the current version."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('type') or not data.get('description'):
            return jsonify({
                'success': False,
                'error': 'type and description are required'
            }), 400
        
        # Add change
        success = current_app.project_manager.add_change(
            change_type=data['type'],
            description=data['description'],
            todo_id=data.get('todo_id'),
            author=data.get('author'),
            category=data.get('category')
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to add change'
            }), 500
        
        # Get recent changes to return updated list
        recent_changes = current_app.project_manager.get_recent_changes(7)
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('change_added', {
                'change': data,
                'recent_changes': recent_changes
            }, room='default')
        
        return jsonify({
            'success': True,
            'message': 'Change added successfully',
            'recent_changes': recent_changes
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/bump', methods=['POST'])
def bump_version():
    """Bump the version."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('type'):
            return jsonify({
                'success': False,
                'error': 'version type is required (major, minor, patch)'
            }), 400
        
        version_type = data['type']
        message = data.get('message', f'Version bump: {version_type}')
        
        # Validate version type
        if version_type not in ['major', 'minor', 'patch']:
            return jsonify({
                'success': False,
                'error': 'Invalid version type. Must be major, minor, or patch'
            }), 400
        
        # Bump version
        new_version = current_app.project_manager.bump_version(version_type, message)
        
        if not new_version:
            return jsonify({
                'success': False,
                'error': 'Failed to bump version'
            }), 500
        
        # Get updated version information
        version_summary = current_app.project_manager.versions.get_version_summary()
        
        # Emit real-time update
        if hasattr(current_app, 'socketio'):
            current_app.socketio.emit('version_bumped', {
                'new_version': new_version,
                'type': version_type,
                'message': message,
                'summary': version_summary
            }, room='default')
        
        return jsonify({
            'success': True,
            'new_version': new_version,
            'type': version_type,
            'message': message,
            'summary': version_summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/history', methods=['GET'])
def get_version_history():
    """Get complete version history."""
    try:
        # Get all changelog data
        changelog_data = current_app.project_manager.versions.changelog_data
        
        # Extract version history
        versions = []
        current_version = changelog_data.get('current_version', '0.0.0')
        
        # Get changes grouped by version if available
        changes = changelog_data.get('changes', [])
        
        # Group changes by date/version for history view
        version_history = {}
        for change in changes:
            change_date = change.get('date', 'unknown')
            if change_date not in version_history:
                version_history[change_date] = []
            version_history[change_date].append(change)
        
        return jsonify({
            'success': True,
            'current_version': current_version,
            'version_history': version_history,
            'total_changes': len(changes)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/summary', methods=['GET'])
def get_version_summary():
    """Get detailed version summary."""
    try:
        summary = current_app.project_manager.versions.get_version_summary()
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/git/status', methods=['GET'])
def get_git_status():
    """Get Git repository status."""
    try:
        version_summary = current_app.project_manager.versions.get_version_summary()
        git_status = version_summary.get('git_status', {})
        
        return jsonify({
            'success': True,
            'git_status': git_status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/changelog', methods=['GET'])
def get_changelog():
    """Get formatted changelog."""
    try:
        # Get changelog data
        changelog_data = current_app.project_manager.versions.changelog_data
        
        # Format for display
        formatted_changelog = {
            'project_name': changelog_data.get('project_name', 'Project Tools'),
            'current_version': changelog_data.get('current_version', '0.0.0'),
            'changes': changelog_data.get('changes', []),
            'last_updated': changelog_data.get('last_updated'),
            'total_changes': len(changelog_data.get('changes', []))
        }
        
        return jsonify({
            'success': True,
            'changelog': formatted_changelog
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@versions_bp.route('/stats', methods=['GET'])
def get_version_stats():
    """Get version statistics and metrics."""
    try:
        # Get recent changes for different time periods
        changes_7d = current_app.project_manager.get_recent_changes(7)
        changes_30d = current_app.project_manager.get_recent_changes(30)
        changes_90d = current_app.project_manager.get_recent_changes(90)
        
        # Calculate statistics
        stats = {
            'changes_last_7_days': len(changes_7d),
            'changes_last_30_days': len(changes_30d),
            'changes_last_90_days': len(changes_90d),
            'current_version': current_app.project_manager.get_current_version(),
        }
        
        # Group changes by type
        change_types = {}
        for change in changes_30d:
            change_type = change.get('type', 'unknown')
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        stats['change_types_30d'] = change_types
        
        # Get version summary for additional metrics
        version_summary = current_app.project_manager.versions.get_version_summary()
        stats.update({
            'total_versions': version_summary.get('total_versions', 0),
            'git_enabled': version_summary.get('git_status', {}).get('enabled', False)
        })
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500