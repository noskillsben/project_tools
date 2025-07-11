#!/usr/bin/env python3
"""
Universal Todo Manager

A reusable todo tracking system for any project with priority management,
status tracking, and category organization.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


class TodoManager:
    """
    Universal todo management system.
    
    Features:
    - Priority-based todo tracking (1-10 scale, configurable)
    - Status management (configurable statuses)
    - Category organization (configurable categories)
    - Flexible file location
    - Optional email integration via formatters
    """
    
    def __init__(self, 
                 todo_path: Union[str, Path] = None,
                 project_root: Union[str, Path] = None,
                 categories: List[str] = None,
                 statuses: List[str] = None,
                 priority_scale: str = "1-10 (10=highest)"):
        """
        Initialize the todo manager.
        
        Args:
            todo_path: Path to todo.json file (default: project_root/todo.json)
            project_root: Project root directory (default: auto-detect)
            categories: Available categories (default: standard set)
            statuses: Available statuses (default: standard set)
            priority_scale: Description of priority scale
        """
        # Set project root
        if project_root is None:
            project_root = self._detect_project_root()
        self.project_root = Path(project_root)
        
        # Set todo file path
        if todo_path is None:
            todo_path = self.project_root / 'todo.json'
        self.todo_path = Path(todo_path)
        
        # Set defaults
        self.default_categories = categories or [
            "bug", "feature", "enhancement", "docs", "refactor", "test"
        ]
        self.default_statuses = statuses or [
            "todo", "in_progress", "testing", "complete"
        ]
        self.priority_scale = priority_scale
        
        # Load data
        self.todo_data = self._load_todos()
    
    def _detect_project_root(self) -> Path:
        """Auto-detect project root directory."""
        # Start from current file location and go up
        current = Path(__file__).resolve()
        
        # Look for common project indicators
        indicators = ['.git', 'pyproject.toml', 'setup.py', 'requirements.txt', 
                     'package.json', 'Cargo.toml', '.gitignore']
        
        for parent in [current.parent] + list(current.parents):
            for indicator in indicators:
                if (parent / indicator).exists():
                    return parent
        
        # Fallback to parent of current file
        return current.parent.parent
    
    def _load_todos(self) -> Dict[str, Any]:
        """Load todo data from JSON file."""
        try:
            if self.todo_path.exists():
                with open(self.todo_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Ensure required structure exists
                data.setdefault('todos', [])
                data.setdefault('categories', self.default_categories)
                data.setdefault('statuses', self.default_statuses)
                data.setdefault('priority_scale', self.priority_scale)
                data.setdefault('dependencies', {})
                
                return data
            else:
                # Create default structure
                default_data = {
                    "todos": [],
                    "categories": self.default_categories,
                    "statuses": self.default_statuses,
                    "priority_scale": self.priority_scale,
                    "dependencies": {}
                }
                self._save_todos(default_data)
                return default_data
        except Exception as e:
            print(f"Error loading todos: {e}")
            return {
                "todos": [], 
                "categories": self.default_categories, 
                "statuses": self.default_statuses,
                "priority_scale": self.priority_scale,
                "dependencies": {}
            }
    
    def _save_todos(self, data: Dict[str, Any] = None) -> bool:
        """Save todo data to JSON file."""
        try:
            # Ensure directory exists
            self.todo_path.parent.mkdir(parents=True, exist_ok=True)
            
            data_to_save = data if data is not None else self.todo_data
            with open(self.todo_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving todos: {e}")
            return False
    
    def get_todos(self, 
                  status: str = None, 
                  category: str = None, 
                  min_priority: int = None,
                  max_priority: int = None,
                  sort_by: str = 'priority') -> List[Dict[str, Any]]:
        """
        Get todos with optional filtering.
        
        Args:
            status: Filter by status
            category: Filter by category
            min_priority: Minimum priority level
            max_priority: Maximum priority level
            sort_by: Sort field ('priority', 'id', 'created_date')
            
        Returns:
            Filtered and sorted list of todos
        """
        todos = self.todo_data.get('todos', [])
        
        # Apply filters
        if status:
            todos = [t for t in todos if t.get('status') == status]
        
        if category:
            todos = [t for t in todos if t.get('category') == category]
        
        if min_priority is not None:
            todos = [t for t in todos if t.get('priority', 0) >= min_priority]
        
        if max_priority is not None:
            todos = [t for t in todos if t.get('priority', 0) <= max_priority]
        
        # Sort todos
        if sort_by == 'priority':
            todos.sort(key=lambda x: (-x.get('priority', 0), x.get('id', 0)))
        elif sort_by == 'id':
            todos.sort(key=lambda x: x.get('id', 0))
        elif sort_by == 'created_date':
            todos.sort(key=lambda x: x.get('created_date', ''), reverse=True)
        
        return todos
    
    def get_high_priority_todos(self, min_priority: int = 8) -> List[Dict[str, Any]]:
        """Get high priority todos."""
        return self.get_todos(min_priority=min_priority, status='todo')
    
    def get_in_progress_todos(self) -> List[Dict[str, Any]]:
        """Get todos currently in progress."""
        return self.get_todos(status='in_progress')
    
    def get_todo_by_id(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific todo by ID."""
        for todo in self.todo_data.get('todos', []):
            if todo.get('id') == todo_id:
                return todo
        return None
    
    def add_todo(self, 
                 title: str,
                 description: str = "",
                 priority: int = 5,
                 category: str = 'feature',
                 target_date: str = None,
                 notes: str = None,
                 custom_fields: Dict[str, Any] = None) -> int:
        """
        Add a new todo item.
        
        Args:
            title: Todo title
            description: Detailed description
            priority: Priority level (1-10 by default)
            category: Category
            target_date: Target completion date (YYYY-MM-DD)
            notes: Additional notes
            custom_fields: Additional custom fields
            
        Returns:
            ID of created todo (-1 if failed)
        """
        todos = self.todo_data.get('todos', [])
        
        # Get next ID
        next_id = max([t.get('id', 0) for t in todos], default=0) + 1
        
        # Create new todo
        new_todo = {
            'id': next_id,
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'todo',
            'category': category,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'target_date': target_date,
            'notes': notes
        }
        
        # Add custom fields
        if custom_fields:
            new_todo.update(custom_fields)
        
        todos.append(new_todo)
        self.todo_data['todos'] = todos
        
        if self._save_todos():
            return next_id
        else:
            return -1
    
    def update_todo_status(self, todo_id: int, status: str) -> bool:
        """Update the status of a todo item."""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo['status'] = status
            if status == 'complete':
                todo['completed_date'] = datetime.now().strftime('%Y-%m-%d')
            
            return self._save_todos()
        
        return False
    
    def update_todo_priority(self, todo_id: int, priority: int) -> bool:
        """Update the priority of a todo item."""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo['priority'] = priority
            return self._save_todos()
        
        return False
    
    def update_todo(self, todo_id: int, **updates) -> bool:
        """Update any fields of a todo item."""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.update(updates)
            return self._save_todos()
        
        return False
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item."""
        todos = self.todo_data.get('todos', [])
        original_count = len(todos)
        
        self.todo_data['todos'] = [t for t in todos if t.get('id') != todo_id]
        
        if len(self.todo_data['todos']) < original_count:
            return self._save_todos()
        
        return False
    
    def complete_todo(self, todo_id: int) -> bool:
        """Complete a todo item."""
        return self.update_todo_status(todo_id, 'complete')
    
    def add_dependency(self, todo_id: int, depends_on_id: int) -> bool:
        """
        Add a dependency for a todo item.
        
        Args:
            todo_id: ID of the todo that depends on another
            depends_on_id: ID of the todo this one depends on
            
        Returns:
            True if dependency was added successfully
        """
        # Validate that both todos exist
        if not self.get_todo_by_id(todo_id) or not self.get_todo_by_id(depends_on_id):
            return False
        
        # Check for circular dependency
        if self._would_create_circular_dependency(todo_id, depends_on_id):
            return False
        
        dependencies = self.todo_data.setdefault('dependencies', {})
        todo_deps = dependencies.setdefault(str(todo_id), [])
        
        if depends_on_id not in todo_deps:
            todo_deps.append(depends_on_id)
            return self._save_todos()
        
        return True
    
    def remove_dependency(self, todo_id: int, depends_on_id: int) -> bool:
        """Remove a dependency for a todo item."""
        dependencies = self.todo_data.get('dependencies', {})
        todo_deps = dependencies.get(str(todo_id), [])
        
        if depends_on_id in todo_deps:
            todo_deps.remove(depends_on_id)
            if not todo_deps:
                del dependencies[str(todo_id)]
            return self._save_todos()
        
        return False
    
    def get_blocked_todos(self) -> List[Dict[str, Any]]:
        """Get todos that are blocked by incomplete dependencies."""
        blocked = []
        dependencies = self.todo_data.get('dependencies', {})
        
        for todo_id_str, dep_ids in dependencies.items():
            todo_id = int(todo_id_str)
            todo = self.get_todo_by_id(todo_id)
            
            if not todo or todo.get('status') == 'complete':
                continue
            
            # Check if any dependencies are incomplete
            for dep_id in dep_ids:
                dep_todo = self.get_todo_by_id(dep_id)
                if not dep_todo or dep_todo.get('status') != 'complete':
                    blocked.append(todo)
                    break
        
        return blocked
    
    def get_unblocked_todos(self) -> List[Dict[str, Any]]:
        """Get todos that are ready to work on (no incomplete dependencies)."""
        all_todos = [t for t in self.get_todos() if t.get('status') != 'complete']
        blocked_ids = [t['id'] for t in self.get_blocked_todos()]
        return [t for t in all_todos if t['id'] not in blocked_ids]
    
    def get_dependency_chain(self, todo_id: int) -> Dict[str, Any]:
        """
        Get the full dependency tree for a todo.
        
        Returns:
            Dictionary with 'dependencies' and 'dependents' lists
        """
        dependencies = self._get_dependencies_recursive(todo_id, set())
        dependents = self._get_dependents_recursive(todo_id, set())
        
        return {
            'todo_id': todo_id,
            'dependencies': list(dependencies),
            'dependents': list(dependents)
        }
    
    def _get_dependencies_recursive(self, todo_id: int, visited: set) -> set:
        """Recursively get all dependencies for a todo."""
        if todo_id in visited:
            return set()
        
        visited.add(todo_id)
        dependencies = set()
        
        todo_deps = self.todo_data.get('dependencies', {}).get(str(todo_id), [])
        for dep_id in todo_deps:
            dependencies.add(dep_id)
            dependencies.update(self._get_dependencies_recursive(dep_id, visited.copy()))
        
        return dependencies
    
    def _get_dependents_recursive(self, todo_id: int, visited: set) -> set:
        """Recursively get all todos that depend on this one."""
        if todo_id in visited:
            return set()
        
        visited.add(todo_id)
        dependents = set()
        
        dependencies = self.todo_data.get('dependencies', {})
        for dependent_id_str, dep_list in dependencies.items():
            dependent_id = int(dependent_id_str)
            if todo_id in dep_list:
                dependents.add(dependent_id)
                dependents.update(self._get_dependents_recursive(dependent_id, visited.copy()))
        
        return dependents
    
    def _would_create_circular_dependency(self, todo_id: int, depends_on_id: int) -> bool:
        """Check if adding a dependency would create a circular dependency."""
        dependents = self._get_dependents_recursive(depends_on_id, set())
        return todo_id in dependents
    
    def complete_todo_with_changelog(self, todo_id: int, version_manager, change_type: str, 
                                   change_description: str = None, auto_version_bump: bool = False) -> bool:
        """
        Complete a todo and add corresponding changelog entry.
        
        Args:
            todo_id: ID of todo to complete
            version_manager: VersionManager instance
            change_type: Type of change for changelog
            change_description: Custom description (uses todo title if None)
            auto_version_bump: Whether to automatically bump version
            
        Returns:
            True if both operations succeeded
        """
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        # Complete the todo
        if not self.complete_todo(todo_id):
            return False
        
        # Add to changelog
        description = change_description or todo.get('title', f'Todo #{todo_id}')
        success = version_manager.add_change_from_todo(todo_id, self, change_type, description)
        
        if success and auto_version_bump:
            # Determine bump type based on change type
            bump_type = 'patch'
            if change_type == 'feature':
                bump_type = 'minor'
            elif change_type in ['breaking', 'major']:
                bump_type = 'major'
            
            version_manager.bump_version(bump_type, f'Auto-bump for completed todo #{todo_id}')
        
        return success
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics for todos."""
        all_todos = self.get_todos()
        
        summary = {
            'total': len(all_todos),
            'by_status': {},
            'by_category': {},
            'by_priority': {},
            'high_priority_count': len(self.get_high_priority_todos()),
            'in_progress_count': len(self.get_in_progress_todos()),
            'blocked_count': len(self.get_blocked_todos()),
            'unblocked_count': len(self.get_unblocked_todos()),
            'dependencies_count': len(self.todo_data.get('dependencies', {})),
            'project_root': str(self.project_root),
            'todo_file': str(self.todo_path)
        }
        
        # Count by status
        for status in self.todo_data.get('statuses', []):
            summary['by_status'][status] = len(self.get_todos(status=status))
        
        # Count by category
        for category in self.todo_data.get('categories', []):
            summary['by_category'][category] = len(self.get_todos(category=category))
        
        # Count by priority ranges
        summary['by_priority'] = {
            'critical (9-10)': len(self.get_todos(min_priority=9)),
            'high (7-8)': len(self.get_todos(min_priority=7, max_priority=8)),
            'medium (4-6)': len(self.get_todos(min_priority=4, max_priority=6)),
            'low (1-3)': len(self.get_todos(min_priority=1, max_priority=3))
        }
        
        return summary
    
    def export_todos(self, format: str = 'json') -> str:
        """
        Export todos in various formats.
        
        Args:
            format: Export format ('json', 'csv', 'markdown')
            
        Returns:
            Exported data as string
        """
        todos = self.get_todos()
        
        if format == 'json':
            return json.dumps(todos, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            if todos:
                fieldnames = todos[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(todos)
            
            return output.getvalue()
        
        elif format == 'markdown':
            md = "# Todos\n\n"
            
            for status in self.todo_data.get('statuses', []):
                status_todos = self.get_todos(status=status)
                if status_todos:
                    md += f"## {status.title()}\n\n"
                    for todo in status_todos:
                        md += f"- **#{todo['id']}**: {todo['title']} (Priority: {todo['priority']})\n"
                        if todo.get('description'):
                            md += f"  - {todo['description']}\n"
                    md += "\n"
            
            return md
        
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Console usage example
if __name__ == "__main__":
    # Create todo manager (will auto-detect project root)
    tm = TodoManager()
    
    # Print summary
    summary = tm.get_summary()
    print(f"Todo Summary for: {summary['project_root']}")
    print(f"  Total: {summary['total']}")
    print(f"  High Priority: {summary['high_priority_count']}")
    print(f"  In Progress: {summary['in_progress_count']}")
    print()
    
    # Show high priority todos
    high_priority = tm.get_high_priority_todos()
    if high_priority:
        print("High Priority Todos:")
        for todo in high_priority:
            print(f"  #{todo['id']}: {todo['title']} (Priority: {todo['priority']})")
    else:
        print("No high priority todos")