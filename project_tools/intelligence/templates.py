"""
Template generation system for AI-assisted project management.

Creates structured markdown and JSON templates with clearly marked sections
for AI enhancement, supporting the organized project_management/ directory structure.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class TemplateGenerator:
    """Base class for generating structured templates with AI placeholders."""
    
    def __init__(self):
        self.placeholder_pattern = re.compile(r'\{ai_[^}]+\}')
    
    def create_template_with_placeholders(self, template_type: str, **kwargs) -> str:
        """Create a template with AI enhancement placeholders."""
        if template_type == "project_intent":
            return self._create_project_intent_template(**kwargs)
        elif template_type == "success_criteria":
            return self._create_success_criteria_template(**kwargs)
        elif template_type == "learning_objectives":
            return self._create_learning_objectives_template(**kwargs)
        elif template_type == "task_chain":
            return self._create_task_chain_template(**kwargs)
        elif template_type == "direction_analysis":
            return self._create_direction_analysis_template(**kwargs)
        elif template_type == "reflection_journal":
            return self._create_reflection_journal_template(**kwargs)
        elif template_type == "portfolio_overview":
            return self._create_portfolio_overview_template(**kwargs)
        else:
            raise ValueError(f"Unknown template type: {template_type}")
    
    def parse_placeholders(self, content: str) -> List[str]:
        """Extract all AI placeholders from template content."""
        return self.placeholder_pattern.findall(content)
    
    def validate_enhanced_content(self, original: str, enhanced: str) -> bool:
        """Validate that enhanced content maintains structure and fills placeholders."""
        original_placeholders = set(self.parse_placeholders(original))
        enhanced_placeholders = set(self.parse_placeholders(enhanced))
        
        # Enhanced content should have fewer or no placeholders
        return len(enhanced_placeholders) <= len(original_placeholders)
    
    def _create_project_intent_template(self, project_name: str = "", **kwargs) -> str:
        """Create project intent template with AI enhancement placeholders."""
        return f"""# Project Intent: {project_name}

## Overview
{"{ai_project_overview_analysis}"}

## Primary Goals
{"{ai_suggested_primary_goals}"}

## Success Indicators
{"{ai_success_metrics_suggestions}"}

## Context & Background
{"{ai_context_analysis}"}

## Key Assumptions
{"{ai_assumption_validation}"}

## Potential Challenges
{"{ai_challenge_identification}"}

## Resource Requirements
{"{ai_resource_estimation}"}

---
*Template generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Ready for AI enhancement*
"""
    
    def _create_success_criteria_template(self, **kwargs) -> str:
        """Create success criteria JSON template."""
        template_data = {
            "criteria": [
                {
                    "id": "criterion_1",
                    "description": "{ai_success_criterion_1}",
                    "measurable": True,
                    "target_value": "{ai_target_value_1}",
                    "current_status": "not_started"
                }
            ],
            "evaluation_method": "{ai_evaluation_method}",
            "review_frequency": "{ai_review_frequency}",
            "stakeholders": ["{ai_stakeholder_identification}"],
            "last_updated": datetime.now().isoformat(),
            "ai_enhanced": False
        }
        return json.dumps(template_data, indent=2)
    
    def _create_learning_objectives_template(self, **kwargs) -> str:
        """Create learning objectives template."""
        return f"""# Learning Objectives

## Core Learning Goals
{"{ai_core_learning_identification}"}

## Skill Development Areas
{"{ai_skill_gap_analysis}"}

## Knowledge Acquisition Targets
{"{ai_knowledge_targets}"}

## Learning Resources
{"{ai_resource_recommendations}"}

## Progress Tracking
{"{ai_progress_tracking_suggestions}"}

## Reflection Questions
{"{ai_reflection_prompts}"}

---
*Generated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    def _create_task_chain_template(self, chain_name: str = "", **kwargs) -> str:
        """Create task chain visualization template."""
        return f"""# Task Chain: {chain_name}

## Chain Overview
{"{ai_chain_analysis}"}

## Task Sequence
{"{ai_task_sequencing_suggestions}"}

## Dependencies Analysis
{"{ai_dependency_optimization}"}

## Milestone Identification
{"{ai_milestone_recommendations}"}

## Risk Assessment
{"{ai_risk_identification}"}

## Parallel Opportunities
{"{ai_parallelization_suggestions}"}

## Next Actions
{"{ai_next_action_recommendations}"}

---
*Chain Template Generated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    def _create_direction_analysis_template(self, **kwargs) -> str:
        """Create direction analysis template."""
        return f"""# Project Direction Analysis

## Current Direction
{"{ai_current_direction_assessment}"}

## Direction Validation
{"{ai_direction_validation}"}

## Alternative Paths
{"{ai_alternative_path_analysis}"}

## Pivot Indicators
{"{ai_pivot_signal_identification}"}

## Resource Alignment
{"{ai_resource_alignment_check}"}

## Success Probability
{"{ai_success_probability_assessment}"}

## Recommended Actions
{"{ai_direction_action_recommendations}"}

---
*Analysis Generated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    def _create_reflection_journal_template(self, **kwargs) -> str:
        """Create reflection journal template."""
        return f"""# Reflection Journal Entry - {datetime.now().strftime('%Y-%m-%d')}

## Recent Progress
{"{ai_progress_analysis}"}

## Key Learnings
{"{ai_learning_extraction}"}

## Energy & Motivation
{"{ai_energy_assessment}"}

## Challenges Encountered
{"{ai_challenge_analysis}"}

## Pattern Recognition
{"{ai_pattern_identification}"}

## Course Corrections
{"{ai_course_correction_suggestions}"}

## Next Session Focus
{"{ai_next_session_recommendations}"}

## Gratitude & Wins
{"{ai_positive_reinforcement}"}

---
*Reflection Template: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    def _create_portfolio_overview_template(self, **kwargs) -> str:
        """Create portfolio overview template."""
        return f"""# Portfolio Overview

## Project Landscape
{"{ai_portfolio_landscape_analysis}"}

## Resource Distribution
{"{ai_resource_distribution_analysis}"}

## Cross-Project Synergies
{"{ai_synergy_identification}"}

## Portfolio Health
{"{ai_portfolio_health_assessment}"}

## Priority Recommendations
{"{ai_priority_recommendations}"}

## Resource Optimization
{"{ai_resource_optimization_suggestions}"}

## Strategic Alignment
{"{ai_strategic_alignment_check}"}

---
*Portfolio Analysis: {datetime.now().strftime('%Y-%m-%d')}*
"""


class AIPlaceholder:
    """Represents an AI enhancement placeholder with metadata."""
    
    def __init__(self, name: str, description: str, content_type: str = "text"):
        self.name = name
        self.description = description
        self.content_type = content_type
        self.filled = False
        self.content = ""
    
    def fill(self, content: str) -> None:
        """Fill the placeholder with AI-generated content."""
        self.content = content
        self.filled = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert placeholder to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "content_type": self.content_type,
            "filled": self.filled,
            "content": self.content
        }


class TemplateValidator:
    """Validates template structure and AI enhancements."""
    
    @staticmethod
    def validate_template_structure(content: str, template_type: str) -> bool:
        """Validate that template has required structure."""
        required_sections = {
            "project_intent": ["Overview", "Primary Goals", "Success Indicators"],
            "task_chain": ["Chain Overview", "Task Sequence", "Dependencies Analysis"],
            "direction_analysis": ["Current Direction", "Direction Validation"],
            "reflection_journal": ["Recent Progress", "Key Learnings", "Energy & Motivation"],
            "portfolio_overview": ["Project Landscape", "Resource Distribution"]
        }
        
        if template_type not in required_sections:
            return True  # Unknown template types are considered valid
        
        for section in required_sections[template_type]:
            if f"## {section}" not in content:
                return False
        
        return True
    
    @staticmethod
    def validate_ai_enhancement(original: str, enhanced: str) -> Dict[str, Any]:
        """Validate AI enhancement quality and completeness."""
        generator = TemplateGenerator()
        
        original_placeholders = generator.parse_placeholders(original)
        enhanced_placeholders = generator.parse_placeholders(enhanced)
        
        filled_placeholders = len(original_placeholders) - len(enhanced_placeholders)
        
        return {
            "valid": len(enhanced_placeholders) <= len(original_placeholders),
            "original_placeholder_count": len(original_placeholders),
            "remaining_placeholder_count": len(enhanced_placeholders),
            "filled_placeholder_count": filled_placeholders,
            "completion_percentage": (filled_placeholders / len(original_placeholders)) * 100 if original_placeholders else 100
        }