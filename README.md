# Project Tools

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-brightgreen)

**AI-Assisted Universal Project Management Platform**

A sophisticated project management package providing todo tracking, version management, and AI-assisted intelligence capabilities for any software project. Designed specifically for coding agents, automated tools, and modern development workflows.

## 🎯 Value Proposition

Transform your project management from basic task tracking into an intelligent, AI-ready system that learns and adapts. Perfect for individual developers, teams, and coding agents who need structured, predictable project intelligence with seamless automation capabilities.

## 🌟 Complete Feature Matrix

### Core Project Management
| Feature | Description |
|---------|-------------|
| **Unified ProjectManager Interface** | Single entry point optimized for coding agents and automated tools |
| **Advanced Todo Management** | Priority-based task tracking with categories, dependencies, and blocking detection |
| **Dependency Tracking** | Complex todo dependencies with circular dependency prevention |
| **Semantic Version Management** | Automated versioning with changelog integration and git tagging |
| **Integrated Workflows** | Seamless todo-to-changelog workflows with automatic version bumping |
| **Universal Design** | Works with any project structure and programming language |
| **Flexible Formatting** | Enhanced email and console formatters with dependency visualization |
| **Complete CLI Interface** | Full command-line interface for all operations |

### AI-Assisted Intelligence System
| Feature | Description |
|---------|-------------|
| **Project Compass** | Intent tracking, success criteria, and strategic context management |
| **Task Chains** | Logical task progressions with milestone tracking and health metrics |
| **Direction Tracker** | Lightweight goal management with assumption tracking and pivot support |
| **Reflection Manager** | Structured reflection templates with energy tracking and learning capture |
| **Portfolio Manager** | Cross-project relationship management and resource optimization |
| **AI Enhancement Engine** | Template-based system with AI enhancement opportunities and recommendations |
| **Organized Artifact Management** | Structured project_management/ directory with categorized intelligence files |
| **Template System** | Markdown templates with AI placeholders for external enhancement |

### Integration & Automation
| Feature | Description |
|---------|-------------|
| **CI/CD Ready** | Optimized for continuous integration and automated workflows |
| **Git Integration** | Optional git tagging, status tracking, and repository awareness |
| **GitHub Integration** | Automatic pushing of todos/changelogs and version tagging with PyGithub |
| **Claude Code Integration** | Auto-generated CLAUDE.md files with project-specific guidance and workflows |
| **Email Reporting** | HTML email generation with dependency visualization |
| **JSON Export/Import** | Complete data export for backup and migration |
| **Webhook Support** | Integration points for external automation |
| **Agent-Optimized API** | Predictable, consistent API designed for coding agents |

## 🚀 Quick Start

### Installation & Guided Setup (Recommended)

The easiest way to get started is with our interactive setup guide:

```bash
# 1. Install project tools
pip install git+https://github.com/noskillsben/project_tools.git

# 2. Navigate to your project directory
cd /path/to/your/project

# 3. Run the guided setup
python -c "
import urllib.request
urllib.request.urlretrieve('https://raw.githubusercontent.com/noskillsben/project_tools/main/project_setup.py', 'project_setup.py')
exec(open('project_setup.py').read())
"
```

**Or download the setup script manually:**

```bash
# Download setup script
curl -O https://raw.githubusercontent.com/noskillsben/project_tools/main/project_setup.py

# Run interactive setup
python project_setup.py
```

The setup guide will:
- 🎯 Ask about your project type (software, business, research, creative, personal)
- ⚙️ Choose complexity level (light, standard, or full intelligence)
- 📋 Create appropriate todos and templates for your project
- 🧭 Set up strategic direction and assumptions tracking
- 🤖 Optionally generate CLAUDE.md file for Claude Code integration
- 🎉 Get you started with clear next steps

### Alternative Installation Methods

#### Direct Installation

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

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/noskillsben/project_tools.git
cd project_tools

# Install in development mode with test dependencies
pip install -e ".[dev]"

# Run tests and validation
pytest
black project_tools tests
flake8 project_tools tests
mypy project_tools
```

## 🎛️ Setup Modes

The setup guide offers three complexity levels to match your needs:

### Light Mode 
**Perfect for:** Simple projects, learning the system, quick task tracking

**Features:**
- ✅ Todo management with priorities and categories
- ✅ Version tracking with changelog
- ✅ Basic project status

**Example projects:** Bug fixes, small features, personal tasks, learning exercises

### Standard Mode
**Perfect for:** Most projects that need strategic direction

**Features:**
- ✅ Everything in Light mode
- ✅ Strategic direction tracking with assumptions
- ✅ Personal reflection and energy tracking
- ✅ Context logging for decisions

**Example projects:** Software development, business initiatives, research projects

### Full Intelligence Mode
**Perfect for:** Complex projects requiring comprehensive tracking

**Features:**
- ✅ Everything in Standard mode
- ✅ AI-enhanced templates and analysis
- ✅ Task chain management and optimization
- ✅ Portfolio management across projects
- ✅ Advanced workflow recommendations

**Example projects:** Startups, large software systems, academic research, business transformations

## 📋 Project Type Templates

The setup automatically configures your project based on type:

| Project Type | Initial Todos | Direction Focus | Key Assumptions |
|--------------|---------------|-----------------|-----------------|
| **Software Development** | Environment setup, architecture planning, core implementation | "Build working MVP with core features" | Technical feasibility, user needs validation |
| **Business/Startup** | Market validation, business strategy, MVP building | "Validate business model and achieve traction" | Market demand exists, business model viable |
| **Research/Study** | Research planning, resource gathering, analysis execution | "Complete research with measurable outcomes" | Scope is realistic, required skills accessible |
| **Creative Project** | Concept development, resource preparation, creation execution | "Produce quality creative output" | Creative vision achievable, tools available |
| **Personal/Life Goal** | Goal definition, skill development, habit formation | "Achieve personal growth objectives" | Motivation sustainable, approach realistic |

### Hello World Example

```python
from project_tools import ProjectManager
from project_tools.formatters import ConsoleFormatter

# Initialize with full intelligence features
project_manager = ProjectManager(enable_intelligence=True)

# Initialize intelligence system
init_result = project_manager.initialize_intelligence("Hello World Project")
print(f"Intelligence initialized: {len(init_result['initialized_components'])} components")

# Add a todo with priority and category
todo_id = project_manager.add_todo(
    title="Implement hello world feature",
    description="Create a basic hello world implementation with tests",
    priority=8,
    category="feature"
)

# Complete todo with automatic changelog integration
project_manager.complete_todo_with_version(
    todo_id, "feature", auto_version_bump=True
)

# Get comprehensive status including intelligence
status = project_manager.get_integrated_status()
print(f"Project Version: {status['version']}")
print(f"Intelligence Active: {status['intelligence']['active']}")

# Get AI enhancement opportunities
enhancements = project_manager.get_ai_enhancement_summary()
print(f"AI Enhancement Opportunities: {enhancements['total_opportunities']}")
```

### Verification & Getting Started

After running the setup script, verify everything is working:

```bash
# Check your project status
python -c "
from project_tools import ProjectManager
pm = ProjectManager()
status = pm.get_integrated_status()
print(f'✅ Project Version: {status[\"version\"]}')
print(f'✅ Total Todos: {status[\"total_todos\"]}')
print(f'✅ Intelligence: {\"Active\" if status.get(\"intelligence\", {}).get(\"active\") else \"Disabled\"}')
"

# View your todos
python -c "
from project_tools import ProjectManager
pm = ProjectManager()
todos = pm.get_todos()
print('📋 Your Current Todos:')
for i, todo in enumerate(todos[:5], 1):
    print(f'{i}. {todo[\"title\"]} (Priority: {todo[\"priority\"]})')
"
```

**Alternative CLI verification (if CLI is installed):**

```bash
# Verify installation
project-tools --version

# Check project status
project-tools status

# Initialize intelligence features (manual setup)
project-tools intelligence init --project-name "My Project"

# Verify intelligence components
project-tools intelligence status
```

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Project Tools Architecture              │
├─────────────────────────────────────────────────────────────┤
│                    Interface Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   CLI Commands  │  │  Python API     │  │  Formatters  │  │
│  │   - todo        │  │  ProjectManager │  │  - Console   │  │
│  │   - version     │  │  - add_todo()   │  │  - Email     │  │
│  │   - intelligence│  │  - bump_version │  │  - JSON      │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                 Intelligence Layer (AI-Assisted)            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │  Compass    │ │ Task Chains │ │ Direction   │ │Portfolio│ │
│  │ - Intent    │ │ - Progress  │ │ - Goals     │ │- Cross  │ │
│  │ - Context   │ │ - Health    │ │ - Pivots    │ │  Project│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
│  ┌─────────────┐ ┌─────────────────────────────────────────┐ │
│  │ Reflection  │ │        AI Enhancement Engine           │ │
│  │ - Learning  │ │      - Template Processing             │ │
│  │ - Energy    │ │      - Opportunity Detection           │ │
│  └─────────────┘ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                     Core Layer                              │
│  ┌─────────────────┐              ┌─────────────────────────┐ │
│  │  Todo Manager   │              │    Version Manager      │ │
│  │  - CRUD Ops     │◄────────────►│    - Semantic Versioning│ │
│  │  - Dependencies │              │    - Changelog          │ │
│  │  - Status Track │              │    - Git Integration    │ │
│  └─────────────────┘              └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Data Storage                             │
│    ┌─────────────┐ ┌─────────────┐ ┌───────────────────────┐ │
│    │ todo.json   │ │changelog.json│ │ project_management/   │ │
│    │ - Todos     │ │ - Versions  │ │ - compass/            │ │
│    │ - Dependencies│ │ - Changes   │ │ - chains/             │ │
│    └─────────────┘ └─────────────┘ │ - direction/          │ │
│                                    │ - reflection/         │ │
│                                    │ - portfolio/          │ │
│                                    └───────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. **Interface Layer** receives commands and exposes APIs
2. **Intelligence Layer** provides AI-assisted analysis and recommendations
3. **Core Layer** handles business logic and data manipulation
4. **Storage Layer** persists data in organized, readable formats

## 🧠 Complete Intelligence System Documentation

The intelligence system transforms basic project management into an AI-assisted platform with structured templates that external AI tools can enhance while keeping core operations deterministic.

### Project Compass - Strategic Direction

The compass tracks project intent, success criteria, and strategic context.

```python
# Access compass through ProjectManager
compass = project_manager.get_compass()

# Initialize compass with project intent
compass.initialize_compass("My Project", force=False)

# Update context as project evolves
compass.add_context_entry("decision", "Added AI enhancement features for better automation")

# Get current project intent and context
intent = compass.get_project_intent()
context_log = compass.get_context_log()
```

**CLI Commands:**
```bash
# Initialize compass
project-tools compass init --vision "Project vision statement"

# Update project context
project-tools compass context "Major milestone achieved"

# View current compass
project-tools compass show
```

**Generated Files:**
- `project_management/compass/project_intent.md` - Project vision and success criteria
- `project_management/compass/success_criteria.json` - Measurable success metrics
- `project_management/compass/learning_objectives.md` - Learning and skill development goals
- `project_management/compass/context_log.json` - Strategic context and decision history

### Task Chains - Logical Progressions

Task chains manage logical task progressions with milestone tracking and health metrics.

```python
# Access task chains
task_chains = project_manager.get_task_chains()

# Create a new task chain
chain_id = task_chains.create_task_chain(
    chain_name="User Authentication System",
    description="Complete user auth implementation"
)

# Add todos to the chain
task_chains.add_todos_to_chain(chain_id, [todo1_id, todo2_id, todo3_id])

# Check chain health
health = task_chains.get_chain_health(chain_id)
```

**CLI Commands:**
```bash
# Create a new task chain
project-tools chains create "Auth System" --description "User authentication"

# Add todos to chain
project-tools chains add-todos 1 --todo-ids 5,6,7

# Check chain health
project-tools chains health 1

# List all chains
project-tools chains list
```

**Generated Files:**
- `project_management/chains/task_chains.json` - Chain definitions and metadata
- `project_management/chains/chain_visualization.html` - Visual chain representations
- `project_management/chains/milestone_decisions.md` - Milestone tracking and decisions
- `project_management/chains/chain_health_report.html` - Health metrics and optimization suggestions

### Direction Tracker - Goal Management

Lightweight goal management with assumption tracking and pivot support.

```python
# Access direction tracker
direction = project_manager.get_direction_tracker()

# Set project direction
direction.set_current_direction(
    direction="Launch MVP by Q2",
    rationale="Market opportunity window is limited",
    success_indicators=["Working prototype", "User feedback", "Technical validation"]
)

# Add key assumptions
assumption_id = direction.add_assumption(
    assumption="Market demand exists for our solution",
    confidence="medium",
    critical=True
)

# Record a pivot consideration
direction.log_pivot_consideration(
    trigger="Market feedback indicated different priorities",
    new_direction_considered="Focus on core features first",
    decision="continue"
)

# Get current direction summary
current = direction.get_direction_summary()
```

**CLI Commands:**
```bash
# Set project direction
project-tools direction set "Launch MVP by Q2" --assumptions "Market demand,Team capacity"

# Record assumption
project-tools direction assume "User testing will validate approach"

# Record pivot
project-tools direction pivot "Market feedback changed priorities"

# Show current direction
project-tools direction show
```

**Generated Files:**
- `project_management/direction/current_direction.md` - Current direction with AI analysis placeholders
- `project_management/direction/direction_history.json` - Historical direction changes
- `project_management/direction/assumptions.json` - Key assumptions and validation status
- `project_management/direction/pivot_log.md` - Pivot considerations and decisions

### Reflection Manager - Personal Accountability

Structured reflection with energy tracking and learning capture.

```python
# Access reflection manager
reflection = project_manager.get_reflection_manager()

# Create a reflection entry
reflection_path = reflection.create_reflection_entry(
    reflection_type="daily",
    custom_prompts=["What challenges did I overcome today?"]
)

# Log energy level with context
reflection.log_energy_level(
    energy_level=8,
    context="Made good progress on authentication system",
    factors=["Good sleep", "Clear requirements", "Uninterrupted time"]
)

# Capture learning
learning_id = reflection.capture_learning(
    learning="JWT implementation more complex than expected",
    category="technical",
    actionable=True
)

# Get reflection insights
insights = reflection.get_reflection_insights(days_back=7)
```

**CLI Commands:**
```bash
# Create daily reflection
project-tools reflect create --type daily --energy 8 --content "Good progress today"

# Add learning
project-tools reflect learning "JWT tokens require careful expiration handling"

# Show energy trends
project-tools reflect energy --days 7

# View recent reflections
project-tools reflect list --recent
```

**Generated Files:**
- `project_management/reflection/reflection_journal.md` - Structured reflection entries
- `project_management/reflection/energy_tracking.json` - Energy level data and patterns
- `project_management/reflection/learning_log.json` - Captured learnings and insights
- `project_management/reflection/course_corrections.md` - Course correction suggestions and analysis

### Portfolio Manager - Cross-Project Insights

Manages relationships between multiple projects and resource optimization.

```python
# Access portfolio manager
portfolio = project_manager.get_portfolio_manager()

# Initialize portfolio
portfolio.initialize_portfolio("Development Portfolio")

# Add project to portfolio
portfolio.add_project_to_portfolio(
    project_id="web_app",
    project_name="Web Application",
    project_path="/projects/web-app",
    project_type="primary"
)

# Define shared resource
resource_id = portfolio.define_shared_resource(
    resource_name="Authentication Service",
    resource_type="service",
    description="Shared user authentication across projects",
    projects_using=["web_app", "mobile_app"]
)

# Get portfolio insights
health = portfolio.get_portfolio_health()
summary = portfolio.get_portfolio_summary()

# Get resource sharing opportunities
optimization = portfolio.get_resource_sharing_opportunities()
```

**CLI Commands:**
```bash
# Initialize portfolio
project-tools portfolio init

# Add project
project-tools portfolio add-project "Web App" --status active --priority high

# Show portfolio overview
project-tools portfolio overview

# Get resource optimization suggestions
project-tools portfolio optimize
```

**Generated Files:**
- `project_management/portfolio/project_hierarchy.json` - Project relationships and metadata
- `project_management/portfolio/shared_resources.md` - Resource sharing and optimization
- `project_management/portfolio/portfolio_dashboard.html` - Portfolio overview dashboard
- `project_management/portfolio/cross_project_lessons.md` - Cross-project learning capture

### AI Enhancement Engine

The AI enhancement system identifies opportunities for AI-assisted improvements across all intelligence components.

```python
# Get AI enhancement opportunities
enhancements = project_manager.get_ai_enhancement_summary()

# Example output structure:
{
    "total_opportunities": 12,
    "by_component": {
        "compass": ["Refine success criteria", "Expand context analysis"],
        "task_chains": ["Optimize task dependencies", "Improve health metrics"],
        "direction": ["Validate assumptions", "Explore alternative approaches"],
        "reflection": ["Identify learning patterns", "Suggest energy improvements"],
        "portfolio": ["Cross-project synergies", "Resource optimization"]
    },
    "priority_recommendations": [
        "Enhance compass success criteria with measurable metrics",
        "Analyze task chain dependencies for optimization opportunities"
    ]
}

# Get session focus recommendations
focus = project_manager.suggest_next_session_focus()
```

**CLI Commands:**
```bash
# Get AI enhancement opportunities
project-tools ai-enhance opportunities

# Get enhancement summary
project-tools ai-enhance summary

# Get session focus recommendations
project-tools ai-enhance focus
```

## 📋 Complete CLI Reference

The CLI provides comprehensive access to all project management and intelligence features.

### Core Project Management

#### Status and Overview
```bash
# Show comprehensive project status
project-tools status

# Export project data
project-tools export json --output project-data.json
project-tools export html --output report.html
```

#### Todo Management
```bash
# Add todos
project-tools todo add "Fix authentication bug" --priority high --category bug
project-tools todo add "Implement dashboard" --priority medium --category feature

# List and filter todos
project-tools todo list --priority high
project-tools todo list --category bug
project-tools todo list --blocked
project-tools todo list --status in_progress

# Update todos
project-tools todo update 5 --status in_progress
project-tools todo update 5 --priority 9
project-tools todo complete 5

# Dependency management
project-tools todo deps add 5 --depends-on 3
project-tools todo deps remove 5 --depends-on 3
project-tools todo deps show 5

# Advanced todo operations
project-tools todo complete 5 --changelog --change-type bug --version-bump
```

#### Version Management
```bash
# Version operations
project-tools version current
project-tools version bump minor --message "Added user authentication"
project-tools version bump major --message "Breaking API changes"

# Changelog management
project-tools version changes --recent 7
project-tools version changelog --format markdown
```

### Intelligence System Commands

#### Intelligence Management
```bash
# Initialize intelligence system
project-tools intelligence init --project-name "My Project"
project-tools intelligence init --force  # Overwrite existing files

# Status and overview
project-tools intelligence status
project-tools intelligence health
```

#### Compass Commands
```bash
# Initialize compass
project-tools compass init --vision "Create the best development tool"

# Update context
project-tools compass context "Completed user authentication milestone"

# View compass information
project-tools compass show
project-tools compass export --format json
```

#### Task Chain Commands
```bash
# Create and manage chains
project-tools chains create "Authentication System" --description "Complete auth flow"
project-tools chains list
project-tools chains show 1

# Add todos to chains
project-tools chains add-todos 1 --todo-ids 5,6,7
project-tools chains remove-todos 1 --todo-ids 6

# Chain health and progress
project-tools chains health 1
project-tools chains progress 1
```

#### Direction Commands
```bash
# Set project direction
project-tools direction set "Launch MVP by Q2" --assumptions "Market demand exists"

# Manage assumptions
project-tools direction assume "User testing will validate core features"
project-tools direction assumptions list

# Record pivots
project-tools direction pivot "Market feedback indicated different priorities" --new-direction "Focus on core features"

# View direction
project-tools direction show
project-tools direction history
```

#### Reflection Commands
```bash
# Create reflections
project-tools reflect create --type daily --energy 8
project-tools reflect create --type weekly --energy 7 --content "Good progress this week"

# Add learnings
project-tools reflect learning "JWT implementation requires careful token management"

# View reflections and trends
project-tools reflect list --recent
project-tools reflect energy --days 7
project-tools reflect learnings --days 30
```

#### Portfolio Commands
```bash
# Initialize and manage portfolio
project-tools portfolio init
project-tools portfolio add-project "Web App" --status active --priority high

# Portfolio insights
project-tools portfolio overview
project-tools portfolio insights
project-tools portfolio optimize

# Project relationships
project-tools portfolio relate "Web App" "Mobile App" --type dependency
```

#### AI Enhancement Commands
```bash
# Get enhancement opportunities
project-tools ai-enhance opportunities
project-tools ai-enhance summary

# Session recommendations
project-tools ai-enhance focus
project-tools ai-enhance recommendations
```

## 🤖 AI Enhancement Workflows

The system is designed with AI enhancement at its core, providing structured templates that external AI tools can improve while maintaining deterministic operation.

### Template System

All intelligence components use Markdown templates with AI enhancement placeholders:

```markdown
# Project Intent

## Vision
{ai_enhance_vision: Expand and refine the project vision based on current context}

## Success Criteria
{ai_enhance_success_criteria: Define measurable, specific success metrics}

## Strategic Context
{ai_enhance_context: Analyze strategic implications and market positioning}
```

### Enhancement Opportunities

The system automatically identifies AI enhancement opportunities:

```python
# Get enhancement opportunities
opportunities = project_manager.get_ai_enhancement_summary()

# Example opportunity detection:
{
    "compass": [
        {
            "type": "vision_refinement",
            "description": "Vision statement could be more specific and measurable",
            "template_location": "project_management/compass/intent.md",
            "ai_placeholder": "{ai_enhance_vision}",
            "priority": "medium"
        }
    ],
    "task_chains": [
        {
            "type": "dependency_optimization",
            "description": "Task dependencies could be optimized for better flow",
            "data_context": "Chain 'Auth System' has 3 sequential tasks that could be parallelized",
            "priority": "high"
        }
    ]
}
```

### AI Integration Patterns

#### External AI Tool Integration
```python
# Get enhancement context for AI tools
enhancement_context = project_manager.get_ai_enhancement_summary()

# AI tool processes templates and suggestions
# AI tool returns enhanced content

# System validates and integrates AI improvements
# while maintaining deterministic core operations
```

#### Continuous Improvement Loop
```bash
# 1. Work on project normally
project-tools todo add "Implement feature X"
project-tools todo complete 1 --changelog

# 2. Regular AI enhancement cycles
project-tools ai-enhance opportunities

# 3. Apply AI suggestions to templates
# (External AI tool enhances templates)

# 4. Review and validate improvements
project-tools intelligence health
```

## 🔗 New Integration Features (v1)

### GitHub Integration with PyGithub

Automatically push todos, changelogs, and create version tags on GitHub:

```python
# Enable GitHub integration during version manager setup
from project_tools import ProjectManager

# Configure GitHub integration
github_config = {
    "enabled": True,
    "github_token": "your_github_token",  # Or use GITHUB_TOKEN environment variable
    "auto_push": True,
    "auto_tag": True,
    "branch": "main"
}

pm = ProjectManager()
pm.versions.github_integration = GitHubIntegration(pm.project_root, github_config)

# Version bumps now automatically push to GitHub and create tags
pm.bump_version('minor', 'Added GitHub integration')
# This will:
# 1. Update changelog.json and todo.json
# 2. Commit changes to git
# 3. Push to GitHub
# 4. Create and push version tag (e.g., v1.1.0)
```

**Features:**
- **Auto-commit and push**: Automatically commits todo/changelog changes and pushes to GitHub
- **Version tagging**: Creates git tags for versions and pushes them to GitHub 
- **Project file sync**: Syncs todo.json, changelog.json, and project_management/ directory
- **Configurable**: Enable/disable auto-push, custom branch, token management

**Setup GitHub Integration:**
```python
# Option 1: Environment variable (recommended)
export GITHUB_TOKEN="your_github_personal_access_token"

# Option 2: Configuration file
from project_tools.github_integration import GitHubIntegration
config = GitHubIntegration.setup_github_integration()  # Interactive setup
```

### Claude Code Integration

Generate CLAUDE.md files automatically for seamless Claude Code integration:

```python
from project_tools import ProjectManager

pm = ProjectManager()

# Generate project-specific CLAUDE.md file
pm.save_claude_md()
# Creates CLAUDE.md with:
# - Current project status and configuration
# - Essential project_tools commands
# - Project-specific examples and workflows
# - Best practices for Claude Code integration

# Get condensed snippet for existing CLAUDE.md files
snippet = pm.get_claude_snippet()
print(snippet)
```

**Generated CLAUDE.md contains:**
- **Project Overview**: Current status, complexity level, active features
- **Essential Commands**: Project-specific todo management, version control
- **Workflow Patterns**: Feature development, bug fixes, strategic review
- **Active Categories**: Current project categories and example usage
- **Setup Information**: Installation, configuration, file structure

**Integration Features:**
- **Auto-detection**: Analyzes project to generate relevant examples
- **Project-specific**: Customizes content based on your actual todos and setup
- **Workflow guidance**: Provides Claude Code with project-specific patterns
- **Setup integration**: Optionally created during interactive setup

**Usage Examples:**
```bash
# Setup script integration (interactive)
python project_setup.py
# Will ask: "Create CLAUDE.md file for Claude Code integration? (y/n)"

# Manual generation
python -c "from project_tools import ProjectManager; ProjectManager().save_claude_md()"

# Get snippet for copy-pasting
python -c "from project_tools import ProjectManager; print(ProjectManager().get_claude_snippet())"
```

## 🔧 Complete API Reference

### ProjectManager Class

The `ProjectManager` class is the primary interface for all project management operations, providing unified access to todo tracking, version management, and AI-assisted intelligence features.

#### Constructor

```python
ProjectManager(todo_manager=None, version_manager=None, project_root=None, 
               enable_git=True, enable_intelligence=True, intelligence_features=None)
```

**Parameters:**
- `todo_manager`: Custom _TodoManager instance (auto-created if None)
- `version_manager`: Custom _VersionManager instance (auto-created if None)  
- `project_root`: Project root directory (auto-detected if None)
- `enable_git`: Whether to enable git operations (default: True)
- `enable_intelligence`: Whether to enable AI intelligence features (default: True)
- `intelligence_features`: Dict of feature flags for intelligence components

#### Core Todo Management Methods

```python
# Add a new todo
def add_todo(title: str, description: str = "", priority: int = 5, 
             category: str = "general", **kwargs) -> int

# Get todos with optional filtering
def get_todos(status: str = None, category: str = None, **kwargs) -> list

# Complete a todo
def complete_todo(todo_id: int) -> bool

# Update todo status
def update_todo_status(todo_id: int, status: str) -> bool

# Add dependency between todos
def add_dependency(todo_id: int, depends_on_id: int) -> bool

# Get todos blocked by dependencies
def get_blocked_todos() -> list

# Get high priority todos
def get_high_priority_todos(min_priority: int = 8) -> list
```

#### Core Version Management Methods

```python
# Add a change to current version
def add_change(change_type: str, description: str, **kwargs) -> bool

# Bump version and return new version string
def bump_version(version_type: str, message: str = None) -> str

# Get the current version
def get_current_version() -> str

# Get recent changes
def get_recent_changes(days: int = 7) -> list
```

#### Integrated Workflow Methods

```python
# Complete todo and add to changelog in one operation
def complete_todo_with_version(todo_id: int, change_type: str, 
                              change_description: str = None, auto_version_bump: bool = False) -> bool

# Get comprehensive status combining todo, version, and intelligence info
def get_integrated_status() -> dict

# Get workflow recommendations based on current project state
def get_workflow_recommendations() -> list
```

#### Intelligence System Access Methods

```python
# Access to the project compass for intent and context tracking
def get_compass()

# Access to the task chain manager for logical task progressions
def get_task_chains()

# Access to the direction tracker for lightweight goal management
def get_direction_tracker()

# Access to the reflection manager for personal accountability
def get_reflection_manager()

# Access to the portfolio manager for project relationships
def get_portfolio_manager()

# Initialize AI-assisted intelligence features
def initialize_intelligence(project_name: str = "", force: bool = False) -> dict

# Get comprehensive intelligence status across all components
def get_intelligence_status() -> dict

# Get AI-assisted suggestions for next working session focus
def suggest_next_session_focus() -> dict

# Evaluate overall project health across all intelligence dimensions
def evaluate_project_health() -> dict

# Get summary of AI enhancement opportunities
def get_ai_enhancement_summary() -> dict

# Generate CLAUDE.md content for Claude Code integration
def generate_claude_md(include_examples: bool = True, include_setup_info: bool = True) -> str

# Save CLAUDE.md file for Claude Code integration
def save_claude_md(file_path: str = None, **kwargs) -> str

# Get condensed Claude Code snippet for copy-pasting
def get_claude_snippet() -> str
```

#### Properties

```python
# Access to todo manager for advanced operations
@property
def todos() -> '_TodoManager'

# Access to version manager for advanced operations
@property  
def versions() -> '_VersionManager'

# Access to intelligence system for AI-assisted project management
@property
def intelligence() -> 'ProjectIntelligence'
```

### Standalone Functions

```python
# Create both managers for a project
def create_project_managers(project_root=None, enable_git=True) -> tuple[_TodoManager, _VersionManager]

# Get quick status overview of a project
def get_project_status(project_root=None, enable_git=True) -> dict
```

### Usage Examples

#### Basic Project Management

```python
from project_tools import ProjectManager

# Initialize with default settings
pm = ProjectManager()

# Add todos with priorities and categories
todo_id = pm.add_todo(
    title="Implement user authentication",
    description="Add login/logout functionality with JWT",
    priority=8,
    category="feature"
)

# Complete todo with automatic changelog integration
pm.complete_todo_with_version(
    todo_id, "feature", auto_version_bump=True
)

# Get comprehensive project status
status = pm.get_integrated_status()
print(f"Version: {status['version']}, Todos: {status['total_todos']}")
```

#### Intelligence-Enhanced Workflow

```python
# Initialize with intelligence features
pm = ProjectManager(enable_intelligence=True)

# Initialize intelligence system
result = pm.initialize_intelligence("My Project")

# Access individual intelligence components
compass = pm.get_compass()
direction_tracker = pm.get_direction_tracker()
reflection = pm.get_reflection_manager()

# Get AI enhancement opportunities
enhancements = pm.get_ai_enhancement_summary()
print(f"AI opportunities: {enhancements['total_opportunities']}")

# Get next session recommendations
focus = pm.suggest_next_session_focus()
print(f"Recommended focus: {focus['primary_focus']}")
```

#### Advanced Configuration

```python
from project_tools import ProjectManager, _TodoManager, _VersionManager

# Custom configuration
custom_todo_manager = _TodoManager(
    project_root="/custom/path",
    categories=["bug", "feature", "enhancement", "security"],
    statuses=["backlog", "todo", "in_progress", "review", "done"]
)

custom_version_manager = _VersionManager(
    project_root="/custom/path",
    enable_git=False
)

# Create ProjectManager with custom components
pm = ProjectManager(
    todo_manager=custom_todo_manager,
    version_manager=custom_version_manager,
    enable_intelligence=True,
    intelligence_features={
        "compass": True,
        "task_chains": True,
        "direction_tracking": False,  # Disable specific features
        "reflection": True,
        "portfolio": True
    }
)
```

## 🧠 Intelligence System API

The intelligence system consists of 9 core components that provide AI-assisted project management capabilities through structured templates and organized artifact management.

### ProjectIntelligence (project_intelligence.py)

The main facade class coordinating all intelligence components.

```python
class ProjectIntelligence:
    def __init__(project_root=".", todo_manager=None, version_manager=None, feature_flags=None)
    
    # Initialization and management
    def initialize_intelligence(project_name: str = "", force: bool = False) -> dict
    def get_comprehensive_status() -> dict
    def suggest_next_session_focus() -> dict
    def evaluate_project_health() -> dict
    def get_ai_enhancement_summary() -> dict
```

**Key Features:**
- Unified access to all intelligence components
- Feature flag support for enabling/disabling components
- Comprehensive status reporting across all dimensions
- AI enhancement opportunity identification

### ProjectCompass (compass.py)

Manages project intent, success criteria, and strategic context tracking.

```python
class ProjectCompass:
    def __init__(project_root: str = ".")
    
    # Initialization and management
    def initialize_compass(project_name: str = "", force: bool = False) -> dict
    def get_compass_status() -> dict
    def generate_compass_summary() -> dict
    def validate_compass_integrity() -> dict
    
    # Content access and updates
    def get_project_intent() -> Optional[str]
    def get_success_criteria() -> Optional[dict]
    def get_learning_objectives() -> Optional[str] 
    def get_context_log() -> Optional[dict]
    def add_context_entry(entry_type: str, content: str, metadata: dict = None)
    def update_success_criteria(criteria_updates: dict)
    
    # AI enhancement
    def get_ai_enhancement_candidates() -> list
```

**Generated Files:**
- `project_management/compass/project_intent.md` - AI-enhanced project vision
- `project_management/compass/success_criteria.json` - Measurable success metrics
- `project_management/compass/learning_objectives.md` - Learning and skill development goals
- `project_management/compass/context_log.json` - Strategic context and decision history

### DirectionTracker (direction.py)

Provides lightweight goal management with assumption tracking and pivot support.

```python
class DirectionTracker:
    def __init__(project_root: str = ".")
    
    # Direction management
    def set_current_direction(direction: str, rationale: str = "", 
                             success_indicators: list = None, time_horizon: str = "3 months") -> bool
    def evaluate_direction_health() -> dict
    def get_direction_summary() -> dict
    
    # Assumption tracking
    def add_assumption(assumption: str, confidence: str = "medium", 
                      validation_method: str = "", critical: bool = False) -> str
    def validate_assumption(assumption_id: str, result: str, evidence: str = "") -> bool
    
    # Pivot management
    def log_pivot_consideration(trigger: str, new_direction_considered: str,
                               decision: str = "continue", reasoning: str = "")
    
    # AI enhancement
    def get_ai_enhancement_candidates() -> list
```

**Generated Files:**
- `project_management/direction/current_direction.md` - Current direction with AI analysis placeholders
- `project_management/direction/direction_history.json` - Historical direction changes
- `project_management/direction/assumptions.json` - Key assumptions and validation status
- `project_management/direction/pivot_log.md` - Pivot considerations and decisions

### TaskChainManager (task_chains.py)

Creates logical task progressions and manages workflow optimization.

```python
class TaskChainManager:
    def __init__(project_root: str = ".", todo_manager=None)
    
    # Chain management
    def create_task_chain(chain_name: str, description: str = "",
                         chain_type: str = "sequential", milestone_criteria: list = None) -> str
    def add_todos_to_chain(chain_id: str, todo_ids: list, sequence_order: list = None) -> bool
    def define_milestone(chain_id: str, name: str, criteria: str, 
                        todo_dependencies: list = None) -> bool
    
    # Health and optimization
    def get_chain_health(chain_id: str) -> dict
    def get_all_chains_summary() -> dict
    def suggest_chain_optimizations(chain_id: str) -> list
    
    # Visualization
    def generate_chain_visualization(chain_id: str) -> str
```

**Generated Files:**
- `project_management/chains/task_chains.json` - Chain definitions and metadata
- `project_management/chains/chain_visualization.html` - Visual chain representations
- `project_management/chains/milestone_decisions.md` - Milestone tracking and decisions
- `project_management/chains/chain_health_report.html` - Health metrics and optimization suggestions

### ReflectionManager (reflection.py)

Provides personal accountability through structured reflection and self-assessment.

```python
class ReflectionManager:
    def __init__(project_root: str = ".")
    
    # Reflection creation
    def create_reflection_entry(reflection_type: str = "weekly", 
                               custom_prompts: list = None) -> str
    def suggest_course_correction(trigger: str, current_situation: str,
                                 proposed_correction: str, urgency: str = "medium")
    
    # Data tracking
    def log_energy_level(energy_level: int, context: str = "", 
                        factors: list = None, session_type: str = "work")
    def capture_learning(learning: str, category: str = "general", 
                        source: str = "", actionable: bool = False, 
                        related_todos: list = None) -> str
    
    # Analysis and insights
    def get_reflection_insights(days_back: int = 30) -> dict
    def get_reflection_summary() -> dict
    def get_ai_enhancement_candidates() -> list
```

**Generated Files:**
- `project_management/reflection/reflection_journal.md` - Structured reflection entries
- `project_management/reflection/energy_tracking.json` - Energy level data and patterns
- `project_management/reflection/learning_log.json` - Captured learnings and insights
- `project_management/reflection/course_corrections.md` - Course correction suggestions and analysis

### PortfolioManager (portfolio.py)

Handles cross-project relationships and portfolio-level optimization.

```python
class PortfolioManager:
    def __init__(project_root: str = ".")
    
    # Portfolio initialization
    def initialize_portfolio(portfolio_name: str = "", force: bool = False) -> dict
    def add_project_to_portfolio(project_id: str, project_name: str, project_path: str,
                                project_type: str = "primary", parent_project: str = None) -> bool
    
    # Resource management
    def define_shared_resource(resource_name: str, resource_type: str, description: str = "",
                              projects_using: list = None, location: str = "") -> str
    def get_resource_sharing_opportunities() -> list
    
    # Cross-project insights
    def log_cross_project_lesson(lesson: str, projects_involved: list,
                                lesson_type: str = "general", actionable_insights: list = None)
    def get_portfolio_health() -> dict
    def get_portfolio_summary() -> dict
    
    # Visualization
    def generate_portfolio_dashboard() -> str
```

**Generated Files:**
- `project_management/portfolio/project_hierarchy.json` - Project relationships and metadata
- `project_management/portfolio/shared_resources.md` - Resource sharing and optimization
- `project_management/portfolio/portfolio_dashboard.html` - Portfolio overview dashboard
- `project_management/portfolio/cross_project_lessons.md` - Cross-project learning capture

### IntelligenceFileManager (file_manager.py)

Centralized file management for intelligence artifacts with organized directory structure.

```python
class IntelligenceFileManager:
    def __init__(project_root: str = ".")
    
    # Directory management
    def ensure_directory_structure()
    def get_file_path(category: str, filename: str) -> Path
    def cleanup_empty_directories() -> list
    
    # File operations
    def save_file(category: str, filename: str, content: Union[str, dict, list]) -> Path
    def load_file(category: str, filename: str) -> Optional[Union[str, dict, list]]
    def file_exists(category: str, filename: str) -> bool
    def list_files(category: str = None) -> dict
    
    # Inventory and maintenance
    def get_artifact_inventory() -> dict
    def backup_intelligence_data(backup_path: str = None) -> str
    def restore_from_backup(backup_path: str) -> bool
    def migrate_files(file_mapping: dict) -> dict
    def get_directory_size() -> dict
```

**Key Constants:**
- `PROJECT_MANAGEMENT_DIR = 'project_management'`
- `INTELLIGENCE_SUBDIRS = {'compass', 'chains', 'direction', 'reflection', 'portfolio'}`

### TemplateGenerator (templates.py)

Creates structured templates with AI enhancement placeholders for external processing.

```python
class TemplateGenerator:
    def __init__()
    
    # Template creation
    def create_template_with_placeholders(template_type: str, **kwargs) -> str
    def parse_placeholders(content: str) -> list
    def validate_enhanced_content(original: str, enhanced: str) -> bool

class TemplateValidator:
    @staticmethod
    def validate_template_structure(content: str, template_type: str) -> bool
    @staticmethod  
    def validate_ai_enhancement(original: str, enhanced: str) -> dict

class AIPlaceholder:
    def __init__(name: str, description: str, content_type: str = "text")
    def fill(content: str)
    def to_dict() -> dict
```

**Supported Template Types:**
- `project_intent` - Project vision and goals
- `success_criteria` - Measurable success metrics  
- `learning_objectives` - Learning and development goals
- `task_chain` - Task chain visualization and analysis
- `direction_analysis` - Direction validation and alternatives
- `reflection_journal` - Reflection entries and insights
- `portfolio_overview` - Portfolio analysis and optimization

### Intelligence Module Exports (__init__.py)

The intelligence module provides clean exports for all components:

```python
from project_tools.intelligence import (
    ProjectCompass,
    TaskChainManager, 
    DirectionTracker,
    ReflectionManager,
    PortfolioManager,
    ProjectIntelligence,
    PROJECT_MANAGEMENT_DIR,
    INTELLIGENCE_SUBDIRS
)
```

### Integration Patterns

#### Complete Intelligence Workflow

```python
from project_tools import ProjectManager

# Initialize with full intelligence
pm = ProjectManager(enable_intelligence=True)
result = pm.initialize_intelligence("My Project")

# Set strategic direction
direction = pm.get_direction_tracker()
direction.set_current_direction(
    direction="Build MVP in 3 months",
    rationale="Market opportunity window is limited",
    success_indicators=["Working prototype", "User feedback", "Technical validation"]
)

# Create task chain
chains = pm.get_task_chains()
chain_id = chains.create_task_chain(
    chain_name="MVP Development",
    description="Core features for minimum viable product",
    chain_type="milestone-based"
)

# Add todos to chain
todo_ids = [
    pm.add_todo("Design user interface", priority=8, category="feature"),
    pm.add_todo("Implement backend API", priority=9, category="feature"),
    pm.add_todo("Setup deployment pipeline", priority=7, category="infrastructure")
]
chains.add_todos_to_chain(chain_id, todo_ids)

# Track project context
compass = pm.get_compass()
compass.add_context_entry("decision", "Chose React for frontend due to team expertise")

# Regular reflection
reflection = pm.get_reflection_manager()
reflection.log_energy_level(7, "Good progress on core features")
reflection.capture_learning(
    "Database schema design impacts API performance significantly",
    category="technical",
    actionable=True
)

# Get AI enhancement opportunities
enhancements = pm.get_ai_enhancement_summary()
print(f"Ready for AI enhancement: {enhancements['total_opportunities']} files")
```

#### Cross-Project Portfolio Management

```python
# Portfolio setup across multiple projects
portfolio = pm.get_portfolio_manager()
portfolio.initialize_portfolio("Development Portfolio")

# Add projects to portfolio
portfolio.add_project_to_portfolio(
    project_id="web_app",
    project_name="Web Application", 
    project_path="/projects/web-app",
    project_type="primary"
)

portfolio.add_project_to_portfolio(
    project_id="mobile_app",
    project_name="Mobile App",
    project_path="/projects/mobile-app", 
    project_type="primary"
)

# Define shared resources
portfolio.define_shared_resource(
    resource_name="Authentication Service",
    resource_type="service",
    description="Shared user authentication across projects",
    projects_using=["web_app", "mobile_app"]
)

# Log cross-project lessons
portfolio.log_cross_project_lesson(
    lesson="State management patterns are crucial for complex UIs",
    projects_involved=["web_app", "mobile_app"],
    lesson_type="technical",
    actionable_insights=["Standardize on Redux pattern", "Create shared state management library"]
)

# Generate portfolio dashboard
dashboard_path = portfolio.generate_portfolio_dashboard()
print(f"Portfolio dashboard generated: {dashboard_path}")
```

## 📁 Complete File Organization

The intelligence system creates a comprehensive, organized directory structure:

```
your_project/
├── todo.json                          # Core todo data with dependencies
├── changelog.json                     # Version history and changes
└── project_management/                # Intelligence artifacts directory
    ├── compass/                       # Strategic direction and intent
    │   ├── project_intent.md          # Project vision and success criteria with AI placeholders
    │   ├── success_criteria.json      # Measurable success metrics
    │   ├── learning_objectives.md     # Learning and skill development goals
    │   └── context_log.json          # Strategic context and decision history
    ├── chains/                        # Logical task progressions
    │   ├── task_chains.json           # Chain definitions and metadata
    │   ├── chain_visualization.html   # Visual chain representations
    │   ├── milestone_decisions.md     # Milestone tracking and decisions
    │   └── chain_health_report.html   # Health metrics and optimization suggestions
    ├── direction/                     # Goal management and pivots
    │   ├── current_direction.md       # Current direction with AI analysis placeholders
    │   ├── direction_history.json     # Historical direction changes
    │   ├── assumptions.json           # Key assumptions and validation status
    │   └── pivot_log.md              # Pivot considerations and decisions
    ├── reflection/                    # Personal accountability
    │   ├── reflection_journal.md      # Structured reflection entries with AI placeholders
    │   ├── energy_tracking.json       # Energy level data and patterns
    │   ├── learning_log.json         # Captured learnings and insights
    │   └── course_corrections.md      # Course correction suggestions and analysis
    └── portfolio/                     # Cross-project management
        ├── project_hierarchy.json     # Project relationships and metadata
        ├── shared_resources.md        # Resource sharing and optimization with AI placeholders
        ├── portfolio_dashboard.html   # Portfolio overview dashboard
        └── cross_project_lessons.md   # Cross-project learning capture
```

### File Type Documentation

#### Core Data Files (JSON)
- **todo.json**: Complete todo data with dependencies, categories, and metadata
- **changelog.json**: Version history with semantic versioning and change tracking

#### Intelligence Templates (Markdown)
- **Structured templates** with AI enhancement placeholders
- **Human-readable** for easy review and manual editing
- **Version controlled** to track evolution over time

#### Logs Directory (JSON)
- **Daily snapshots** of each intelligence component
- **Historical tracking** for trend analysis
- **AI training data** for pattern recognition

#### Integration Files
- **opportunities.json**: Current AI enhancement opportunities with priority
- **enhancement_history.json**: Track AI improvements over time
- **dashboards/**: Auto-generated HTML reports for web viewing

### Backup and Migration

```python
# Complete data export
project_manager.export_all_data("backup_YYYYMMDD.json")

# Selective intelligence export
intelligence_data = project_manager.intelligence.export_intelligence_data()

# Import and restore
project_manager.import_data("backup_YYYYMMDD.json")
```

```bash
# CLI backup operations
project-tools export complete --output full_backup.json
project-tools export intelligence --output intelligence_backup.json

# Restore operations
project-tools import --file full_backup.json --validate
```

## 🔗 Advanced Integration Examples

### Intelligence-Aware CI/CD Workflows

```yaml
# GitHub Actions example with intelligence integration
name: Intelligent Project Management
on: [push, pull_request]

jobs:
  project-intelligence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Project Tools
        run: |
          pip install git+https://github.com/noskillsben/project_tools.git
          
      - name: Update Project Status
        run: |
          python3 -c "
          from project_tools import ProjectManager
          pm = ProjectManager(enable_intelligence=True)
          
          # Get comprehensive status
          status = pm.get_integrated_status()
          print(f'Version: {status[\"version\"]}')
          print(f'High Priority Todos: {status[\"high_priority_todos\"]}')
          print(f'Intelligence Active: {status[\"intelligence\"][\"active\"]}')
          
          # Get AI enhancement opportunities
          enhancements = pm.get_ai_enhancement_summary()
          print(f'AI Opportunities: {enhancements[\"total_opportunities\"]}')
          
          # Update compass context for CI
          if pm.intelligence:
              pm.get_compass().add_context_entry('automation', 'CI/CD pipeline executed successfully')
          "
          
      - name: Generate Intelligence Report
        run: |
          project-tools intelligence status > intelligence_report.txt
          project-tools ai-enhance opportunities >> intelligence_report.txt
          
      - name: Upload Intelligence Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: intelligence-report
          path: |
            intelligence_report.txt
            project_management/
```

### Portfolio Management Across Multiple Projects

```python
# Cross-project portfolio management
def manage_portfolio():
    projects = [
        {"path": "/projects/web-app", "name": "Web Application"},
        {"path": "/projects/mobile-app", "name": "Mobile Application"},
        {"path": "/projects/api-service", "name": "API Service"}
    ]
    
    portfolio_insights = []
    
    for project in projects:
        pm = ProjectManager(project_root=project["path"], enable_intelligence=True)
        
        # Get project status
        status = pm.get_integrated_status()
        
        # Add to portfolio
        portfolio = pm.get_portfolio_manager()
        portfolio.add_project_to_portfolio(
            project_id=project["name"].lower().replace(" ", "_"),
            project_name=project["name"],
            project_path=project["path"],
            project_type="active" if status["in_progress_todos"] > 0 else "maintenance"
        )
        
        portfolio_insights.append({
            "project": project["name"],
            "status": status,
            "ai_opportunities": pm.get_ai_enhancement_summary()
        })
    
    return portfolio_insights

# Resource optimization across projects
def optimize_resources():
    portfolio_manager = ProjectManager().get_portfolio_manager()
    optimization = portfolio_manager.get_resource_sharing_opportunities()
    
    for opportunity in optimization:
        print(f"• {opportunity['type']}: {opportunity.get('resource_name', 'N/A')}")
```

### AI Enhancement Integration Patterns

```python
# AI-assisted workflow enhancement
class AIProjectManager:
    def __init__(self, ai_service):
        self.pm = ProjectManager(enable_intelligence=True)
        self.ai_service = ai_service
    
    def enhanced_project_planning(self):
        # Get current project state
        status = self.pm.get_integrated_status()
        opportunities = self.pm.get_ai_enhancement_summary()
        
        # AI analysis of project state
        ai_analysis = self.ai_service.analyze_project_status(status, opportunities)
        
        # Apply AI recommendations
        for recommendation in ai_analysis["recommendations"]:
            if recommendation["type"] == "todo_prioritization":
                self.apply_todo_prioritization(recommendation)
            elif recommendation["type"] == "task_chain_optimization":
                self.optimize_task_chains(recommendation)
            elif recommendation["type"] == "direction_adjustment":
                self.adjust_project_direction(recommendation)
    
    def continuous_improvement_cycle(self):
        # Daily AI enhancement cycle
        while True:
            # Get enhancement opportunities
            opportunities = self.pm.get_ai_enhancement_summary()
            
            if opportunities["total_opportunities"] > 0:
                # Process with AI
                enhanced_content = self.ai_service.enhance_templates(opportunities)
                
                # Validate and apply improvements
                self.validate_and_apply_enhancements(enhanced_content)
            
            # Wait for next cycle
            time.sleep(86400)  # 24 hours
```

## 🛠️ Full Project Setup Examples

### Recommended: Use the Setup Guide

**For most users, the interactive setup guide is the best way to get started:**

```bash
# Quick setup for any project type
curl -O https://raw.githubusercontent.com/noskillsben/project_tools/main/project_setup.py
python project_setup.py
```

The setup guide handles all the complexity and gives you a project configured for your specific needs.

### Manual Setup Examples

#### Individual Developer Setup

```bash
# 1. Install project tools
pip install git+https://github.com/noskillsben/project_tools.git

# 2. Navigate to your project
cd /path/to/your/project

# 3. Use the setup guide (recommended)
python project_setup.py

# OR manual setup:
# 3. Initialize with intelligence features
project-tools intelligence init --project-name "My Awesome Project"

# 4. Set up project compass
project-tools compass init --vision "Create the best solution for my users"

# 5. Add initial todos
project-tools todo add "Set up development environment" --priority high --category setup
project-tools todo add "Implement core features" --priority high --category feature
project-tools todo add "Write comprehensive tests" --priority medium --category testing

# 6. Create task chain
project-tools chains create "MVP Development" --description "Essential features for MVP"
project-tools chains add-todos 1 --todo-ids 1,2,3

# 7. Set project direction
project-tools direction set "Launch MVP in 2 months" --assumptions "Core features sufficient,No major blockers"

# 8. Verify setup
project-tools status
project-tools intelligence status
```

### Team Setup with Git Integration

```bash
# 1. Team lead initializes project
git clone https://github.com/your-team/project.git
cd project
pip install git+https://github.com/noskillsben/project_tools.git

# 2. Use setup guide for team project (recommended)
curl -O https://raw.githubusercontent.com/noskillsben/project_tools/main/project_setup.py
python project_setup.py
# Choose "Software Development" and "Standard" or "Full Intelligence" mode

# 3. Commit project setup
git add project_management/ todo.json changelog.json project_setup_summary.json
git commit -m "Initialize project tools with guided setup"
git push

# 4. Team members setup
# Each team member runs:
pip install git+https://github.com/noskillsben/project_tools.git
git pull  # Get the project setup
python -c "from project_tools import ProjectManager; print('✅ Project tools ready:', ProjectManager().get_integrated_status())"

# OR manual team setup:
# 2. Initialize team intelligence system
project-tools intelligence init --project-name "Team Project"

# 3. Set up shared compass
project-tools compass init --vision "Deliver high-quality software that delights users"

# 4. Create team workflows
project-tools chains create "Sprint 1" --description "First sprint deliverables"
project-tools chains create "Code Review" --description "Review and quality assurance"

# 5. Set team direction
project-tools direction set "Complete sprint goals" --assumptions "Team capacity stable,Requirements clear"

# 6. Commit intelligence setup
git add project_management/ todo.json changelog.json
git commit -m "Initialize project intelligence system"
git push

# 7. Team members setup
# Each team member runs:
pip install git+https://github.com/noskillsben/project_tools.git
project-tools status  # Verify they can access project data
```

### CI/CD Integration Setup

```yaml
# .github/workflows/project-intelligence.yml
name: Project Intelligence Update

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM

jobs:
  intelligence-update:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install Project Tools
        run: |
          pip install git+https://github.com/noskillsben/project_tools.git
          
      - name: Update Intelligence Context
        run: |
          project-tools compass context "CI/CD pipeline execution on $(date)"
          
      - name: Generate Status Report
        run: |
          project-tools status > project_status.txt
          project-tools intelligence status > intelligence_status.txt
          project-tools ai-enhance opportunities > ai_opportunities.txt
          
      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: project-reports
          path: |
            project_status.txt
            intelligence_status.txt
            ai_opportunities.txt
            project_management/
            
      - name: Commit Intelligence Updates
        if: github.ref == 'refs/heads/main'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add project_management/
          git diff --staged --quiet || git commit -m "Update intelligence data from CI/CD"
          git push
```

### AI Agent Integration Setup

```python
# ai_agent_integration.py
from project_tools import ProjectManager
import json
import logging

class AIProjectAgent:
    """AI agent that uses Project Tools for intelligent project management."""
    
    def __init__(self, project_root=None):
        self.pm = ProjectManager(
            project_root=project_root,
            enable_intelligence=True,
            enable_git=True
        )
        self.logger = logging.getLogger(__name__)
        
    def autonomous_project_management(self):
        """Run autonomous project management cycle."""
        try:
            # 1. Assess current project state
            status = self.pm.get_integrated_status()
            self.logger.info(f"Project status: {status['version']} - {status['total_todos']} todos")
            
            # 2. Get AI enhancement opportunities
            opportunities = self.pm.get_ai_enhancement_summary()
            
            # 3. Process high-priority todos
            high_priority = self.pm.get_high_priority_todos()
            for todo in high_priority[:3]:  # Process top 3
                self.process_todo_autonomously(todo)
                
            # 4. Update project intelligence
            self.update_intelligence_context()
            
            # 5. Generate recommendations
            recommendations = self.pm.get_workflow_recommendations()
            self.logger.info(f"Generated {len(recommendations)} recommendations")
            
            return {
                "status": "success",
                "processed_todos": len(high_priority[:3]),
                "recommendations": recommendations,
                "ai_opportunities": opportunities["total_opportunities"]
            }
            
        except Exception as e:
            self.logger.error(f"Error in autonomous management: {e}")
            return {"status": "error", "message": str(e)}
    
    def process_todo_autonomously(self, todo):
        """Process a todo item autonomously."""
        # AI agent logic for handling specific todos
        if todo["category"] == "bug":
            self.handle_bug_autonomously(todo)
        elif todo["category"] == "feature":
            self.handle_feature_autonomously(todo)
        elif todo["category"] == "test":
            self.handle_test_autonomously(todo)
    
    def update_intelligence_context(self):
        """Update intelligence context with AI insights."""
        compass = self.pm.get_compass()
        if compass:
            compass.add_context_entry("automation", "AI agent performed autonomous project analysis")
            
        reflection = self.pm.get_reflection_manager()
        if reflection:
            reflection.create_reflection_entry(
                reflection_type="ai_analysis",
                custom_prompts=["What optimization opportunities were identified?"]
            )
            reflection.log_energy_level(7, "AI analysis completed")
            reflection.capture_learning(
                "Autonomous project management provides consistent monitoring",
                category="automation",
                actionable=True
            )

# Usage example
if __name__ == "__main__":
    agent = AIProjectAgent()
    result = agent.autonomous_project_management()
    print(json.dumps(result, indent=2))
```

## ⚙️ Enhanced Configuration Documentation

### Project Manager Configuration

```python
# Basic configuration
pm = ProjectManager(
    project_root="/path/to/project",      # Custom project root
    enable_git=True,                      # Git integration
    enable_intelligence=True,             # AI features
    intelligence_features={               # Feature flags
        "compass": True,
        "task_chains": True,
        "direction": True,
        "reflection": True,
        "portfolio": True,
        "ai_enhancement": True
    }
)

# Advanced configuration with custom managers
from project_tools._todo_manager import _TodoManager
from project_tools._version_manager import _VersionManager

todo_manager = _TodoManager(
    project_root="/custom/path",
    categories=["bug", "feature", "enhancement", "research", "deployment", "security"],
    statuses=["backlog", "todo", "in_progress", "review", "testing", "done"],
    todo_path="/custom/todos.json"
)

version_manager = _VersionManager(
    project_root="/custom/path",
    enable_git=False,                     # Disable git integration
    changelog_path="/custom/changelog.json"
)

pm = ProjectManager(
    todo_manager=todo_manager,
    version_manager=version_manager,
    enable_intelligence=True
)
```

### Intelligence System Configuration

```python
# Configure intelligence features
intelligence_config = {
    "compass": {
        "auto_context_updates": True,
        "vision_tracking": True
    },
    "task_chains": {
        "auto_health_monitoring": True,
        "milestone_tracking": True
    },
    "direction": {
        "assumption_validation": True,
        "pivot_detection": True
    },
    "reflection": {
        "energy_tracking": True,
        "learning_categorization": True
    },
    "portfolio": {
        "cross_project_insights": True,
        "resource_optimization": True
    }
}

pm = ProjectManager(
    enable_intelligence=True,
    intelligence_features=intelligence_config
)
```

### Git Integration Configuration

```python
# Git configuration options
version_manager = _VersionManager(
    enable_git=True,
    git_config={
        "auto_tag": True,                 # Automatically create git tags
        "tag_prefix": "v",                # Tag prefix (v1.0.0)
        "push_tags": False,               # Don't auto-push tags
        "track_status": True,             # Include git status in reports
        "commit_changelog": True          # Auto-commit changelog updates
    }
)
```

### File Location Customization

```python
# Custom file locations
pm = ProjectManager(project_root="/my/project")

# Customize file paths
pm.todos.todo_path = "/custom/location/todos.json"
pm.versions.changelog_path = "/custom/location/changelog.json"

# Intelligence system custom paths
if pm.intelligence:
    pm.intelligence.file_manager.base_dir = "/custom/project_management"
```

### Environment Variable Configuration

```bash
# Environment variables for configuration
export PROJECT_TOOLS_ROOT="/default/project/path"
export PROJECT_TOOLS_ENABLE_GIT="true"
export PROJECT_TOOLS_ENABLE_INTELLIGENCE="true"
export PROJECT_TOOLS_TODO_PATH="/custom/todos.json"
export PROJECT_TOOLS_CHANGELOG_PATH="/custom/changelog.json"
export PROJECT_TOOLS_INTELLIGENCE_PATH="/custom/project_management"
```

```python
# Using environment variables
import os
from project_tools import ProjectManager

pm = ProjectManager(
    project_root=os.getenv("PROJECT_TOOLS_ROOT"),
    enable_git=os.getenv("PROJECT_TOOLS_ENABLE_GIT", "true").lower() == "true",
    enable_intelligence=os.getenv("PROJECT_TOOLS_ENABLE_INTELLIGENCE", "true").lower() == "true"
)
```

## 👥 Target Audience and Use Cases

### Individual Developers

**Benefits:**
- Structured project organization without overhead
- AI-assisted project intelligence for better decision-making
- Seamless integration with existing development workflows
- Personal accountability through reflection system

**Common Use Cases:**
```python
# Daily development workflow
pm = ProjectManager(enable_intelligence=True)

# Morning: Review status and set focus
status = pm.get_integrated_status()
focus = pm.suggest_next_session_focus()

# During work: Track progress
todo_id = pm.add_todo("Fix API endpoint bug", priority=8, category="bug")
pm.complete_todo_with_version(todo_id, "bug", auto_version_bump=True)

# Evening: Reflect on progress
reflection = pm.get_reflection_manager()
reflection.create_reflection(
    type="daily",
    content="Fixed critical API bug, improved error handling",
    energy_level=7,
    learnings=["Error handling patterns need standardization"]
)
```

### Development Teams

**Benefits:**
- Shared project intelligence and context
- Coordinated task management with dependency tracking
- Team reflection and learning capture
- Integrated version management with team workflows

**Common Use Cases:**
```bash
# Team standup integration
project-tools status | grep "high_priority\|blocked"
project-tools chains list --active

# Sprint planning
project-tools chains create "Sprint 15" --description "Q2 feature delivery"
project-tools direction set "Complete user dashboard" --assumptions "Design approved,API ready"

# Team retrospectives
project-tools reflect list --team --recent
project-tools portfolio insights
```

### Coding Agents and AI Tools

**Benefits:**
- Predictable, consistent API designed for automation
- Rich context and intelligence for AI decision-making
- Template system designed for AI enhancement
- Comprehensive status and recommendation endpoints

**Agent Integration Patterns:**
```python
class ProjectManagementAgent:
    def __init__(self):
        self.pm = ProjectManager(enable_intelligence=True)
    
    def autonomous_workflow(self):
        # Get comprehensive project state
        status = self.pm.get_integrated_status()
        recommendations = self.pm.get_workflow_recommendations()
        
        # Process high-priority items
        for todo in self.pm.get_high_priority_todos()[:3]:
            self.process_todo_intelligently(todo)
        
        # Update project intelligence
        self.update_project_context(status)
        
        # Generate AI-enhanced recommendations
        return self.generate_enhanced_recommendations()
```

### CI/CD and DevOps

**Benefits:**
- Automated project status tracking
- Integration with build and deployment pipelines
- Historical project health monitoring
- Automated reporting and alerting

**DevOps Integration:**
```yaml
# Automated project health monitoring
- name: Monitor Project Health
  run: |
    health=$(project-tools intelligence health --json)
    if [ "$(echo $health | jq '.overall_health < 0.7')" = "true" ]; then
      echo "Project health below threshold"
      project-tools ai-enhance opportunities
      exit 1
    fi
```

### Project Managers and Technical Leaders

**Benefits:**
- High-level project overview with intelligence insights
- Portfolio management across multiple projects
- Strategic direction tracking and pivot management
- Team performance and energy monitoring

**Management Workflows:**
```python
# Executive dashboard
pm = ProjectManager(enable_intelligence=True)

# Get portfolio overview
portfolio = pm.get_portfolio_manager()
insights = portfolio.get_portfolio_insights()

# Strategic assessment
compass = pm.get_compass()
direction = compass.get_current_direction()

# Team health monitoring
reflection = pm.get_reflection_manager()
team_energy = reflection.get_team_energy_trends()
```

## 🚨 Troubleshooting

### Common Installation Issues

**Package Not Found Error**
```bash
# Error: No module named 'project_tools'
# Solution: Ensure proper installation
pip uninstall project-tools  # Remove any conflicting versions
pip install git+https://github.com/noskillsben/project_tools.git

# Verify installation
python -c "from project_tools import ProjectManager; print('Success')"
```

**CLI Command Not Found**
```bash
# Error: command not found: project-tools
# Solution: Check installation and PATH
pip show project-tools  # Verify package is installed
which project-tools     # Check if CLI is in PATH

# Reinstall with force
pip install --force-reinstall git+https://github.com/noskillsben/project_tools.git
```

### Intelligence System Issues

**Intelligence Not Initializing**
```python
# Check intelligence status
pm = ProjectManager(enable_intelligence=True)
status = pm.get_intelligence_status()

if not status["intelligence_active"]:
    # Force initialization
    result = pm.initialize_intelligence(force=True)
    print(result)
```

**Template Files Missing**
```bash
# Reinitialize intelligence system
project-tools intelligence init --force

# Verify directory structure
ls -la project_management/
```

### Data File Issues

**Corrupted JSON Files**
```python
# Backup and reset
import shutil
import os

# Backup existing files
shutil.copy("todo.json", "todo.json.backup")
shutil.copy("changelog.json", "changelog.json.backup")

# Initialize fresh managers
pm = ProjectManager()
# Data will be recreated with defaults
```

**Permission Issues**
```bash
# Fix file permissions
chmod 644 todo.json changelog.json
chmod -R 755 project_management/

# Check directory ownership
ls -la | grep -E "(todo|changelog|project_management)"
```

### Git Integration Issues

**Git Not Available**
```python
# Disable git integration
pm = ProjectManager(enable_git=False)

# Or configure git settings
pm.versions.git_config = {
    "auto_tag": False,
    "push_tags": False,
    "track_status": False
}
```

**Version Conflicts**
- **Python 3.7+**: Required for proper type hints and pathlib support
- **Git**: Optional, disable with `enable_git=False` if not available
- **Dependencies**: Only uses Python standard library for core functionality

### Performance Considerations

**Large Projects (1000+ todos)**
```python
# Optimize for large datasets
pm = ProjectManager()

# Periodic cleanup of completed items
completed_todos = pm.get_todos(status="complete")
old_todos = [t for t in completed_todos if is_older_than_30_days(t)]

# Archive old todos instead of keeping in active dataset
pm.todos.archive_todos(old_todos)
```

**Memory Usage Optimization**
```python
# For very large projects, consider selective loading
pm = ProjectManager()

# Load only active todos
active_todos = pm.get_todos(status=["todo", "in_progress"])

# Use streaming for large operations
for todo in pm.todos.iterate_todos(batch_size=100):
    process_todo(todo)
```

## 📄 License and Contributing

### License
MIT License - see LICENSE file for details.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper tests
4. Run the full test suite: `pytest --cov=project_tools`
5. Ensure code quality: `black project_tools tests && flake8 project_tools tests && mypy project_tools`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- **API Consistency**: Maintain the unified ProjectManager interface
- **Intelligence Integration**: Ensure new features work with the AI enhancement system
- **Documentation**: Update both README and docstrings
- **Testing**: Include comprehensive tests for new functionality
- **Backward Compatibility**: Maintain compatibility with existing workflows

### Community and Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/noskillsben/project_tools/issues)
- **Discussions**: Join conversations about features and use cases
- **Documentation**: Contribute to documentation improvements
- **Examples**: Share your integration patterns and use cases

## 🎯 Quick Reference

### Getting Started
```bash
# 1. Install and setup (recommended)
pip install git+https://github.com/noskillsben/project_tools.git
curl -O https://raw.githubusercontent.com/noskillsben/project_tools/main/project_setup.py
python project_setup.py

# 2. Check your setup
python -c "from project_tools import ProjectManager; pm = ProjectManager(); print('Status:', pm.get_integrated_status())"
```

### Essential Commands
```bash
# Manual setup (if not using setup guide)
project-tools intelligence init --project-name "My Project"

# Daily workflow
project-tools status
project-tools todo add "Task" --priority high
project-tools todo complete 1 --changelog --version-bump

# Intelligence features (if enabled)
project-tools ai-enhance opportunities
project-tools compass context "Major milestone completed"
project-tools reflect create --type daily --energy 8
```

### Essential Python API
```python
from project_tools import ProjectManager

pm = ProjectManager(enable_intelligence=True)
todo_id = pm.add_todo("Task", priority=8, category="feature")
pm.complete_todo_with_version(todo_id, "feature", auto_version_bump=True)
status = pm.get_integrated_status()
opportunities = pm.get_ai_enhancement_summary()
```

---

**Project Tools** transforms project management from basic task tracking into an intelligent, AI-ready system that learns and adapts. Perfect for modern development workflows where structure, intelligence, and automation are essential for success.