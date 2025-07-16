"""
TaskChainManager class for creating logical task progressions and managing task dependencies.

Builds on the existing todo dependency system to create structured task chains with
milestone tracking, chain health monitoring, and AI-assisted optimization.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path

from .file_manager import IntelligenceFileManager
from .templates import TemplateGenerator


class TaskChainManager:
    """
    Manages logical task progressions and chain-based workflow optimization.
    
    Creates task chains that build on existing todo dependencies while adding
    higher-level workflow structure, milestone tracking, and AI-assisted optimization.
    """
    
    def __init__(self, project_root: str = ".", todo_manager=None):
        self.project_root = Path(project_root)
        self.file_manager = IntelligenceFileManager(project_root)
        self.template_generator = TemplateGenerator()
        self.category = "chains"
        self.todo_manager = todo_manager
        
        # Standard chain files
        self.files = {
            "task_chains": "task_chains.json",
            "chain_visualization": "chain_visualization.html",
            "milestone_decisions": "milestone_decisions.md",
            "chain_health_report": "chain_health_report.html"
        }
    
    def create_task_chain(self, 
                         chain_name: str, 
                         description: str = "",
                         chain_type: str = "sequential",
                         milestone_criteria: List[str] = None) -> str:
        """
        Create a new task chain definition.
        
        Args:
            chain_name: Unique name for the task chain
            description: Description of the chain's purpose
            chain_type: Type of chain (sequential, parallel, milestone-based)
            milestone_criteria: List of criteria for identifying milestones
            
        Returns:
            Chain ID for the created chain
        """
        self.file_manager.ensure_directory_structure()
        
        chains_data = self._load_chains_data()
        
        chain_id = f"chain_{len(chains_data['chains']) + 1}"
        
        new_chain = {
            "id": chain_id,
            "name": chain_name,
            "description": description,
            "type": chain_type,
            "created": datetime.now().isoformat(),
            "status": "active",
            "milestones": [],
            "milestone_criteria": milestone_criteria or [],
            "todo_sequence": [],
            "dependencies": [],
            "health_metrics": {
                "completion_rate": 0.0,
                "blocked_tasks": 0,
                "average_task_age": 0,
                "milestone_progress": 0.0
            },
            "ai_suggestions": {
                "optimization_opportunities": [],
                "risk_factors": [],
                "next_actions": []
            }
        }
        
        chains_data["chains"].append(new_chain)
        chains_data["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["task_chains"], chains_data)
        
        return chain_id
    
    def add_todos_to_chain(self, chain_id: str, todo_ids: List[Union[str, int]], 
                          sequence_order: Optional[List[int]] = None) -> bool:
        """
        Add todos to a task chain in specified order.
        
        Args:
            chain_id: ID of the target chain
            todo_ids: List of todo IDs to add to the chain
            sequence_order: Optional specific ordering (otherwise uses provided order)
            
        Returns:
            True if todos were successfully added
        """
        chains_data = self._load_chains_data()
        
        chain = self._find_chain_by_id(chains_data, chain_id)
        if not chain:
            return False
        
        # Convert todo_ids to strings for consistency
        todo_ids = [str(tid) for tid in todo_ids]
        
        if sequence_order:
            # Use custom ordering
            ordered_todos = [todo_ids[i] for i in sequence_order if i < len(todo_ids)]
        else:
            # Use provided order
            ordered_todos = todo_ids
        
        # Add todos to chain sequence
        for todo_id in ordered_todos:
            if todo_id not in chain["todo_sequence"]:
                chain["todo_sequence"].append(todo_id)
        
        # Update chain metadata
        chain["last_updated"] = datetime.now().isoformat()
        
        # Save updated chains data
        self.file_manager.save_file(self.category, self.files["task_chains"], chains_data)
        
        # Update chain health metrics
        self._update_chain_health(chain_id)
        
        return True
    
    def define_milestone(self, chain_id: str, name: str, criteria: str, 
                        todo_dependencies: List[str] = None) -> bool:
        """
        Define a milestone within a task chain.
        
        Args:
            chain_id: ID of the target chain
            name: Name of the milestone
            criteria: Criteria for milestone completion
            todo_dependencies: List of todo IDs that must be completed for this milestone
            
        Returns:
            True if milestone was successfully created
        """
        chains_data = self._load_chains_data()
        
        chain = self._find_chain_by_id(chains_data, chain_id)
        if not chain:
            return False
        
        milestone = {
            "id": f"milestone_{len(chain['milestones']) + 1}",
            "name": name,
            "criteria": criteria,
            "todo_dependencies": todo_dependencies or [],
            "status": "pending",
            "created": datetime.now().isoformat(),
            "completed": None
        }
        
        chain["milestones"].append(milestone)
        chain["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["task_chains"], chains_data)
        
        return True
    
    def get_chain_health(self, chain_id: str) -> Dict[str, Any]:
        """
        Get comprehensive health metrics for a task chain.
        
        Args:
            chain_id: ID of the chain to analyze
            
        Returns:
            Dictionary with health metrics and recommendations
        """
        chains_data = self._load_chains_data()
        chain = self._find_chain_by_id(chains_data, chain_id)
        
        if not chain:
            return {"error": "Chain not found"}
        
        health = {
            "chain_id": chain_id,
            "chain_name": chain["name"],
            "overall_health": "unknown",
            "metrics": chain.get("health_metrics", {}),
            "issues": [],
            "recommendations": [],
            "ai_suggestions": chain.get("ai_suggestions", {}),
            "last_updated": datetime.now().isoformat()
        }
        
        # Calculate health metrics if we have todo manager integration
        if self.todo_manager:
            health.update(self._calculate_chain_health_with_todos(chain))
        
        # Determine overall health status
        completion_rate = health["metrics"].get("completion_rate", 0)
        blocked_tasks = health["metrics"].get("blocked_tasks", 0)
        
        if completion_rate > 0.8 and blocked_tasks == 0:
            health["overall_health"] = "excellent"
        elif completion_rate > 0.6 and blocked_tasks <= 1:
            health["overall_health"] = "good"
        elif completion_rate > 0.4:
            health["overall_health"] = "fair"
        else:
            health["overall_health"] = "poor"
        
        return health
    
    def generate_chain_visualization(self, chain_id: str) -> str:
        """
        Generate HTML visualization of task chain structure and progress.
        
        Args:
            chain_id: ID of the chain to visualize
            
        Returns:
            Path to the generated HTML file
        """
        chains_data = self._load_chains_data()
        chain = self._find_chain_by_id(chains_data, chain_id)
        
        if not chain:
            return ""
        
        # Generate visualization template with AI enhancement placeholders
        viz_content = self.template_generator.create_template_with_placeholders(
            "task_chain", chain_name=chain["name"]
        )
        
        # Create more detailed HTML structure
        html_content = self._create_chain_visualization_html(chain)
        
        # Save visualization
        file_path = self.file_manager.save_file(
            self.category, 
            f"chain_{chain_id}_visualization.html",
            html_content
        )
        
        return str(file_path)
    
    def get_all_chains_summary(self) -> Dict[str, Any]:
        """
        Get summary information for all task chains.
        
        Returns:
            Summary data for reporting and dashboard display
        """
        chains_data = self._load_chains_data()
        
        summary = {
            "total_chains": len(chains_data["chains"]),
            "active_chains": 0,
            "completed_chains": 0,
            "chains_with_issues": 0,
            "total_todos_in_chains": 0,
            "chains": []
        }
        
        for chain in chains_data["chains"]:
            chain_summary = {
                "id": chain["id"],
                "name": chain["name"],
                "status": chain["status"],
                "todo_count": len(chain["todo_sequence"]),
                "milestone_count": len(chain["milestones"]),
                "completion_rate": chain.get("health_metrics", {}).get("completion_rate", 0),
                "health": "unknown"
            }
            
            # Update counters
            if chain["status"] == "active":
                summary["active_chains"] += 1
            elif chain["status"] == "completed":
                summary["completed_chains"] += 1
            
            summary["total_todos_in_chains"] += len(chain["todo_sequence"])
            
            # Get health status
            health = self.get_chain_health(chain["id"])
            chain_summary["health"] = health.get("overall_health", "unknown")
            
            if health.get("overall_health") in ["poor", "fair"]:
                summary["chains_with_issues"] += 1
            
            summary["chains"].append(chain_summary)
        
        return summary
    
    def suggest_chain_optimizations(self, chain_id: str) -> List[Dict[str, str]]:
        """
        Generate AI-assisted suggestions for chain optimization.
        
        Args:
            chain_id: ID of the chain to analyze
            
        Returns:
            List of optimization suggestions with AI placeholders
        """
        suggestions = []
        
        health = self.get_chain_health(chain_id)
        
        # Template-based suggestions with AI enhancement placeholders
        if health["metrics"].get("blocked_tasks", 0) > 0:
            suggestions.append({
                "type": "blocked_tasks",
                "priority": "high",
                "template": "{ai_blocked_task_resolution_suggestions}",
                "context": f"Chain has {health['metrics']['blocked_tasks']} blocked tasks"
            })
        
        if health["metrics"].get("completion_rate", 0) < 0.5:
            suggestions.append({
                "type": "low_progress",
                "priority": "medium",
                "template": "{ai_progress_acceleration_suggestions}",
                "context": f"Completion rate is {health['metrics']['completion_rate']:.1%}"
            })
        
        milestone_progress = health["metrics"].get("milestone_progress", 0)
        if milestone_progress < 0.3:
            suggestions.append({
                "type": "milestone_focus",
                "priority": "medium",
                "template": "{ai_milestone_achievement_strategies}",
                "context": f"Milestone progress is {milestone_progress:.1%}"
            })
        
        return suggestions
    
    def _load_chains_data(self) -> Dict[str, Any]:
        """Load task chains data from file or create empty structure."""
        data = self.file_manager.load_file(self.category, self.files["task_chains"])
        
        if data is None:
            data = {
                "chains": [],
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            }
        
        return data
    
    def _find_chain_by_id(self, chains_data: Dict, chain_id: str) -> Optional[Dict]:
        """Find a chain by its ID."""
        for chain in chains_data["chains"]:
            if chain["id"] == chain_id:
                return chain
        return None
    
    def _update_chain_health(self, chain_id: str) -> None:
        """Update health metrics for a specific chain."""
        if not self.todo_manager:
            return
        
        chains_data = self._load_chains_data()
        chain = self._find_chain_by_id(chains_data, chain_id)
        
        if not chain:
            return
        
        # Calculate health metrics
        health_metrics = self._calculate_chain_health_with_todos(chain)
        chain["health_metrics"].update(health_metrics["metrics"])
        
        # Save updated data
        self.file_manager.save_file(self.category, self.files["task_chains"], chains_data)
    
    def _calculate_chain_health_with_todos(self, chain: Dict) -> Dict[str, Any]:
        """Calculate detailed health metrics using todo manager data."""
        if not self.todo_manager:
            return {"metrics": {}}
        
        todo_ids = chain["todo_sequence"]
        total_todos = len(todo_ids)
        
        if total_todos == 0:
            return {
                "metrics": {
                    "completion_rate": 0.0,
                    "blocked_tasks": 0,
                    "average_task_age": 0,
                    "milestone_progress": 0.0
                }
            }
        
        completed_todos = 0
        blocked_todos = 0
        
        # Analyze each todo in the chain
        for todo_id in todo_ids:
            try:
                todo = self.todo_manager.get_todo(todo_id)
                if todo:
                    if todo.get("status") == "completed":
                        completed_todos += 1
                    elif todo.get("blocked", False):
                        blocked_todos += 1
            except:
                # Todo not found or error accessing it
                continue
        
        completion_rate = completed_todos / total_todos if total_todos > 0 else 0
        
        # Calculate milestone progress
        completed_milestones = sum(
            1 for m in chain["milestones"] 
            if m["status"] == "completed"
        )
        total_milestones = len(chain["milestones"])
        milestone_progress = (
            completed_milestones / total_milestones 
            if total_milestones > 0 else 0
        )
        
        return {
            "metrics": {
                "completion_rate": completion_rate,
                "blocked_tasks": blocked_todos,
                "average_task_age": 0,  # Would need creation dates from todos
                "milestone_progress": milestone_progress
            }
        }
    
    def _create_chain_visualization_html(self, chain: Dict) -> str:
        """Create detailed HTML visualization for a task chain."""
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Task Chain: {chain['name']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .chain-header {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .milestone {{ background: #e8f4f8; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }}
        .todo-item {{ background: #f9f9f9; padding: 8px; margin: 5px 0; border-left: 3px solid #ccc; }}
        .completed {{ background: #e8f5e8; border-left-color: #4CAF50; }}
        .blocked {{ background: #ffe8e8; border-left-color: #f44336; }}
        .ai-placeholder {{ background: #fff3cd; padding: 10px; margin: 10px 0; border: 1px dashed #ffc107; }}
    </style>
</head>
<body>
    <div class="chain-header">
        <h1>Task Chain: {chain['name']}</h1>
        <p><strong>Description:</strong> {chain['description']}</p>
        <p><strong>Type:</strong> {chain['type']}</p>
        <p><strong>Created:</strong> {chain['created']}</p>
        <p><strong>Status:</strong> {chain['status']}</p>
    </div>
    
    <h2>Milestones</h2>
    {self._generate_milestones_html(chain['milestones'])}
    
    <h2>Task Sequence</h2>
    {self._generate_todos_html(chain['todo_sequence'])}
    
    <h2>AI Enhancement Opportunities</h2>
    <div class="ai-placeholder">
        {{ai_chain_optimization_insights}}
    </div>
    
    <div class="ai-placeholder">
        {{ai_bottleneck_identification}}
    </div>
    
    <div class="ai-placeholder">
        {{ai_parallel_execution_opportunities}}
    </div>
    
    <p><em>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
</body>
</html>
"""
        return html_template
    
    def _generate_milestones_html(self, milestones: List[Dict]) -> str:
        """Generate HTML for milestone display."""
        if not milestones:
            return "<p>No milestones defined for this chain.</p>"
        
        html = ""
        for milestone in milestones:
            status_class = "completed" if milestone["status"] == "completed" else ""
            html += f"""
            <div class="milestone {status_class}">
                <h3>{milestone['name']}</h3>
                <p><strong>Criteria:</strong> {milestone['criteria']}</p>
                <p><strong>Status:</strong> {milestone['status']}</p>
                <p><strong>Dependencies:</strong> {', '.join(milestone.get('todo_dependencies', []))}</p>
            </div>
            """
        
        return html
    
    def _generate_todos_html(self, todo_sequence: List[str]) -> str:
        """Generate HTML for todo sequence display."""
        if not todo_sequence:
            return "<p>No todos in this chain sequence.</p>"
        
        html = ""
        for todo_id in todo_sequence:
            # Default display if no todo manager integration
            html += f"""
            <div class="todo-item">
                <strong>Todo ID:</strong> {todo_id}
            </div>
            """
        
        return html