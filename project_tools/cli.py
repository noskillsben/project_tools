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
    
    # Intelligence commands
    intel_parser = subparsers.add_parser("intelligence", help="AI-assisted project management")
    intel_subparsers = intel_parser.add_subparsers(dest="intel_action", help="Intelligence actions")
    
    # Intelligence init
    init_intel_parser = intel_subparsers.add_parser("init", help="Initialize intelligence features")
    init_intel_parser.add_argument("--project-name", help="Project name for templates")
    init_intel_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    
    # Intelligence status
    status_intel_parser = intel_subparsers.add_parser("status", help="Show intelligence status")
    status_intel_parser.add_argument("--format", choices=["console", "json"], default="console")
    
    # Compass commands
    compass_parser = subparsers.add_parser("compass", help="Project compass management")
    compass_subparsers = compass_parser.add_subparsers(dest="compass_action", help="Compass actions")
    
    # Compass init
    init_compass_parser = compass_subparsers.add_parser("init", help="Initialize project compass")
    init_compass_parser.add_argument("--project-name", help="Project name")
    init_compass_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    
    # Compass context
    context_parser = compass_subparsers.add_parser("context", help="Add context entry")
    context_parser.add_argument("type", choices=["decision", "assumption", "learning", "milestone"])
    context_parser.add_argument("content", help="Context content")
    
    # Chains commands
    chains_parser = subparsers.add_parser("chains", help="Task chain management")
    chains_subparsers = chains_parser.add_subparsers(dest="chains_action", help="Chain actions")
    
    # Chain create
    create_chain_parser = chains_subparsers.add_parser("create", help="Create task chain")
    create_chain_parser.add_argument("name", help="Chain name")
    create_chain_parser.add_argument("--description", help="Chain description")
    create_chain_parser.add_argument("--type", choices=["sequential", "parallel", "milestone"], default="sequential")
    
    # Chain add todos
    add_todos_parser = chains_subparsers.add_parser("add-todos", help="Add todos to chain")
    add_todos_parser.add_argument("chain_id", help="Chain ID")
    add_todos_parser.add_argument("todo_ids", nargs="+", help="Todo IDs to add")
    
    # Chain health
    health_parser = chains_subparsers.add_parser("health", help="Show chain health")
    health_parser.add_argument("chain_id", nargs="?", help="Chain ID (all chains if not specified)")
    
    # Direction commands
    direction_parser = subparsers.add_parser("direction", help="Direction tracking")
    direction_subparsers = direction_parser.add_subparsers(dest="direction_action", help="Direction actions")
    
    # Direction set
    set_direction_parser = direction_subparsers.add_parser("set", help="Set current direction")
    set_direction_parser.add_argument("direction", help="Direction statement")
    set_direction_parser.add_argument("--rationale", help="Rationale for this direction")
    set_direction_parser.add_argument("--time-horizon", default="3 months", help="Time horizon")
    
    # Direction assumption
    assumption_parser = direction_subparsers.add_parser("assume", help="Add assumption")
    assumption_parser.add_argument("assumption", help="Assumption statement")
    assumption_parser.add_argument("--confidence", choices=["low", "medium", "high"], default="medium")
    assumption_parser.add_argument("--critical", action="store_true", help="Mark as critical assumption")
    
    # Direction pivot
    pivot_parser = direction_subparsers.add_parser("pivot", help="Log pivot consideration")
    pivot_parser.add_argument("trigger", help="What triggered the pivot consideration")
    pivot_parser.add_argument("new_direction", help="Alternative direction considered")
    pivot_parser.add_argument("--decision", choices=["continue", "pivot", "delay"], default="continue")
    
    # Reflection commands
    reflect_parser = subparsers.add_parser("reflect", help="Reflection management")
    reflect_subparsers = reflect_parser.add_subparsers(dest="reflect_action", help="Reflection actions")
    
    # Reflection create
    create_reflect_parser = reflect_subparsers.add_parser("create", help="Create reflection entry")
    create_reflect_parser.add_argument("--type", choices=["daily", "weekly", "monthly", "project"], default="weekly")
    
    # Reflection energy
    energy_parser = reflect_subparsers.add_parser("energy", help="Log energy level")
    energy_parser.add_argument("level", type=int, choices=range(1, 11), help="Energy level (1-10)")
    energy_parser.add_argument("--context", help="Context for this energy reading")
    
    # Reflection learning
    learning_parser = reflect_subparsers.add_parser("learning", help="Capture learning")
    learning_parser.add_argument("learning", help="Learning insight")
    learning_parser.add_argument("--category", help="Learning category")
    learning_parser.add_argument("--actionable", action="store_true", help="Mark as actionable")
    
    # Portfolio commands
    portfolio_parser = subparsers.add_parser("portfolio", help="Portfolio management")
    portfolio_subparsers = portfolio_parser.add_subparsers(dest="portfolio_action", help="Portfolio actions")
    
    # Portfolio init
    init_portfolio_parser = portfolio_subparsers.add_parser("init", help="Initialize portfolio")
    init_portfolio_parser.add_argument("--name", help="Portfolio name")
    
    # Portfolio add project
    add_project_parser = portfolio_subparsers.add_parser("add-project", help="Add project to portfolio")
    add_project_parser.add_argument("project_id", help="Project ID")
    add_project_parser.add_argument("project_name", help="Project name")
    add_project_parser.add_argument("project_path", help="Project path")
    add_project_parser.add_argument("--type", default="primary", help="Project type")
    
    # AI Enhancement command
    ai_parser = subparsers.add_parser("ai-enhance", help="AI enhancement opportunities")
    ai_parser.add_argument("--format", choices=["console", "json"], default="console")
    
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
    elif args.command == "intelligence":
        return handle_intelligence(project_manager, formatter, args)
    elif args.command == "compass":
        return handle_compass(project_manager, formatter, args)
    elif args.command == "chains":
        return handle_chains(project_manager, formatter, args)
    elif args.command == "direction":
        return handle_direction(project_manager, formatter, args)
    elif args.command == "reflect":
        return handle_reflection(project_manager, formatter, args)
    elif args.command == "portfolio":
        return handle_portfolio(project_manager, formatter, args)
    elif args.command == "ai-enhance":
        return handle_ai_enhance(project_manager, formatter, args)
    
    return 1


def handle_status(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle status command."""
    if args.format == "json":
        import json
        status = project_manager.get_integrated_status()
        print(json.dumps(status, indent=2))
    else:
        print(formatter.format_combined_status(
            project_manager._todo_manager, 
            project_manager._version_manager
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
        
        print(formatter.format_todos_table(todo_manager, args.status))
        
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
            # Create simple HTML table for todos
            html_parts.append("<table border='1'>")
            html_parts.append("<tr><th>ID</th><th>Title</th><th>Status</th><th>Priority</th></tr>")
            for todo in data["todos"]:
                html_parts.append(f"<tr><td>{todo.get('id', '')}</td><td>{todo.get('title', '')}</td><td>{todo.get('status', '')}</td><td>{todo.get('priority', '')}</td></tr>")
            html_parts.append("</table>")
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


def handle_intelligence(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle intelligence commands."""
    if not project_manager.intelligence:
        print("Intelligence features are not enabled")
        return 1
    
    if args.intel_action == "init":
        result = project_manager.initialize_intelligence(
            args.project_name or "", args.force
        )
        if "error" in result:
            print(f"Error: {result['error']}")
            return 1
        
        print(f"Intelligence initialized for project: {result['project_name']}")
        print(f"Components initialized: {', '.join(result['initialized_components'])}")
        for component, files in result.get("created_files", {}).items():
            print(f"  {component}: {len(files)} files created")
        
    elif args.intel_action == "status":
        status = project_manager.get_intelligence_status()
        if args.format == "json":
            import json
            print(json.dumps(status, indent=2))
        else:
            print(formatter.format_intelligence_status(status))
    
    return 0


def handle_compass(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle compass commands."""
    compass = project_manager.get_compass()
    if not compass:
        print("Compass features are not enabled")
        return 1
    
    if args.compass_action == "init":
        created_files = compass.initialize_compass(
            args.project_name or "", args.force
        )
        print("Project compass initialized:")
        for file_type, path in created_files.items():
            print(f"  {file_type}: {path}")
    
    elif args.compass_action == "context":
        compass.add_context_entry(args.type, args.content)
        print(f"Added {args.type} context entry")
    
    return 0


def handle_chains(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle task chain commands."""
    chains = project_manager.get_task_chains()
    if not chains:
        print("Task chain features are not enabled")
        return 1
    
    if args.chains_action == "create":
        chain_id = chains.create_task_chain(
            args.name, args.description or "", args.type
        )
        print(f"Created task chain: {chain_id}")
    
    elif args.chains_action == "add-todos":
        success = chains.add_todos_to_chain(args.chain_id, args.todo_ids)
        if success:
            print(f"Added {len(args.todo_ids)} todos to chain {args.chain_id}")
        else:
            print(f"Failed to add todos to chain {args.chain_id}")
            return 1
    
    elif args.chains_action == "health":
        if args.chain_id:
            health = chains.get_chain_health(args.chain_id)
            print(formatter.format_chain_health(health))
        else:
            summary = chains.get_all_chains_summary()
            print(formatter.format_chains_summary(summary))
    
    return 0


def handle_direction(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle direction tracking commands."""
    direction = project_manager.get_direction_tracker()
    if not direction:
        print("Direction tracking features are not enabled")
        return 1
    
    if args.direction_action == "set":
        success = direction.set_current_direction(
            args.direction, args.rationale or "", time_horizon=args.time_horizon
        )
        if success:
            print("Current direction set successfully")
        else:
            print("Failed to set direction")
            return 1
    
    elif args.direction_action == "assume":
        assumption_id = direction.add_assumption(
            args.assumption, args.confidence, critical=args.critical
        )
        print(f"Added assumption: {assumption_id}")
    
    elif args.direction_action == "pivot":
        direction.log_pivot_consideration(
            args.trigger, args.new_direction, args.decision
        )
        print("Pivot consideration logged")
    
    return 0


def handle_reflection(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle reflection commands."""
    reflection = project_manager.get_reflection_manager()
    if not reflection:
        print("Reflection features are not enabled")
        return 1
    
    if args.reflect_action == "create":
        entry_path = reflection.create_reflection_entry(args.type)
        print(f"Reflection entry created: {entry_path}")
    
    elif args.reflect_action == "energy":
        reflection.log_energy_level(args.level, args.context or "")
        print(f"Energy level {args.level} logged")
    
    elif args.reflect_action == "learning":
        learning_id = reflection.capture_learning(
            args.learning, args.category or "general", actionable=args.actionable
        )
        print(f"Learning captured: {learning_id}")
    
    return 0


def handle_portfolio(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle portfolio commands."""
    portfolio = project_manager.get_portfolio_manager()
    if not portfolio:
        print("Portfolio features are not enabled")
        return 1
    
    if args.portfolio_action == "init":
        created_files = portfolio.initialize_portfolio(args.name or "")
        print("Portfolio initialized:")
        for file_type, path in created_files.items():
            print(f"  {file_type}: {path}")
    
    elif args.portfolio_action == "add-project":
        success = portfolio.add_project_to_portfolio(
            args.project_id, args.project_name, args.project_path, args.type
        )
        if success:
            print(f"Added project {args.project_name} to portfolio")
        else:
            print(f"Failed to add project {args.project_name}")
            return 1
    
    return 0


def handle_ai_enhance(project_manager: ProjectManager, formatter: ConsoleFormatter, args) -> int:
    """Handle AI enhancement opportunities command."""
    if not project_manager.intelligence:
        print("Intelligence features are not enabled")
        return 1
    
    enhancement_summary = project_manager.get_ai_enhancement_summary()
    
    if args.format == "json":
        import json
        print(json.dumps(enhancement_summary, indent=2))
    else:
        print(formatter.format_ai_enhancement_summary(enhancement_summary))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())