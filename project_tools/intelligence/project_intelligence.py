"""
ProjectIntelligence facade class that coordinates all intelligence components.

Provides the main interface integrating ProjectCompass, TaskChainManager, DirectionTracker,
ReflectionManager, and PortfolioManager with feature flag support and comprehensive reporting.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .file_manager import IntelligenceFileManager
from .compass import ProjectCompass
from .task_chains import TaskChainManager
from .direction import DirectionTracker
from .reflection import ReflectionManager
from .portfolio import PortfolioManager


class ProjectIntelligence:
    """
    Facade class coordinating all project intelligence components.
    
    Provides unified access to compass, task chains, direction tracking,
    reflection management, and portfolio oversight with feature flag
    support and comprehensive status reporting.
    """
    
    def __init__(self, 
                 project_root: str = ".",
                 todo_manager=None,
                 version_manager=None,
                 feature_flags: Dict[str, bool] = None):
        self.project_root = Path(project_root)
        self.todo_manager = todo_manager
        self.version_manager = version_manager
        
        # Default feature flags
        self.feature_flags = {
            "compass": True,
            "task_chains": True,
            "direction_tracking": True,
            "reflection": True,
            "portfolio": True,
            "ai_suggestions": True,
            "enhanced_reporting": True
        }
        
        if feature_flags:
            self.feature_flags.update(feature_flags)
        
        # Initialize file manager
        self.file_manager = IntelligenceFileManager(project_root)
        
        # Initialize intelligence components based on feature flags
        self.compass = ProjectCompass(project_root) if self.feature_flags["compass"] else None
        self.task_chains = TaskChainManager(project_root, todo_manager) if self.feature_flags["task_chains"] else None
        self.direction = DirectionTracker(project_root) if self.feature_flags["direction_tracking"] else None
        self.reflection = ReflectionManager(project_root) if self.feature_flags["reflection"] else None
        self.portfolio = PortfolioManager(project_root) if self.feature_flags["portfolio"] else None
    
    def initialize_intelligence(self, project_name: str = "", force: bool = False) -> Dict[str, Any]:
        """
        Initialize all enabled intelligence components.
        
        Args:
            project_name: Name of the project for template customization
            force: Whether to overwrite existing files
            
        Returns:
            Summary of initialization results for each component
        """
        self.file_manager.ensure_directory_structure()
        
        results = {
            "project_name": project_name or self.project_root.name,
            "initialized_components": [],
            "created_files": {},
            "feature_flags": self.feature_flags.copy(),
            "initialization_time": datetime.now().isoformat()
        }
        
        # Initialize compass
        if self.compass and self.feature_flags["compass"]:
            try:
                compass_files = self.compass.initialize_compass(project_name, force)
                results["created_files"]["compass"] = compass_files
                results["initialized_components"].append("compass")
            except Exception as e:
                results["errors"] = results.get("errors", {})
                results["errors"]["compass"] = str(e)
        
        # Initialize portfolio
        if self.portfolio and self.feature_flags["portfolio"]:
            try:
                portfolio_files = self.portfolio.initialize_portfolio(project_name, force)
                results["created_files"]["portfolio"] = portfolio_files
                results["initialized_components"].append("portfolio")
            except Exception as e:
                results["errors"] = results.get("errors", {})
                results["errors"]["portfolio"] = str(e)
        
        # Other components don't need explicit initialization
        if self.task_chains and self.feature_flags["task_chains"]:
            results["initialized_components"].append("task_chains")
        
        if self.direction and self.feature_flags["direction_tracking"]:
            results["initialized_components"].append("direction_tracking")
        
        if self.reflection and self.feature_flags["reflection"]:
            results["initialized_components"].append("reflection")
        
        return results
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status across all intelligence components.
        
        Returns:
            Unified status report with data from all enabled components
        """
        status = {
            "intelligence_active": len(self.feature_flags) > 0,
            "feature_flags": self.feature_flags.copy(),
            "components": {},
            "file_organization": self.file_manager.get_artifact_inventory(),
            "ai_enhancement_opportunities": [],
            "overall_recommendations": [],
            "last_updated": datetime.now().isoformat()
        }
        
        # Compass status
        if self.compass and self.feature_flags["compass"]:
            status["components"]["compass"] = self.compass.generate_compass_summary()
            # Add AI enhancement candidates
            compass_candidates = self.compass.get_ai_enhancement_candidates()
            status["ai_enhancement_opportunities"].extend(compass_candidates)
        
        # Task chains status
        if self.task_chains and self.feature_flags["task_chains"]:
            status["components"]["task_chains"] = self.task_chains.get_all_chains_summary()
        
        # Direction tracking status
        if self.direction and self.feature_flags["direction_tracking"]:
            status["components"]["direction"] = self.direction.get_direction_summary()
            # Add AI enhancement candidates
            direction_candidates = self.direction.get_ai_enhancement_candidates()
            status["ai_enhancement_opportunities"].extend(direction_candidates)
        
        # Reflection status
        if self.reflection and self.feature_flags["reflection"]:
            status["components"]["reflection"] = self.reflection.get_reflection_summary()
            # Add AI enhancement candidates
            reflection_candidates = self.reflection.get_ai_enhancement_candidates()
            status["ai_enhancement_opportunities"].extend(reflection_candidates)
        
        # Portfolio status
        if self.portfolio and self.feature_flags["portfolio"]:
            status["components"]["portfolio"] = self.portfolio.get_portfolio_summary()
        
        # Generate overall recommendations
        status["overall_recommendations"] = self._generate_overall_recommendations(status)
        
        return status
    
    def suggest_next_session_focus(self) -> Dict[str, Any]:
        """
        Suggest focus areas for the next working session based on intelligence data.
        
        Returns:
            Recommendations for session focus with AI enhancement opportunities
        """
        suggestions = {
            "primary_focus": None,
            "secondary_activities": [],
            "reflection_prompts": [],
            "ai_enhancement_tasks": [],
            "energy_considerations": None,
            "suggested_duration": "60 minutes",
            "generated_at": datetime.now().isoformat()
        }
        
        # Get data from all components
        status = self.get_comprehensive_status()
        
        # Analyze direction health
        if self.direction and status.get("components", {}).get("direction"):
            direction_data = status["components"]["direction"]
            if direction_data.get("needs_attention"):
                suggestions["primary_focus"] = "direction_clarification"
                suggestions["reflection_prompts"].append("Is the current direction still valid?")
        
        # Analyze task chains for blocked items
        if self.task_chains and status.get("components", {}).get("task_chains"):
            chains_data = status["components"]["task_chains"]
            if chains_data.get("chains_with_issues", 0) > 0:
                if not suggestions["primary_focus"]:
                    suggestions["primary_focus"] = "unblock_tasks"
                suggestions["secondary_activities"].append("Review blocked task chains")
        
        # Check reflection frequency
        if self.reflection and status.get("components", {}).get("reflection"):
            reflection_data = status["components"]["reflection"]
            if not reflection_data.get("reflection_active"):
                suggestions["secondary_activities"].append("Create reflection entry")
                suggestions["reflection_prompts"].append("What has been energizing lately?")
        
        # Add AI enhancement opportunities
        ai_candidates = status.get("ai_enhancement_opportunities", [])
        if ai_candidates:
            suggestions["ai_enhancement_tasks"] = [
                {
                    "file": candidate["file_type"],
                    "path": candidate["path"],
                    "placeholder_count": candidate.get("placeholder_count", 0)
                }
                for candidate in ai_candidates[:3]  # Limit to top 3
            ]
        
        # Default focus if nothing urgent
        if not suggestions["primary_focus"]:
            suggestions["primary_focus"] = "productive_work"
            suggestions["reflection_prompts"].append("What would make this session most valuable?")
        
        return suggestions
    
    def evaluate_project_health(self) -> Dict[str, Any]:
        """
        Evaluate overall project health across all intelligence dimensions.
        
        Returns:
            Comprehensive project health assessment
        """
        health = {
            "overall_score": 0.0,
            "health_category": "unknown",
            "dimension_scores": {},
            "strengths": [],
            "areas_for_improvement": [],
            "urgent_actions": [],
            "ai_insights": [],
            "evaluated_at": datetime.now().isoformat()
        }
        
        scores = []
        
        # Evaluate compass health
        if self.compass and self.feature_flags["compass"]:
            compass_status = self.compass.get_compass_status()
            if compass_status["initialized"]:
                compass_score = 0.8  # Base score for having compass
                health["dimension_scores"]["compass"] = compass_score
                scores.append(compass_score)
                health["strengths"].append("Project compass is active")
            else:
                health["areas_for_improvement"].append("Initialize project compass")
                health["dimension_scores"]["compass"] = 0.2
                scores.append(0.2)
        
        # Evaluate direction health
        if self.direction and self.feature_flags["direction_tracking"]:
            direction_summary = self.direction.get_direction_summary()
            if direction_summary["has_current_direction"]:
                direction_score = 0.6
                if direction_summary["direction_health"] in ["strong", "good"]:
                    direction_score = 0.9
                elif direction_summary["direction_health"] == "at_risk":
                    direction_score = 0.3
                    health["urgent_actions"].append("Address direction risks")
                
                health["dimension_scores"]["direction"] = direction_score
                scores.append(direction_score)
            else:
                health["areas_for_improvement"].append("Set current project direction")
                health["dimension_scores"]["direction"] = 0.1
                scores.append(0.1)
        
        # Evaluate reflection health
        if self.reflection and self.feature_flags["reflection"]:
            reflection_summary = self.reflection.get_reflection_summary()
            reflection_score = 0.3  # Base score
            
            if reflection_summary["reflection_active"]:
                reflection_score = 0.7
                health["strengths"].append("Active reflection practice")
            
            if reflection_summary["recent_learnings"] > 0:
                reflection_score += 0.2
                health["strengths"].append("Capturing learnings regularly")
            
            health["dimension_scores"]["reflection"] = min(reflection_score, 1.0)
            scores.append(health["dimension_scores"]["reflection"])
        
        # Evaluate portfolio health
        if self.portfolio and self.feature_flags["portfolio"]:
            portfolio_summary = self.portfolio.get_portfolio_summary()
            if portfolio_summary["portfolio_active"]:
                portfolio_score = 0.6
                if portfolio_summary["overall_health"] == "optimal":
                    portfolio_score = 0.9
                elif portfolio_summary["needs_attention"]:
                    portfolio_score = 0.4
                    health["areas_for_improvement"].append("Address portfolio optimization opportunities")
                
                health["dimension_scores"]["portfolio"] = portfolio_score
                scores.append(portfolio_score)
            else:
                health["dimension_scores"]["portfolio"] = 0.2
                scores.append(0.2)
        
        # Calculate overall score
        if scores:
            health["overall_score"] = sum(scores) / len(scores)
        
        # Determine health category
        if health["overall_score"] >= 0.8:
            health["health_category"] = "excellent"
        elif health["overall_score"] >= 0.6:
            health["health_category"] = "good"
        elif health["overall_score"] >= 0.4:
            health["health_category"] = "fair"
        else:
            health["health_category"] = "needs_attention"
        
        # Add AI insights
        if self.feature_flags["ai_suggestions"]:
            health["ai_insights"] = [
                {
                    "type": "health_optimization",
                    "template": "{ai_project_health_improvement_suggestions}",
                    "context": f"Overall health score: {health['overall_score']:.2f}"
                },
                {
                    "type": "strength_leveraging",
                    "template": "{ai_strength_amplification_strategies}",
                    "context": f"Identified strengths: {len(health['strengths'])}"
                }
            ]
        
        return health
    
    def get_ai_enhancement_summary(self) -> Dict[str, Any]:
        """
        Get summary of all AI enhancement opportunities across components.
        
        Returns:
            Consolidated AI enhancement opportunities and priorities
        """
        enhancement_summary = {
            "total_opportunities": 0,
            "opportunities_by_component": {},
            "prioritized_tasks": [],
            "estimated_enhancement_time": 0,
            "ai_readiness_score": 0.0,
            "last_analyzed": datetime.now().isoformat()
        }
        
        all_opportunities = []
        
        # Collect opportunities from all components
        for component_name, component in [
            ("compass", self.compass),
            ("direction", self.direction),
            ("reflection", self.reflection)
        ]:
            if component and self.feature_flags.get(component_name.replace("_", "")):
                try:
                    opportunities = component.get_ai_enhancement_candidates()
                    enhancement_summary["opportunities_by_component"][component_name] = len(opportunities)
                    all_opportunities.extend(opportunities)
                except AttributeError:
                    # Component doesn't have AI enhancement candidates method
                    pass
        
        enhancement_summary["total_opportunities"] = len(all_opportunities)
        
        # Prioritize opportunities
        enhancement_summary["prioritized_tasks"] = sorted(
            all_opportunities,
            key=lambda x: x.get("placeholder_count", 0),
            reverse=True
        )[:5]  # Top 5 priorities
        
        # Estimate enhancement time (rough estimate: 5 minutes per placeholder)
        total_placeholders = sum(
            opp.get("placeholder_count", 0) 
            for opp in all_opportunities
        )
        enhancement_summary["estimated_enhancement_time"] = total_placeholders * 5
        
        # Calculate AI readiness score (percentage of files ready for enhancement)
        status = self.get_comprehensive_status()
        total_files = sum(
            len(category["files"]) 
            for category in status["file_organization"]["categories"].values()
            if category["exists"]
        )
        
        if total_files > 0:
            enhancement_summary["ai_readiness_score"] = len(all_opportunities) / total_files
        
        return enhancement_summary
    
    def _generate_overall_recommendations(self, status: Dict) -> List[str]:
        """Generate overall recommendations based on comprehensive status."""
        recommendations = []
        
        # Check if intelligence is being used
        active_components = len([
            comp for comp in status["components"].values()
            if isinstance(comp, dict) and comp.get("active", True)
        ])
        
        if active_components == 0:
            recommendations.append("Initialize intelligence components to get started")
        
        # Check AI enhancement opportunities
        ai_opportunities = len(status.get("ai_enhancement_opportunities", []))
        if ai_opportunities > 0:
            recommendations.append(f"Consider AI enhancement for {ai_opportunities} template files")
        
        # Component-specific recommendations
        if status.get("components", {}).get("direction", {}).get("needs_attention"):
            recommendations.append("Review and update project direction")
        
        if status.get("components", {}).get("reflection", {}).get("reflection_active") is False:
            recommendations.append("Start regular reflection practice")
        
        return recommendations