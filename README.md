# Project Tools

A universal project management package providing todo tracking and version management capabilities for any software project.

## Features

- **Unified ProjectManager Interface**: Single entry point optimized for coding agents and automated tools
- **Todo Management**: Priority-based task tracking with categories and status management
- **Dependency Tracking**: Todo dependencies with blocked/unblocked detection and circular dependency prevention
- **Version Management**: Semantic versioning with changelog tracking and git integration
- **Integrated Workflows**: Seamless todo-to-changelog workflows with automatic version bumping
- **Universal Design**: Works with any project structure and programming language
- **Flexible Formatting**: Enhanced email and console formatters with dependency visualization
- **Command Line Interface**: Full CLI for all operations with project-tools command
- **CI/CD Ready**: Optimized for iterative development and future GitHub Actions integration

## Quick Start

### Installation

#### Direct Installation (Recommended)

```bash
# Install from GitHub repository
pip install git+https://github.com/noskillsben/project_tools.git

# Install a specific version/tag
pip install git+https://github.com/noskillsben/project_tools.git@v1.0.0

# For development installation (editable)
pip install -e git+https://github.com/noskillsben/project_tools.git#egg=project-tools

# Update to new versions
pip install --upgrade git+https://github.com/noskillsben/project_tools.git
```

#### Alternative Installation Methods

```bash
# Local development installation
git clone https://github.com/noskillsben/project_tools.git
cd project_tools
pip install -e .

# Copy method (legacy)
cp -r project_tools /path/to/your/project/
```

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/noskillsben/project_tools.git
cd project_tools

# Install in development mode with test dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black project_tools tests
flake8 project_tools tests
mypy project_tools
```

### Basic Usage

#### Python API

```python
from project_tools import ProjectManager
from project_tools.formatters import EmailFormatter, ConsoleFormatter

# Initialize the unified project manager (auto-detects project root)
project_manager = ProjectManager()

# Add a todo
todo_id = project_manager.add_todo(
    title="Fix authentication bug",
    description="User login fails with special characters",
    priority=9,
    category="bug"
)

# Complete todo with automatic changelog integration
project_manager.complete_todo_with_version(
    todo_id, "bug", auto_version_bump=True
)

# Get integrated status and recommendations
status = project_manager.get_integrated_status()
recommendations = project_manager.get_workflow_recommendations()

# Access underlying managers for advanced operations
todos = project_manager.todos.get_todos(status="in_progress")
version = project_manager.versions.get_current_version()
```

#### Command Line Interface

```bash
# Show project status
project-tools status

# Add a todo
project-tools todo add "Fix authentication bug" --priority high --category bug

# List todos with dependency information
project-tools todo list --priority high

# Show dependency tree for a specific todo
project-tools todo deps 5

# Complete a todo and add to changelog with version bump
project-tools todo complete 5 --changelog --change-type bug --version-bump

# Show blocked todos
project-tools todo list --blocked

# Bump version
project-tools version bump minor --message "Added user authentication"

# Export project data
project-tools export json --output project-status.json
```

## Core Workflows

### Adding and Managing Todos

```python
project_manager = ProjectManager()

# Add a basic todo
todo_id = project_manager.add_todo(
    title="Implement user dashboard",
    description="Create a dashboard showing user statistics and recent activity",
    priority=7,
    category="feature"
)

# Add with dependencies
backend_id = project_manager.add_todo("Implement backend API", priority=8)
frontend_id = project_manager.add_todo("Implement frontend UI", priority=7)
testing_id = project_manager.add_todo("Integration testing", priority=9)

# Set up dependencies: testing depends on both backend and frontend
project_manager.add_dependency(testing_id, backend_id)
project_manager.add_dependency(testing_id, frontend_id)

# Check project status
blocked_todos = project_manager.get_blocked_todos()
high_priority = project_manager.get_high_priority_todos()
```

### Integrated Todo-to-Changelog Workflow

```python
# Complete a todo and automatically add to changelog with version bump
project_manager.complete_todo_with_version(
    todo_id=5,
    change_type="feature",  # "feature", "bug", "enhancement", etc.
    change_description="Custom description (optional)",
    auto_version_bump=True  # Automatically bump version based on change type
)

# Get workflow recommendations based on current state
recommendations = project_manager.get_workflow_recommendations()
for rec in recommendations:
    print(f"• {rec}")

# Example output:
# • Focus on 3 high-priority todos
# • Resolve 2 blocked todos by completing their dependencies  
# • Start with 1 high-priority todos that are ready to work on
# • Add 5 completed todos to changelog
```

### Version Management

```python
# Add changes to current version
project_manager.add_change(
    change_type="feature",
    description="Add user authentication system"
)

# Bump version
new_version = project_manager.bump_version("minor", "Added user authentication")

# Get current version and recent changes
current_version = project_manager.get_current_version()
recent_changes = project_manager.get_recent_changes(days=7)
```

### Advanced Operations

For advanced operations, access the underlying managers through the `todos` and `versions` properties:

```python
# Access todo manager directly
todo_summary = project_manager.todos.get_summary()
dependency_chain = project_manager.todos.get_dependency_chain(todo_id)

# Access version manager directly
version_summary = project_manager.versions.get_version_summary()
changelog = project_manager.versions.get_changelog()
```

## Output Formatting

### Console Formatter

```python
from project_tools.formatters import ConsoleFormatter

formatter = ConsoleFormatter(width=100)

# Display todo table with dependency information
print(formatter.format_todos_table(project_manager.todos))
# Output includes dependency symbols: ⏳ Blocked  🔗 Has dependencies  ⚡ Others depend on this

# Show dependency tree for a specific todo
print(formatter.format_dependency_tree(project_manager.todos, todo_id=5))

# Show blocked todos with blocking dependencies
print(formatter.format_blocked_todos(project_manager.todos))

# Combined status report with dependency counts
print(formatter.format_combined_status(project_manager.todos, project_manager.versions))
```

### Email Formatter

```python
from project_tools.formatters import EmailFormatter

formatter = EmailFormatter()

# Combined report with dependency separation (ready vs blocked todos)
report_html = formatter.format_combined_report(
    project_manager.todos,
    project_manager.versions
)

# Integration report showing completed todos with changelog entries
integration_html = formatter.format_integration_report(
    project_manager.todos, 
    project_manager.versions
)

# Enhanced summary table with dependency information
summary_html = formatter.create_summary_table(
    project_manager.todos, 
    project_manager.versions
)
```

## Configuration

### Custom File Locations

```python
# Custom project root
project_manager = ProjectManager(project_root="/path/to/project")

# Access underlying managers for custom configuration
project_manager.todos.todo_path = "/custom/path/todos.json"
project_manager.versions.changelog_path = "/custom/path/changelog.json"
```

### Custom Categories and Statuses

```python
# Configure through underlying managers
from project_tools import ProjectManager
from project_tools._todo_manager import _TodoManager
from project_tools._version_manager import _VersionManager

# Create managers with custom configuration
todo_manager = _TodoManager(
    categories=["bug", "feature", "enhancement", "research", "deployment"],
    statuses=["backlog", "todo", "in_progress", "review", "testing", "done"]
)

# Create ProjectManager with custom managers
project_manager = ProjectManager(
    todo_manager=todo_manager,
    version_manager=_VersionManager(enable_git=False)
)
```

## Data Storage

The package creates these files in your project root:

```
your_project/
├── todo.json          # Todo data with dependencies
├── changelog.json     # Version and change history
└── project_tools/     # Package files (if copied locally)
```

### todo.json Format

```json
{
  "todos": [
    {
      "id": 1,
      "title": "Fix login bug",
      "description": "Users cannot login with special characters",
      "priority": 9,
      "status": "in_progress",
      "category": "bug",
      "created_date": "2025-06-28",
      "target_date": null,
      "notes": "Affects approximately 15% of users"
    }
  ],
  "categories": ["bug", "feature", "enhancement", "docs", "refactor"],
  "statuses": ["todo", "in_progress", "testing", "complete"],
  "priority_scale": "1-10 (10=highest)",
  "dependencies": {
    "3": [1, 2]
  }
}
```

### changelog.json Format

```json
{
  "current_version": "1.2.0",
  "versions": {
    "1.2.0": {
      "date": "2025-06-28",
      "changes": [
        {
          "type": "feature",
          "description": "Add user authentication system",
          "todo_id": 5,
          "todo_priority": 8,
          "todo_category": "feature"
        },
        {
          "type": "bug", 
          "description": "Fix login with special characters",
          "todo_id": 1,
          "todo_priority": 9,
          "todo_category": "bug"
        }
      ]
    }
  }
}
```

## Integration Examples

### With Daily Email Reports

```python
def generate_daily_report():
    project_manager = ProjectManager()
    formatter = EmailFormatter()
    
    # Get recent activity
    report = formatter.format_combined_report(
        project_manager.todos, 
        project_manager.versions,
        changes_days=1
    )
    
    if report:
        send_email("Daily Project Report", report)
```

### With Git Hooks

```bash
#!/bin/bash
# post-commit hook
python3 -c "
from project_tools import ProjectManager
pm = ProjectManager()
pm.versions.tag_current_version()
"
```

### With CI/CD

```yaml
# GitHub Actions example
- name: Update Project Status
  run: |
    python3 -c "
    from project_tools import ProjectManager
    pm = ProjectManager()
    status = pm.get_integrated_status()
    print(f'Version: {status[\"version\"]}')
    print(f'High Priority Todos: {status[\"high_priority_todos\"]}')
    "
```

## Benefits for Coding Agents

This package is specifically designed with coding agents and automated tools in mind:

- **Single Entry Point**: No decision paralysis - always use `ProjectManager`
- **Predictable API**: Consistent method signatures and return types
- **Workflow Recommendations**: AI-powered suggestions based on current project state
- **Integrated Operations**: Complete workflows in single method calls
- **Clear Dependencies**: Built-in dependency tracking prevents circular dependencies
- **Status Monitoring**: Comprehensive project status with all relevant metrics

## Troubleshooting

### Common Installation Issues

**Repository Access Issues**
```bash
# Error: Repository not found
# Solution: Ensure you're using the correct repository URL
pip install git+https://github.com/noskillsben/project_tools.git
```

**Permission Denied**
```bash
# Error: Permission denied (publickey)
# Solution: Use HTTPS instead of SSH
pip install git+https://github.com/noskillsben/project_tools.git
# Not: git+ssh://git@github.com/noskillsben/project_tools.git
```

**Package Not Found After Installation**
```bash
# Check if package is properly installed
pip show project-tools
pip list | grep project

# Reinstall in development mode
pip uninstall project-tools
pip install -e git+https://github.com/noskillsben/project_tools.git#egg=project-tools
```

**Import Errors**
```python
# Make sure you're importing from the correct package name
from project_tools import ProjectManager
from project_tools.formatters import ConsoleFormatter, EmailFormatter

# For advanced usage (not recommended for most users):
# from project_tools._todo_manager import _TodoManager
# from project_tools._version_manager import _VersionManager
```

**CLI Command Not Found**
```bash
# Make sure the package installed the CLI script
which project-tools
pip show project-tools

# Try reinstalling
pip install --force-reinstall git+https://github.com/noskillsben/project_tools.git
```

### Version Compatibility

- **Python 3.7+**: Required for proper type hints and pathlib support
- **Git**: Optional, disable with `ProjectManager(enable_git=False)` if not available
- **Dependencies**: Only uses Python standard library for core functionality

### Performance Considerations

- **Large Projects**: For projects with 1000+ todos, consider periodic cleanup of completed items
- **File Locking**: The package uses atomic file operations but doesn't implement file locking
- **Memory Usage**: All data is loaded into memory; not suitable for extremely large datasets

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Support

For issues and questions, please create an issue in the project repository.