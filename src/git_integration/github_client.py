"""
GitHub API client for repository management
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from github import Github, GithubException
from rich.console import Console

console = Console()

class GitHubClient:
    """GitHub API client for managing repositories"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.github = None
        self.user = None
        
        if token:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with GitHub"""
        try:
            self.github = Github(self.token)
            self.user = self.github.get_user()
            
            # Test authentication
            _ = self.user.login
            
            console.print(f"✅ Autenticato su GitHub come: {self.user.login}", style="green")
            
        except Exception as e:
            console.print(f"❌ Errore autenticazione GitHub: {str(e)}", style="red")
            self.github = None
            self.user = None
            raise
    
    def set_token(self, token: str):
        """Set GitHub token and authenticate
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self._authenticate()
    
    def is_authenticated(self) -> bool:
        """Check if client is authenticated"""
        return self.github is not None and self.user is not None
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information
        
        Returns:
            User information dictionary
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated with GitHub")
        
        return {
            'login': self.user.login,
            'name': self.user.name,
            'email': self.user.email,
            'avatar_url': self.user.avatar_url,
            'public_repos': self.user.public_repos,
            'private_repos': self.user.total_private_repos,
            'followers': self.user.followers,
            'following': self.user.following
        }
    
    def list_repositories(self, 
                         type: str = 'all', 
                         sort: str = 'updated',
                         limit: int = 50) -> List[Dict[str, Any]]:
        """List user repositories
        
        Args:
            type: Repository type ('all', 'owner', 'public', 'private')
            sort: Sort order ('created', 'updated', 'pushed', 'full_name')
            limit: Maximum number of repositories
            
        Returns:
            List of repository information
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated with GitHub")
        
        try:
            repos = self.user.get_repos(type=type, sort=sort)
            
            repo_list = []
            for i, repo in enumerate(repos):
                if i >= limit:
                    break
                
                repo_info = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'private': repo.private,
                    'html_url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'ssh_url': repo.ssh_url,
                    'default_branch': repo.default_branch,
                    'language': repo.language,
                    'size': repo.size,
                    'created_at': repo.created_at.isoformat() if repo.created_at else None,
                    'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
                    'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None
                }
                
                repo_list.append(repo_info)
            
            return repo_list
            
        except Exception as e:
            console.print(f"❌ Errore nel recupero repository: {str(e)}", style="red")
            raise
    
    def get_repository(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get repository information
        
        Args:
            repo_name: Repository name (user/repo format)
            
        Returns:
            Repository information or None
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated with GitHub")
        
        try:
            repo = self.github.get_repo(repo_name)
            
            return {
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'private': repo.private,
                'html_url': repo.html_url,
                'clone_url': repo.clone_url,
                'ssh_url': repo.ssh_url,
                'default_branch': repo.default_branch,
                'language': repo.language,
                'size': repo.size,
                'created_at': repo.created_at.isoformat() if repo.created_at else None,
                'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
                'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None
            }
            
        except GithubException as e:
            if e.status == 404:
                return None
            raise
        except Exception as e:
            console.print(f"❌ Errore nel recupero repository: {str(e)}", style="red")
            raise
    
    def create_repository(self, 
                         name: str,
                         description: str = "",
                         private: bool = False,
                         auto_init: bool = True,
                         gitignore_template: Optional[str] = None,
                         license_template: Optional[str] = None) -> Dict[str, Any]:
        """Create a new repository
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether repository should be private
            auto_init: Initialize with README
            gitignore_template: Gitignore template to use
            license_template: License template to use
            
        Returns:
            Created repository information
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated with GitHub")
        
        try:
            # Check if repository already exists
            existing = self.get_repository(f"{self.user.login}/{name}")
            if existing:
                raise Exception(f"Repository '{name}' already exists")
            
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init,
                gitignore_template=gitignore_template,
                license_template=license_template
            )
            
            console.print(f"✅ Repository '{name}' creato con successo", style="green")
            
            return {
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'private': repo.private,
                'html_url': repo.html_url,
                'clone_url': repo.clone_url,
                'ssh_url': repo.ssh_url,
                'default_branch': repo.default_branch
            }
            
        except Exception as e:
            console.print(f"❌ Errore nella creazione repository: {str(e)}", style="red")
            raise
    
    def check_repository_exists(self, repo_name: str) -> bool:
        """Check if repository exists
        
        Args:
            repo_name: Repository name (user/repo format)
            
        Returns:
            True if repository exists
        """
        try:
            return self.get_repository(repo_name) is not None
        except:
            return False
    
    def suggest_repository_name(self, project_path: Path) -> str:
        """Suggest repository name based on project path
        
        Args:
            project_path: Project directory path
            
        Returns:
            Suggested repository name
        """
        base_name = project_path.name.lower()
        
        # Clean the name
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9\-_]', '-', base_name)
        clean_name = re.sub(r'-+', '-', clean_name)
        clean_name = clean_name.strip('-')
        
        if not clean_name:
            clean_name = "my-project"
        
        # Check if name is available
        if not self.is_authenticated():
            return clean_name
        
        original_name = clean_name
        counter = 1
        
        while self.check_repository_exists(f"{self.user.login}/{clean_name}"):
            clean_name = f"{original_name}-{counter}"
            counter += 1
        
        return clean_name
    
    def get_gitignore_templates(self) -> List[str]:
        """Get available gitignore templates
        
        Returns:
            List of gitignore template names
        """
        try:
            response = requests.get("https://api.github.com/gitignore/templates")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            console.print(f"⚠️ Impossibile recuperare template gitignore: {str(e)}", style="yellow")
            # Return common templates as fallback
            return [
                'Python', 'Node', 'PHP', 'Java', 'C++', 'C#', 'Go', 'Rust',
                'Swift', 'Kotlin', 'Ruby', 'Laravel', 'Django', 'React',
                'Vue', 'Angular', 'WordPress', 'VisualStudio', 'Xcode'
            ]
    
    def get_license_templates(self) -> List[Dict[str, str]]:
        """Get available license templates
        
        Returns:
            List of license template information
        """
        try:
            response = requests.get("https://api.github.com/licenses")
            response.raise_for_status()
            licenses = response.json()
            
            return [
                {
                    'key': license['key'],
                    'name': license['name'],
                    'spdx_id': license['spdx_id']
                }
                for license in licenses
            ]
        except Exception as e:
            console.print(f"⚠️ Impossibile recuperare template licenze: {str(e)}", style="yellow")
            # Return common licenses as fallback
            return [
                {'key': 'mit', 'name': 'MIT License', 'spdx_id': 'MIT'},
                {'key': 'apache-2.0', 'name': 'Apache License 2.0', 'spdx_id': 'Apache-2.0'},
                {'key': 'gpl-3.0', 'name': 'GNU General Public License v3.0', 'spdx_id': 'GPL-3.0'},
                {'key': 'bsd-3-clause', 'name': 'BSD 3-Clause License', 'spdx_id': 'BSD-3-Clause'},
                {'key': 'unlicense', 'name': 'The Unlicense', 'spdx_id': 'Unlicense'}
            ]
    
    def detect_project_language(self, project_path: Path) -> Optional[str]:
        """Detect primary programming language in project
        
        Args:
            project_path: Project directory path
            
        Returns:
            Detected language or None
        """
        language_indicators = {
            'Python': ['*.py', 'requirements.txt', 'setup.py', 'pyproject.toml'],
            'JavaScript': ['*.js', 'package.json', '*.ts', 'tsconfig.json'],
            'Node': ['package.json', 'yarn.lock', 'package-lock.json'],
            'PHP': ['*.php', 'composer.json', 'composer.lock'],
            'Laravel': ['artisan', 'composer.json'],  # Laravel specific
            'Java': ['*.java', 'pom.xml', 'build.gradle'],
            'C++': ['*.cpp', '*.cc', '*.cxx', '*.h', '*.hpp', 'CMakeLists.txt'],
            'C#': ['*.cs', '*.csproj', '*.sln'],
            'Go': ['*.go', 'go.mod', 'go.sum'],
            'Rust': ['*.rs', 'Cargo.toml', 'Cargo.lock'],
            'Swift': ['*.swift', 'Package.swift'],
            'Kotlin': ['*.kt', '*.kts'],
            'Ruby': ['*.rb', 'Gemfile', 'Gemfile.lock'],
            'Vue': ['*.vue', 'vue.config.js'],
            'React': ['*.jsx', '*.tsx'],
            'Angular': ['angular.json', '*.component.ts']
        }
        
        for language, patterns in language_indicators.items():
            for pattern in patterns:
                if pattern.startswith('*.'):
                    extension = pattern[1:]
                    if any(project_path.rglob(pattern)):
                        return language
                else:
                    if (project_path / pattern).exists():
                        return language
        
        return None
    
    def validate_token(self, token: str) -> bool:
        """Validate GitHub token
        
        Args:
            token: GitHub personal access token
            
        Returns:
            True if token is valid
        """
        try:
            temp_github = Github(token)
            user = temp_github.get_user()
            _ = user.login  # This will raise an exception if token is invalid
            return True
        except Exception:
            return False