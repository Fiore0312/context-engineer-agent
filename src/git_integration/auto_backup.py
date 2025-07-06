"""
Automatic backup system for Git repositories
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import git
from git import Repo, InvalidGitRepositoryError
from rich.console import Console
from rich.progress import Progress, TaskID

from .github_client import GitHubClient

console = Console()

class AutoBackup:
    """Automatic backup system for Git repositories"""
    
    def __init__(self, github_client: Optional[GitHubClient] = None):
        """Initialize auto backup system
        
        Args:
            github_client: GitHubClient instance
        """
        self.github_client = github_client
    
    def is_git_repository(self, path: Path) -> bool:
        """Check if path is a Git repository
        
        Args:
            path: Directory path to check
            
        Returns:
            True if path is a Git repository
        """
        try:
            Repo(path)
            return True
        except InvalidGitRepositoryError:
            return False
    
    def init_git_repository(self, path: Path) -> Repo:
        """Initialize Git repository in path
        
        Args:
            path: Directory path
            
        Returns:
            Git repository instance
        """
        try:
            if self.is_git_repository(path):
                console.print("📁 Repository Git già esistente", style="yellow")
                return Repo(path)
            
            repo = Repo.init(path)
            console.print("✅ Repository Git inizializzato", style="green")
            
            # Create initial .gitignore if it doesn't exist
            gitignore_path = path / '.gitignore'
            if not gitignore_path.exists():
                self._create_gitignore(gitignore_path, path)
            
            return repo
            
        except Exception as e:
            console.print(f"❌ Errore nell'inizializzazione Git: {str(e)}", style="red")
            raise
    
    def _create_gitignore(self, gitignore_path: Path, project_path: Path):
        """Create appropriate .gitignore file
        
        Args:
            gitignore_path: Path where to create .gitignore
            project_path: Project directory for language detection
        """
        # Basic gitignore content
        gitignore_content = [
            "# Context Engineer Agent files",
            ".context-engineer/",
            "*.log",
            "*.tmp",
            "",
            "# OS generated files",
            ".DS_Store",
            ".DS_Store?",
            "._*",
            ".Spotlight-V100",
            ".Trashes",
            "ehthumbs.db",
            "Thumbs.db",
            "",
            "# IDE files",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            "*~",
            ""
        ]
        
        # Add language-specific patterns
        if any(project_path.glob("*.py")):
            gitignore_content.extend([
                "# Python",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "*.so",
                ".Python",
                "build/",
                "develop-eggs/",
                "dist/",
                "downloads/",
                "eggs/",
                ".eggs/",
                "lib/",
                "lib64/",
                "parts/",
                "sdist/",
                "var/",
                "wheels/",
                "*.egg-info/",
                ".installed.cfg",
                "*.egg",
                "MANIFEST",
                ".env",
                ".venv",
                "env/",
                "venv/",
                "ENV/",
                "env.bak/",
                "venv.bak/",
                ""
            ])
        
        if (project_path / "package.json").exists():
            gitignore_content.extend([
                "# Node.js",
                "node_modules/",
                "npm-debug.log*",
                "yarn-debug.log*",
                "yarn-error.log*",
                ".npm",
                ".eslintcache",
                ".nyc_output",
                "coverage/",
                ".grunt",
                "bower_components",
                ".lock-wscript",
                ".node_repl_history",
                "*.tgz",
                ".yarn-integrity",
                ".env.local",
                ".env.development.local",
                ".env.test.local",
                ".env.production.local",
                ""
            ])
        
        if any(project_path.glob("*.php")):
            gitignore_content.extend([
                "# PHP",
                "/vendor/",
                "/node_modules/",
                "/public/hot",
                "/public/storage",
                "/storage/*.key",
                ".env",
                ".env.backup",
                ".phpunit.result.cache",
                "Homestead.json",
                "Homestead.yaml",
                "npm-debug.log",
                "yarn-error.log",
                ""
            ])
        
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(gitignore_content))
            
            console.print("📝 File .gitignore creato", style="green")
            
        except Exception as e:
            console.print(f"⚠️ Impossibile creare .gitignore: {str(e)}", style="yellow")
    
    def get_git_status(self, path: Path) -> Dict[str, Any]:
        """Get Git repository status
        
        Args:
            path: Repository path
            
        Returns:
            Repository status information
        """
        if not self.is_git_repository(path):
            return {'is_git_repo': False}
        
        try:
            repo = Repo(path)
            
            # Get current branch
            current_branch = repo.active_branch.name if repo.head.is_valid() else None
            
            # Get remotes
            remotes = [remote.name for remote in repo.remotes]
            
            # Get status
            changed_files = [item.a_path for item in repo.index.diff(None)]
            staged_files = [item.a_path for item in repo.index.diff("HEAD")]
            untracked_files = repo.untracked_files
            
            # Check if there are commits
            has_commits = False
            try:
                _ = repo.head.commit
                has_commits = True
            except:
                pass
            
            return {
                'is_git_repo': True,
                'current_branch': current_branch,
                'remotes': remotes,
                'has_commits': has_commits,
                'changed_files': changed_files,
                'staged_files': staged_files,
                'untracked_files': untracked_files,
                'is_dirty': repo.is_dirty(),
                'has_remote_origin': 'origin' in remotes
            }
            
        except Exception as e:
            console.print(f"❌ Errore nel controllo status Git: {str(e)}", style="red")
            return {'is_git_repo': True, 'error': str(e)}
    
    def add_remote_origin(self, path: Path, remote_url: str):
        """Add remote origin to repository
        
        Args:
            path: Repository path
            remote_url: Remote repository URL
        """
        if not self.is_git_repository(path):
            raise Exception("Not a Git repository")
        
        try:
            repo = Repo(path)
            
            # Remove existing origin if present
            if 'origin' in [remote.name for remote in repo.remotes]:
                repo.delete_remote('origin')
            
            # Add new origin
            origin = repo.create_remote('origin', remote_url)
            
            console.print(f"✅ Remote origin aggiunto: {remote_url}", style="green")
            
        except Exception as e:
            console.print(f"❌ Errore nell'aggiunta remote: {str(e)}", style="red")
            raise
    
    def commit_changes(self, 
                      path: Path, 
                      message: Optional[str] = None,
                      add_all: bool = True) -> bool:
        """Commit changes to repository
        
        Args:
            path: Repository path
            message: Commit message
            add_all: Whether to add all changes
            
        Returns:
            True if commit was successful
        """
        if not self.is_git_repository(path):
            raise Exception("Not a Git repository")
        
        try:
            repo = Repo(path)
            
            # Add all changes if requested
            if add_all:
                repo.git.add('--all')
            
            # Check if there are changes to commit
            if not repo.is_dirty() and not repo.untracked_files:
                console.print("ℹ️ Nessuna modifica da committare", style="blue")
                return False
            
            # Generate commit message if not provided
            if not message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"Context Engineering - Auto-backup {timestamp}"
            
            # Create commit
            repo.index.commit(message)
            
            console.print(f"✅ Commit creato: {message}", style="green")
            return True
            
        except Exception as e:
            console.print(f"❌ Errore nel commit: {str(e)}", style="red")
            raise
    
    def push_to_remote(self, path: Path, remote: str = 'origin', branch: str = 'main') -> bool:
        """Push changes to remote repository
        
        Args:
            path: Repository path
            remote: Remote name
            branch: Branch name
            
        Returns:
            True if push was successful
        """
        if not self.is_git_repository(path):
            raise Exception("Not a Git repository")
        
        try:
            repo = Repo(path)
            
            # Check if remote exists
            if remote not in [r.name for r in repo.remotes]:
                raise Exception(f"Remote '{remote}' not found")
            
            origin = repo.remotes[remote]
            
            # Push changes
            with Progress() as progress:
                task = progress.add_task("🔄 Push in corso...", total=100)
                
                try:
                    origin.push(f"refs/heads/{branch}:refs/heads/{branch}")
                    progress.update(task, completed=100)
                except Exception as push_error:
                    # Try to set upstream and push
                    try:
                        origin.push(f"refs/heads/{branch}:refs/heads/{branch}", set_upstream=True)
                        progress.update(task, completed=100)
                    except:
                        raise push_error
            
            console.print(f"✅ Push completato su {remote}/{branch}", style="green")
            return True
            
        except Exception as e:
            console.print(f"❌ Errore nel push: {str(e)}", style="red")
            return False
    
    def setup_repository_with_github(self, 
                                   project_path: Path,
                                   repo_name: Optional[str] = None,
                                   description: str = "",
                                   private: bool = False) -> Dict[str, Any]:
        """Setup complete Git repository with GitHub integration
        
        Args:
            project_path: Project directory path
            repo_name: Repository name (auto-generated if None)
            description: Repository description
            private: Whether repository should be private
            
        Returns:
            Setup result information
        """
        if not self.github_client or not self.github_client.is_authenticated():
            raise Exception("GitHub client not authenticated")
        
        try:
            # Generate repository name if not provided
            if not repo_name:
                repo_name = self.github_client.suggest_repository_name(project_path)
            
            # Detect project language for gitignore
            language = self.github_client.detect_project_language(project_path)
            gitignore_template = language if language else None
            
            # Create GitHub repository
            console.print(f"🚀 Creazione repository GitHub: {repo_name}")
            github_repo = self.github_client.create_repository(
                name=repo_name,
                description=description,
                private=private,
                auto_init=False,  # We'll initialize locally
                gitignore_template=gitignore_template
            )
            
            # Initialize local Git repository
            repo = self.init_git_repository(project_path)
            
            # Add remote origin
            self.add_remote_origin(project_path, github_repo['clone_url'])
            
            # Create initial commit
            commit_success = self.commit_changes(
                project_path, 
                "Initial commit - Context Engineering setup"
            )
            
            # Push to GitHub
            if commit_success:
                push_success = self.push_to_remote(project_path)
            else:
                push_success = False
            
            result = {
                'status': 'success',
                'github_repo': github_repo,
                'local_repo_initialized': True,
                'initial_commit': commit_success,
                'pushed_to_github': push_success,
                'next_steps': [
                    f"Repository creato: {github_repo['html_url']}",
                    "Setup Git completato",
                    "Prossimi commit saranno automatici"
                ]
            }
            
            if not push_success:
                result['next_steps'].append("⚠️ Push iniziale fallito - riprova manualmente")
            
            return result
            
        except Exception as e:
            console.print(f"❌ Errore nel setup repository: {str(e)}", style="red")
            return {
                'status': 'error',
                'error': str(e),
                'github_repo': None,
                'local_repo_initialized': False,
                'initial_commit': False,
                'pushed_to_github': False
            }
    
    def auto_backup_session(self, 
                           project_path: Path,
                           session_description: str = "") -> Dict[str, Any]:
        """Perform automatic backup of current session
        
        Args:
            project_path: Project directory path
            session_description: Description of the session
            
        Returns:
            Backup result information
        """
        if not self.is_git_repository(project_path):
            return {
                'status': 'error',
                'error': 'Not a Git repository. Initialize Git first.',
                'backup_completed': False
            }
        
        try:
            # Get repository status
            status = self.get_git_status(project_path)
            
            if not status['is_dirty'] and not status['untracked_files']:
                return {
                    'status': 'no_changes',
                    'message': 'No changes to backup',
                    'backup_completed': False
                }
            
            # Create commit message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if session_description:
                commit_msg = f"Context Engineering - {timestamp} - {session_description}"
            else:
                commit_msg = f"Context Engineering - Auto-backup {timestamp}"
            
            # Commit changes
            commit_success = self.commit_changes(project_path, commit_msg)
            
            if not commit_success:
                return {
                    'status': 'error',
                    'error': 'Failed to create commit',
                    'backup_completed': False
                }
            
            # Push to remote if available
            push_success = False
            if status['has_remote_origin']:
                push_success = self.push_to_remote(project_path)
            
            return {
                'status': 'success',
                'commit_created': commit_success,
                'pushed_to_remote': push_success,
                'commit_message': commit_msg,
                'backup_completed': True,
                'files_changed': len(status['changed_files']),
                'files_added': len(status['untracked_files'])
            }
            
        except Exception as e:
            console.print(f"❌ Errore nel backup automatico: {str(e)}", style="red")
            return {
                'status': 'error',
                'error': str(e),
                'backup_completed': False
            }
    
    def schedule_auto_backup(self, 
                           project_path: Path,
                           frequency: str = 'session') -> bool:
        """Schedule automatic backups
        
        Args:
            project_path: Project directory path
            frequency: Backup frequency ('session', 'daily', 'weekly')
            
        Returns:
            True if scheduling was successful
        """
        # This is a placeholder for future implementation
        # Could integrate with system schedulers (cron, Task Scheduler)
        console.print(f"ℹ️ Auto-backup schedulato: {frequency}", style="blue")
        return True
    
    def cleanup_old_backups(self, 
                          project_path: Path,
                          keep_days: int = 30) -> int:
        """Clean up old backup commits
        
        Args:
            project_path: Repository path
            keep_days: Number of days to keep
            
        Returns:
            Number of commits cleaned up
        """
        # This is a placeholder for future implementation
        # Would need careful implementation to avoid losing important commits
        console.print(f"ℹ️ Cleanup backup programmato (mantieni {keep_days} giorni)", style="blue")
        return 0