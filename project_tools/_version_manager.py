#!/usr/bin/env python3
"""
Universal Version Manager

A reusable version tracking and changelog management system for any project
with semantic versioning, git integration, and flexible change tracking.
"""

import json
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


class _VersionManager:
    """
    Universal version tracking and changelog management system.
    
    Features:
    - Semantic versioning (MAJOR.MINOR.PATCH)
    - Changelog tracking with optional todo references
    - Optional git tag integration 
    - Flexible file location
    - Optional email integration via formatters
    """
    
    def __init__(self, 
                 changelog_path: Union[str, Path] = None,
                 project_root: Union[str, Path] = None,
                 enable_git: bool = True,
                 initial_version: str = "1.0.0"):
        """
        Initialize the version manager.
        
        Args:
            changelog_path: Path to changelog.json file (default: project_root/changelog.json)
            project_root: Project root directory (default: auto-detect)
            enable_git: Whether to enable git operations
            initial_version: Initial version if creating new changelog
        """
        # Set project root
        if project_root is None:
            project_root = self._detect_project_root()
        self.project_root = Path(project_root)
        
        # Set changelog file path
        if changelog_path is None:
            changelog_path = self.project_root / 'changelog.json'
        self.changelog_path = Path(changelog_path)
        
        # Configuration
        self.enable_git = enable_git
        self.initial_version = initial_version
        
        # Load data
        self.changelog_data = self._load_changelog()
    
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
    
    def _load_changelog(self) -> Dict[str, Any]:
        """Load changelog data from JSON file."""
        try:
            if self.changelog_path.exists():
                with open(self.changelog_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Ensure required structure
                data.setdefault('current_version', self.initial_version)
                data.setdefault('versions', {})
                
                return data
            else:
                # Create default structure
                default_data = {
                    "current_version": self.initial_version,
                    "versions": {
                        self.initial_version: {
                            "date": datetime.now().strftime('%Y-%m-%d'),
                            "changes": [
                                {
                                    "type": "feature",
                                    "description": "Initial release with version management system",
                                    "todo_id": None
                                }
                            ]
                        }
                    }
                }
                self._save_changelog(default_data)
                return default_data
        except Exception as e:
            print(f"Error loading changelog: {e}")
            return {
                "current_version": self.initial_version, 
                "versions": {}
            }
    
    def _save_changelog(self, data: Dict[str, Any] = None) -> bool:
        """Save changelog data to JSON file."""
        try:
            # Ensure directory exists
            self.changelog_path.parent.mkdir(parents=True, exist_ok=True)
            
            data_to_save = data if data is not None else self.changelog_data
            with open(self.changelog_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving changelog: {e}")
            return False
    
    def get_current_version(self) -> str:
        """Get the current version string."""
        return self.changelog_data.get('current_version', self.initial_version)
    
    def get_version_info(self, version: str = None) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific version.
        
        Args:
            version: Version to get info for (default: current)
            
        Returns:
            Version information or None if not found
        """
        if version is None:
            version = self.get_current_version()
        
        return self.changelog_data.get('versions', {}).get(version)
    
    def get_all_versions(self, sort_desc: bool = True) -> List[str]:
        """
        Get all version numbers.
        
        Args:
            sort_desc: Sort in descending order (newest first)
            
        Returns:
            List of version strings
        """
        versions = list(self.changelog_data.get('versions', {}).keys())
        
        # Sort by semantic version
        try:
            versions.sort(
                key=lambda v: [int(x) for x in v.split('.')], 
                reverse=sort_desc
            )
        except ValueError:
            # Fallback to string sort if not semantic versioning
            versions.sort(reverse=sort_desc)
        
        return versions
    
    def get_recent_changes(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get changes from the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of change entries with version info
        """
        cutoff_date = datetime.now().date()
        recent_changes = []
        
        for version, version_data in self.changelog_data.get('versions', {}).items():
            try:
                version_date = datetime.strptime(version_data['date'], '%Y-%m-%d').date()
                days_ago = (cutoff_date - version_date).days
                
                if days_ago <= days:
                    for change in version_data.get('changes', []):
                        change_with_version = change.copy()
                        change_with_version['version'] = version
                        change_with_version['date'] = version_data['date']
                        recent_changes.append(change_with_version)
            except (ValueError, KeyError) as e:
                continue
        
        # Sort by date (newest first)
        recent_changes.sort(key=lambda x: x['date'], reverse=True)
        return recent_changes
    
    def add_change(self, 
                   change_type: str, 
                   description: str, 
                   todo_id: Optional[int] = None,
                   version: str = None,
                   custom_fields: Dict[str, Any] = None) -> bool:
        """
        Add a change to the specified version.
        
        Args:
            change_type: Type of change (feature, bug, enhancement, docs, refactor)
            description: Description of the change
            todo_id: Associated todo ID if applicable
            version: Version to add to (default: current)
            custom_fields: Additional custom fields
            
        Returns:
            True if change added successfully
        """
        if version is None:
            version = self.get_current_version()
        
        # Ensure version exists
        if version not in self.changelog_data.get('versions', {}):
            self.changelog_data.setdefault('versions', {})[version] = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'changes': []
            }
        
        # Add the change
        change_entry = {
            'type': change_type,
            'description': description,
            'todo_id': todo_id
        }
        
        # Add custom fields
        if custom_fields:
            change_entry.update(custom_fields)
        
        self.changelog_data['versions'][version]['changes'].append(change_entry)
        
        return self._save_changelog()
    
    def add_change_from_todo(self, todo_id: int, todo_manager, change_type: str, 
                           custom_description: str = None) -> bool:
        """
        Add a changelog entry from a todo item.
        
        Args:
            todo_id: ID of the todo item
            todo_manager: TodoManager instance
            change_type: Type of change for changelog
            custom_description: Custom description (uses todo title if None)
            
        Returns:
            True if change added successfully
        """
        todo = todo_manager.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        description = custom_description or todo.get('title', f'Todo #{todo_id}')
        
        # Include additional metadata from todo
        custom_fields = {
            'todo_priority': todo.get('priority'),
            'todo_category': todo.get('category')
        }
        
        return self.add_change(
            change_type=change_type,
            description=description,
            todo_id=todo_id,
            custom_fields=custom_fields
        )
    
    def complete_todo_and_log(self, todo_id: int, todo_manager, change_type: str, 
                            auto_bump: bool = False) -> bool:
        """
        Complete a todo and add corresponding changelog entry.
        
        Args:
            todo_id: ID of todo to complete
            todo_manager: TodoManager instance  
            change_type: Type of change for changelog
            auto_bump: Whether to automatically bump version
            
        Returns:
            True if both operations succeeded
        """
        # Validate todo exists
        todo = todo_manager.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        # Complete the todo
        if not todo_manager.complete_todo(todo_id):
            return False
        
        # Add to changelog
        success = self.add_change_from_todo(todo_id, todo_manager, change_type)
        
        if success and auto_bump:
            # Determine bump type based on change type
            bump_type = 'patch'
            if change_type == 'feature':
                bump_type = 'minor'
            elif change_type in ['breaking', 'major']:
                bump_type = 'major'
            
            self.bump_version(bump_type, f'Auto-bump for completed todo #{todo_id}')
        
        return success
    
    def bump_version(self, version_type: str = 'patch', message: str = None) -> str:
        """
        Bump version and return new version number.
        
        Args:
            version_type: Type of version bump (major, minor, patch)
            message: Optional message for the version
            
        Returns:
            New version number
        """
        current_version = self.get_current_version()
        new_version = self._increment_version(current_version, version_type)
        
        # Create new version entry
        self.changelog_data['versions'][new_version] = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'changes': []
        }
        
        # Add message as a change if provided
        if message:
            self.add_change('docs', message, version=new_version)
        
        # Update current version
        self.changelog_data['current_version'] = new_version
        
        # Save changes
        if self._save_changelog():
            return new_version
        else:
            return current_version
    
    def get_changelog(self) -> Dict[str, Any]:
        """Get the full changelog data."""
        return self.changelog_data
    
    def create_new_version(self, 
                          version_type: str = 'patch',
                          custom_version: str = None,
                          changes: List[Dict[str, Any]] = None) -> str:
        """
        Create a new version with optional changes.
        
        Args:
            version_type: Type of version bump (major, minor, patch)
            custom_version: Custom version string (overrides version_type)
            changes: List of changes for this version
            
        Returns:
            New version number
        """
        current_version = self.get_current_version()
        
        if custom_version:
            new_version = custom_version
        else:
            new_version = self._increment_version(current_version, version_type)
        
        # Create new version entry
        self.changelog_data['versions'][new_version] = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'changes': changes or []
        }
        
        # Update current version
        self.changelog_data['current_version'] = new_version
        
        # Save changes
        if self._save_changelog():
            return new_version
        else:
            return current_version
    
    def _increment_version(self, version: str, version_type: str) -> str:
        """
        Increment version number based on type.
        
        Args:
            version: Current version (e.g., "1.2.3")
            version_type: Type of increment (major, minor, patch)
            
        Returns:
            New version number
        """
        try:
            # Parse version components
            parts = version.split('.')
            if len(parts) >= 3:
                major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            elif len(parts) == 2:
                major, minor, patch = int(parts[0]), int(parts[1]), 0
            else:
                major, minor, patch = int(parts[0]), 0, 0
            
            if version_type.lower() == 'major':
                major += 1
                minor = 0
                patch = 0
            elif version_type.lower() == 'minor':
                minor += 1
                patch = 0
            else:  # patch
                patch += 1
            
            return f"{major}.{minor}.{patch}"
        except (ValueError, IndexError):
            print(f"Invalid version format: {version}")
            return "1.0.1"  # Fallback
    
    def tag_current_version(self, push_tags: bool = False, prefix: str = "v") -> bool:
        """
        Create git tag for current version.
        
        Args:
            push_tags: Whether to push tags to remote
            prefix: Tag prefix (default: "v")
            
        Returns:
            True if tagging successful
        """
        if not self.enable_git:
            print("Git operations disabled")
            return False
        
        current_version = self.get_current_version()
        tag_name = f"{prefix}{current_version}"
        
        try:
            # Check if git is available and we're in a git repo
            subprocess.run(['git', 'status'], 
                          check=True, capture_output=True, text=True,
                          cwd=self.project_root)
            
            # Create annotated tag
            version_info = self.get_version_info()
            if version_info:
                changes = version_info.get('changes', [])
                tag_message = f"Version {current_version}\n\n"
                
                for change in changes:
                    tag_message += f"- {change['type']}: {change['description']}\n"
            else:
                tag_message = f"Version {current_version}"
            
            # Create tag
            subprocess.run(['git', 'tag', '-a', tag_name, '-m', tag_message], 
                          check=True, capture_output=True, text=True,
                          cwd=self.project_root)
            
            # Push tags if requested
            if push_tags:
                subprocess.run(['git', 'push', 'origin', '--tags'], 
                              check=True, capture_output=True, text=True,
                              cwd=self.project_root)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Git tagging failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during tagging: {e}")
            return False
    
    def get_git_status(self) -> Dict[str, Any]:
        """
        Get current git status information.
        
        Returns:
            Git status information or error info
        """
        if not self.enable_git:
            return {'error': 'Git operations disabled'}
        
        try:
            # Get current branch
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, check=True,
                                         cwd=self.project_root)
            current_branch = branch_result.stdout.strip()
            
            # Get last commit
            commit_result = subprocess.run(['git', 'log', '-1', '--format=%H %s'], 
                                         capture_output=True, text=True, check=True,
                                         cwd=self.project_root)
            last_commit = commit_result.stdout.strip()
            
            # Get status
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True, check=True,
                                         cwd=self.project_root)
            has_changes = bool(status_result.stdout.strip())
            
            # Get tags
            tag_result = subprocess.run(['git', 'tag', '--sort=-version:refname'], 
                                      capture_output=True, text=True, check=True,
                                      cwd=self.project_root)
            tags = tag_result.stdout.strip().split('\n') if tag_result.stdout.strip() else []
            
            return {
                'branch': current_branch,
                'last_commit': last_commit,
                'has_uncommitted_changes': has_changes,
                'latest_tags': tags[:5],  # Get last 5 tags
                'project_root': str(self.project_root)
            }
            
        except subprocess.CalledProcessError as e:
            return {'error': f'Git operation failed: {e}'}
        except Exception as e:
            return {'error': f'Unexpected error: {e}'}
    
    def get_version_summary(self) -> Dict[str, Any]:
        """
        Get summary of version and changelog status.
        
        Returns:
            Version summary information
        """
        current_version = self.get_current_version()
        version_info = self.get_version_info()
        recent_changes = self.get_recent_changes(7)
        git_status = self.get_git_status()
        
        return {
            'current_version': current_version,
            'version_date': version_info.get('date') if version_info else None,
            'total_changes_current': len(version_info.get('changes', [])) if version_info else 0,
            'recent_changes_7d': len(recent_changes),
            'total_versions': len(self.changelog_data.get('versions', {})),
            'git_status': git_status,
            'project_root': str(self.project_root),
            'changelog_file': str(self.changelog_path)
        }
    
    def export_changelog(self, format: str = 'markdown') -> str:
        """
        Export changelog in various formats.
        
        Args:
            format: Export format ('markdown', 'json', 'text')
            
        Returns:
            Exported changelog as string
        """
        if format == 'json':
            return json.dumps(self.changelog_data, indent=2, ensure_ascii=False)
        
        elif format == 'markdown':
            md = f"# Changelog\n\n"
            md += f"Current Version: **{self.get_current_version()}**\n\n"
            
            versions = self.get_all_versions(sort_desc=True)
            for version in versions:
                version_info = self.get_version_info(version)
                if version_info:
                    md += f"## [{version}] - {version_info['date']}\n\n"
                    
                    # Group changes by type
                    changes_by_type = {}
                    for change in version_info.get('changes', []):
                        change_type = change['type']
                        if change_type not in changes_by_type:
                            changes_by_type[change_type] = []
                        changes_by_type[change_type].append(change)
                    
                    # Output changes by type
                    type_order = ['feature', 'enhancement', 'bug', 'refactor', 'docs', 'test']
                    for change_type in type_order:
                        if change_type in changes_by_type:
                            md += f"### {change_type.title()}\n"
                            for change in changes_by_type[change_type]:
                                todo_ref = f" (#{change['todo_id']})" if change['todo_id'] else ""
                                md += f"- {change['description']}{todo_ref}\n"
                            md += "\n"
                    
                    # Handle any other types not in the standard list
                    for change_type, changes in changes_by_type.items():
                        if change_type not in type_order:
                            md += f"### {change_type.title()}\n"
                            for change in changes:
                                todo_ref = f" (#{change['todo_id']})" if change['todo_id'] else ""
                                md += f"- {change['description']}{todo_ref}\n"
                            md += "\n"
            
            return md
        
        elif format == 'text':
            text = f"Changelog - Current Version: {self.get_current_version()}\n"
            text += "=" * 50 + "\n\n"
            
            versions = self.get_all_versions(sort_desc=True)
            for version in versions:
                version_info = self.get_version_info(version)
                if version_info:
                    text += f"{version} ({version_info['date']})\n"
                    text += "-" * 30 + "\n"
                    
                    for change in version_info.get('changes', []):
                        todo_ref = f" (#{change['todo_id']})" if change['todo_id'] else ""
                        text += f"  {change['type']}: {change['description']}{todo_ref}\n"
                    text += "\n"
            
            return text
        
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Console usage example
if __name__ == "__main__":
    # Create version manager (will auto-detect project root)
    vm = VersionManager()
    
    # Print current status
    summary = vm.get_version_summary()
    print(f"Version Summary for: {summary['project_root']}")
    print(f"  Current Version: {summary['current_version']}")
    print(f"  Total Versions: {summary['total_versions']}")
    print(f"  Recent Changes (7d): {summary['recent_changes_7d']}")
    
    # Show recent changes
    recent = vm.get_recent_changes(7)
    if recent:
        print("\nRecent Changes:")
        for change in recent:
            print(f"  {change['version']} ({change['date']}): {change['type']} - {change['description']}")
    
    # Show git status
    git_info = vm.get_git_status()
    if 'error' not in git_info:
        print(f"\nGit Status:")
        print(f"  Branch: {git_info['branch']}")
        print(f"  Has Changes: {git_info['has_uncommitted_changes']}")
        print(f"  Latest Tags: {git_info['latest_tags'][:3]}")
    else:
        print(f"\nGit Status: {git_info['error']}")