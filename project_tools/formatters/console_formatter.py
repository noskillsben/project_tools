#!/usr/bin/env python3
"""
Console Formatter for Project Tools

Provides console/terminal formatting for todos and version changes.
"""

from typing import List, Dict, Any, Optional
import textwrap


class ConsoleFormatter:
    """
    Console formatter for todos and version changes.
    
    Generates formatted text output suitable for terminal display.
    """
    
    def __init__(self, width: int = 80):
        """
        Initialize the console formatter.
        
        Args:
            width: Terminal width for text wrapping
        """
        self.width = width
    
    def format_todos_table(self, todo_manager, status: str = None) -> str:
        """
        Format todos as a table for console display.
        
        Args:
            todo_manager: _TodoManager instance
            status: Filter by status (None for all)
            
        Returns:
            Formatted table string
        """
        todos = todo_manager.get_todos(status=status)
        
        if not todos:
            return "No todos found."
        
        # Calculate column widths with dependency column
        id_width = max(3, max(len(str(t.get('id', 0))) for t in todos))
        deps_width = 4  # For dependency symbols
        priority_width = 8
        status_width = max(6, max(len(t.get('status', '')) for t in todos))
        category_width = max(8, max(len(t.get('category', '')) for t in todos))
        
        # Remaining width for title
        title_width = self.width - id_width - deps_width - priority_width - status_width - category_width - 12
        
        # Header
        header = f"{'ID':<{id_width}} {'Deps':<{deps_width}} {'Priority':<{priority_width}} {'Status':<{status_width}} {'Category':<{category_width}} {'Title':<{title_width}}"
        separator = "─" * len(header)
        
        output = [header, separator]
        
        # Rows
        for todo in todos:
            title = todo.get('title', '')
            if len(title) > title_width:
                title = title[:title_width-3] + "..."
            
            # Get dependency symbol
            dep_symbol = self._get_dependency_symbol(todo, todo_manager)
            
            row = f"{todo.get('id', 0):<{id_width}} {dep_symbol:<{deps_width}} {todo.get('priority', 0):<{priority_width}} {todo.get('status', ''):<{status_width}} {todo.get('category', ''):<{category_width}} {title:<{title_width}}"
            output.append(row)
        
        # Add legend
        output.append(separator)
        output.append("Legend: ⏳ Blocked  🔗 Has dependencies  ⚡ Others depend on this")
        
        return "\n".join(output)
    
    def _get_dependency_symbol(self, todo: Dict[str, Any], todo_manager) -> str:
        """Get symbol indicating dependency status."""
        if not todo_manager:
            return '  '
        
        todo_id = todo['id']
        blocked_ids = [t['id'] for t in todo_manager.get_blocked_todos()]
        dependencies = todo_manager.todo_data.get('dependencies', {})
        
        if todo_id in blocked_ids:
            return '⏳'  # Blocked
        elif str(todo_id) in dependencies:
            return '🔗'  # Has dependencies
        else:
            # Check if other todos depend on this one
            for deps in dependencies.values():
                if todo_id in deps:
                    return '⚡'  # Others depend on this
            return '  '  # No dependencies
    
    def format_dependency_tree(self, todo_manager, todo_id: int) -> str:
        """
        Format dependency tree for a specific todo.
        
        Args:
            todo_manager: _TodoManager instance
            todo_id: ID of the todo to show dependencies for
            
        Returns:
            Formatted dependency tree
        """
        todo = todo_manager.get_todo_by_id(todo_id)
        if not todo:
            return f"Todo #{todo_id} not found."
        
        chain = todo_manager.get_dependency_chain(todo_id)
        output = []
        
        # Show the todo itself
        output.append(f"Todo #{todo_id}: {todo.get('title', '')}")
        output.append(f"Status: {todo.get('status', '')} | Priority: {todo.get('priority', 0)}")
        output.append("═" * min(self.width, 50))
        output.append("")
        
        # Show dependencies (what this todo depends on)
        if chain['dependencies']:
            output.append("Dependencies (must complete first):")
            for dep_id in chain['dependencies']:
                dep_todo = todo_manager.get_todo_by_id(dep_id)
                if dep_todo:
                    status_symbol = '✓' if dep_todo.get('status') == 'complete' else '○'
                    output.append(f"  {status_symbol} #{dep_id}: {dep_todo.get('title', '')} [{dep_todo.get('status', '')}]")
        else:
            output.append("✅ No dependencies - ready to work on!")
        
        output.append("")
        
        # Show dependents (what depends on this todo)
        if chain['dependents']:
            output.append("Todos that depend on this:")
            for dep_id in chain['dependents']:
                dep_todo = todo_manager.get_todo_by_id(dep_id)
                if dep_todo:
                    output.append(f"  → #{dep_id}: {dep_todo.get('title', '')} [{dep_todo.get('status', '')}]")
        else:
            output.append("No other todos depend on this one.")
        
        return "\n".join(output)
    
    def format_blocked_todos(self, todo_manager) -> str:
        """
        Format list of blocked todos.
        
        Args:
            todo_manager: _TodoManager instance
            
        Returns:
            Formatted blocked todos list
        """
        blocked = todo_manager.get_blocked_todos()
        if not blocked:
            return "✅ No blocked todos found."
        
        output = [f"⏳ Blocked Todos ({len(blocked)}):"]
        output.append("═" * 30)
        output.append("")
        
        for todo in blocked:
            # Get blocking dependencies
            todo_deps = todo_manager.todo_data.get('dependencies', {}).get(str(todo['id']), [])
            blocking_todos = []
            
            for dep_id in todo_deps:
                dep_todo = todo_manager.get_todo_by_id(dep_id)
                if dep_todo and dep_todo.get('status') != 'complete':
                    blocking_todos.append(f"#{dep_id}")
            
            output.append(f"#{todo['id']}: {todo.get('title', '')}")
            blocking_text = ", ".join(blocking_todos) if blocking_todos else "Unknown"
            output.append(f"  Waiting for: {blocking_text}")
            output.append("")
        
        return "\n".join(output)
    
    def format_todo_details(self, todo_manager, todo_id: int) -> str:
        """
        Format detailed view of a single todo.
        
        Args:
            todo_manager: _TodoManager instance
            todo_id: ID of todo to display
            
        Returns:
            Formatted todo details
        """
        todo = todo_manager.get_todo_by_id(todo_id)
        
        if not todo:
            return f"Todo #{todo_id} not found."
        
        output = []
        output.append(f"Todo #{todo['id']}: {todo.get('title', '')}")
        output.append("═" * min(self.width, len(output[0])))
        output.append("")
        
        # Basic info
        output.append(f"Priority:     {todo.get('priority', 0)}")
        output.append(f"Status:       {todo.get('status', '')}")
        output.append(f"Category:     {todo.get('category', '')}")
        output.append(f"Created:      {todo.get('created_date', '')}")
        
        if todo.get('target_date'):
            output.append(f"Target Date:  {todo['target_date']}")
        
        if todo.get('completed_date'):
            output.append(f"Completed:    {todo['completed_date']}")
        
        output.append("")
        
        # Description
        if todo.get('description'):
            output.append("Description:")
            wrapped = textwrap.fill(todo['description'], width=self.width-2)
            for line in wrapped.split('\n'):
                output.append(f"  {line}")
            output.append("")
        
        # Notes
        if todo.get('notes'):
            output.append("Notes:")
            wrapped = textwrap.fill(todo['notes'], width=self.width-2)
            for line in wrapped.split('\n'):
                output.append(f"  {line}")
        
        return "\n".join(output)
    
    def format_todo_summary(self, todo_manager) -> str:
        """
        Format todo summary statistics.
        
        Args:
            todo_manager: _TodoManager instance
            
        Returns:
            Formatted summary string
        """
        summary = todo_manager.get_summary()
        
        output = []
        output.append("Todo Summary")
        output.append("═" * 12)
        output.append("")
        output.append(f"Total Todos:      {summary['total']}")
        output.append(f"High Priority:    {summary['high_priority_count']}")
        output.append(f"In Progress:      {summary['in_progress_count']}")
        output.append(f"Blocked:          {summary.get('blocked_count', 0)}")
        output.append(f"Ready to Work:    {summary.get('unblocked_count', 0)}")
        if summary.get('dependencies_count', 0) > 0:
            output.append(f"Dependencies:     {summary['dependencies_count']} todos have dependencies")
        output.append("")
        
        # By status
        output.append("By Status:")
        for status, count in summary['by_status'].items():
            output.append(f"  {status:12} {count}")
        output.append("")
        
        # By category
        output.append("By Category:")
        for category, count in summary['by_category'].items():
            output.append(f"  {category:12} {count}")
        output.append("")
        
        # By priority
        output.append("By Priority:")
        for priority_range, count in summary['by_priority'].items():
            output.append(f"  {priority_range:12} {count}")
        
        return "\n".join(output)
    
    def format_version_history(self, version_manager, limit: int = 10) -> str:
        """
        Format version history for console display.
        
        Args:
            version_manager: _VersionManager instance
            limit: Maximum number of versions to show
            
        Returns:
            Formatted version history
        """
        versions = version_manager.get_all_versions(sort_desc=True)[:limit]
        
        if not versions:
            return "No versions found."
        
        output = []
        output.append("Version History")
        output.append("═" * 15)
        output.append("")
        
        for version in versions:
            version_info = version_manager.get_version_info(version)
            if version_info:
                current_marker = " (current)" if version == version_manager.get_current_version() else ""
                output.append(f"{version}{current_marker} - {version_info['date']}")
                
                changes = version_info.get('changes', [])
                if changes:
                    # Group by type
                    by_type = {}
                    for change in changes:
                        change_type = change.get('type', 'other')
                        if change_type not in by_type:
                            by_type[change_type] = []
                        by_type[change_type].append(change)
                    
                    for change_type, type_changes in by_type.items():
                        output.append(f"  {change_type.title()}:")
                        for change in type_changes:
                            desc = change.get('description', '')
                            if len(desc) > self.width - 6:
                                desc = desc[:self.width-9] + "..."
                            todo_ref = f" (#{change['todo_id']})" if change.get('todo_id') else ""
                            output.append(f"    • {desc}{todo_ref}")
                
                output.append("")
        
        return "\n".join(output)
    
    def format_version_summary(self, version_manager) -> str:
        """
        Format version summary statistics.
        
        Args:
            version_manager: _VersionManager instance
            
        Returns:
            Formatted summary string
        """
        summary = version_manager.get_version_summary()
        
        output = []
        output.append("Version Summary")
        output.append("═" * 15)
        output.append("")
        output.append(f"Current Version:     {summary['current_version']}")
        output.append(f"Version Date:        {summary.get('version_date', 'Unknown')}")
        output.append(f"Total Versions:      {summary['total_versions']}")
        output.append(f"Recent Changes (7d): {summary['recent_changes_7d']}")
        output.append("")
        
        # Git status
        git_status = summary.get('git_status', {})
        if 'error' not in git_status:
            output.append("Git Status:")
            output.append(f"  Branch:              {git_status.get('branch', 'Unknown')}")
            output.append(f"  Uncommitted Changes: {git_status.get('has_uncommitted_changes', 'Unknown')}")
            if git_status.get('latest_tags'):
                output.append(f"  Latest Tags:         {', '.join(git_status['latest_tags'][:3])}")
        else:
            output.append(f"Git Status: {git_status['error']}")
        
        return "\n".join(output)
    
    def format_recent_changes(self, version_manager, days: int = 7) -> str:
        """
        Format recent changes for console display.
        
        Args:
            version_manager: _VersionManager instance
            days: Number of days to look back
            
        Returns:
            Formatted recent changes
        """
        changes = version_manager.get_recent_changes(days)
        
        if not changes:
            return f"No changes in the last {days} days."
        
        output = []
        output.append(f"Recent Changes ({days} days)")
        output.append("═" * (len(output[0])))
        output.append("")
        
        current_date = None
        for change in changes:
            # Group by date
            if change['date'] != current_date:
                if current_date is not None:
                    output.append("")
                current_date = change['date']
                output.append(f"{change['date']} (v{change['version']})")
                output.append("─" * len(output[-1]))
            
            # Format change
            desc = change.get('description', '')
            if len(desc) > self.width - 4:
                desc = desc[:self.width-7] + "..."
            
            todo_ref = f" (#{change['todo_id']})" if change.get('todo_id') else ""
            output.append(f"  {change.get('type', 'other')}: {desc}{todo_ref}")
        
        return "\n".join(output)
    
    def format_combined_status(self, todo_manager, version_manager) -> str:
        """
        Format a combined status report.
        
        Args:
            todo_manager: _TodoManager instance
            version_manager: _VersionManager instance
            
        Returns:
            Formatted combined status
        """
        output = []
        
        # Header
        output.append("Project Status Report")
        output.append("═" * 21)
        output.append("")
        
        # Version info
        version_summary = version_manager.get_version_summary()
        output.append(f"Version: {version_summary['current_version']} ({version_summary.get('version_date', 'Unknown')})")
        
        # Todo counts with dependency info
        todo_summary = todo_manager.get_summary()
        blocked_count = todo_summary.get('blocked_count', 0)
        unblocked_count = todo_summary.get('unblocked_count', 0)
        output.append(f"Todos: {todo_summary['total']} total, {todo_summary['high_priority_count']} high priority, {todo_summary['in_progress_count']} in progress")
        if blocked_count > 0 or unblocked_count > 0:
            output.append(f"       {blocked_count} blocked, {unblocked_count} ready to work")
        output.append("")
        
        # High priority todos
        high_priority = todo_manager.get_high_priority_todos()
        if high_priority:
            output.append("High Priority Todos:")
            for todo in high_priority[:5]:  # Show top 5
                title = todo.get('title', '')
                if len(title) > self.width - 10:
                    title = title[:self.width-13] + "..."
                output.append(f"  #{todo['id']}: {title} (P{todo.get('priority', 0)})")
            
            if len(high_priority) > 5:
                output.append(f"  ... and {len(high_priority) - 5} more")
            output.append("")
        
        # Recent changes
        recent_changes = version_manager.get_recent_changes(3)
        if recent_changes:
            output.append("Recent Changes (3 days):")
            for change in recent_changes[:5]:  # Show top 5
                desc = change.get('description', '')
                if len(desc) > self.width - 8:
                    desc = desc[:self.width-11] + "..."
                output.append(f"  {change.get('type', 'other')}: {desc}")
            
            if len(recent_changes) > 5:
                output.append(f"  ... and {len(recent_changes) - 5} more")
        
        return "\n".join(output)