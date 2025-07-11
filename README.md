# Project Tools

A universal project management package providing todo tracking and version management capabilities for any software project.

## Features

- **Todo Management**: Priority-based task tracking with categories and status management
- **Dependency Tracking**: Todo dependencies with blocked/unblocked detection and circular dependency prevention
- **Version Management**: Semantic versioning with changelog tracking and git integration
- **Integrated Workflows**: Seamless todo-to-changelog workflows with automatic version bumping
- **Universal Design**: Works with any project structure and programming language
- **Flexible Formatting**: Enhanced email and console formatters with dependency visualization
- **Command Line Interface**: Full CLI for all operations with project-tools command
- **ProjectManager**: Unified interface coordinating todos and versions with workflow recommendations
- **Modern Packaging**: pip-installable private GitHub package with proper Python packaging standards

## Quick Start

### Installation

#### Private Package Installation (Recommended)

1. **Create a GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with `repo` scope for private repositories
   - Copy the token for later use

2. **Set up environment variables** (for secure authentication)
   ```bash
   export GITHUB_TOKEN="your_personal_access_token_here"
   ```

3. **Install the package**
   ```bash
   # Install from private GitHub repository
   pip install git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git
   
   # Or install a specific version/tag
   pip install git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git@v1.0.0
   
   # For development installation (editable)
   pip install -e git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git#egg=project-tools
   ```

4. **Update to new versions**
   ```bash
   pip install --upgrade git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git
   ```

#### Alternative Installation Methods

```bash
# Local development installation
git clone https://github.com/yourusername/project-tools.git
cd project-tools
pip install -e .

# Copy method (legacy)
cp -r project_tools /path/to/your/project/
```

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/project-tools.git
cd project-tools

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

#### Python API

```python
from project_tools import TodoManager, VersionManager, ProjectManager
from project_tools.formatters import EmailFormatter

# Option 1: Use ProjectManager for integrated workflows
project_manager = ProjectManager()

# Add a todo with dependencies
todo_id = project_manager.todo_manager.add_todo(
    title="Implement user dashboard",
    description="Create dashboard with user statistics",
    priority=8,
    category="feature"
)

# Complete todo with automatic changelog entry and version bump
project_manager.complete_todo_with_version(
    todo_id, "feature", auto_version_bump=True
)

# Get integrated status and recommendations
status = project_manager.get_integrated_status()
recommendations = project_manager.get_workflow_recommendations()

# Option 2: Use individual managers
todo_manager = TodoManager()
version_manager = VersionManager()

# Add a todo
todo_id = todo_manager.add_todo(
    title="Fix authentication bug",
    description="User login fails with special characters",
    priority=9,
    category="bug"
)

# Complete todo with changelog integration
todo_manager.complete_todo_with_changelog(
    todo_id, version_manager, "bug", auto_version_bump=True
)

# Format for email with dependency information
formatter = EmailFormatter()
email_content = formatter.format_combined_report(todo_manager, version_manager)
integration_report = formatter.format_integration_report(todo_manager, version_manager)
```

## Todo Management

### Creating Todos

```python
todo_manager = TodoManager()

# Add a basic todo
todo_id = todo_manager.add_todo(
    title="Implement user dashboard",
    description="Create a dashboard showing user statistics and recent activity",
    priority=7,
    category="feature"
)

# Add with target date and notes
todo_id = todo_manager.add_todo(
    title="Fix memory leak",
    description="Application consumes excessive memory during image processing",
    priority=10,
    category="bug",
    target_date="2025-07-15",
    notes="Occurs specifically with large PNG files"
)
```

### Managing Todos

```python
# Update todo status
todo_manager.update_todo_status(todo_id, "in_progress")
todo_manager.update_todo_status(todo_id, "completed")

# Update priority
todo_manager.update_todo_priority(todo_id, 8)

# Get todos with filtering
high_priority = todo_manager.get_high_priority_todos(min_priority=8)
in_progress = todo_manager.get_in_progress_todos()
bugs = todo_manager.get_todos(category="bug")

# Get summary statistics
summary = todo_manager.get_summary()
print(f"Total todos: {summary['total']}")
print(f"High priority: {summary['high_priority_count']}")
print(f"Blocked todos: {summary['blocked_count']}")
print(f"Ready to work: {summary['unblocked_count']}")
```

### Todo Dependencies

```python
# Create todos with dependencies
backend_id = todo_manager.add_todo("Implement backend API", priority=8)
frontend_id = todo_manager.add_todo("Implement frontend UI", priority=7)
testing_id = todo_manager.add_todo("Integration testing", priority=9)

# Set up dependencies: testing depends on both backend and frontend
todo_manager.add_dependency(testing_id, backend_id)
todo_manager.add_dependency(testing_id, frontend_id)

# Check which todos are blocked
blocked_todos = todo_manager.get_blocked_todos()
unblocked_todos = todo_manager.get_unblocked_todos()

# Get dependency chain for a todo
chain = todo_manager.get_dependency_chain(testing_id)
print(f"Dependencies: {chain['dependencies']}")
print(f"Dependents: {chain['dependents']}")

# Remove dependency
todo_manager.remove_dependency(testing_id, backend_id)
```

## Integrated Workflows

### Todo-to-Changelog Integration

```python
# Complete a todo and automatically add to changelog
todo_manager.complete_todo_with_changelog(
    todo_id=5,
    version_manager=version_manager,
    change_type="feature",
    change_description="Custom description (optional)",
    auto_version_bump=True  # Automatically bump version based on change type
)

# Using VersionManager integration methods
version_manager.add_change_from_todo(todo_id, todo_manager, "bug")
version_manager.complete_todo_and_log(todo_id, todo_manager, "feature", auto_bump=True)

# Using ProjectManager for unified operations
project_manager = ProjectManager(todo_manager, version_manager)
project_manager.complete_todo_with_version(todo_id, "enhancement", auto_version_bump=True)
```

### Workflow Recommendations

```python
project_manager = ProjectManager()

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

## Version Management

### Managing Versions

```python
version_manager = VersionManager()

# Add changes to current version
version_manager.add_change(
    change_type="feature",
    description="Add user authentication system"
)

# Create new version
new_version = version_manager.create_new_version(version_type="minor")

# Create git tag
version_manager.tag_current_version(push_tags=True)
```

### Version Types

- **patch**: Bug fixes and small changes (1.0.0 → 1.0.1)
- **minor**: New features, backwards compatible (1.0.0 → 1.1.0)  
- **major**: Breaking changes (1.0.0 → 2.0.0)

### Change Types

- **feature**: New functionality
- **enhancement**: Improvements to existing features
- **bug**: Bug fixes
- **refactor**: Code restructuring
- **docs**: Documentation changes
- **test**: Test additions or modifications

## Formatters

### Email Formatter

```python
from project_tools.formatters import EmailFormatter

formatter = EmailFormatter()

# Format todos for email
todos_html = formatter.format_todos_for_email(
    todo_manager,
    include_in_progress=True,
    min_priority=8
)

# Format recent changes
changes_html = formatter.format_changes_for_email(
    version_manager,
    days=7
)

# Combined report with dependency separation (ready vs blocked todos)
report_html = formatter.format_combined_report(
    todo_manager,
    version_manager
)

# Integration report showing completed todos with changelog entries
integration_html = formatter.format_integration_report(todo_manager, version_manager)

# Enhanced summary table with dependency information
summary_html = formatter.create_summary_table(todo_manager, version_manager)
```

### Console Formatter

```python
from project_tools.formatters import ConsoleFormatter

formatter = ConsoleFormatter(width=100)

# Display todo table with dependency information
print(formatter.format_todos_table(todo_manager))
# Output includes dependency symbols: ⏳ Blocked  🔗 Has dependencies  ⚡ Others depend on this

# Show dependency tree for a specific todo
print(formatter.format_dependency_tree(todo_manager, todo_id=5))

# Show blocked todos with blocking dependencies
print(formatter.format_blocked_todos(todo_manager))

# Display version history
print(formatter.format_version_history(version_manager, limit=5))

# Combined status report with dependency counts
print(formatter.format_combined_status(todo_manager, version_manager))
```

## Configuration

### Custom File Locations

```python
# Custom paths
todo_manager = TodoManager(todo_path="/custom/path/todos.json")
version_manager = VersionManager(changelog_path="/custom/path/changelog.json")

# Custom project root
todo_manager = TodoManager(project_root="/path/to/project")
```

### Custom Categories and Statuses

```python
todo_manager = TodoManager(
    categories=["bug", "feature", "enhancement", "research", "deployment"],
    statuses=["backlog", "todo", "in_progress", "review", "testing", "done"]
)
```

### Disable Git Integration

```python
version_manager = VersionManager(enable_git=False)
```

## File Structure

The package creates these files in your project:

```
your_project/
├── todo.json          # Todo data
├── changelog.json     # Version and change history
└── project_tools/     # Package files (if copied locally)
    ├── __init__.py
    ├── todo_manager.py
    ├── version_manager.py
    └── formatters/
        ├── __init__.py
        ├── email_formatter.py
        └── console_formatter.py
```

## Data Format

### todo.json

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

### changelog.json

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
    todo_manager = TodoManager()
    version_manager = VersionManager()
    formatter = EmailFormatter()
    
    # Get recent activity
    report = formatter.format_combined_report(
        todo_manager, 
        version_manager,
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
from project_tools import VersionManager
vm = VersionManager()
vm.tag_current_version()
"
```

### With CI/CD

```yaml
# GitHub Actions example
- name: Update Project Status
  run: |
    python3 -c "
    from project_tools import get_project_status
    status = get_project_status()
    print(f'Version: {status[\"version\"]}')
    print(f'High Priority Todos: {status[\"high_priority_todos\"]}')
    "
```

## Troubleshooting

### Common Installation Issues

**Authentication Error**
```bash
# Error: Repository not found or access denied
# Solution: Check your GitHub token has 'repo' scope for private repositories
export GITHUB_TOKEN="your_token_with_repo_scope"
pip install git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git
```

**Permission Denied**
```bash
# Error: Permission denied (publickey)
# Solution: Use HTTPS with token instead of SSH
pip install git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git
# Not: git+ssh://git@github.com/yourusername/project-tools.git
```

**Package Not Found After Installation**
```bash
# Check if package is properly installed
pip show project-tools
pip list | grep project

# Reinstall in development mode
pip uninstall project-tools
pip install -e git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git#egg=project-tools
```

**Import Errors**
```python
# Make sure you're importing from the correct package name
from project_tools import TodoManager, VersionManager, ProjectManager
from project_tools.formatters import ConsoleFormatter, EmailFormatter

# Not: from project_tools.project_tools import ...
```

**CLI Command Not Found**
```bash
# Make sure the package installed the CLI script
which project-tools
pip show project-tools

# Try reinstalling
pip install --force-reinstall git+https://${GITHUB_TOKEN}@github.com/yourusername/project-tools.git
```

### Version Compatibility

- **Python 3.7+**: Required for proper type hints and pathlib support
- **Git**: Optional, disable with `VersionManager(enable_git=False)` if not available
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