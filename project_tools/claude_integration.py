#!/usr/bin/env python3
"""
Claude Code Integration for Project Tools

Generates CLAUDE.md content to help Claude Code understand and effectively
use the project_tools framework for project management tasks.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ClaudeIntegration:
    """Generates Claude Code integration content and documentation"""
    
    def __init__(self, project_manager):
        self.pm = project_manager
        self.project_root = Path(project_manager.todos.project_root)
    
    def generate_claude_md(self, include_examples: bool = True, include_setup_info: bool = True) -> str:
        """Generate complete CLAUDE.md content for the project"""
        
        # Analyze current project state
        project_state = self._analyze_project_state()
        
        content = self._generate_header()
        content += self._generate_overview(project_state)
        content += self._generate_commands_section(project_state)
        content += self._generate_workflow_section(project_state)
        
        if include_examples:
            content += self._generate_examples_section(project_state)
        
        if include_setup_info:
            content += self._generate_setup_section(project_state)
        
        content += self._generate_footer()
        
        return content
    
    def _analyze_project_state(self) -> Dict[str, Any]:
        """Analyze current project state to customize CLAUDE.md content"""
        todos = self.pm.get_todos()
        
        state = {
            "has_todos": len(todos) > 0,
            "todo_count": len(todos),
            "has_intelligence": self.pm.intelligence is not None,
            "complexity_level": self._detect_complexity_level(),
            "project_type": self._detect_project_type(),
            "has_dependencies": any(todo.get('dependencies') for todo in todos),
            "categories": list(set(todo.get('category', 'general') for todo in todos)),
            "current_version": self.pm.get_current_version(),
            "has_changelog": len(self.pm.versions.get_all_versions()) > 1,
            "has_github": self._has_github_integration()
        }
        
        return state
    
    def _detect_complexity_level(self) -> str:
        """Detect the complexity level based on active features"""
        if not self.pm.intelligence:
            return "light"
        
        # Count enabled components to estimate complexity
        components = []
        if hasattr(self.pm.intelligence, 'compass') and self.pm.intelligence.compass:
            components.append('compass')
        if hasattr(self.pm.intelligence, 'direction') and self.pm.intelligence.direction:
            components.append('direction')
        if hasattr(self.pm.intelligence, 'reflection') and self.pm.intelligence.reflection:
            components.append('reflection')
        if hasattr(self.pm.intelligence, 'task_chains') and self.pm.intelligence.task_chains:
            components.append('task_chains')
        if hasattr(self.pm.intelligence, 'portfolio') and self.pm.intelligence.portfolio:
            components.append('portfolio')
        
        if len(components) <= 3:
            return "standard"
        else:
            return "full"
    
    def _detect_project_type(self) -> str:
        """Try to detect project type from setup or todos"""
        try:
            # Try to find setup summary
            summary_paths = [
                self.project_root / "project_management" / "setup_summary.json",
                self.project_root / "project_setup_summary.json"
            ]
            
            for path in summary_paths:
                if path.exists():
                    with open(path) as f:
                        summary = json.load(f)
                        return summary.get("project_type", "software")
            
            # Fallback to guessing from files
            if (self.project_root / "package.json").exists():
                return "software"
            elif (self.project_root / "pyproject.toml").exists():
                return "software"
            elif (self.project_root / "requirements.txt").exists():
                return "software"
            else:
                return "general"
                
        except Exception:
            return "general"
    
    def _has_github_integration(self) -> bool:
        """Check if GitHub integration is available"""
        try:
            return hasattr(self.pm.versions, 'github_integration') and \
                   self.pm.versions.github_integration is not None
        except Exception:
            return False
    
    def _generate_header(self) -> str:
        """Generate CLAUDE.md header"""
        return """# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Management with Project Tools

This project uses the `project_tools` framework for comprehensive project management including todos, version tracking, and AI-assisted intelligence features.

"""
    
    def _generate_overview(self, state: Dict[str, Any]) -> str:
        """Generate project overview section"""
        complexity = state['complexity_level']
        project_type = state['project_type']
        
        content = f"""## Project Overview

**Project Type**: {project_type.title()}
**Management Complexity**: {complexity.title()}
**Current Status**: {state['todo_count']} active todos, Version {state['current_version']}

"""
        
        if state['has_intelligence']:
            content += """**Intelligence Features Active**: This project uses AI-assisted project intelligence including strategic direction tracking, reflection management, and workflow optimization.

"""
        
        return content
    
    def _generate_commands_section(self, state: Dict[str, Any]) -> str:
        """Generate essential commands section"""
        content = """## Essential Commands

### Project Status
```python
from project_tools import ProjectManager
pm = ProjectManager()

# Get comprehensive project status
status = pm.get_integrated_status()
print(f"Project Status: {status}")

# Get current todos
todos = pm.get_todos()
for todo in todos:
    print(f"• {todo['title']} (Priority: {todo['priority']}, Status: {todo['status']})")
```

### Todo Management
```python
# Add new todo
todo_id = pm.add_todo(
    title="Task description", 
    description="Detailed description",
    priority=8,  # 1-10 scale
    category="feature"  # or bug, docs, etc.
)

# Complete todo and add to changelog
pm.complete_todo_with_version(
    todo_id=todo_id,
    change_type="feature",  # feature, bug, enhancement, docs
    auto_bump=True  # automatically bump version
)

# Get blocked/unblocked todos
blocked = pm.get_blocked_todos()
ready = pm.get_ready_todos()
```

### Version Management
```python
# Bump version
new_version = pm.bump_version('minor', 'Added new feature')

# Get version history
versions = pm.get_all_versions()
recent_changes = pm.get_recent_changes(days=7)
```

"""
        
        if state['has_intelligence']:
            content += """### AI Intelligence Features
```python
# Get AI enhancement opportunities
recommendations = pm.get_ai_enhancement_summary()
print(f"AI Recommendations: {recommendations}")

# Access strategic direction
direction = pm.get_direction_tracker()
current_direction = direction.get_current_direction()

# Log reflections
reflection = pm.get_reflection_manager()
reflection.capture_learning("Key insight from recent work", "development")
```

"""
        
        if state['has_github']:
            content += """### GitHub Integration
```python
# GitHub sync is automatic on version bumps, but you can also:
# - Auto-commits todos and changelog changes
# - Creates version tags
# - Syncs project management files
```

"""
        
        return content
    
    def _generate_workflow_section(self, state: Dict[str, Any]) -> str:
        """Generate common workflow patterns"""
        content = """## Common Workflow Patterns

### 1. Feature Development
```python
# 1. Add feature todo
feature_id = pm.add_todo("Implement user authentication", 
                        "Add login/logout with session management", 
                        priority=8, category="feature")

# 2. Add dependencies if needed
pm.add_todo_dependency(feature_id, setup_todo_id)

# 3. Work on the feature...

# 4. Complete and version
pm.complete_todo_with_version(feature_id, "feature", auto_bump=True)
```

### 2. Bug Fix
```python
# 1. Add bug todo
bug_id = pm.add_todo("Fix authentication redirect", 
                    "Users not properly redirected after login",
                    priority=9, category="bug")

# 2. Fix the bug...

# 3. Complete with patch version bump
pm.complete_todo_with_version(bug_id, "bug", auto_bump=True)
```

### 3. Project Planning
```python
# Get project overview
status = pm.get_integrated_status()

# Check what's ready to work on
ready_todos = pm.get_ready_todos()

# See what's blocked
blocked_todos = pm.get_blocked_todos()
```

"""
        
        if state['has_intelligence']:
            content += """### 4. Strategic Review
```python
# Review current direction
direction = pm.get_direction_tracker()
current = direction.get_current_direction()

# Check assumptions
assumptions = direction.get_assumptions()
critical_assumptions = [a for a in assumptions if a['critical']]

# Log insights
reflection = pm.get_reflection_manager()
reflection.capture_learning("Important project insight", "strategy")
```

"""
        
        return content
    
    def _generate_examples_section(self, state: Dict[str, Any]) -> str:
        """Generate project-specific examples"""
        project_type = state['project_type']
        
        content = f"""## Project-Specific Examples

### Common {project_type.title()} Tasks
"""
        
        if project_type == "software":
            content += """```python
# Software development examples
pm.add_todo("Set up CI/CD pipeline", "Configure GitHub Actions for testing and deployment", 7, "infrastructure")
pm.add_todo("Add unit tests", "Achieve 80% test coverage for core modules", 8, "testing")
pm.add_todo("Update documentation", "Update README and API docs", 6, "docs")
pm.add_todo("Performance optimization", "Improve API response times", 7, "enhancement")
```
"""
        elif project_type == "business":
            content += """```python
# Business development examples
pm.add_todo("Market research", "Analyze competitor pricing and features", 8, "research")
pm.add_todo("Customer interviews", "Conduct 10 customer discovery interviews", 9, "validation")
pm.add_todo("MVP development", "Build minimum viable product", 9, "development")
pm.add_todo("Launch preparation", "Prepare marketing materials and launch plan", 7, "marketing")
```
"""
        else:
            content += """```python
# General project examples
pm.add_todo("Research phase", "Gather information and define requirements", 8, "research")
pm.add_todo("Planning phase", "Create detailed project plan and timeline", 7, "planning")
pm.add_todo("Implementation", "Execute main project deliverables", 9, "implementation")
pm.add_todo("Review and iterate", "Evaluate results and make improvements", 6, "review")
```
"""
        
        if state['categories']:
            content += f"""
### Active Project Categories
Current categories in use: {', '.join(state['categories'])}

```python
# Filter todos by category
categories = {state['categories']}
for category in categories:
    category_todos = [t for t in pm.get_todos() if t.get('category') == category]
    print(f"{{category}}: {{len(category_todos)}} todos")
```
"""
        
        return content
    
    def _generate_setup_section(self, state: Dict[str, Any]) -> str:
        """Generate setup and configuration information"""
        content = """## Setup Information

### Installation
```bash
pip install git+https://github.com/noskillsben/project_tools.git
```

### Initialization
```python
from project_tools import ProjectManager

# Initialize with current settings
pm = ProjectManager()

# Or customize configuration
pm = ProjectManager(
    enable_intelligence=True,
    todo_path="custom_todos.json",
    changelog_path="custom_changelog.json"
)
```

"""
        
        if state['complexity_level'] != 'light':
            content += f"""### Current Configuration
- **Complexity Level**: {state['complexity_level'].title()}
- **Intelligence Features**: {'Enabled' if state['has_intelligence'] else 'Disabled'}
- **GitHub Integration**: {'Enabled' if state['has_github'] else 'Disabled'}

"""
        
        content += """### File Structure
```
project_root/
├── todo.json              # Todo data and dependencies
├── changelog.json         # Version history
"""
        
        if state['has_intelligence']:
            content += """├── project_management/    # Intelligence files
│   ├── compass/          # Strategic context
│   ├── direction/        # Goal tracking
│   ├── reflection/       # Learning capture
│   └── chains/           # Task workflows
"""
        
        content += """└── CLAUDE.md            # This file
```

"""
        
        return content
    
    def _generate_footer(self) -> str:
        """Generate footer with additional guidance"""
        return f"""## Important Implementation Guidelines

### Todo Management Best Practices
- Use descriptive titles and detailed descriptions
- Set realistic priorities (1-10 scale)
- Use categories consistently across the project
- Add dependencies to enforce proper workflow order
- Complete todos through the version system when they represent releasable changes

### Version Management
- Use semantic versioning (major.minor.patch)
- Bump patch for bug fixes
- Bump minor for new features
- Bump major for breaking changes
- Always include meaningful change descriptions

### Working with Claude Code
- Use `pm.get_integrated_status()` to understand current project state
- Check `pm.get_ready_todos()` to see what can be worked on
- Use `pm.complete_todo_with_version()` to properly track completed work
- Leverage the intelligence features for strategic guidance when available

---
*Generated by project_tools Claude Integration on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    def save_claude_md(self, file_path: Optional[str] = None, **kwargs) -> Path:
        """Save CLAUDE.md file to specified path"""
        if file_path is None:
            file_path = self.project_root / "CLAUDE.md"
        else:
            file_path = Path(file_path)
        
        content = self.generate_claude_md(**kwargs)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def print_claude_snippet(self) -> str:
        """Generate a condensed snippet for copy-pasting to CLAUDE.md"""
        state = self._analyze_project_state()
        
        snippet = f"""
# Project Tools Integration

This project uses project_tools framework. Key commands:

```python
from project_tools import ProjectManager
pm = ProjectManager()

# Status: pm.get_integrated_status()
# Add todo: pm.add_todo("title", "desc", priority, "category")  
# Complete: pm.complete_todo_with_version(id, "change_type", auto_bump=True)
# Ready todos: pm.get_ready_todos()
```

Current: {state['todo_count']} todos, v{state['current_version']}, {state['complexity_level']} mode
"""
        
        if state['has_intelligence']:
            snippet += "\nIntelligence: pm.get_ai_enhancement_summary() for AI recommendations"
        
        return snippet


def generate_claude_md_for_project(project_root: str = ".") -> str:
    """Standalone function to generate CLAUDE.md content"""
    from project_tools import ProjectManager
    
    pm = ProjectManager()
    integration = ClaudeIntegration(pm)
    return integration.generate_claude_md()


def create_claude_md_file(project_root: str = ".", file_path: str = None) -> Path:
    """Standalone function to create CLAUDE.md file"""
    from project_tools import ProjectManager
    
    pm = ProjectManager()
    integration = ClaudeIntegration(pm)
    return integration.save_claude_md(file_path)


if __name__ == "__main__":
    # CLI usage
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--snippet":
        # Print snippet for copy-pasting
        from project_tools import ProjectManager
        pm = ProjectManager()
        integration = ClaudeIntegration(pm)
        print(integration.print_claude_snippet())
    else:
        # Create full CLAUDE.md file
        file_path = create_claude_md_file()
        print(f"CLAUDE.md created at: {file_path}")