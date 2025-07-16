"""
GitHub Integration for Project Tools

Optional integration with GitHub for automatic pushing of project changes
and version tagging. Requires PyGithub package and GitHub access token.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, List
import subprocess
import logging

# Try to import PyGithub, make it optional
try:
    from github import Github, Repository
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    Github = None
    Repository = None

logger = logging.getLogger(__name__)


class GitHubIntegration:
    """Handles GitHub integration for automatic syncing and version tagging"""
    
    def __init__(self, project_root: str = ".", config: Optional[Dict] = None):
        self.project_root = Path(project_root)
        self.config = config or {}
        self.github_client = None
        self.repo = None
        self.enabled = False
        
        if GITHUB_AVAILABLE:
            self._initialize_github()
        else:
            logger.warning("PyGithub not available. Install with: pip install PyGithub")
    
    def _initialize_github(self):
        """Initialize GitHub client and repository"""
        try:
            # Get GitHub token from config or environment
            token = self.config.get('github_token') or os.getenv('GITHUB_TOKEN')
            if not token:
                logger.info("No GitHub token found. GitHub integration disabled.")
                return
            
            # Get repository info
            repo_name = self._get_repo_name()
            if not repo_name:
                logger.info("Not a GitHub repository. GitHub integration disabled.")
                return
            
            # Initialize GitHub client
            self.github_client = Github(token)
            self.repo = self.github_client.get_repo(repo_name)
            self.enabled = True
            
            logger.info(f"GitHub integration enabled for repository: {repo_name}")
            
        except Exception as e:
            logger.warning(f"Failed to initialize GitHub integration: {e}")
            self.enabled = False
    
    def _get_repo_name(self) -> Optional[str]:
        """Get GitHub repository name from git remote"""
        try:
            # Try to get remote origin URL
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            remote_url = result.stdout.strip()
            
            # Parse GitHub repository name from URL
            if 'github.com' in remote_url:
                if remote_url.startswith('git@github.com:'):
                    # SSH format: git@github.com:owner/repo.git
                    repo_part = remote_url.replace('git@github.com:', '').replace('.git', '')
                elif remote_url.startswith('https://github.com/'):
                    # HTTPS format: https://github.com/owner/repo.git
                    repo_part = remote_url.replace('https://github.com/', '').replace('.git', '')
                else:
                    return None
                
                return repo_part
            
            return None
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def is_available(self) -> bool:
        """Check if GitHub integration is available and configured"""
        return GITHUB_AVAILABLE and self.enabled
    
    def get_status(self) -> Dict:
        """Get GitHub integration status"""
        return {
            "available": GITHUB_AVAILABLE,
            "enabled": self.enabled,
            "repository": self.repo.full_name if self.repo else None,
            "authenticated": self.github_client is not None
        }
    
    def commit_and_push_changes(self, 
                               files: List[str], 
                               commit_message: str,
                               branch: str = "main") -> bool:
        """Commit and push specified files to GitHub"""
        if not self.is_available():
            logger.debug("GitHub integration not available")
            return False
        
        try:
            # Stage files
            for file_path in files:
                subprocess.run(['git', 'add', file_path], 
                             cwd=self.project_root, check=True)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'diff', '--staged', '--quiet'], 
                                  cwd=self.project_root, capture_output=True)
            
            if result.returncode == 0:
                # No changes staged
                logger.debug("No changes to commit")
                return True
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         cwd=self.project_root, check=True)
            
            # Push to GitHub
            subprocess.run(['git', 'push', 'origin', branch], 
                         cwd=self.project_root, check=True)
            
            logger.info(f"Successfully pushed changes to GitHub: {commit_message}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to push changes to GitHub: {e}")
            return False
    
    def create_version_tag(self, version: str, message: str = None) -> bool:
        """Create and push a version tag to GitHub"""
        if not self.is_available():
            logger.debug("GitHub integration not available")
            return False
        
        try:
            tag_name = f"v{version}" if not version.startswith('v') else version
            tag_message = message or f"Release {version}"
            
            # Create local tag
            subprocess.run(['git', 'tag', '-a', tag_name, '-m', tag_message], 
                         cwd=self.project_root, check=True)
            
            # Push tag to GitHub
            subprocess.run(['git', 'push', 'origin', tag_name], 
                         cwd=self.project_root, check=True)
            
            logger.info(f"Successfully created and pushed tag: {tag_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create version tag: {e}")
            return False
    
    def auto_sync_project_files(self, version_bumped: bool = False) -> bool:
        """Automatically sync project files to GitHub"""
        if not self.is_available():
            return False
        
        files_to_sync = ['todo.json', 'changelog.json']
        
        # Add intelligence files if they exist
        project_mgmt_dir = self.project_root / 'project_management'
        if project_mgmt_dir.exists():
            files_to_sync.append('project_management/')
        
        # Add CLAUDE.md if it exists
        claude_md = self.project_root / 'CLAUDE.md'
        if claude_md.exists():
            files_to_sync.append('CLAUDE.md')
        
        # Create appropriate commit message
        if version_bumped:
            commit_message = "🚀 Version bump with project updates"
        else:
            commit_message = "📝 Update project todos and tracking data"
        
        return self.commit_and_push_changes(files_to_sync, commit_message)
    
    def sync_on_todo_complete(self, todo_title: str, version: str = None) -> bool:
        """Sync to GitHub when a todo is completed"""
        if not self.is_available():
            return False
        
        commit_message = f"✅ Completed: {todo_title}"
        if version:
            commit_message += f" (v{version})"
        
        files = ['todo.json', 'changelog.json']
        
        # Add intelligence files if they exist
        project_mgmt_dir = self.project_root / 'project_management'
        if project_mgmt_dir.exists():
            files.append('project_management/')
        
        return self.commit_and_push_changes(files, commit_message)
    
    def sync_on_version_bump(self, version: str, message: str) -> bool:
        """Sync to GitHub and create tag when version is bumped"""
        if not self.is_available():
            return False
        
        # First, commit and push the changes
        commit_message = f"🔖 Bump version to {version}: {message}"
        files = ['todo.json', 'changelog.json']
        
        # Add intelligence files if they exist
        project_mgmt_dir = self.project_root / 'project_management'
        if project_mgmt_dir.exists():
            files.append('project_management/')
        
        if self.commit_and_push_changes(files, commit_message):
            # Then create the version tag
            return self.create_version_tag(version, message)
        
        return False
    
    @staticmethod
    def get_config_template() -> Dict:
        """Get template for GitHub configuration"""
        return {
            "github_integration": {
                "enabled": True,
                "auto_push": True,
                "auto_tag": True,
                "branch": "main",
                "github_token": "YOUR_GITHUB_TOKEN_HERE"
            }
        }
    
    @staticmethod
    def setup_github_integration(project_root: str = ".") -> Dict:
        """Interactive setup for GitHub integration"""
        print("\n🔗 GitHub Integration Setup")
        print("=" * 40)
        
        config = {}
        
        # Check if git repository
        try:
            subprocess.run(['git', 'status'], cwd=project_root, 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Not a git repository. GitHub integration requires git.")
            return {"github_integration": {"enabled": False}}
        
        # Ask if user wants GitHub integration
        enable = input("Enable GitHub integration for auto-sync and version tagging? (y/n): ").lower().strip()
        
        if enable not in ['y', 'yes']:
            return {"github_integration": {"enabled": False}}
        
        print("\n📋 GitHub integration will:")
        print("• Auto-commit and push todo/changelog changes")
        print("• Create version tags when you bump versions")
        print("• Sync project management files")
        
        # Get GitHub token
        print(f"\n🔑 You'll need a GitHub Personal Access Token with 'repo' permissions.")
        print("Create one at: https://github.com/settings/tokens")
        
        use_env = input("Use GITHUB_TOKEN environment variable? (y/n): ").lower().strip()
        
        if use_env in ['y', 'yes']:
            token = os.getenv('GITHUB_TOKEN')
            if not token:
                print("❌ GITHUB_TOKEN environment variable not found")
                return {"github_integration": {"enabled": False}}
            config['github_token'] = None  # Use environment variable
        else:
            token = input("Enter your GitHub token (will be stored in config): ").strip()
            if not token:
                print("❌ No token provided")
                return {"github_integration": {"enabled": False}}
            config['github_token'] = token
        
        # Get branch preference
        branch = input("Git branch to use (default: main): ").strip() or "main"
        
        config.update({
            "enabled": True,
            "auto_push": True,
            "auto_tag": True,
            "branch": branch
        })
        
        # Test the configuration
        test_integration = GitHubIntegration(project_root, config)
        if test_integration.is_available():
            status = test_integration.get_status()
            print(f"✅ GitHub integration configured for: {status['repository']}")
        else:
            print("❌ Failed to configure GitHub integration")
            return {"github_integration": {"enabled": False}}
        
        return {"github_integration": config}


def setup_github_integration_cli():
    """CLI entry point for GitHub integration setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup GitHub integration for project_tools")
    parser.add_argument("--project-root", default=".", 
                       help="Project root directory (default: current directory)")
    
    args = parser.parse_args()
    
    config = GitHubIntegration.setup_github_integration(args.project_root)
    
    # Save config to file
    config_file = Path(args.project_root) / "project_tools_config.json"
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            existing_config = json.load(f)
        existing_config.update(config)
        config = existing_config
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n💾 Configuration saved to: {config_file}")


if __name__ == "__main__":
    setup_github_integration_cli()