#!/usr/bin/env python3
"""
Command-line interface for project-tools.
Provides console commands for managing todos, versions, and project workflows.
"""

import argparse
import sys
import os
from typing import Optional

from . import ProjectManager, create_project_managers
from ._todo_manager import _TodoManager
from ._version_manager import _VersionManager
from .formatters import ConsoleFormatter


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Universal project management tools for todos, versioning, and workflows"
    )
    parser.add_argument(
        "--project-dir", 
        default=os.getcwd(),
        help="Project directory path (default: current directory)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show project summary")
    status_parser.add_argument(
        "--format", choices=["console", "json"], default="console",
        help="Output format"
    )
    
    # Todo commands
    todo_parser = subparsers.add_parser("todo", help="Todo management")
    todo_subparsers = todo_parser.add_subparsers(dest="todo_action", help="Todo actions")
    
    # Todo add
    add_parser = todo_subparsers.add_parser("add", help="Add new todo")
    add_parser.add_argument("title", help="Todo title")
    add_parser.add_argument("--description", help="Todo description")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    add_parser.add_argument("--category", help="Todo category")
    add_parser.add_argument("--depends-on", nargs="+", help="Todo IDs this depends on")
    
    # Todo list
    list_parser = todo_subparsers.add_parser("list", help="List todos")
    list_parser.add_argument("--status", choices=["pending", "in_progress", "completed"])
    list_parser.add_argument("--priority", choices=["low", "medium", "high"])
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--blocked", action="store_true", help="Show only blocked todos")
    list_parser.add_argument("--unblocked", action="store_true", help="Show only unblocked todos")
    
    # Todo complete
    complete_parser = todo_subparsers.add_parser("complete", help="Complete todo")
    complete_parser.add_argument("todo_id", help="Todo ID to complete")
    complete_parser.add_argument("--changelog", action="store_true", help="Add to changelog")
    complete_parser.add_argument("--change-type", choices=["feature", "bugfix", "enhancement", "docs"], 
                                default="feature", help="Change type for changelog")
    complete_parser.add_argument("--version-bump", action="store_true", help="Auto version bump")
    
    # Todo deps
    deps_parser = todo_subparsers.add_parser("deps", help="Show dependency tree")
    deps_parser.add_argument("todo_id", nargs="?", help="Todo ID (show all if not specified)")
    
    # Version commands
    version_parser = subparsers.add_parser("version", help="Version management")
    version_subparsers = version_parser.add_subparsers(dest="version_action", help="Version actions")
    
    # Version bump
    bump_parser = version_subparsers.add_parser("bump", help="Create new version")
    bump_parser.add_argument("bump_type", choices=["major", "minor", "patch"], help="Version bump type")
    bump_parser.add_argument("--message", help="Version message")
    
    # Version tag
    tag_parser = version_subparsers.add_parser("tag", help="Create git tag")
    tag_parser.add_argument("--push", action="store_true", help="Push tag to remote")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export project data")
    export_parser.add_argument("format", choices=["json", "csv", "html"], help="Export format")
    export_parser.add_argument("--output", help="Output file path")
    export_parser.add_argument("--todos", action="store_true", help="Include todos")
    export_parser.add_argument("--changelog", action="store_true", help="Include changelog")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return execute_command(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def execute_command(args) -> int:
    """Execute the parsed command."""
    # Initialize managers
    os.chdir(args.project_dir)
    todo_manager, version_manager = create_project_managers()
    project_manager = ProjectManager(todo_manager, version_manager)
    formatter = ConsoleFormatter()
    
    if args.command == "status":
        return handle_status(project_manager, formatter, args)
    elif args.command == "todo":
        return handle_todo(todo_manager, version_manager, formatter, args)
    elif args.command == "version":
        return handle_version(version_manager, formatter, args)
    elif args.command == "export":
        return handle_export(todo_manager, version_manager, formatter, args)
    
    return 1


def handle_status(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle status command."""
    if args.format == "json":
        import json
        status = project_manager.get_integrated_status()
        print(json.dumps(status, indent=2))
    else:
        print(formatter.format_combined_status(
            project_manager.todo_manager, 
            project_manager.version_manager
        ))
    return 0


def handle_todo(todo_manager: _TodoManager, version_manager: _VersionManager, 
                formatter: ConsoleFormatter, args) -> int:
    """Handle todo commands."""
    if args.todo_action == "add":
        todo_id = todo_manager.add_todo(
            title=args.title,
            description=args.description or "",
            priority=args.priority,
            category=args.category or "general"
        )
        
        if args.depends_on:
            for dep_id in args.depends_on:
                todo_manager.add_dependency(todo_id, dep_id)
        
        print(f"Todo created with ID: {todo_id}")
        
    elif args.todo_action == "list":
        todos = todo_manager.get_todos()
        
        # Apply filters
        if args.status:
            todos = [t for t in todos if t.get("status") == args.status]
        if args.priority:
            todos = [t for t in todos if t.get("priority") == args.priority]
        if args.category:
            todos = [t for t in todos if t.get("category") == args.category]
        if args.blocked:
            blocked_ids = [t["id"] for t in todo_manager.get_blocked_todos()]
            todos = [t for t in todos if t["id"] in blocked_ids]
        if args.unblocked:
            unblocked_ids = [t["id"] for t in todo_manager.get_unblocked_todos()]
            todos = [t for t in todos if t["id"] in unblocked_ids]
        
        print(formatter.format_todos_table(todos))
        
    elif args.todo_action == "complete":
        if args.changelog:
            todo_manager.complete_todo_with_changelog(
                args.todo_id, version_manager, args.change_type,
                auto_version_bump=args.version_bump
            )
            print(f"Todo {args.todo_id} completed and added to changelog")
        else:
            todo_manager.complete_todo(args.todo_id)
            print(f"Todo {args.todo_id} completed")
            
    elif args.todo_action == "deps":
        if args.todo_id:
            print(formatter.format_dependency_tree(todo_manager, args.todo_id))
        else:
            blocked = todo_manager.get_blocked_todos()
            if blocked:
                print("Blocked todos:")
                print(formatter.format_blocked_todos(todo_manager))
            else:
                print("No blocked todos found")
    
    return 0


def handle_version(version_manager: _VersionManager, formatter: ConsoleFormatter, args) -> int:
    """Handle version commands."""
    if args.version_action == "bump":
        new_version = version_manager.bump_version(args.bump_type, args.message)
        print(f"Version bumped to: {new_version}")
        
    elif args.version_action == "tag":
        current_version = version_manager.get_current_version()
        tag_name = f"v{current_version}"
        
        import subprocess
        try:
            subprocess.run(["git", "tag", tag_name], check=True)
            print(f"Created tag: {tag_name}")
            
            if args.push:
                subprocess.run(["git", "push", "origin", tag_name], check=True)
                print(f"Pushed tag: {tag_name}")
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e}")
            return 1
    
    return 0


def handle_export(todo_manager: _TodoManager, version_manager: _VersionManager,
                 formatter: ConsoleFormatter, args) -> int:
    """Handle export command."""
    data = {}
    
    if args.todos:
        data["todos"] = todo_manager.get_todos()
    if args.changelog:
        data["changelog"] = version_manager.get_changelog()
    
    if not data:
        data = {
            "todos": todo_manager.get_todos(),
            "changelog": version_manager.get_changelog()
        }
    
    if args.format == "json":
        import json
        output = json.dumps(data, indent=2)
    elif args.format == "csv":
        # Simple CSV export for todos
        import csv
        import io
        output_buffer = io.StringIO()
        if "todos" in data:
            writer = csv.DictWriter(output_buffer, fieldnames=["id", "title", "status", "priority", "category"])
            writer.writeheader()
            for todo in data["todos"]:
                writer.writerow(todo)
        output = output_buffer.getvalue()
    elif args.format == "html":
        # Basic HTML export
        html_parts = ["<html><body>"]
        if "todos" in data:
            html_parts.append("<h2>Todos</h2>")
            html_parts.append(formatter.format_todos_table(data["todos"]))
        if "changelog" in data:
            html_parts.append("<h2>Changelog</h2>")
            # Add changelog formatting here
        html_parts.append("</body></html>")
        output = "\n".join(html_parts)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Exported to: {args.output}")
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())