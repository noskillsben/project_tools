"""
Project Intelligence API endpoints for Project Tools Web GUI
"""

from flask import Blueprint, request, jsonify, current_app

intelligence_bp = Blueprint('intelligence', __name__)

@intelligence_bp.route('/status', methods=['GET'])
def get_intelligence_status():
    """Get comprehensive intelligence status."""
    try:
        if not current_app.project_manager.intelligence:
            return jsonify({
                'success': True,
                'intelligence_active': False,
                'message': 'Intelligence features not enabled'
            })
        
        status = current_app.project_manager.get_intelligence_status()
        return jsonify({
            'success': True,
            **status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/initialize', methods=['POST'])
def initialize_intelligence():
    """Initialize intelligence features."""
    try:
        data = request.get_json() or {}
        
        if not current_app.project_manager.intelligence:
            return jsonify({
                'success': False,
                'error': 'Intelligence features not enabled'
            }), 400
        
        project_name = data.get('project_name', '')
        force = data.get('force', False)
        
        result = current_app.project_manager.initialize_intelligence(project_name, force)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get workflow recommendations."""
    try:
        recommendations = current_app.project_manager.get_workflow_recommendations()
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/session-focus', methods=['GET'])
def get_session_focus():
    """Get next session focus suggestions."""
    try:
        if not current_app.project_manager.intelligence:
            return jsonify({
                'success': False,
                'error': 'Intelligence features not enabled'
            }), 400
        
        focus = current_app.project_manager.suggest_next_session_focus()
        
        return jsonify({
            'success': True,
            'session_focus': focus
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/health', methods=['GET'])
def get_project_health():
    """Get project health evaluation."""
    try:
        if not current_app.project_manager.intelligence:
            return jsonify({
                'success': False,
                'error': 'Intelligence features not enabled'
            }), 400
        
        health = current_app.project_manager.evaluate_project_health()
        
        return jsonify({
            'success': True,
            'project_health': health
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/enhancements', methods=['GET'])
def get_ai_enhancements():
    """Get AI enhancement opportunities."""
    try:
        if not current_app.project_manager.intelligence:
            return jsonify({
                'success': False,
                'error': 'Intelligence features not enabled'
            }), 400
        
        enhancements = current_app.project_manager.get_ai_enhancement_summary()
        
        return jsonify({
            'success': True,
            'ai_enhancements': enhancements
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/compass', methods=['GET'])
def get_compass():
    """Get project compass information."""
    try:
        compass = current_app.project_manager.get_compass()
        
        if not compass:
            return jsonify({
                'success': True,
                'compass_active': False,
                'message': 'Compass not available'
            })
        
        # Get compass data if available
        compass_data = {}
        if hasattr(compass, 'get_status'):
            compass_data = compass.get_status()
        
        return jsonify({
            'success': True,
            'compass_active': True,
            'compass': compass_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/direction', methods=['GET'])
def get_direction():
    """Get direction tracker information."""
    try:
        direction = current_app.project_manager.get_direction_tracker()
        
        if not direction:
            return jsonify({
                'success': True,
                'direction_active': False,
                'message': 'Direction tracker not available'
            })
        
        # Get direction data if available
        direction_data = {}
        if hasattr(direction, 'get_status'):
            direction_data = direction.get_status()
        
        return jsonify({
            'success': True,
            'direction_active': True,
            'direction': direction_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/task-chains', methods=['GET'])
def get_task_chains():
    """Get task chain information."""
    try:
        task_chains = current_app.project_manager.get_task_chains()
        
        if not task_chains:
            return jsonify({
                'success': True,
                'task_chains_active': False,
                'message': 'Task chains not available'
            })
        
        # Get task chain data if available
        chains_data = {}
        if hasattr(task_chains, 'get_status'):
            chains_data = task_chains.get_status()
        
        return jsonify({
            'success': True,
            'task_chains_active': True,
            'task_chains': chains_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/reflection', methods=['GET'])
def get_reflection():
    """Get reflection manager information."""
    try:
        reflection = current_app.project_manager.get_reflection_manager()
        
        if not reflection:
            return jsonify({
                'success': True,
                'reflection_active': False,
                'message': 'Reflection not available'
            })
        
        # Get reflection data if available
        reflection_data = {}
        if hasattr(reflection, 'get_status'):
            reflection_data = reflection.get_status()
        
        return jsonify({
            'success': True,
            'reflection_active': True,
            'reflection': reflection_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    """Get portfolio manager information."""
    try:
        portfolio = current_app.project_manager.get_portfolio_manager()
        
        if not portfolio:
            return jsonify({
                'success': True,
                'portfolio_active': False,
                'message': 'Portfolio not available'
            })
        
        # Get portfolio data if available
        portfolio_data = {}
        if hasattr(portfolio, 'get_status'):
            portfolio_data = portfolio.get_status()
        
        return jsonify({
            'success': True,
            'portfolio_active': True,
            'portfolio': portfolio_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@intelligence_bp.route('/dashboard', methods=['GET'])
def get_intelligence_dashboard():
    """Get comprehensive intelligence dashboard data."""
    try:
        # Get integrated status which includes intelligence data
        integrated_status = current_app.project_manager.get_integrated_status()
        
        # Get additional intelligence-specific data
        intelligence_data = {
            'integrated_status': integrated_status,
            'recommendations': current_app.project_manager.get_workflow_recommendations()
        }
        
        # Add intelligence-specific data if available
        if current_app.project_manager.intelligence:
            try:
                intelligence_data.update({
                    'session_focus': current_app.project_manager.suggest_next_session_focus(),
                    'project_health': current_app.project_manager.evaluate_project_health(),
                    'ai_enhancements': current_app.project_manager.get_ai_enhancement_summary()
                })
            except Exception as e:
                # If intelligence features fail, continue with basic data
                intelligence_data['intelligence_error'] = str(e)
        
        return jsonify({
            'success': True,
            'dashboard': intelligence_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500