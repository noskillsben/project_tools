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
from .intelligence import ProjectIntelligence
from .claude_integration import ClaudeIntegration

__version__ = "1.1.1"
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
    
    This is the main entry point for todo tracking, version management, integrated workflows,
    and AI-assisted project intelligence. Designed to provide a clean, predictable API that's
    perfect for coding agents and automated tools.
    
    Features:
    - Unified interface combining todo and version management
    - Integrated workflows for seamless todo-to-changelog operations
    - AI-assisted project intelligence with organized artifact management
    - Workflow recommendations based on current project state
    - Project compass, direction tracking, reflection management, and portfolio oversight
    - Optimized for iterative development and CI/CD integration
    - Organized project_management/ directory structure for intelligence artifacts
    """
    
    def __init__(self, todo_manager=None, version_manager=None, project_root=None, enable_git=True, 
                 enable_intelligence=True, intelligence_features=None):
        """
        Initialize the unified project manager.
        
        Args:
            todo_manager: _TodoManager instance (created if None)
            version_manager: _VersionManager instance (created if None)
            project_root: Project root directory (auto-detected if None)
            enable_git: Whether to enable git operations
            enable_intelligence: Whether to enable AI-assisted intelligence features
            intelligence_features: Dict of feature flags for intelligence components
        """
        if todo_manager is None or version_manager is None:
            tm, vm = create_project_managers(project_root, enable_git)
            self._todo_manager = todo_manager or tm
            self._version_manager = version_manager or vm
        else:
            self._todo_manager = todo_manager
            self._version_manager = version_manager
        
        # Initialize intelligence system
        self._intelligence = None
        if enable_intelligence:
            self._intelligence = ProjectIntelligence(
                project_root=self._todo_manager.project_root,
                todo_manager=self._todo_manager,
                version_manager=self._version_manager,
                feature_flags=intelligence_features
            )
    
    @property
    def todos(self) -> '_TodoManager':
        """Access to the todo manager for advanced operations."""
        return self._todo_manager
    
    @property
    def versions(self) -> '_VersionManager':
        """Access to the version manager for advanced operations."""
        return self._version_manager
    
    @property
    def intelligence(self) -> 'ProjectIntelligence':
        """Access to the intelligence system for AI-assisted project management."""
        return self._intelligence
    
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
        Get comprehensive status combining todo, version, and intelligence information.
        
        Returns:
            Integrated status dictionary with intelligence data when available
        """
        todo_summary = self._todo_manager.get_summary()
        version_summary = self._version_manager.get_version_summary()
        
        # Get dependency information
        blocked_todos = self._todo_manager.get_blocked_todos()
        unblocked_todos = self._todo_manager.get_unblocked_todos()
        
        status = {
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
        
        # Add intelligence data if available
        if self._intelligence:
            intelligence_status = self._intelligence.get_comprehensive_status()
            status['intelligence'] = {
                'active': intelligence_status['intelligence_active'],
                'components': intelligence_status['components'],
                'file_organization': intelligence_status['file_organization'],
                'ai_enhancement_opportunities': len(intelligence_status['ai_enhancement_opportunities']),
                'recommendations': intelligence_status['overall_recommendations']
            }
        else:
            status['intelligence'] = {'active': False}
        
        return status
    
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
    
    # Intelligence access methods
    def get_compass(self):
        """Access to the project compass for intent and context tracking."""
        return self._intelligence.compass if self._intelligence else None
    
    def get_task_chains(self):
        """Access to the task chain manager for logical task progressions."""
        return self._intelligence.task_chains if self._intelligence else None
    
    def get_direction_tracker(self):
        """Access to the direction tracker for lightweight goal management."""
        return self._intelligence.direction if self._intelligence else None
    
    def get_reflection_manager(self):
        """Access to the reflection manager for personal accountability."""
        return self._intelligence.reflection if self._intelligence else None
    
    def get_portfolio_manager(self):
        """Access to the portfolio manager for project relationships."""
        return self._intelligence.portfolio if self._intelligence else None
    
    def initialize_intelligence(self, project_name: str = "", force: bool = False) -> dict:
        """
        Initialize AI-assisted intelligence features with organized artifact structure.
        
        Args:
            project_name: Name of the project for template customization
            force: Whether to overwrite existing files
            
        Returns:
            Summary of initialization results
        """
        if not self._intelligence:
            return {"error": "Intelligence features are not enabled"}
        
        return self._intelligence.initialize_intelligence(project_name, force)
    
    def get_intelligence_status(self) -> dict:
        """
        Get comprehensive intelligence status across all components.
        
        Returns:
            Intelligence status with organized artifact information
        """
        if not self._intelligence:
            return {"intelligence_active": False, "reason": "Intelligence features not enabled"}
        
        return self._intelligence.get_comprehensive_status()
    
    def suggest_next_session_focus(self) -> dict:
        """
        Get AI-assisted suggestions for next working session focus.
        
        Returns:
            Session focus recommendations with AI enhancement opportunities
        """
        if not self._intelligence:
            return {"error": "Intelligence features are not enabled"}
        
        return self._intelligence.suggest_next_session_focus()
    
    def evaluate_project_health(self) -> dict:
        """
        Evaluate overall project health across all intelligence dimensions.
        
        Returns:
            Comprehensive project health assessment
        """
        if not self._intelligence:
            return {"error": "Intelligence features are not enabled"}
        
        return self._intelligence.evaluate_project_health()
    
    def get_ai_enhancement_summary(self) -> dict:
        """
        Get summary of AI enhancement opportunities across organized artifacts.
        
        Returns:
            AI enhancement opportunities and priorities in project_management/ structure
        """
        if not self._intelligence:
            return {"error": "Intelligence features are not enabled"}
        
        return self._intelligence.get_ai_enhancement_summary()
    
    # Claude Code Integration
    def generate_claude_md(self, include_examples: bool = True, include_setup_info: bool = True) -> str:
        """
        Generate CLAUDE.md content for Claude Code integration.
        
        Args:
            include_examples: Whether to include project-specific examples
            include_setup_info: Whether to include setup and configuration info
            
        Returns:
            Complete CLAUDE.md content as string
        """
        integration = ClaudeIntegration(self)
        return integration.generate_claude_md(include_examples, include_setup_info)
    
    def save_claude_md(self, file_path: str = None, **kwargs) -> str:
        """
        Save CLAUDE.md file for Claude Code integration.
        
        Args:
            file_path: Path to save file (default: project_root/CLAUDE.md)
            **kwargs: Additional arguments passed to generate_claude_md
            
        Returns:
            Path to the saved file
        """
        integration = ClaudeIntegration(self)
        saved_path = integration.save_claude_md(file_path, **kwargs)
        return str(saved_path)
    
    def get_claude_snippet(self) -> str:
        """
        Get a condensed Claude Code snippet for copy-pasting to existing CLAUDE.md files.
        
        Returns:
            Condensed snippet with essential project_tools commands
        """
        integration = ClaudeIntegration(self)
        return integration.print_claude_snippet()


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