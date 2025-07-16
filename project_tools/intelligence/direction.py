"""
DirectionTracker class for lightweight goal management without formal OKR overhead.

Provides simple direction setting, assumption tracking, pivot detection, and AI-assisted
direction evaluation within the organized project_management/ structure.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .file_manager import IntelligenceFileManager
from .templates import TemplateGenerator


class DirectionTracker:
    """
    Manages lightweight project direction tracking and pivot detection.
    
    Provides simple goal management focused on direction clarity rather than
    formal OKR structures, with AI-assisted evaluation and pivot recommendations.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.file_manager = IntelligenceFileManager(project_root)
        self.template_generator = TemplateGenerator()
        self.category = "direction"
        
        # Standard direction files
        self.files = {
            "current_direction": "current_direction.md",
            "direction_history": "direction_history.json",
            "assumptions": "assumptions.json",
            "pivot_log": "pivot_log.md"
        }
    
    def set_current_direction(self, 
                             direction: str, 
                             rationale: str = "",
                             success_indicators: List[str] = None,
                             time_horizon: str = "3 months") -> bool:
        """
        Set the current project direction with rationale and success indicators.
        
        Args:
            direction: Clear statement of current direction
            rationale: Why this direction was chosen
            success_indicators: List of indicators that would show success
            time_horizon: Expected timeframe for evaluating this direction
            
        Returns:
            True if direction was successfully set
        """
        self.file_manager.ensure_directory_structure()
        
        # Archive current direction to history first
        current = self._load_current_direction()
        if current and current.get("direction"):
            self._archive_direction(current)
        
        # Create new direction template with AI enhancement placeholders
        direction_template = self.template_generator.create_template_with_placeholders(
            "direction_analysis"
        )
        
        # Create structured direction content
        direction_content = f"""# Current Project Direction

## Direction Statement
{direction}

## Rationale
{rationale}

## Success Indicators
{self._format_success_indicators(success_indicators or [])}

## Time Horizon
{time_horizon}

## Key Assumptions
{{ai_assumption_identification}}

## Risk Assessment
{{ai_risk_factor_analysis}}

## Alternative Paths Considered
{{ai_alternative_path_evaluation}}

## Pivot Triggers
{{ai_pivot_signal_identification}}

---
*Direction set: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Ready for AI enhancement and regular evaluation*
"""
        
        # Save current direction
        self.file_manager.save_file(self.category, self.files["current_direction"], direction_content)
        
        # Update direction history
        self._log_direction_change(direction, rationale, time_horizon)
        
        return True
    
    def add_assumption(self, 
                      assumption: str, 
                      confidence: str = "medium",
                      validation_method: str = "",
                      critical: bool = False) -> str:
        """
        Add a key assumption that underlies the current direction.
        
        Args:
            assumption: The assumption statement
            confidence: Confidence level (low/medium/high)
            validation_method: How this assumption could be validated
            critical: Whether this assumption is critical to direction success
            
        Returns:
            Assumption ID for tracking
        """
        assumptions_data = self._load_assumptions_data()
        
        assumption_id = f"assumption_{len(assumptions_data['assumptions']) + 1}"
        
        new_assumption = {
            "id": assumption_id,
            "assumption": assumption,
            "confidence": confidence,
            "validation_method": validation_method,
            "critical": critical,
            "status": "active",
            "created": datetime.now().isoformat(),
            "validated": None,
            "validation_result": None
        }
        
        assumptions_data["assumptions"].append(new_assumption)
        assumptions_data["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["assumptions"], assumptions_data)
        
        return assumption_id
    
    def validate_assumption(self, assumption_id: str, result: str, evidence: str = "") -> bool:
        """
        Record the validation result for an assumption.
        
        Args:
            assumption_id: ID of the assumption to validate
            result: Validation result (confirmed/rejected/unclear)
            evidence: Evidence supporting the validation result
            
        Returns:
            True if assumption was successfully updated
        """
        assumptions_data = self._load_assumptions_data()
        
        assumption = self._find_assumption_by_id(assumptions_data, assumption_id)
        if not assumption:
            return False
        
        assumption["validated"] = datetime.now().isoformat()
        assumption["validation_result"] = result
        assumption["evidence"] = evidence
        
        if result == "rejected":
            assumption["status"] = "invalidated"
        elif result == "confirmed":
            assumption["status"] = "validated"
        
        self.file_manager.save_file(self.category, self.files["assumptions"], assumptions_data)
        
        return True
    
    def log_pivot_consideration(self, 
                               trigger: str, 
                               new_direction_considered: str,
                               decision: str = "continue",
                               reasoning: str = "") -> None:
        """
        Log when a pivot was considered and the decision made.
        
        Args:
            trigger: What triggered the pivot consideration
            new_direction_considered: Alternative direction that was considered
            decision: Decision made (continue/pivot/delay)
            reasoning: Reasoning behind the decision
        """
        pivot_entry = f"""
## Pivot Consideration - {datetime.now().strftime('%Y-%m-%d')}

**Trigger:** {trigger}

**Alternative Direction Considered:** {new_direction_considered}

**Decision:** {decision}

**Reasoning:** {reasoning}

**AI Analysis Opportunities:**
{{ai_pivot_decision_analysis}}

{{ai_missed_opportunity_assessment}}

---
"""
        
        # Append to pivot log
        current_log = self.file_manager.load_file(self.category, self.files["pivot_log"]) or ""
        updated_log = current_log + pivot_entry
        
        self.file_manager.save_file(self.category, self.files["pivot_log"], updated_log)
    
    def evaluate_direction_health(self) -> Dict[str, Any]:
        """
        Evaluate the health of the current direction based on assumptions and progress.
        
        Returns:
            Dictionary with direction health assessment
        """
        current = self._load_current_direction()
        assumptions = self._load_assumptions_data()
        history = self._load_direction_history()
        
        health = {
            "overall_health": "unknown",
            "direction_age_days": 0,
            "critical_assumptions_at_risk": 0,
            "validated_assumptions": 0,
            "pivot_frequency": 0,
            "recommendations": [],
            "ai_enhancement_opportunities": [],
            "last_evaluated": datetime.now().isoformat()
        }
        
        if not current:
            health["overall_health"] = "no_direction"
            health["recommendations"].append("Set a current direction to begin tracking")
            return health
        
        # Calculate direction age
        if "created" in current:
            try:
                created_date = datetime.fromisoformat(current["created"].replace('Z', '+00:00'))
                health["direction_age_days"] = (datetime.now() - created_date).days
            except:
                pass
        
        # Analyze assumptions
        if assumptions and "assumptions" in assumptions:
            total_assumptions = len(assumptions["assumptions"])
            critical_assumptions = [a for a in assumptions["assumptions"] if a.get("critical", False)]
            validated_assumptions = [a for a in assumptions["assumptions"] if a.get("status") == "validated"]
            invalidated_critical = [a for a in critical_assumptions if a.get("status") == "invalidated"]
            
            health["critical_assumptions_at_risk"] = len(invalidated_critical)
            health["validated_assumptions"] = len(validated_assumptions)
            
            # Health assessment based on assumptions
            if len(invalidated_critical) > 0:
                health["overall_health"] = "at_risk"
                health["recommendations"].append("Critical assumptions have been invalidated - consider pivot")
            elif len(validated_assumptions) / total_assumptions > 0.7 if total_assumptions > 0 else False:
                health["overall_health"] = "strong"
            else:
                health["overall_health"] = "uncertain"
                health["recommendations"].append("Validate more assumptions to increase direction confidence")
        
        # Analyze pivot frequency
        if history and "direction_changes" in history:
            recent_changes = [
                change for change in history["direction_changes"]
                if self._is_recent_change(change.get("timestamp", ""))
            ]
            health["pivot_frequency"] = len(recent_changes)
            
            if len(recent_changes) > 3:
                health["recommendations"].append("High pivot frequency detected - consider longer evaluation periods")
        
        # Add AI enhancement opportunities
        health["ai_enhancement_opportunities"] = [
            {
                "type": "direction_validation",
                "template": "{ai_direction_validation_analysis}",
                "context": f"Direction is {health['direction_age_days']} days old"
            },
            {
                "type": "assumption_review",
                "template": "{ai_assumption_strength_assessment}",
                "context": f"{health['validated_assumptions']} assumptions validated"
            }
        ]
        
        return health
    
    def get_direction_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive summary of current direction status.
        
        Returns:
            Summary suitable for status reports and dashboard display
        """
        current = self._load_current_direction()
        health = self.evaluate_direction_health()
        assumptions = self._load_assumptions_data()
        
        summary = {
            "has_current_direction": current is not None and bool(current.get("direction")),
            "direction_health": health["overall_health"],
            "direction_age_days": health["direction_age_days"],
            "total_assumptions": 0,
            "critical_assumptions": 0,
            "validated_assumptions": health["validated_assumptions"],
            "assumptions_at_risk": health["critical_assumptions_at_risk"],
            "recent_pivot_considerations": 0,
            "needs_attention": False
        }
        
        if assumptions and "assumptions" in assumptions:
            all_assumptions = assumptions["assumptions"]
            summary["total_assumptions"] = len(all_assumptions)
            summary["critical_assumptions"] = len([a for a in all_assumptions if a.get("critical", False)])
        
        # Check if direction needs attention
        summary["needs_attention"] = (
            health["overall_health"] in ["at_risk", "no_direction"] or
            health["critical_assumptions_at_risk"] > 0 or
            health["direction_age_days"] > 90
        )
        
        return summary
    
    def get_ai_enhancement_candidates(self) -> List[Dict[str, str]]:
        """
        Identify direction files that could benefit from AI enhancement.
        
        Returns:
            List of files with enhancement opportunities
        """
        candidates = []
        
        # Check current direction for AI placeholders
        current = self.file_manager.load_file(self.category, self.files["current_direction"])
        if current and isinstance(current, str) and '{ai_' in current:
            placeholders = self.template_generator.parse_placeholders(current)
            candidates.append({
                "file_type": "current_direction",
                "path": str(self.file_manager.get_file_path(self.category, self.files["current_direction"])),
                "enhancement_type": "direction_analysis",
                "placeholder_count": len(placeholders),
                "placeholders": placeholders
            })
        
        # Check for pivot log enhancement opportunities
        pivot_log = self.file_manager.load_file(self.category, self.files["pivot_log"])
        if pivot_log and isinstance(pivot_log, str) and '{ai_' in pivot_log:
            placeholders = self.template_generator.parse_placeholders(pivot_log)
            candidates.append({
                "file_type": "pivot_log", 
                "path": str(self.file_manager.get_file_path(self.category, self.files["pivot_log"])),
                "enhancement_type": "pivot_analysis",
                "placeholder_count": len(placeholders),
                "placeholders": placeholders
            })
        
        return candidates
    
    def _load_current_direction(self) -> Optional[Dict[str, Any]]:
        """Load current direction data, parsing from markdown if needed."""
        content = self.file_manager.load_file(self.category, self.files["current_direction"])
        
        if not content:
            return None
        
        # If it's a string (markdown), parse basic info
        if isinstance(content, str):
            # Extract direction from markdown
            lines = content.split('\n')
            direction = ""
            rationale = ""
            created = ""
            
            for i, line in enumerate(lines):
                if line.startswith('## Direction Statement'):
                    if i + 1 < len(lines):
                        direction = lines[i + 1].strip()
                elif line.startswith('## Rationale'):
                    if i + 1 < len(lines):
                        rationale = lines[i + 1].strip()
                elif '*Direction set:' in line:
                    # Extract timestamp
                    import re
                    match = re.search(r'\*Direction set: ([^*]+)\*', line)
                    if match:
                        created = match.group(1).strip()
            
            return {
                "direction": direction,
                "rationale": rationale,
                "created": created
            }
        
        return content
    
    def _load_direction_history(self) -> Dict[str, Any]:
        """Load direction history data."""
        data = self.file_manager.load_file(self.category, self.files["direction_history"])
        
        if data is None:
            data = {
                "direction_changes": [],
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        
        return data
    
    def _load_assumptions_data(self) -> Dict[str, Any]:
        """Load assumptions data."""
        data = self.file_manager.load_file(self.category, self.files["assumptions"])
        
        if data is None:
            data = {
                "assumptions": [],
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        
        return data
    
    def _archive_direction(self, current_direction: Dict) -> None:
        """Archive current direction to history."""
        history = self._load_direction_history()
        
        archived_entry = {
            "direction": current_direction.get("direction", ""),
            "rationale": current_direction.get("rationale", ""),
            "archived": datetime.now().isoformat(),
            "duration_days": 0  # Could calculate if we had start date
        }
        
        if "archived_directions" not in history:
            history["archived_directions"] = []
        
        history["archived_directions"].append(archived_entry)
        history["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["direction_history"], history)
    
    def _log_direction_change(self, direction: str, rationale: str, time_horizon: str) -> None:
        """Log a direction change to history."""
        history = self._load_direction_history()
        
        change_entry = {
            "direction": direction,
            "rationale": rationale,
            "time_horizon": time_horizon,
            "timestamp": datetime.now().isoformat(),
            "change_type": "new_direction"
        }
        
        history["direction_changes"].append(change_entry)
        history["last_updated"] = datetime.now().isoformat()
        
        self.file_manager.save_file(self.category, self.files["direction_history"], history)
    
    def _find_assumption_by_id(self, assumptions_data: Dict, assumption_id: str) -> Optional[Dict]:
        """Find an assumption by its ID."""
        for assumption in assumptions_data.get("assumptions", []):
            if assumption["id"] == assumption_id:
                return assumption
        return None
    
    def _format_success_indicators(self, indicators: List[str]) -> str:
        """Format success indicators for markdown display."""
        if not indicators:
            return "{ai_success_indicator_suggestions}"
        
        formatted = "\n".join(f"- {indicator}" for indicator in indicators)
        return formatted + "\n\n{ai_additional_success_indicators}"
    
    def _is_recent_change(self, timestamp: str, days: int = 30) -> bool:
        """Check if a timestamp represents a recent change."""
        try:
            change_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            cutoff_date = datetime.now() - timedelta(days=days)
            return change_date > cutoff_date
        except:
            return False