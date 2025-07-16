"""
ReflectionManager class for personal accountability and regular self-assessment.

Provides reflection prompts, learning capture, energy tracking, and course correction
suggestions within the organized project_management/ structure.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .file_manager import IntelligenceFileManager
from .templates import TemplateGenerator


class ReflectionManager:
    """
    Manages personal accountability through structured reflection and self-assessment.
    
    Provides tools for regular reflection, learning capture, energy tracking,
    and course correction identification with AI-assisted prompts and analysis.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.file_manager = IntelligenceFileManager(project_root)
        self.template_generator = TemplateGenerator()
        self.category = "reflection"
        
        # Standard reflection files
        self.files = {
            "reflection_journal": "reflection_journal.md",
            "energy_tracking": "energy_tracking.json",
            "learning_log": "learning_log.json",
            "course_corrections": "course_corrections.md"
        }
    
    def create_reflection_entry(self, 
                               reflection_type: str = "weekly",
                               custom_prompts: List[str] = None) -> str:
        """
        Create a new reflection entry with AI-enhanced prompts.
        
        Args:
            reflection_type: Type of reflection (daily, weekly, monthly, project)
            custom_prompts: Additional custom reflection prompts
            
        Returns:
            Path to the created reflection entry
        """
        self.file_manager.ensure_directory_structure()
        
        # Generate reflection template with AI enhancement placeholders
        reflection_content = self.template_generator.create_template_with_placeholders(
            "reflection_journal"
        )
        
        # Add reflection type-specific prompts
        type_specific_prompts = self._get_type_specific_prompts(reflection_type)
        
        # Create comprehensive reflection entry
        entry_content = f"""# {reflection_type.title()} Reflection - {datetime.now().strftime('%Y-%m-%d')}

## Reflection Type: {reflection_type}

{reflection_content}

## Type-Specific Prompts

{type_specific_prompts}

## Custom Prompts
{self._format_custom_prompts(custom_prompts or [])}

## AI Enhancement Opportunities
{{ai_personalized_reflection_prompts}}

{{ai_pattern_recognition_insights}}

{{ai_next_session_recommendations}}

---
*Reflection created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Save to journal (append to existing)
        existing_journal = self.file_manager.load_file(self.category, self.files["reflection_journal"]) or ""
        updated_journal = existing_journal + "\n\n" + entry_content
        
        file_path = self.file_manager.save_file(self.category, self.files["reflection_journal"], updated_journal)
        
        return str(file_path)
    
    def log_energy_level(self, 
                        energy_level: int,
                        context: str = "",
                        factors: List[str] = None,
                        session_type: str = "work") -> None:
        """
        Log current energy level with context for tracking patterns.
        
        Args:
            energy_level: Energy level from 1-10
            context: Context for this energy reading
            factors: Factors affecting energy level
            session_type: Type of session (work, reflection, break, etc.)
        """
        if not (1 <= energy_level <= 10):
            raise ValueError("Energy level must be between 1 and 10")
        
        energy_data = self._load_energy_data()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "energy_level": energy_level,
            "context": context,
            "factors": factors or [],
            "session_type": session_type,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "hour": datetime.now().hour
        }
        
        energy_data["entries"].append(entry)
        energy_data["last_updated"] = datetime.now().isoformat()
        
        # Update daily summary
        self._update_daily_energy_summary(energy_data, entry)
        
        self.file_manager.save_file(self.category, self.files["energy_tracking"], energy_data)
    
    def capture_learning(self, 
                        learning: str,
                        category: str = "general",
                        source: str = "",
                        actionable: bool = False,
                        related_todos: List[str] = None) -> str:
        """
        Capture a learning moment with categorization and context.
        
        Args:
            learning: The learning insight or discovery
            category: Category of learning (technical, process, personal, etc.)
            source: Source of the learning (experiment, mistake, reading, etc.)
            actionable: Whether this learning suggests specific actions
            related_todos: Todo IDs related to this learning
            
        Returns:
            Learning entry ID
        """
        learning_data = self._load_learning_data()
        
        learning_id = f"learning_{len(learning_data['learnings']) + 1}"
        
        entry = {
            "id": learning_id,
            "learning": learning,
            "category": category,
            "source": source,
            "actionable": actionable,
            "related_todos": related_todos or [],
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d'),
            "reviewed": False,
            "applied": False
        }
        
        learning_data["learnings"].append(entry)
        learning_data["last_updated"] = datetime.now().isoformat()
        
        # Update category summary
        self._update_learning_category_summary(learning_data, entry)
        
        self.file_manager.save_file(self.category, self.files["learning_log"], learning_data)
        
        return learning_id
    
    def suggest_course_correction(self, 
                                 trigger: str,
                                 current_situation: str,
                                 proposed_correction: str,
                                 urgency: str = "medium") -> None:
        """
        Log a course correction suggestion with AI enhancement opportunities.
        
        Args:
            trigger: What triggered the need for course correction
            current_situation: Description of current situation
            proposed_correction: Suggested course correction
            urgency: Urgency level (low, medium, high)
        """
        correction_entry = f"""
## Course Correction - {datetime.now().strftime('%Y-%m-%d')}

**Trigger:** {trigger}

**Current Situation:** {current_situation}

**Proposed Correction:** {proposed_correction}

**Urgency:** {urgency}

**Impact Assessment:**
{{ai_impact_assessment_analysis}}

**Implementation Strategy:**
{{ai_implementation_strategy_suggestions}}

**Risk Mitigation:**
{{ai_risk_mitigation_recommendations}}

**Success Metrics:**
{{ai_success_metric_identification}}

---
"""
        
        # Append to course corrections log
        existing_corrections = self.file_manager.load_file(self.category, self.files["course_corrections"]) or ""
        updated_corrections = existing_corrections + correction_entry
        
        self.file_manager.save_file(self.category, self.files["course_corrections"], updated_corrections)
    
    def get_reflection_insights(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Generate insights from recent reflection data.
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            Dictionary with reflection insights and patterns
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        insights = {
            "period_analyzed": f"Last {days_back} days",
            "energy_insights": self._analyze_energy_patterns(cutoff_date),
            "learning_insights": self._analyze_learning_patterns(cutoff_date),
            "reflection_frequency": self._analyze_reflection_frequency(cutoff_date),
            "course_correction_frequency": self._analyze_course_corrections(cutoff_date),
            "ai_enhancement_opportunities": [],
            "recommendations": []
        }
        
        # Generate AI enhancement opportunities
        insights["ai_enhancement_opportunities"] = [
            {
                "type": "energy_optimization",
                "template": "{ai_energy_pattern_optimization}",
                "context": f"Average energy: {insights['energy_insights'].get('average_energy', 0):.1f}"
            },
            {
                "type": "learning_application",
                "template": "{ai_learning_application_suggestions}",
                "context": f"{insights['learning_insights'].get('total_learnings', 0)} learnings captured"
            }
        ]
        
        # Generate recommendations
        if insights["energy_insights"].get("average_energy", 0) < 6:
            insights["recommendations"].append("Consider energy management strategies")
        
        if insights["reflection_frequency"].get("entries_count", 0) < 4:
            insights["recommendations"].append("Increase reflection frequency for better insights")
        
        return insights
    
    def get_reflection_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive summary of reflection activity.
        
        Returns:
            Summary suitable for status reports
        """
        energy_data = self._load_energy_data()
        learning_data = self._load_learning_data()
        
        # Get recent data (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        
        summary = {
            "reflection_active": False,
            "recent_energy_entries": 0,
            "average_recent_energy": 0,
            "recent_learnings": 0,
            "actionable_learnings": 0,
            "total_learnings": len(learning_data.get("learnings", [])),
            "learning_categories": {},
            "last_reflection": None,
            "course_corrections_pending": 0
        }
        
        # Analyze energy data
        if energy_data and "entries" in energy_data:
            recent_energy = [
                e for e in energy_data["entries"] 
                if self._is_recent_entry(e.get("timestamp", ""), 7)
            ]
            summary["recent_energy_entries"] = len(recent_energy)
            if recent_energy:
                summary["average_recent_energy"] = sum(e["energy_level"] for e in recent_energy) / len(recent_energy)
                summary["reflection_active"] = True
        
        # Analyze learning data
        if learning_data and "learnings" in learning_data:
            all_learnings = learning_data["learnings"]
            recent_learnings = [
                l for l in all_learnings 
                if self._is_recent_entry(l.get("timestamp", ""), 7)
            ]
            summary["recent_learnings"] = len(recent_learnings)
            summary["actionable_learnings"] = len([l for l in all_learnings if l.get("actionable", False)])
            
            # Count by category
            category_counts = {}
            for learning in all_learnings:
                category = learning.get("category", "general")
                category_counts[category] = category_counts.get(category, 0) + 1
            summary["learning_categories"] = category_counts
        
        # Check for recent reflection entries
        journal = self.file_manager.load_file(self.category, self.files["reflection_journal"])
        if journal and isinstance(journal, str):
            # Look for recent date patterns in journal
            import re
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            dates = re.findall(date_pattern, journal)
            if dates:
                try:
                    latest_date = max(datetime.strptime(date, '%Y-%m-%d') for date in dates)
                    summary["last_reflection"] = latest_date.strftime('%Y-%m-%d')
                    if latest_date > recent_cutoff:
                        summary["reflection_active"] = True
                except:
                    pass
        
        return summary
    
    def get_ai_enhancement_candidates(self) -> List[Dict[str, str]]:
        """
        Identify reflection files that could benefit from AI enhancement.
        
        Returns:
            List of files with enhancement opportunities
        """
        candidates = []
        
        # Check reflection journal for AI placeholders
        journal = self.file_manager.load_file(self.category, self.files["reflection_journal"])
        if journal and isinstance(journal, str) and '{ai_' in journal:
            placeholders = self.template_generator.parse_placeholders(journal)
            candidates.append({
                "file_type": "reflection_journal",
                "path": str(self.file_manager.get_file_path(self.category, self.files["reflection_journal"])),
                "enhancement_type": "reflection_analysis",
                "placeholder_count": len(placeholders),
                "placeholders": placeholders
            })
        
        # Check course corrections for AI placeholders
        corrections = self.file_manager.load_file(self.category, self.files["course_corrections"])
        if corrections and isinstance(corrections, str) and '{ai_' in corrections:
            placeholders = self.template_generator.parse_placeholders(corrections)
            candidates.append({
                "file_type": "course_corrections",
                "path": str(self.file_manager.get_file_path(self.category, self.files["course_corrections"])),
                "enhancement_type": "course_correction_analysis",
                "placeholder_count": len(placeholders),
                "placeholders": placeholders
            })
        
        return candidates
    
    def _get_type_specific_prompts(self, reflection_type: str) -> str:
        """Get reflection prompts specific to the reflection type."""
        prompts = {
            "daily": [
                "What was most energizing about today?",
                "What drained my energy?",
                "What did I learn that I can apply tomorrow?",
                "What would I do differently?"
            ],
            "weekly": [
                "What patterns do I notice in my energy and productivity?",
                "What progress did I make toward my goals?",
                "What obstacles did I encounter and how did I handle them?",
                "What do I want to focus on next week?"
            ],
            "monthly": [
                "How has my direction evolved this month?",
                "What assumptions have been validated or challenged?",
                "What skills have I developed?",
                "How can I optimize my approach for next month?"
            ],
            "project": [
                "What has this project taught me about my working style?",
                "What would I do differently if starting this project again?",
                "What knowledge can I transfer to future projects?",
                "How has this project changed my perspective?"
            ]
        }
        
        type_prompts = prompts.get(reflection_type, prompts["weekly"])
        return "\n".join(f"- {prompt}" for prompt in type_prompts)
    
    def _format_custom_prompts(self, custom_prompts: List[str]) -> str:
        """Format custom prompts for display."""
        if not custom_prompts:
            return "{ai_custom_prompt_suggestions}"
        
        formatted = "\n".join(f"- {prompt}" for prompt in custom_prompts)
        return formatted + "\n\n{ai_additional_custom_prompts}"
    
    def _load_energy_data(self) -> Dict[str, Any]:
        """Load energy tracking data."""
        data = self.file_manager.load_file(self.category, self.files["energy_tracking"])
        
        if data is None:
            data = {
                "entries": [],
                "daily_summaries": {},
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        
        return data
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Load learning log data."""
        data = self.file_manager.load_file(self.category, self.files["learning_log"])
        
        if data is None:
            data = {
                "learnings": [],
                "category_summaries": {},
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        
        return data
    
    def _update_daily_energy_summary(self, energy_data: Dict, entry: Dict) -> None:
        """Update daily energy summary statistics."""
        date = entry["date"]
        
        if "daily_summaries" not in energy_data:
            energy_data["daily_summaries"] = {}
        
        if date not in energy_data["daily_summaries"]:
            energy_data["daily_summaries"][date] = {
                "entries": 0,
                "total_energy": 0,
                "min_energy": 10,
                "max_energy": 1
            }
        
        daily = energy_data["daily_summaries"][date]
        daily["entries"] += 1
        daily["total_energy"] += entry["energy_level"]
        daily["min_energy"] = min(daily["min_energy"], entry["energy_level"])
        daily["max_energy"] = max(daily["max_energy"], entry["energy_level"])
        daily["average_energy"] = daily["total_energy"] / daily["entries"]
    
    def _update_learning_category_summary(self, learning_data: Dict, entry: Dict) -> None:
        """Update learning category summary statistics."""
        category = entry["category"]
        
        if "category_summaries" not in learning_data:
            learning_data["category_summaries"] = {}
        
        if category not in learning_data["category_summaries"]:
            learning_data["category_summaries"][category] = {
                "count": 0,
                "actionable_count": 0,
                "last_entry": None
            }
        
        summary = learning_data["category_summaries"][category]
        summary["count"] += 1
        if entry.get("actionable", False):
            summary["actionable_count"] += 1
        summary["last_entry"] = entry["timestamp"]
    
    def _analyze_energy_patterns(self, cutoff_date: datetime) -> Dict[str, Any]:
        """Analyze energy patterns from recent data."""
        energy_data = self._load_energy_data()
        
        if not energy_data.get("entries"):
            return {"average_energy": 0, "pattern_insights": []}
        
        recent_entries = [
            e for e in energy_data["entries"]
            if self._parse_timestamp(e.get("timestamp", "")) > cutoff_date
        ]
        
        if not recent_entries:
            return {"average_energy": 0, "pattern_insights": []}
        
        avg_energy = sum(e["energy_level"] for e in recent_entries) / len(recent_entries)
        
        return {
            "average_energy": avg_energy,
            "total_entries": len(recent_entries),
            "pattern_insights": [
                f"Average energy level: {avg_energy:.1f}/10",
                f"Total energy readings: {len(recent_entries)}"
            ]
        }
    
    def _analyze_learning_patterns(self, cutoff_date: datetime) -> Dict[str, Any]:
        """Analyze learning patterns from recent data."""
        learning_data = self._load_learning_data()
        
        if not learning_data.get("learnings"):
            return {"total_learnings": 0, "categories": {}}
        
        recent_learnings = [
            l for l in learning_data["learnings"]
            if self._parse_timestamp(l.get("timestamp", "")) > cutoff_date
        ]
        
        categories = {}
        for learning in recent_learnings:
            category = learning.get("category", "general")
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_learnings": len(recent_learnings),
            "categories": categories,
            "actionable_count": len([l for l in recent_learnings if l.get("actionable", False)])
        }
    
    def _analyze_reflection_frequency(self, cutoff_date: datetime) -> Dict[str, Any]:
        """Analyze reflection frequency from journal entries."""
        # This would need more sophisticated parsing of the reflection journal
        # For now, return basic structure
        return {
            "entries_count": 0,
            "frequency_assessment": "needs_analysis"
        }
    
    def _analyze_course_corrections(self, cutoff_date: datetime) -> Dict[str, Any]:
        """Analyze course correction frequency and patterns."""
        # This would need parsing of the course corrections file
        # For now, return basic structure
        return {
            "corrections_count": 0,
            "urgency_distribution": {}
        }
    
    def _is_recent_entry(self, timestamp: str, days: int) -> bool:
        """Check if an entry timestamp is within the specified number of days."""
        try:
            entry_date = self._parse_timestamp(timestamp)
            cutoff_date = datetime.now() - timedelta(days=days)
            return entry_date > cutoff_date
        except:
            return False
    
    def _parse_timestamp(self, timestamp: str) -> datetime:
        """Parse timestamp string to datetime object."""
        try:
            # Handle ISO format with or without timezone
            if timestamp.endswith('Z'):
                timestamp = timestamp[:-1] + '+00:00'
            return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            # Fallback to current time if parsing fails
            return datetime.now()