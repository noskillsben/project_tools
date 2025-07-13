#!/usr/bin/env python3
"""
Email Formatter for Project Tools

Provides HTML email formatting for todos and version changes.
"""

from typing import List, Dict, Any, Optional


class EmailFormatter:
    """
    Email formatter for todos and version changes.
    
    Generates HTML-formatted content suitable for email inclusion.
    """
    
    def __init__(self, 
                 todo_section_title: str = "📋 Current Todos",
                 changes_section_title: str = "🔄 Recent Changes"):
        """
        Initialize the email formatter.
        
        Args:
            todo_section_title: Title for todo section
            changes_section_title: Title for changes section
        """
        self.todo_section_title = todo_section_title
        self.changes_section_title = changes_section_title
    
    def format_todos_for_email(self, 
                              todo_manager,
                              include_in_progress: bool = True,
                              min_priority: int = 8) -> str:
        """
        Format todos for inclusion in email.
        
        Args:
            todo_manager: _TodoManager instance
            include_in_progress: Whether to include in-progress todos
            min_priority: Minimum priority for high-priority todos
            
        Returns:
            HTML formatted todo section
        """
        # Get all incomplete todos (priority >= min_priority and not completed)
        all_todos = todo_manager.get_todos(min_priority=min_priority, sort_by='priority')
        incomplete_todos = [t for t in all_todos if t['status'] not in ['complete', 'completed']]
        
        if not incomplete_todos:
            return ""
        
        # Get dependency information
        blocked_todos = todo_manager.get_blocked_todos()
        blocked_ids = [t['id'] for t in blocked_todos]
        
        html = f'''
        <div style="margin-bottom: 30px; background: linear-gradient(135deg, #fff3e0, #fce4ec); border-radius: 12px; padding: 20px; border-left: 4px solid #ff9800;">
            <h2 style="font-size: 20px; font-weight: bold; margin: 0 0 15px 0; color: #f57c00;">{self.todo_section_title}</h2>
        '''
        
        # Separate blocked and unblocked todos
        ready_todos = [t for t in incomplete_todos if t['id'] not in blocked_ids]
        blocked_incomplete = [t for t in incomplete_todos if t['id'] in blocked_ids]
        
        # Ready to work todos first
        if ready_todos:
            html += '<div style="margin-bottom: 15px;">'
            html += '<h3 style="font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #2e7d32;">✅ Ready to Work (Priority Order)</h3>'
            html += '<ul style="margin: 0 0 0 20px; padding: 0;">'
            
            for todo in ready_todos:
                # Status indicators
                if todo['status'] == 'in_progress':
                    status_indicator = "🔄"
                    status_color = "#1976d2"
                else:
                    status_indicator = "📌"
                    status_color = "#666"
                
                # Priority indicators
                if todo['priority'] >= 9:
                    priority_indicator = "🔴"
                elif todo['priority'] >= 7:
                    priority_indicator = "🟡"
                else:
                    priority_indicator = "🟢"
                    
                category_emoji = self._get_category_emoji(todo.get('category', 'feature'))
                dep_symbol = self._get_dependency_symbol_html(todo, todo_manager)
                
                html += f'''
                <li style="margin-bottom: 8px; line-height: 1.4;">
                    <strong>{priority_indicator} {status_indicator} {dep_symbol} #{todo['id']}: {todo['title']}</strong> {category_emoji}
                    <br><span style="font-size: 14px; color: #666; margin-left: 20px;">Priority {todo['priority']} • {todo.get('description', '')}</span>
                </li>
                '''
            
            html += '</ul></div>'
        
        # Blocked todos section
        if blocked_incomplete:
            html += '<div style="margin-bottom: 10px;">'
            html += '<h3 style="font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #d32f2f;">⏳ Blocked Tasks</h3>'
            html += '<ul style="margin: 0 0 0 20px; padding: 0;">'
            
            for todo in blocked_incomplete:
                # Get blocking dependencies
                todo_deps = todo_manager.todo_data.get('dependencies', {}).get(str(todo['id']), [])
                blocking_todos = []
                
                for dep_id in todo_deps:
                    dep_todo = todo_manager.get_todo_by_id(dep_id)
                    if dep_todo and dep_todo.get('status') != 'complete':
                        blocking_todos.append(f"#{dep_id}")
                
                blocking_text = ", ".join(blocking_todos) if blocking_todos else "Unknown"
                
                # Priority indicators
                if todo['priority'] >= 9:
                    priority_indicator = "🔴"
                elif todo['priority'] >= 7:
                    priority_indicator = "🟡"
                else:
                    priority_indicator = "🟢"
                    
                category_emoji = self._get_category_emoji(todo.get('category', 'feature'))
                
                html += f'''
                <li style="margin-bottom: 8px; line-height: 1.4; opacity: 0.7;">
                    <strong>{priority_indicator} ⏳ #{todo['id']}: {todo['title']}</strong> {category_emoji}
                    <br><span style="font-size: 14px; color: #666; margin-left: 20px;">Priority {todo['priority']} • Waiting for: {blocking_text}</span>
                </li>
                '''
            
            html += '</ul></div>'
        
        html += '</div>'
        return html
    
    def format_changes_for_email(self, 
                                version_manager,
                                days: int = 1) -> str:
        """
        Format recent changes for inclusion in email.
        
        Args:
            version_manager: _VersionManager instance
            days: Number of days to look back
            
        Returns:
            HTML formatted changes section
        """
        recent_changes = version_manager.get_recent_changes(days)
        
        if not recent_changes:
            return ""
        
        html = f'''
        <div style="margin-bottom: 30px; background: linear-gradient(135deg, #f8f9fa, #e3f2fd); border-radius: 12px; padding: 20px; border-left: 4px solid #2196f3;">
            <h2 style="font-size: 20px; font-weight: bold; margin: 0 0 15px 0; color: #1976d2;">{self.changes_section_title}</h2>
        '''
        
        # Group changes by date first, then by version
        changes_by_date = {}
        for change in recent_changes:
            date = change['date']
            if date not in changes_by_date:
                changes_by_date[date] = {}
            
            version = change['version']
            if version not in changes_by_date[date]:
                changes_by_date[date][version] = []
            changes_by_date[date][version].append(change)
        
        # Sort dates (newest first)
        for date in sorted(changes_by_date.keys(), reverse=True):
            # Add date header
            html += f'<div style="margin-bottom: 20px;">'
            html += f'<h3 style="font-size: 18px; font-weight: bold; margin: 0 0 10px 0; color: #1565c0; border-bottom: 1px solid #e0e0e0; padding-bottom: 5px;">📅 {date}</h3>'
            
            # Sort versions within the date (newest first)
            versions_for_date = changes_by_date[date]
            for version in sorted(versions_for_date.keys(), key=lambda v: [int(x) for x in v.split('.')], reverse=True):
                changes = versions_for_date[version]
                
                html += f'<div style="margin-bottom: 15px; margin-left: 15px;">'
                html += f'<h4 style="font-size: 16px; font-weight: bold; margin: 0 0 8px 0; color: #1976d2;">🚀 Version {version}</h4>'
                html += '<ul style="margin: 0 0 10px 20px; padding: 0;">'
                
                for change in changes:
                    emoji = self._get_change_emoji(change.get('type', 'feature'))
                    todo_ref = f" (#{change['todo_id']})" if change.get('todo_id') else ""
                    html += f'<li style="margin-bottom: 5px;">{emoji} {change.get("description", "")}{todo_ref}</li>'
                
                html += '</ul></div>'
            
            html += '</div>'
        
        html += '</div>'
        return html
    
    def format_combined_report(self,
                              todo_manager,
                              version_manager,
                              include_todos: bool = True,
                              include_changes: bool = True,
                              todo_min_priority: int = 8,
                              changes_days: int = 1) -> str:
        """
        Format a combined todos and changes report for email.
        
        Args:
            todo_manager: _TodoManager instance
            version_manager: _VersionManager instance
            include_todos: Whether to include todos section
            include_changes: Whether to include changes section
            todo_min_priority: Minimum priority for todos
            changes_days: Days to look back for changes
            
        Returns:
            HTML formatted combined report
        """
        sections = []
        
        if include_changes:
            changes_html = self.format_changes_for_email(version_manager, changes_days)
            if changes_html:
                sections.append(changes_html)
        
        if include_todos:
            todos_html = self.format_todos_for_email(todo_manager, min_priority=todo_min_priority)
            if todos_html:
                sections.append(todos_html)
        
        return ''.join(sections)
    
    def _get_category_emoji(self, category: str) -> str:
        """Get emoji for todo category."""
        emoji_map = {
            'bug': '🐛',
            'feature': '✨', 
            'enhancement': '🚀',
            'docs': '📚',
            'refactor': '♻️',
            'test': '🧪'
        }
        return emoji_map.get(category.lower(), '🔧')
    
    def _get_change_emoji(self, change_type: str) -> str:
        """Get emoji for change type."""
        emoji_map = {
            'feature': '✨',
            'bug': '🐛', 
            'enhancement': '🚀',
            'docs': '📚',
            'refactor': '♻️',
            'test': '🧪'
        }
        return emoji_map.get(change_type.lower(), '🔧')
    
    def create_summary_table(self,
                           todo_manager,
                           version_manager) -> str:
        """
        Create a summary table for email header.
        
        Args:
            todo_manager: _TodoManager instance
            version_manager: _VersionManager instance
            
        Returns:
            HTML formatted summary table
        """
        todo_summary = todo_manager.get_summary()
        version_summary = version_manager.get_version_summary()
        
        html = '''
        <div style="margin-bottom: 20px; background: #f5f5f5; border-radius: 8px; padding: 15px;">
            <h3 style="margin: 0 0 10px 0; color: #333;">📊 Project Summary</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 5px; font-weight: bold;">Version:</td>
                    <td style="padding: 5px;">{version}</td>
                    <td style="padding: 5px; font-weight: bold;">Total Todos:</td>
                    <td style="padding: 5px;">{total_todos}</td>
                </tr>
                <tr>
                    <td style="padding: 5px; font-weight: bold;">High Priority:</td>
                    <td style="padding: 5px;">{high_priority}</td>
                    <td style="padding: 5px; font-weight: bold;">In Progress:</td>
                    <td style="padding: 5px;">{in_progress}</td>
                </tr>
                <tr>
                    <td style="padding: 5px; font-weight: bold;">Blocked:</td>
                    <td style="padding: 5px;">{blocked}</td>
                    <td style="padding: 5px; font-weight: bold;">Ready to Work:</td>
                    <td style="padding: 5px;">{ready}</td>
                </tr>
            </table>
        </div>
        '''.format(
            version=version_summary['current_version'],
            total_todos=todo_summary['total'],
            high_priority=todo_summary['high_priority_count'],
            in_progress=todo_summary['in_progress_count'],
            blocked=todo_summary.get('blocked_count', 0),
            ready=todo_summary.get('unblocked_count', 0)
        )
        
        return html
    
    def _get_dependency_symbol_html(self, todo: Dict[str, Any], todo_manager) -> str:
        """Get HTML symbol indicating dependency status."""
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
            return ''  # No dependencies
    
    def format_integration_report(self, todo_manager, version_manager) -> str:
        """
        Format integration report showing recent todo completions with changelog entries.
        
        Args:
            todo_manager: _TodoManager instance
            version_manager: _VersionManager instance
            
        Returns:
            HTML formatted integration report
        """
        recent_changes = version_manager.get_recent_changes(30)
        todo_ids_in_changelog = [c.get('todo_id') for c in recent_changes if c.get('todo_id')]
        completed_todos = todo_manager.get_todos(status='complete')
        
        # Find completed todos that have corresponding changelog entries
        integrated_todos = []
        unlogged_todos = []
        
        for todo in completed_todos:
            if todo['id'] in todo_ids_in_changelog:
                # Find the corresponding changelog entry
                changelog_entry = next((c for c in recent_changes if c.get('todo_id') == todo['id']), None)
                integrated_todos.append((todo, changelog_entry))
            else:
                unlogged_todos.append(todo)
        
        if not integrated_todos and not unlogged_todos:
            return ""
        
        html = '''
        <div style="margin-bottom: 30px; background: linear-gradient(135deg, #e8f5e8, #f0f8ff); border-radius: 12px; padding: 20px; border-left: 4px solid #4caf50;">
            <h2 style="font-size: 20px; font-weight: bold; margin: 0 0 15px 0; color: #2e7d32;">🔗 Integration Report</h2>
        '''
        
        if integrated_todos:
            html += '<div style="margin-bottom: 15px;">'
            html += '<h3 style="font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #2e7d32;">✅ Recently Completed & Logged</h3>'
            html += '<ul style="margin: 0 0 0 20px; padding: 0;">'
            
            for todo, change in integrated_todos:
                change_emoji = self._get_change_emoji(change.get('type', 'feature'))
                html += f'''
                <li style="margin-bottom: 8px; line-height: 1.4;">
                    <strong>✓ #{todo['id']}: {todo.get('title', '')}</strong>
                    <br><span style="font-size: 14px; color: #666; margin-left: 20px;">{change_emoji} {change.get('type', 'feature')}: {change.get('description', '')}</span>
                </li>
                '''
            
            html += '</ul></div>'
        
        if unlogged_todos:
            html += '<div style="margin-bottom: 10px;">'
            html += '<h3 style="font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #f57c00;">⚠️ Completed but Not Logged</h3>'
            html += '<ul style="margin: 0 0 0 20px; padding: 0;">'
            
            for todo in unlogged_todos[:5]:  # Show max 5
                html += f'''
                <li style="margin-bottom: 5px; line-height: 1.4;">
                    <strong>#{todo['id']}: {todo.get('title', '')}</strong>
                    <span style="font-size: 12px; color: #999; margin-left: 10px;">(needs changelog entry)</span>
                </li>
                '''
            
            if len(unlogged_todos) > 5:
                html += f'<li style="font-style: italic; color: #666;">... and {len(unlogged_todos) - 5} more</li>'
            
            html += '</ul></div>'
        
        html += '</div>'
        return html