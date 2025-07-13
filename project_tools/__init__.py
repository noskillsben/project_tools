"""
Project Tools

A universal project management package providing todo tracking and version management
capabilities for any software project.

Features:
- Todo management with priority tracking and status management
- Version management with semantic versioning and changelog tracking
- Optional git integration for tagging and status tracking
- Flexible formatters for email and console output
- Project-agnostic design for use across different codebases
- Unified ProjectManager interface optimized for coding agents and automated tools

Basic Usage:
    from project_tools import ProjectManager
    from project_tools.formatters import EmailFormatter
    
    # Initialize the unified project manager (auto-detects project root)
    project_manager = ProjectManager()
    
    # Add a todo
    todo_id = project_manager.add_todo(
        title="Fix bug in login system",
        description="User authentication fails with special characters",
        priority=9,
        category="bug"
    )
    
    # Complete todo with automatic changelog integration
    project_manager.complete_todo_with_version(
        todo_id, "bug", auto_version_bump=True
    )
    
    # Get workflow recommendations
    recommendations = project_manager.get_workflow_recommendations()
"""

from ._todo_manager import _TodoManager
from ._version_manager import _VersionManager

__version__ = "1.0.0"
__author__ = "Project Tools Contributors"
__email__ = "noreply@projecttools.dev"

__all__ = [
    'ProjectManager',
    'create_project_managers',
    'get_project_status'
]


class ProjectManager:
    """
    Primary interface for all project management operations.
    
    This is the main entry point for todo tracking, version management, and integrated workflows.
    Designed to provide a clean, predictable API that's perfect for coding agents and automated tools.
    
    Features:
    - Unified interface combining todo and version management
    - Integrated workflows for seamless todo-to-changelog operations
    - Workflow recommendations based on current project state
    - Optimized for iterative development and CI/CD integration
    """
    
    def __init__(self, todo_manager=None, version_manager=None, project_root=None, enable_git=True):
        """
        Initialize the unified project manager.
        
        Args:
            todo_manager: _TodoManager instance (created if None)
            version_manager: _VersionManager instance (created if None)
            project_root: Project root directory (auto-detected if None)
            enable_git: Whether to enable git operations
        """
        if todo_manager is None or version_manager is None:
            tm, vm = create_project_managers(project_root, enable_git)
            self._todo_manager = todo_manager or tm
            self._version_manager = version_manager or vm
        else:
            self._todo_manager = todo_manager
            self._version_manager = version_manager
    
    @property
    def todos(self) -> '_TodoManager':
        """Access to the todo manager for advanced operations."""
        return self._todo_manager
    
    @property
    def versions(self) -> '_VersionManager':
        """Access to the version manager for advanced operations."""
        return self._version_manager
    
    # Pass-through methods for common todo operations
    def add_todo(self, title: str, description: str = "", priority: int = 5, 
                 category: str = "general", **kwargs) -> int:
        """Add a new todo."""
        return self._todo_manager.add_todo(title, description, priority, category, **kwargs)
    
    def get_todos(self, status: str = None, category: str = None, **kwargs) -> list:
        """Get todos with optional filtering."""
        return self._todo_manager.get_todos(status=status, category=category, **kwargs)
    
    def complete_todo(self, todo_id: int) -> bool:
        """Complete a todo."""
        return self._todo_manager.complete_todo(todo_id)
    
    def update_todo_status(self, todo_id: int, status: str) -> bool:
        """Update todo status."""
        return self._todo_manager.update_todo_status(todo_id, status)
    
    def add_dependency(self, todo_id: int, depends_on_id: int) -> bool:
        """Add a dependency between todos."""
        return self._todo_manager.add_dependency(todo_id, depends_on_id)
    
    def get_blocked_todos(self) -> list:
        """Get todos that are blocked by dependencies."""
        return self._todo_manager.get_blocked_todos()
    
    def get_high_priority_todos(self, min_priority: int = 8) -> list:
        """Get high priority todos."""
        return self._todo_manager.get_high_priority_todos(min_priority)
    
    # Pass-through methods for common version operations
    def add_change(self, change_type: str, description: str, **kwargs) -> bool:
        """Add a change to the current version."""
        return self._version_manager.add_change(change_type, description, **kwargs)
    
    def bump_version(self, version_type: str, message: str = None) -> str:
        """Bump version and return new version string."""
        return self._version_manager.bump_version(version_type, message)
    
    def get_current_version(self) -> str:
        """Get the current version."""
        return self._version_manager.get_current_version()
    
    def get_recent_changes(self, days: int = 7) -> list:
        """Get recent changes."""
        return self._version_manager.get_recent_changes(days)
    
    def complete_todo_with_version(self, todo_id: int, change_type: str, 
                                 change_description: str = None, auto_version_bump: bool = False) -> bool:
        """
        Complete a todo and add corresponding changelog entry in one operation.
        
        Args:
            todo_id: ID of todo to complete
            change_type: Type of change for changelog
            change_description: Custom description (uses todo title if None)
            auto_version_bump: Whether to automatically bump version
            
        Returns:
            True if both operations succeeded
        """
        return self._todo_manager.complete_todo_with_changelog(
            todo_id, self._version_manager, change_type, change_description, auto_version_bump
        )
    
    def get_integrated_status(self) -> dict:
        """
        Get comprehensive status combining todo and version information.
        
        Returns:
            Integrated status dictionary
        """
        todo_summary = self._todo_manager.get_summary()
        version_summary = self._version_manager.get_version_summary()
        
        # Get dependency information
        blocked_todos = self._todo_manager.get_blocked_todos()
        unblocked_todos = self._todo_manager.get_unblocked_todos()
        
        return {
            'version': version_summary['current_version'],
            'version_date': version_summary['version_date'],
            'total_todos': todo_summary['total'],
            'high_priority_todos': todo_summary['high_priority_count'],
            'in_progress_todos': todo_summary['in_progress_count'],
            'blocked_todos': len(blocked_todos),
            'unblocked_todos': len(unblocked_todos),
            'dependencies_count': todo_summary['dependencies_count'],
            'recent_changes': version_summary['recent_changes_7d'],
            'total_versions': version_summary['total_versions'],
            'project_root': todo_summary['project_root'],
            'git_status': version_summary['git_status'],
            'todo_details': {
                'by_status': todo_summary['by_status'],
                'by_category': todo_summary['by_category'],
                'by_priority': todo_summary['by_priority']
            }
        }
    
    def get_workflow_recommendations(self) -> list:
        """
        Get workflow recommendations based on current project state.
        
        Returns:
            List of recommended actions
        """
        recommendations = []
        
        blocked_todos = self._todo_manager.get_blocked_todos()
        unblocked_todos = self._todo_manager.get_unblocked_todos()
        high_priority = self._todo_manager.get_high_priority_todos()
        
        if blocked_todos:
            recommendations.append(f"Resolve {len(blocked_todos)} blocked todos by completing their dependencies")
        
        if high_priority:
            recommendations.append(f"Focus on {len(high_priority)} high-priority todos")
        
        if unblocked_todos:
            ready_high_priority = [t for t in unblocked_todos if t.get('priority', 0) >= 8]
            if ready_high_priority:
                recommendations.append(f"Start with {len(ready_high_priority)} high-priority todos that are ready to work on")
        
        # Check for completed todos not in changelog
        recent_changes = self._version_manager.get_recent_changes(30)
        todo_ids_in_changelog = [c.get('todo_id') for c in recent_changes if c.get('todo_id')]
        completed_todos = self._todo_manager.get_todos(status='complete')
        
        unlogged_completed = [t for t in completed_todos if t['id'] not in todo_ids_in_changelog]
        if unlogged_completed:
            recommendations.append(f"Add {len(unlogged_completed)} completed todos to changelog")
        
        return recommendations


def create_project_managers(project_root=None, enable_git=True):
    """
    Convenience function to create both managers for a project.
    
    Args:
        project_root: Project root directory (auto-detected if None)
        enable_git: Whether to enable git operations in version manager
        
    Returns:
        tuple: (_TodoManager, _VersionManager) instances
    """
    todo_manager = _TodoManager(project_root=project_root)
    version_manager = _VersionManager(project_root=project_root, enable_git=enable_git)
    
    return todo_manager, version_manager


def get_project_status(project_root=None, enable_git=True):
    """
    Get a quick status overview of a project.
    
    Args:
        project_root: Project root directory (auto-detected if None)
        enable_git: Whether to enable git operations
        
    Returns:
        dict: Combined status information
    """
    todo_manager, version_manager = create_project_managers(project_root, enable_git)
    
    todo_summary = todo_manager.get_summary()
    version_summary = version_manager.get_version_summary()
    
    return {
        'version': version_summary['current_version'],
        'total_todos': todo_summary['total'],
        'high_priority_todos': todo_summary['high_priority_count'],
        'in_progress_todos': todo_summary['in_progress_count'],
        'blocked_todos': todo_summary['blocked_count'],
        'unblocked_todos': todo_summary['unblocked_count'],
        'dependencies_count': todo_summary['dependencies_count'],
        'recent_changes': len(version_manager.get_recent_changes(7)),
        'project_root': todo_summary['project_root'],
        'git_status': version_summary['git_status']
    }