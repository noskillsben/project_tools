"""
Intelligence module for AI-assisted project management.

This module provides template-based AI assistance pipelines for project management,
focusing on creating structured templates that external AI tools can enhance while
keeping the core system deterministic and AI-free.
"""

from .file_manager import PROJECT_MANAGEMENT_DIR, INTELLIGENCE_SUBDIRS
from .compass import ProjectCompass
from .task_chains import TaskChainManager
from .direction import DirectionTracker
from .reflection import ReflectionManager
from .portfolio import PortfolioManager
from .project_intelligence import ProjectIntelligence

__all__ = [
    'ProjectCompass',
    'TaskChainManager',
    'DirectionTracker', 
    'ReflectionManager',
    'PortfolioManager',
    'ProjectIntelligence',
    'PROJECT_MANAGEMENT_DIR',
    'INTELLIGENCE_SUBDIRS'
]