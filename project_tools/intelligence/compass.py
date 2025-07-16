"""
ProjectCompass class for managing project intent, success criteria, learning goals, and context tracking.

Provides structured templates and file management for AI-assisted project direction and purpose.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .file_manager import IntelligenceFileManager
from .templates import TemplateGenerator


class ProjectCompass:
    """
    Manages project intent, success criteria, learning goals, and context tracking.
    
    Creates and maintains structured templates in the project_management/compass/
    directory that external AI tools can enhance with intelligent insights.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.file_manager = IntelligenceFileManager(project_root)
        self.template_generator = TemplateGenerator()
        self.category = "compass"
        
        # Standard compass files
        self.files = {
            "project_intent": "project_intent.md",
            "success_criteria": "success_criteria.json", 
            "context_log": "context_log.json",
            "learning_objectives": "learning_objectives.md"
        }
    
    def initialize_compass(self, project_name: str = "", force: bool = False) -> Dict[str, str]:
        """
        Initialize compass with template files for AI enhancement.
        
        Args:
            project_name: Name of the project for template customization
            force: Whether to overwrite existing files
            
        Returns:
            Dictionary mapping file types to created file paths
        """
        self.file_manager.ensure_directory_structure()
        
        if not project_name:
            project_name = self.project_root.name
        
        created_files = {}
        
        # Create project intent template
        if force or not self.file_manager.file_exists(self.category, self.files["project_intent"]):
            intent_content = self.template_generator.create_template_with_placeholders(
                "project_intent", project_name=project_name
            )
            path = self.file_manager.save_file(self.category, self.files["project_intent"], intent_content)
            created_files["project_intent"] = str(path)
        
        # Create success criteria template
        if force or not self.file_manager.file_exists(self.category, self.files["success_criteria"]):
            criteria_content = self.template_generator.create_template_with_placeholders(
                "success_criteria"
            )
            path = self.file_manager.save_file(self.category, self.files["success_criteria"], criteria_content)
            created_files["success_criteria"] = str(path)
        
        # Create learning objectives template
        if force or not self.file_manager.file_exists(self.category, self.files["learning_objectives"]):
            learning_content = self.template_generator.create_template_with_placeholders(
                "learning_objectives"
            )
            path = self.file_manager.save_file(self.category, self.files["learning_objectives"], learning_content)
            created_files["learning_objectives"] = str(path)
        
        # Initialize context log
        if force or not self.file_manager.file_exists(self.category, self.files["context_log"]):
            context_data = {
                "project_name": project_name,
                "created": datetime.now().isoformat(),
                "context_entries": [],
                "key_assumptions": [],
                "major_decisions": [],
                "learning_milestones": []
            }
            path = self.file_manager.save_file(self.category, self.files["context_log"], context_data)
            created_files["context_log"] = str(path)
        
        return created_files
    
    def get_project_intent(self) -> Optional[str]:
        """Get the current project intent content."""
        return self.file_manager.load_file(self.category, self.files["project_intent"])
    
    def get_success_criteria(self) -> Optional[Dict[str, Any]]:
        """Get the current success criteria data."""
        return self.file_manager.load_file(self.category, self.files["success_criteria"])
    
    def get_learning_objectives(self) -> Optional[str]:
        """Get the current learning objectives content."""
        return self.file_manager.load_file(self.category, self.files["learning_objectives"])
    
    def get_context_log(self) -> Optional[Dict[str, Any]]:
        """Get the complete context log data."""
        return self.file_manager.load_file(self.category, self.files["context_log"])
    
    def add_context_entry(self, entry_type: str, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Add a new context entry to the log.
        
        Args:
            entry_type: Type of entry (decision, assumption, learning, milestone, etc.)
            content: The context content
            metadata: Additional metadata for the entry
        """
        context_log = self.get_context_log() or {
            "project_name": self.project_root.name,
            "created": datetime.now().isoformat(),
            "context_entries": [],
            "key_assumptions": [],
            "major_decisions": [],
            "learning_milestones": []
        }
        
        entry = {
            "id": len(context_log["context_entries"]) + 1,
            "type": entry_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        context_log["context_entries"].append(entry)
        
        # Also add to specific lists based on type
        if entry_type == "assumption":
            context_log["key_assumptions"].append(entry)
        elif entry_type == "decision":
            context_log["major_decisions"].append(entry)
        elif entry_type == "learning":
            context_log["learning_milestones"].append(entry)
        
        self.file_manager.save_file(self.category, self.files["context_log"], context_log)
    
    def update_success_criteria(self, criteria_updates: Dict[str, Any]) -> None:
        """
        Update success criteria with new data.
        
        Args:
            criteria_updates: Dictionary with updates to merge into success criteria
        """
        current_criteria = self.get_success_criteria() or {}
        current_criteria.update(criteria_updates)
        current_criteria["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["success_criteria"], current_criteria)
    
    def get_compass_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of all compass components.
        
        Returns:
            Dictionary with status information for all compass files
        """
        status = {
            "initialized": True,
            "last_checked": datetime.now().isoformat(),
            "files": {}
        }
        
        for file_type, filename in self.files.items():
            exists = self.file_manager.file_exists(self.category, filename)
            status["files"][file_type] = {
                "exists": exists,
                "filename": filename,
                "path": str(self.file_manager.get_file_path(self.category, filename)) if exists else None
            }
            
            if exists and file_type == "context_log":
                context_data = self.get_context_log()
                if context_data:
                    status["files"][file_type]["entry_count"] = len(context_data.get("context_entries", []))
                    status["files"][file_type]["last_entry"] = (
                        context_data["context_entries"][-1]["timestamp"] 
                        if context_data.get("context_entries") else None
                    )
        
        # Check if compass is fully initialized
        status["initialized"] = all(
            status["files"][file_type]["exists"] 
            for file_type in self.files.keys()
        )
        
        return status
    
    def generate_compass_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of current compass state for reporting.
        
        Returns:
            Summary dictionary suitable for status reports
        """
        summary = {
            "compass_active": False,
            "project_intent_defined": False,
            "success_criteria_count": 0,
            "learning_objectives_defined": False,
            "context_entries": 0,
            "key_assumptions": 0,
            "major_decisions": 0,
            "last_activity": None
        }
        
        status = self.get_compass_status()
        summary["compass_active"] = status["initialized"]
        
        if status["files"]["project_intent"]["exists"]:
            intent = self.get_project_intent()
            summary["project_intent_defined"] = intent is not None and len(intent.strip()) > 0
        
        if status["files"]["success_criteria"]["exists"]:
            criteria = self.get_success_criteria()
            if criteria and "criteria" in criteria:
                summary["success_criteria_count"] = len(criteria["criteria"])
        
        if status["files"]["learning_objectives"]["exists"]:
            objectives = self.get_learning_objectives()
            summary["learning_objectives_defined"] = objectives is not None and len(objectives.strip()) > 0
        
        if status["files"]["context_log"]["exists"]:
            context = self.get_context_log()
            if context:
                summary["context_entries"] = len(context.get("context_entries", []))
                summary["key_assumptions"] = len(context.get("key_assumptions", []))
                summary["major_decisions"] = len(context.get("major_decisions", []))
                
                if context.get("context_entries"):
                    summary["last_activity"] = context["context_entries"][-1]["timestamp"]
        
        return summary
    
    def get_ai_enhancement_candidates(self) -> List[Dict[str, str]]:
        """
        Identify compass files that could benefit from AI enhancement.
        
        Returns:
            List of files with their paths and enhancement suggestions
        """
        candidates = []
        
        for file_type, filename in self.files.items():
            if self.file_manager.file_exists(self.category, filename):
                file_path = self.file_manager.get_file_path(self.category, filename)
                
                if filename.endswith('.md'):
                    content = self.file_manager.load_file(self.category, filename)
                    if content and '{ai_' in content:
                        placeholders = self.template_generator.parse_placeholders(content)
                        candidates.append({
                            "file_type": file_type,
                            "path": str(file_path),
                            "enhancement_type": "template_completion",
                            "placeholder_count": len(placeholders),
                            "placeholders": placeholders
                        })
        
        return candidates
    
    def validate_compass_integrity(self) -> Dict[str, Any]:
        """
        Validate the integrity and completeness of compass data.
        
        Returns:
            Validation results with any issues found
        """
        validation = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "recommendations": []
        }
        
        status = self.get_compass_status()
        
        # Check file existence
        for file_type, file_info in status["files"].items():
            if not file_info["exists"]:
                validation["issues"].append(f"Missing {file_type} file: {file_info['filename']}")
                validation["valid"] = False
        
        # Check content quality
        if status["files"]["context_log"]["exists"]:
            context = self.get_context_log()
            if context and len(context.get("context_entries", [])) == 0:
                validation["warnings"].append("Context log exists but has no entries")
                validation["recommendations"].append("Add context entries as the project progresses")
        
        # Check for AI enhancement opportunities
        candidates = self.get_ai_enhancement_candidates()
        if candidates:
            validation["recommendations"].append(
                f"Found {len(candidates)} files that could benefit from AI enhancement"
            )
        
        return validation