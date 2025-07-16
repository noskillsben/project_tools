"""
PortfolioManager class for handling parent-child project relationships and cross-project learning.

Manages project hierarchies, shared resources, cross-project insights, and portfolio-level
optimization within the organized project_management/ structure.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path

from .file_manager import IntelligenceFileManager
from .templates import TemplateGenerator


class PortfolioManager:
    """
    Manages portfolio-level project relationships and cross-project optimization.
    
    Handles parent-child project relationships, shared resource tracking, 
    cross-project learning capture, and portfolio health monitoring with
    AI-assisted insights and optimization suggestions.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.file_manager = IntelligenceFileManager(project_root)
        self.template_generator = TemplateGenerator()
        self.category = "portfolio"
        
        # Standard portfolio files
        self.files = {
            "project_hierarchy": "project_hierarchy.json",
            "shared_resources": "shared_resources.md",
            "portfolio_dashboard": "portfolio_dashboard.html",
            "cross_project_lessons": "cross_project_lessons.md"
        }
    
    def initialize_portfolio(self, portfolio_name: str = "", force: bool = False) -> Dict[str, str]:
        """
        Initialize portfolio management with template files.
        
        Args:
            portfolio_name: Name of the portfolio for template customization
            force: Whether to overwrite existing files
            
        Returns:
            Dictionary mapping file types to created file paths
        """
        self.file_manager.ensure_directory_structure()
        
        if not portfolio_name:
            portfolio_name = self.project_root.name + " Portfolio"
        
        created_files = {}
        
        # Create project hierarchy template
        if force or not self.file_manager.file_exists(self.category, self.files["project_hierarchy"]):
            hierarchy_data = {
                "portfolio_name": portfolio_name,
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "projects": [],
                "relationships": [],
                "shared_resources": [],
                "cross_project_dependencies": []
            }
            path = self.file_manager.save_file(self.category, self.files["project_hierarchy"], hierarchy_data)
            created_files["project_hierarchy"] = str(path)
        
        # Create shared resources template
        if force or not self.file_manager.file_exists(self.category, self.files["shared_resources"]):
            resources_content = self.template_generator.create_template_with_placeholders(
                "portfolio_overview"
            )
            path = self.file_manager.save_file(self.category, self.files["shared_resources"], resources_content)
            created_files["shared_resources"] = str(path)
        
        # Create cross-project lessons template
        if force or not self.file_manager.file_exists(self.category, self.files["cross_project_lessons"]):
            lessons_content = f"""# Cross-Project Lessons

## Overview
This document captures insights, patterns, and learnings that apply across multiple projects in the portfolio.

## Pattern Recognition
{{ai_cross_project_pattern_identification}}

## Resource Optimization Opportunities
{{ai_resource_sharing_recommendations}}

## Common Success Factors
{{ai_success_pattern_analysis}}

## Recurring Challenges
{{ai_common_challenge_identification}}

## Knowledge Transfer Opportunities
{{ai_knowledge_transfer_suggestions}}

## Portfolio-Level Insights
{{ai_portfolio_optimization_insights}}

---
*Portfolio lessons initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            path = self.file_manager.save_file(self.category, self.files["cross_project_lessons"], lessons_content)
            created_files["cross_project_lessons"] = str(path)
        
        return created_files
    
    def add_project_to_portfolio(self, 
                                project_id: str,
                                project_name: str,
                                project_path: str,
                                project_type: str = "primary",
                                parent_project: Optional[str] = None) -> bool:
        """
        Add a project to the portfolio hierarchy.
        
        Args:
            project_id: Unique identifier for the project
            project_name: Display name for the project
            project_path: File system path to the project
            project_type: Type of project (primary, subproject, experiment, etc.)
            parent_project: ID of parent project if this is a subproject
            
        Returns:
            True if project was successfully added
        """
        hierarchy_data = self._load_hierarchy_data()
        
        # Check if project already exists
        if any(p["id"] == project_id for p in hierarchy_data["projects"]):
            return False
        
        new_project = {
            "id": project_id,
            "name": project_name,
            "path": project_path,
            "type": project_type,
            "parent_project": parent_project,
            "added": datetime.now().isoformat(),
            "status": "active",
            "health": "unknown",
            "shared_resources": [],
            "dependencies": [],
            "metrics": {
                "todo_count": 0,
                "completion_rate": 0.0,
                "last_activity": None
            }
        }
        
        hierarchy_data["projects"].append(new_project)
        hierarchy_data["last_updated"] = datetime.now().isoformat()
        
        # Add parent-child relationship if specified
        if parent_project:
            self._add_project_relationship(hierarchy_data, parent_project, project_id, "parent-child")
        
        self.file_manager.save_file(self.category, self.files["project_hierarchy"], hierarchy_data)
        
        return True
    
    def define_shared_resource(self, 
                              resource_name: str,
                              resource_type: str,
                              description: str = "",
                              projects_using: List[str] = None,
                              location: str = "") -> str:
        """
        Define a shared resource used across multiple projects.
        
        Args:
            resource_name: Name of the shared resource
            resource_type: Type of resource (code, data, tool, knowledge, etc.)
            description: Description of the resource
            projects_using: List of project IDs that use this resource
            location: Location or path to the resource
            
        Returns:
            Resource ID for tracking
        """
        hierarchy_data = self._load_hierarchy_data()
        
        resource_id = f"resource_{len(hierarchy_data['shared_resources']) + 1}"
        
        shared_resource = {
            "id": resource_id,
            "name": resource_name,
            "type": resource_type,
            "description": description,
            "projects_using": projects_using or [],
            "location": location,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "usage_count": len(projects_using) if projects_using else 0
        }
        
        hierarchy_data["shared_resources"].append(shared_resource)
        hierarchy_data["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["project_hierarchy"], hierarchy_data)
        
        return resource_id
    
    def log_cross_project_lesson(self, 
                                lesson: str,
                                projects_involved: List[str],
                                lesson_type: str = "general",
                                actionable_insights: List[str] = None) -> None:
        """
        Log a lesson learned that applies across multiple projects.
        
        Args:
            lesson: The lesson learned
            projects_involved: List of project IDs where this lesson was observed
            lesson_type: Type of lesson (technical, process, management, etc.)
            actionable_insights: Specific actionable insights from this lesson
        """
        lesson_entry = f"""
## Cross-Project Lesson - {datetime.now().strftime('%Y-%m-%d')}

**Lesson Type:** {lesson_type}

**Projects Involved:** {', '.join(projects_involved)}

**Lesson Learned:** {lesson}

**Actionable Insights:**
{self._format_actionable_insights(actionable_insights or [])}

**AI Enhancement Opportunities:**
{{ai_lesson_application_suggestions}}

{{ai_pattern_extrapolation}}

{{ai_similar_situation_identification}}

---
"""
        
        # Append to cross-project lessons
        existing_lessons = self.file_manager.load_file(self.category, self.files["cross_project_lessons"]) or ""
        updated_lessons = existing_lessons + lesson_entry
        
        self.file_manager.save_file(self.category, self.files["cross_project_lessons"], updated_lessons)
    
    def get_portfolio_health(self) -> Dict[str, Any]:
        """
        Assess overall portfolio health and identify optimization opportunities.
        
        Returns:
            Comprehensive portfolio health assessment
        """
        hierarchy_data = self._load_hierarchy_data()
        
        health = {
            "overall_health": "unknown",
            "total_projects": len(hierarchy_data.get("projects", [])),
            "active_projects": 0,
            "shared_resources": len(hierarchy_data.get("shared_resources", [])),
            "cross_project_dependencies": len(hierarchy_data.get("cross_project_dependencies", [])),
            "resource_utilization": {},
            "project_health_distribution": {},
            "optimization_opportunities": [],
            "ai_recommendations": [],
            "last_assessed": datetime.now().isoformat()
        }
        
        if not hierarchy_data.get("projects"):
            health["overall_health"] = "no_projects"
            return health
        
        # Analyze project distribution
        active_projects = [p for p in hierarchy_data["projects"] if p.get("status") == "active"]
        health["active_projects"] = len(active_projects)
        
        # Analyze project health distribution
        health_counts = {}
        for project in hierarchy_data["projects"]:
            project_health = project.get("health", "unknown")
            health_counts[project_health] = health_counts.get(project_health, 0) + 1
        health["project_health_distribution"] = health_counts
        
        # Analyze resource utilization
        for resource in hierarchy_data.get("shared_resources", []):
            resource_name = resource["name"]
            usage_count = len(resource.get("projects_using", []))
            health["resource_utilization"][resource_name] = {
                "usage_count": usage_count,
                "utilization_score": min(usage_count / max(len(active_projects), 1), 1.0)
            }
        
        # Generate optimization opportunities
        health["optimization_opportunities"] = self._identify_optimization_opportunities(hierarchy_data)
        
        # Generate AI recommendations
        health["ai_recommendations"] = [
            {
                "type": "resource_optimization",
                "template": "{ai_resource_sharing_optimization}",
                "context": f"{health['shared_resources']} shared resources across {health['total_projects']} projects"
            },
            {
                "type": "project_synergy",
                "template": "{ai_project_synergy_identification}",
                "context": f"{health['active_projects']} active projects with {health['cross_project_dependencies']} dependencies"
            }
        ]
        
        # Determine overall health
        if health["active_projects"] == 0:
            health["overall_health"] = "inactive"
        elif len(health["optimization_opportunities"]) == 0:
            health["overall_health"] = "optimal"
        elif len(health["optimization_opportunities"]) <= 2:
            health["overall_health"] = "good"
        else:
            health["overall_health"] = "needs_attention"
        
        return health
    
    def generate_portfolio_dashboard(self) -> str:
        """
        Generate HTML dashboard for portfolio overview.
        
        Returns:
            Path to the generated dashboard HTML file
        """
        hierarchy_data = self._load_hierarchy_data()
        health = self.get_portfolio_health()
        
        # Create dashboard HTML with AI enhancement placeholders
        dashboard_html = self._create_portfolio_dashboard_html(hierarchy_data, health)
        
        file_path = self.file_manager.save_file(
            self.category,
            self.files["portfolio_dashboard"],
            dashboard_html
        )
        
        return str(file_path)
    
    def get_resource_sharing_opportunities(self) -> List[Dict[str, Any]]:
        """
        Identify opportunities for increased resource sharing between projects.
        
        Returns:
            List of resource sharing opportunities with AI enhancement templates
        """
        hierarchy_data = self._load_hierarchy_data()
        opportunities = []
        
        # Analyze underutilized resources
        for resource in hierarchy_data.get("shared_resources", []):
            usage_count = len(resource.get("projects_using", []))
            total_projects = len(hierarchy_data.get("projects", []))
            
            if usage_count < total_projects / 2 and total_projects > 2:
                opportunities.append({
                    "type": "underutilized_resource",
                    "resource_name": resource["name"],
                    "current_usage": usage_count,
                    "potential_usage": total_projects,
                    "ai_template": "{ai_resource_adoption_strategy}",
                    "context": f"Resource '{resource['name']}' used by {usage_count}/{total_projects} projects"
                })
        
        # Identify potential new shared resources
        if len(hierarchy_data.get("projects", [])) > 1:
            opportunities.append({
                "type": "new_resource_identification",
                "ai_template": "{ai_shared_resource_identification}",
                "context": f"Portfolio has {len(hierarchy_data.get('projects', []))} projects that could share resources"
            })
        
        return opportunities
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """
        Get portfolio summary for status reporting.
        
        Returns:
            Summary suitable for dashboard and status reports
        """
        hierarchy_data = self._load_hierarchy_data()
        health = self.get_portfolio_health()
        
        summary = {
            "portfolio_active": len(hierarchy_data.get("projects", [])) > 0,
            "total_projects": health["total_projects"],
            "active_projects": health["active_projects"],
            "shared_resources": health["shared_resources"],
            "overall_health": health["overall_health"],
            "optimization_opportunities": len(health["optimization_opportunities"]),
            "needs_attention": health["overall_health"] in ["needs_attention", "inactive"],
            "resource_sharing_score": 0.0
        }
        
        # Calculate resource sharing score
        if hierarchy_data.get("shared_resources") and hierarchy_data.get("projects"):
            total_possible_sharing = len(hierarchy_data["projects"]) * len(hierarchy_data["shared_resources"])
            actual_sharing = sum(
                len(resource.get("projects_using", []))
                for resource in hierarchy_data["shared_resources"]
            )
            summary["resource_sharing_score"] = actual_sharing / total_possible_sharing if total_possible_sharing > 0 else 0
        
        return summary
    
    def _load_hierarchy_data(self) -> Dict[str, Any]:
        """Load portfolio hierarchy data."""
        data = self.file_manager.load_file(self.category, self.files["project_hierarchy"])
        
        if data is None:
            data = {
                "portfolio_name": f"{self.project_root.name} Portfolio",
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "projects": [],
                "relationships": [],
                "shared_resources": [],
                "cross_project_dependencies": []
            }
        
        return data
    
    def _add_project_relationship(self, hierarchy_data: Dict, parent_id: str, child_id: str, relationship_type: str) -> None:
        """Add a relationship between two projects."""
        relationship = {
            "parent_project": parent_id,
            "child_project": child_id,
            "relationship_type": relationship_type,
            "created": datetime.now().isoformat()
        }
        
        hierarchy_data["relationships"].append(relationship)
    
    def _identify_optimization_opportunities(self, hierarchy_data: Dict) -> List[Dict[str, str]]:
        """Identify portfolio optimization opportunities."""
        opportunities = []
        
        projects = hierarchy_data.get("projects", [])
        resources = hierarchy_data.get("shared_resources", [])
        
        # Check for projects without shared resources
        projects_without_resources = [
            p for p in projects 
            if not p.get("shared_resources")
        ]
        
        if len(projects_without_resources) > 0:
            opportunities.append({
                "type": "isolated_projects",
                "description": f"{len(projects_without_resources)} projects not using shared resources",
                "impact": "medium"
            })
        
        # Check for underutilized shared resources
        underutilized_resources = [
            r for r in resources
            if len(r.get("projects_using", [])) < len(projects) / 3
        ]
        
        if underutilized_resources:
            opportunities.append({
                "type": "underutilized_resources",
                "description": f"{len(underutilized_resources)} shared resources are underutilized",
                "impact": "high"
            })
        
        # Check for missing cross-project dependencies
        if len(projects) > 1 and len(hierarchy_data.get("cross_project_dependencies", [])) == 0:
            opportunities.append({
                "type": "missing_dependencies",
                "description": "No cross-project dependencies mapped",
                "impact": "low"
            })
        
        return opportunities
    
    def _format_actionable_insights(self, insights: List[str]) -> str:
        """Format actionable insights for display."""
        if not insights:
            return "{ai_actionable_insight_extraction}"
        
        formatted = "\n".join(f"- {insight}" for insight in insights)
        return formatted + "\n\n{ai_additional_actionable_insights}"
    
    def _create_portfolio_dashboard_html(self, hierarchy_data: Dict, health: Dict) -> str:
        """Create HTML dashboard for portfolio overview."""
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Dashboard - {hierarchy_data.get('portfolio_name', 'Portfolio')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .dashboard-header {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .metric-card {{ background: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3; }}
        .project-list {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .resource-list {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .ai-placeholder {{ background: #fff3cd; padding: 10px; margin: 10px 0; border: 1px dashed #ffc107; }}
        .health-excellent {{ border-left-color: #4CAF50; }}
        .health-good {{ border-left-color: #FF9800; }}
        .health-needs-attention {{ border-left-color: #f44336; }}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>Portfolio Dashboard</h1>
        <p><strong>Portfolio:</strong> {hierarchy_data.get('portfolio_name', 'Unnamed Portfolio')}</p>
        <p><strong>Overall Health:</strong> {health['overall_health']}</p>
        <p><strong>Last Updated:</strong> {health['last_assessed']}</p>
    </div>
    
    <div class="metrics-grid">
        <div class="metric-card">
            <h3>Projects</h3>
            <p><strong>Total:</strong> {health['total_projects']}</p>
            <p><strong>Active:</strong> {health['active_projects']}</p>
        </div>
        <div class="metric-card">
            <h3>Shared Resources</h3>
            <p><strong>Count:</strong> {health['shared_resources']}</p>
        </div>
        <div class="metric-card">
            <h3>Dependencies</h3>
            <p><strong>Cross-Project:</strong> {health['cross_project_dependencies']}</p>
        </div>
        <div class="metric-card">
            <h3>Optimization</h3>
            <p><strong>Opportunities:</strong> {len(health['optimization_opportunities'])}</p>
        </div>
    </div>
    
    <div class="project-list">
        <h2>Projects</h2>
        {self._generate_projects_html(hierarchy_data.get('projects', []))}
    </div>
    
    <div class="resource-list">
        <h2>Shared Resources</h2>
        {self._generate_resources_html(hierarchy_data.get('shared_resources', []))}
    </div>
    
    <h2>AI Enhancement Opportunities</h2>
    <div class="ai-placeholder">
        {{ai_portfolio_optimization_insights}}
    </div>
    
    <div class="ai-placeholder">
        {{ai_project_synergy_analysis}}
    </div>
    
    <div class="ai-placeholder">
        {{ai_resource_optimization_recommendations}}
    </div>
    
    <p><em>Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
</body>
</html>
"""
        return html_template
    
    def _generate_projects_html(self, projects: List[Dict]) -> str:
        """Generate HTML for project list display."""
        if not projects:
            return "<p>No projects in portfolio.</p>"
        
        html = ""
        for project in projects:
            health_class = f"health-{project.get('health', 'unknown').replace('_', '-')}"
            html += f"""
            <div class="metric-card {health_class}">
                <h4>{project['name']}</h4>
                <p><strong>Type:</strong> {project.get('type', 'unknown')}</p>
                <p><strong>Status:</strong> {project.get('status', 'unknown')}</p>
                <p><strong>Health:</strong> {project.get('health', 'unknown')}</p>
                <p><strong>Path:</strong> {project.get('path', 'N/A')}</p>
            </div>
            """
        
        return html
    
    def _generate_resources_html(self, resources: List[Dict]) -> str:
        """Generate HTML for shared resources display."""
        if not resources:
            return "<p>No shared resources defined.</p>"
        
        html = ""
        for resource in resources:
            usage_count = len(resource.get("projects_using", []))
            html += f"""
            <div class="metric-card">
                <h4>{resource['name']}</h4>
                <p><strong>Type:</strong> {resource.get('type', 'unknown')}</p>
                <p><strong>Usage:</strong> {usage_count} projects</p>
                <p><strong>Description:</strong> {resource.get('description', 'No description')}</p>
            </div>
            """
        
        return html