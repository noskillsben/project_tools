"""
Centralized file management system for intelligence artifacts.

Manages the project_management/ directory structure and provides utilities
for organizing, accessing, and maintaining intelligence files.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

PROJECT_MANAGEMENT_DIR = 'project_management'

INTELLIGENCE_SUBDIRS = {
    'compass': 'compass',
    'chains': 'chains', 
    'direction': 'direction',
    'reflection': 'reflection',
    'portfolio': 'portfolio'
}


class IntelligenceFileManager:
    """Manages files and directories for intelligence artifacts."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.intelligence_root = self.project_root / PROJECT_MANAGEMENT_DIR
        self.subdirs = {
            name: self.intelligence_root / path 
            for name, path in INTELLIGENCE_SUBDIRS.items()
        }
    
    def ensure_directory_structure(self) -> None:
        """Create the project_management directory structure if it doesn't exist."""
        self.intelligence_root.mkdir(exist_ok=True)
        
        for subdir_path in self.subdirs.values():
            subdir_path.mkdir(exist_ok=True)
        
        # Create a README explaining the structure
        readme_path = self.intelligence_root / "README.md"
        if not readme_path.exists():
            self._create_structure_readme(readme_path)
    
    def get_file_path(self, category: str, filename: str) -> Path:
        """Get the full path for a file in a specific intelligence category."""
        if category not in self.subdirs:
            raise ValueError(f"Unknown intelligence category: {category}")
        
        return self.subdirs[category] / filename
    
    def save_file(self, category: str, filename: str, content: Union[str, Dict, List]) -> Path:
        """Save content to a file in the specified intelligence category."""
        file_path = self.get_file_path(category, filename)
        
        if isinstance(content, (dict, list)):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return file_path
    
    def load_file(self, category: str, filename: str) -> Optional[Union[str, Dict, List]]:
        """Load content from a file in the specified intelligence category."""
        file_path = self.get_file_path(category, filename)
        
        if not file_path.exists():
            return None
        
        try:
            # Try to load as JSON first
            with open(file_path, 'r', encoding='utf-8') as f:
                if filename.endswith('.json'):
                    return json.load(f)
                else:
                    return f.read()
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fallback to text
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def file_exists(self, category: str, filename: str) -> bool:
        """Check if a file exists in the specified intelligence category."""
        return self.get_file_path(category, filename).exists()
    
    def list_files(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """List all files in intelligence directories."""
        if category:
            if category not in self.subdirs:
                raise ValueError(f"Unknown intelligence category: {category}")
            
            subdir = self.subdirs[category]
            if subdir.exists():
                return {category: [f.name for f in subdir.iterdir() if f.is_file()]}
            else:
                return {category: []}
        
        files_by_category = {}
        for cat_name, subdir in self.subdirs.items():
            if subdir.exists():
                files_by_category[cat_name] = [f.name for f in subdir.iterdir() if f.is_file()]
            else:
                files_by_category[cat_name] = []
        
        return files_by_category
    
    def get_artifact_inventory(self) -> Dict[str, Any]:
        """Get a comprehensive inventory of all intelligence artifacts."""
        inventory = {
            "structure_created": self.intelligence_root.exists(),
            "last_updated": datetime.now().isoformat(),
            "categories": {}
        }
        
        for category, subdir in self.subdirs.items():
            if subdir.exists():
                files = list(subdir.iterdir())
                inventory["categories"][category] = {
                    "exists": True,
                    "file_count": len([f for f in files if f.is_file()]),
                    "files": [
                        {
                            "name": f.name,
                            "size": f.stat().st_size,
                            "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                        }
                        for f in files if f.is_file()
                    ]
                }
            else:
                inventory["categories"][category] = {
                    "exists": False,
                    "file_count": 0,
                    "files": []
                }
        
        return inventory
    
    def cleanup_empty_directories(self) -> List[str]:
        """Remove empty intelligence subdirectories and return list of removed dirs."""
        removed = []
        
        for category, subdir in self.subdirs.items():
            if subdir.exists() and not any(subdir.iterdir()):
                shutil.rmtree(subdir)
                removed.append(category)
        
        # Remove main intelligence directory if completely empty
        if (self.intelligence_root.exists() and 
            not any(self.intelligence_root.iterdir())):
            shutil.rmtree(self.intelligence_root)
            removed.append(PROJECT_MANAGEMENT_DIR)
        
        return removed
    
    def backup_intelligence_data(self, backup_path: Optional[str] = None) -> str:
        """Create a backup of all intelligence data."""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{PROJECT_MANAGEMENT_DIR}_backup_{timestamp}"
        
        backup_full_path = self.project_root / backup_path
        
        if self.intelligence_root.exists():
            shutil.copytree(self.intelligence_root, backup_full_path)
        
        return str(backup_full_path)
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore intelligence data from a backup."""
        backup_full_path = Path(backup_path)
        
        if not backup_full_path.exists():
            return False
        
        # Remove current intelligence directory
        if self.intelligence_root.exists():
            shutil.rmtree(self.intelligence_root)
        
        # Restore from backup
        shutil.copytree(backup_full_path, self.intelligence_root)
        
        return True
    
    def migrate_files(self, file_mapping: Dict[str, Dict[str, str]]) -> Dict[str, bool]:
        """Migrate files according to a mapping: {category: {old_name: new_name}}."""
        results = {}
        
        for category, mappings in file_mapping.items():
            if category not in self.subdirs:
                continue
            
            for old_name, new_name in mappings.items():
                old_path = self.get_file_path(category, old_name)
                new_path = self.get_file_path(category, new_name)
                
                if old_path.exists():
                    old_path.rename(new_path)
                    results[f"{category}/{old_name}"] = True
                else:
                    results[f"{category}/{old_name}"] = False
        
        return results
    
    def get_directory_size(self) -> Dict[str, int]:
        """Get the size of each intelligence directory in bytes."""
        sizes = {}
        
        for category, subdir in self.subdirs.items():
            if subdir.exists():
                total_size = sum(f.stat().st_size for f in subdir.rglob('*') if f.is_file())
                sizes[category] = total_size
            else:
                sizes[category] = 0
        
        return sizes
    
    def _create_structure_readme(self, readme_path: Path) -> None:
        """Create a README explaining the intelligence directory structure."""
        content = f"""# Project Intelligence Directory Structure

This directory contains AI-assisted project management artifacts organized by category.

## Directory Structure

- **compass/**: Project intent, success criteria, and learning objectives
- **chains/**: Task chain definitions, visualizations, and health reports  
- **direction/**: Direction tracking, assumptions, and pivot analysis
- **reflection/**: Reflection journals, energy tracking, and course corrections
- **portfolio/**: Portfolio management, project hierarchies, and cross-project insights

## File Organization

All intelligence artifacts are organized here to keep the project root clean while
maintaining easy access to AI-enhanced project management features.

## AI Enhancement

Files in this directory are designed to work with external AI tools (like Claude)
that can enhance templates with intelligent suggestions and analysis.

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)