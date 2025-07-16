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
    
    # Intelligence formatting methods
    def format_intelligence_status(self, status: Dict[str, Any]) -> str:
        """
        Format intelligence status for console display.
        
        Args:
            status: Intelligence status dictionary
            
        Returns:
            Formatted intelligence status
        """
        if not status.get('intelligence_active'):
            return "Intelligence features are not active."
        
        output = []
        output.append("Intelligence Status")
        output.append("═" * 19)
        output.append("")
        
        # Feature flags
        feature_flags = status.get('feature_flags', {})
        active_features = [name for name, enabled in feature_flags.items() if enabled]
        output.append(f"Active Features: {', '.join(active_features)}")
        output.append("")
        
        # Components status
        components = status.get('components', {})
        for comp_name, comp_data in components.items():
            if isinstance(comp_data, dict):
                output.append(f"{comp_name.title()} Status:")
                
                # Component-specific formatting
                if comp_name == 'compass':
                    output.append(f"  Active: {'✓' if comp_data.get('compass_active') else '✗'}")
                    if comp_data.get('project_intent_defined'):
                        output.append(f"  Project Intent: Defined")
                    if comp_data.get('success_criteria_count', 0) > 0:
                        output.append(f"  Success Criteria: {comp_data['success_criteria_count']}")
                
                elif comp_name == 'task_chains':
                    total_chains = comp_data.get('total_chains', 0)
                    active_chains = comp_data.get('active_chains', 0)
                    output.append(f"  Chains: {active_chains}/{total_chains} active")
                
                elif comp_name == 'direction':
                    has_direction = comp_data.get('has_current_direction')
                    output.append(f"  Current Direction: {'Set' if has_direction else 'Not set'}")
                    if comp_data.get('needs_attention'):
                        output.append(f"  ⚠️  Needs attention")
                
                elif comp_name == 'reflection':
                    active = comp_data.get('reflection_active')
                    output.append(f"  Active: {'✓' if active else '✗'}")
                    recent_learnings = comp_data.get('recent_learnings', 0)
                    if recent_learnings > 0:
                        output.append(f"  Recent Learnings: {recent_learnings}")
                
                elif comp_name == 'portfolio':
                    active = comp_data.get('portfolio_active')
                    output.append(f"  Active: {'✓' if active else '✗'}")
                    if comp_data.get('total_projects', 0) > 0:
                        output.append(f"  Projects: {comp_data['total_projects']}")
                
                output.append("")
        
        # File organization
        file_org = status.get('file_organization', {})
        if file_org.get('structure_created'):
            output.append("File Organization:")
            for category, info in file_org.get('categories', {}).items():
                if info.get('exists') and info.get('file_count', 0) > 0:
                    output.append(f"  {category}/: {info['file_count']} files")
            output.append("")
        
        # AI enhancement opportunities
        ai_opportunities = status.get('ai_enhancement_opportunities', [])
        if ai_opportunities:
            output.append(f"AI Enhancement Opportunities: {len(ai_opportunities)} files ready")
            for opp in ai_opportunities[:3]:  # Show top 3
                file_type = opp.get('file_type', 'unknown')
                placeholder_count = opp.get('placeholder_count', 0)
                output.append(f"  {file_type}: {placeholder_count} placeholders")
            if len(ai_opportunities) > 3:
                output.append(f"  ... and {len(ai_opportunities) - 3} more")
            output.append("")
        
        # Recommendations
        recommendations = status.get('overall_recommendations', [])
        if recommendations:
            output.append("Recommendations:")
            for rec in recommendations:
                output.append(f"  • {rec}")
        
        return "\n".join(output)
    
    def format_chain_health(self, health: Dict[str, Any]) -> str:
        """
        Format task chain health for console display.
        
        Args:
            health: Chain health dictionary
            
        Returns:
            Formatted chain health
        """
        if "error" in health:
            return f"Error: {health['error']}"
        
        output = []
        output.append(f"Chain Health: {health['chain_name']} ({health['chain_id']})")
        output.append("═" * (len(output[0])))
        output.append("")
        
        # Overall health
        health_status = health.get('overall_health', 'unknown')
        health_symbol = {
            'excellent': '🟢',
            'good': '🟡', 
            'fair': '🟠',
            'poor': '🔴',
            'unknown': '⚪'
        }.get(health_status, '⚪')
        
        output.append(f"Overall Health: {health_symbol} {health_status.title()}")
        output.append("")
        
        # Metrics
        metrics = health.get('metrics', {})
        if metrics:
            output.append("Metrics:")
            completion_rate = metrics.get('completion_rate', 0)
            output.append(f"  Completion Rate: {completion_rate:.1%}")
            
            blocked_tasks = metrics.get('blocked_tasks', 0)
            if blocked_tasks > 0:
                output.append(f"  Blocked Tasks: {blocked_tasks}")
            
            milestone_progress = metrics.get('milestone_progress', 0)
            if milestone_progress > 0:
                output.append(f"  Milestone Progress: {milestone_progress:.1%}")
            
            output.append("")
        
        # Issues
        issues = health.get('issues', [])
        if issues:
            output.append("Issues:")
            for issue in issues:
                output.append(f"  ⚠️  {issue}")
            output.append("")
        
        # Recommendations
        recommendations = health.get('recommendations', [])
        if recommendations:
            output.append("Recommendations:")
            for rec in recommendations:
                output.append(f"  • {rec}")
        
        return "\n".join(output)
    
    def format_chains_summary(self, summary: Dict[str, Any]) -> str:
        """
        Format task chains summary for console display.
        
        Args:
            summary: Chains summary dictionary
            
        Returns:
            Formatted chains summary
        """
        output = []
        output.append("Task Chains Summary")
        output.append("═" * 19)
        output.append("")
        
        total_chains = summary.get('total_chains', 0)
        active_chains = summary.get('active_chains', 0)
        output.append(f"Total Chains: {total_chains}")
        output.append(f"Active Chains: {active_chains}")
        
        chains_with_issues = summary.get('chains_with_issues', 0)
        if chains_with_issues > 0:
            output.append(f"Chains with Issues: {chains_with_issues}")
        
        total_todos = summary.get('total_todos_in_chains', 0)
        if total_todos > 0:
            output.append(f"Todos in Chains: {total_todos}")
        
        output.append("")
        
        # Individual chains
        chains = summary.get('chains', [])
        if chains:
            output.append("Chains:")
            for chain in chains[:5]:  # Show top 5
                name = chain.get('name', 'Unnamed')
                health = chain.get('health', 'unknown')
                todo_count = chain.get('todo_count', 0)
                
                health_symbol = {
                    'excellent': '🟢',
                    'good': '🟡',
                    'fair': '🟠', 
                    'poor': '🔴',
                    'unknown': '⚪'
                }.get(health, '⚪')
                
                output.append(f"  {health_symbol} {name} ({todo_count} todos)")
            
            if len(chains) > 5:
                output.append(f"  ... and {len(chains) - 5} more")
        
        return "\n".join(output)
    
    def format_ai_enhancement_summary(self, summary: Dict[str, Any]) -> str:
        """
        Format AI enhancement summary for console display.
        
        Args:
            summary: AI enhancement summary dictionary
            
        Returns:
            Formatted enhancement summary
        """
        if "error" in summary:
            return f"Error: {summary['error']}"
        
        output = []
        output.append("AI Enhancement Opportunities")
        output.append("═" * 28)
        output.append("")
        
        total_opportunities = summary.get('total_opportunities', 0)
        output.append(f"Total Opportunities: {total_opportunities}")
        
        if total_opportunities == 0:
            output.append("No AI enhancement opportunities found.")
            return "\n".join(output)
        
        # By component
        by_component = summary.get('opportunities_by_component', {})
        if by_component:
            output.append("")
            output.append("By Component:")
            for component, count in by_component.items():
                output.append(f"  {component}: {count} files")
        
        # Estimated time
        estimated_time = summary.get('estimated_enhancement_time', 0)
        if estimated_time > 0:
            hours = estimated_time // 60
            minutes = estimated_time % 60
            time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            output.append(f"Estimated Time: {time_str}")
        
        # AI readiness score
        readiness_score = summary.get('ai_readiness_score', 0)
        output.append(f"AI Readiness Score: {readiness_score:.1%}")
        output.append("")
        
        # Prioritized tasks
        prioritized = summary.get('prioritized_tasks', [])
        if prioritized:
            output.append("Top Priorities:")
            for i, task in enumerate(prioritized[:5], 1):
                file_type = task.get('file_type', 'unknown')
                placeholder_count = task.get('placeholder_count', 0)
                output.append(f"  {i}. {file_type} ({placeholder_count} placeholders)")
        
        return "\n".join(output)