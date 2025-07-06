"""
Advanced project detection and path discovery system
"""

import os
import fnmatch
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from datetime import datetime
import json
from rich.console import Console
from rich.progress import Progress, track

console = Console()

class ProjectDetector:
    """Advanced project detection and path discovery"""
    
    def __init__(self, preferences_manager=None):
        """Initialize project detector
        
        Args:
            preferences_manager: PreferencesManager instance for user paths
        """
        self.preferences_manager = preferences_manager
        
        # Default search paths
        self.default_paths = [
            "/mnt/c/xampp/htdocs",
            "/mnt/c/Users",
            "/mnt/c/projects",
            "/mnt/c/dev",
            "/mnt/c/code",
            "~/projects",
            "~/development",
            "~/code",
            "~/workspace"
        ]
        
        # Project indicators by framework/language
        self.project_indicators = {
            'php_laravel': {
                'files': ['artisan', 'composer.json'],
                'directories': ['app', 'routes', 'resources'],
                'patterns': ['*.php']
            },
            'php_symfony': {
                'files': ['composer.json', 'symfony.lock'],
                'directories': ['src', 'config'],
                'patterns': ['*.php']
            },
            'javascript_react': {
                'files': ['package.json'],
                'directories': ['src', 'public'],
                'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
                'content_check': ['react', 'jsx']
            },
            'javascript_vue': {
                'files': ['package.json', 'vue.config.js'],
                'directories': ['src'],
                'patterns': ['*.vue', '*.js'],
                'content_check': ['vue']
            },
            'javascript_angular': {
                'files': ['angular.json', 'package.json'],
                'directories': ['src/app'],
                'patterns': ['*.ts', '*.component.ts']
            },
            'javascript_node': {
                'files': ['package.json'],
                'directories': ['src', 'lib'],
                'patterns': ['*.js', '*.ts'],
                'exclude_indicators': ['react', 'vue', 'angular']
            },
            'python_django': {
                'files': ['manage.py', 'requirements.txt'],
                'directories': ['apps', 'templates'],
                'patterns': ['*.py']
            },
            'python_flask': {
                'files': ['app.py', 'requirements.txt'],
                'patterns': ['*.py'],
                'content_check': ['flask']
            },
            'python_fastapi': {
                'files': ['main.py', 'requirements.txt'],
                'patterns': ['*.py'],
                'content_check': ['fastapi']
            },
            'python_general': {
                'files': ['requirements.txt', 'setup.py', 'pyproject.toml'],
                'patterns': ['*.py']
            },
            'dotnet': {
                'files': ['*.csproj', '*.sln'],
                'patterns': ['*.cs']
            },
            'java_spring': {
                'files': ['pom.xml', 'build.gradle'],
                'directories': ['src/main/java'],
                'patterns': ['*.java'],
                'content_check': ['spring']
            },
            'java_general': {
                'files': ['pom.xml', 'build.gradle'],
                'directories': ['src'],
                'patterns': ['*.java']
            },
            'go': {
                'files': ['go.mod', 'go.sum'],
                'patterns': ['*.go']
            },
            'rust': {
                'files': ['Cargo.toml', 'Cargo.lock'],
                'directories': ['src'],
                'patterns': ['*.rs']
            },
            'mobile_flutter': {
                'files': ['pubspec.yaml'],
                'directories': ['lib', 'android', 'ios'],
                'patterns': ['*.dart']
            },
            'mobile_react_native': {
                'files': ['package.json', 'metro.config.js'],
                'directories': ['android', 'ios'],
                'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx']
            },
            'wordpress': {
                'files': ['wp-config.php', 'wp-load.php'],
                'directories': ['wp-content', 'wp-admin'],
                'patterns': ['*.php']
            },
            'static_site': {
                'files': ['index.html'],
                'patterns': ['*.html', '*.css', '*.js']
            }
        }
    
    def get_search_paths(self) -> List[Path]:
        """Get list of paths to search for projects
        
        Returns:
            List of Path objects to search
        """
        paths = self.default_paths.copy()
        
        # Add user-configured paths
        if self.preferences_manager:
            user_paths = self.preferences_manager.get_preference(
                'directories.default_project_paths', []
            )
            paths.extend(user_paths)
        
        # Expand user paths and resolve
        resolved_paths = []
        for path_str in paths:
            try:
                if path_str.startswith('~'):
                    path = Path(path_str).expanduser()
                else:
                    path = Path(path_str)
                
                if path.exists() and path.is_dir():
                    resolved_paths.append(path)
            except Exception:
                continue
        
        # Remove duplicates while preserving order
        seen = set()
        unique_paths = []
        for path in resolved_paths:
            if path not in seen:
                seen.add(path)
                unique_paths.append(path)
        
        return unique_paths
    
    def scan_for_projects(self, 
                         max_depth: int = 3,
                         include_hidden: bool = False,
                         progress_callback: Optional[callable] = None) -> List[Dict[str, Any]]:
        """Scan for projects in configured paths
        
        Args:
            max_depth: Maximum directory depth to scan
            include_hidden: Whether to include hidden directories
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of detected projects
        """
        projects = []
        search_paths = self.get_search_paths()
        
        console.print(f"🔍 Scansione progetti in {len(search_paths)} percorsi...", style="blue")
        
        with Progress() as progress:
            task = progress.add_task("Scansione in corso...", total=len(search_paths))
            
            for search_path in search_paths:
                console.print(f"  📁 Scansione: {search_path}", style="dim")
                
                try:
                    path_projects = self._scan_path(
                        search_path, 
                        max_depth=max_depth,
                        include_hidden=include_hidden
                    )
                    projects.extend(path_projects)
                except Exception as e:
                    console.print(f"  ⚠️ Errore scansione {search_path}: {str(e)}", style="yellow")
                
                progress.update(task, advance=1)
                
                if progress_callback:
                    progress_callback(len(projects))
        
        # Remove duplicates and sort by last modified
        unique_projects = self._deduplicate_projects(projects)
        sorted_projects = sorted(
            unique_projects, 
            key=lambda x: x.get('last_modified', ''), 
            reverse=True
        )
        
        console.print(f"✅ Trovati {len(sorted_projects)} progetti", style="green")
        
        return sorted_projects
    
    def _scan_path(self, 
                   path: Path, 
                   max_depth: int,
                   include_hidden: bool,
                   current_depth: int = 0) -> List[Dict[str, Any]]:
        """Recursively scan a path for projects
        
        Args:
            path: Path to scan
            max_depth: Maximum scan depth
            include_hidden: Include hidden directories
            current_depth: Current recursion depth
            
        Returns:
            List of detected projects in this path
        """
        projects = []
        
        if current_depth > max_depth:
            return projects
        
        try:
            # Check if current directory is a project
            project_info = self.detect_project_type(path)
            if project_info:
                project_info['path'] = str(path)
                project_info['last_modified'] = self._get_last_modified(path)
                project_info['size'] = self._estimate_project_size(path)
                projects.append(project_info)
        except Exception:
            pass
        
        # Scan subdirectories
        try:
            for item in path.iterdir():
                if not item.is_dir():
                    continue
                
                # Skip hidden directories unless explicitly included
                if item.name.startswith('.') and not include_hidden:
                    continue
                
                # Skip common non-project directories
                if item.name.lower() in {
                    'node_modules', 'vendor', '__pycache__', '.git', 
                    '.vscode', '.idea', 'dist', 'build', 'target',
                    'bin', 'obj', '.next', '.nuxt'
                }:
                    continue
                
                # Recursive scan
                subprojects = self._scan_path(
                    item, max_depth, include_hidden, current_depth + 1
                )
                projects.extend(subprojects)
                
        except PermissionError:
            pass
        except Exception:
            pass
        
        return projects
    
    def detect_project_type(self, path: Path) -> Optional[Dict[str, Any]]:
        """Detect project type and gather information
        
        Args:
            path: Project directory path
            
        Returns:
            Project information dictionary or None
        """
        if not path.is_dir():
            return None
        
        # Check against each project type
        for project_type, indicators in self.project_indicators.items():
            if self._matches_indicators(path, indicators):
                return {
                    'name': path.name,
                    'type': project_type,
                    'language': self._extract_language(project_type),
                    'framework': self._extract_framework(project_type),
                    'confidence': self._calculate_confidence(path, indicators),
                    'description': self._generate_description(path, project_type),
                    'has_git': (path / '.git').exists(),
                    'has_context_engineering': (path / 'CLAUDE.md').exists()
                }
        
        return None
    
    def _matches_indicators(self, path: Path, indicators: Dict[str, Any]) -> bool:
        """Check if path matches project indicators
        
        Args:
            path: Project path
            indicators: Indicator configuration
            
        Returns:
            True if path matches indicators
        """
        # Check required files
        if 'files' in indicators:
            file_matches = 0
            for file_pattern in indicators['files']:
                if '*' in file_pattern:
                    matches = list(path.glob(file_pattern))
                    if matches:
                        file_matches += 1
                else:
                    if (path / file_pattern).exists():
                        file_matches += 1
            
            # Require at least one file match
            if file_matches == 0:
                return False
        
        # Check required directories
        if 'directories' in indicators:
            for dir_name in indicators['directories']:
                if not (path / dir_name).exists():
                    return False
        
        # Check pattern files exist
        if 'patterns' in indicators:
            pattern_found = False
            for pattern in indicators['patterns']:
                if list(path.rglob(pattern)):
                    pattern_found = True
                    break
            
            if not pattern_found:
                return False
        
        # Check content for specific keywords
        if 'content_check' in indicators:
            content_found = self._check_content_keywords(path, indicators['content_check'])
            if not content_found:
                return False
        
        # Check exclusion indicators
        if 'exclude_indicators' in indicators:
            for exclude_keyword in indicators['exclude_indicators']:
                if self._check_content_keywords(path, [exclude_keyword]):
                    return False
        
        return True
    
    def _check_content_keywords(self, path: Path, keywords: List[str]) -> bool:
        """Check if any file contains specific keywords
        
        Args:
            path: Directory path
            keywords: Keywords to search for
            
        Returns:
            True if keywords found in files
        """
        # Check common configuration files
        config_files = [
            'package.json', 'composer.json', 'requirements.txt',
            'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle'
        ]
        
        for config_file in config_files:
            file_path = path / config_file
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                    for keyword in keywords:
                        if keyword.lower() in content:
                            return True
                except Exception:
                    continue
        
        return False
    
    def _extract_language(self, project_type: str) -> str:
        """Extract primary language from project type
        
        Args:
            project_type: Project type string
            
        Returns:
            Primary programming language
        """
        if project_type.startswith('php'):
            return 'php'
        elif project_type.startswith('javascript'):
            return 'javascript'
        elif project_type.startswith('python'):
            return 'python'
        elif project_type.startswith('java'):
            return 'java'
        elif 'dotnet' in project_type:
            return 'csharp'
        elif project_type == 'go':
            return 'go'
        elif project_type == 'rust':
            return 'rust'
        elif 'flutter' in project_type:
            return 'dart'
        else:
            return 'unknown'
    
    def _extract_framework(self, project_type: str) -> Optional[str]:
        """Extract framework from project type
        
        Args:
            project_type: Project type string
            
        Returns:
            Framework name or None
        """
        parts = project_type.split('_')
        if len(parts) > 1:
            return parts[1]
        return None
    
    def _calculate_confidence(self, path: Path, indicators: Dict[str, Any]) -> float:
        """Calculate confidence score for project detection
        
        Args:
            path: Project path
            indicators: Project indicators
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 0.0
        total_checks = 0
        
        # File indicators
        if 'files' in indicators:
            for file_pattern in indicators['files']:
                total_checks += 1
                if '*' in file_pattern:
                    if list(path.glob(file_pattern)):
                        score += 1
                else:
                    if (path / file_pattern).exists():
                        score += 1
        
        # Directory indicators
        if 'directories' in indicators:
            for dir_name in indicators['directories']:
                total_checks += 1
                if (path / dir_name).exists():
                    score += 1
        
        # Pattern indicators
        if 'patterns' in indicators:
            total_checks += 1
            for pattern in indicators['patterns']:
                if list(path.rglob(pattern)):
                    score += 1
                    break
        
        return score / total_checks if total_checks > 0 else 0.0
    
    def _generate_description(self, path: Path, project_type: str) -> str:
        """Generate project description
        
        Args:
            path: Project path
            project_type: Detected project type
            
        Returns:
            Project description
        """
        language = self._extract_language(project_type)
        framework = self._extract_framework(project_type)
        
        if framework:
            return f"Progetto {language.title()} con framework {framework.title()}"
        else:
            return f"Progetto {language.title()}"
    
    def _get_last_modified(self, path: Path) -> str:
        """Get last modification time of project
        
        Args:
            path: Project path
            
        Returns:
            ISO format timestamp
        """
        try:
            # Get the most recent modification time from project files
            latest_time = path.stat().st_mtime
            
            # Check a few key files for more recent modifications
            check_files = ['CLAUDE.md', 'package.json', 'composer.json', 'requirements.txt']
            for filename in check_files:
                file_path = path / filename
                if file_path.exists():
                    file_time = file_path.stat().st_mtime
                    latest_time = max(latest_time, file_time)
            
            return datetime.fromtimestamp(latest_time).isoformat()
        except Exception:
            return datetime.now().isoformat()
    
    def _estimate_project_size(self, path: Path) -> Dict[str, int]:
        """Estimate project size metrics
        
        Args:
            path: Project path
            
        Returns:
            Size metrics dictionary
        """
        try:
            file_count = 0
            total_size = 0
            
            # Count files and size (excluding common large directories)
            exclude_dirs = {'.git', 'node_modules', 'vendor', '__pycache__', 'dist', 'build'}
            
            for item in path.rglob('*'):
                # Skip if parent directory is in exclude list
                if any(part in exclude_dirs for part in item.parts):
                    continue
                
                if item.is_file():
                    file_count += 1
                    try:
                        total_size += item.stat().st_size
                    except Exception:
                        pass
            
            return {
                'files': file_count,
                'size_bytes': total_size,
                'size_mb': round(total_size / (1024 * 1024), 2)
            }
        except Exception:
            return {'files': 0, 'size_bytes': 0, 'size_mb': 0}
    
    def _deduplicate_projects(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate projects from list
        
        Args:
            projects: List of project dictionaries
            
        Returns:
            Deduplicated list
        """
        seen_paths = set()
        unique_projects = []
        
        for project in projects:
            path = project.get('path', '')
            if path not in seen_paths:
                seen_paths.add(path)
                unique_projects.append(project)
        
        return unique_projects
    
    def filter_projects(self, 
                       projects: List[Dict[str, Any]],
                       language: Optional[str] = None,
                       framework: Optional[str] = None,
                       has_git: Optional[bool] = None,
                       has_context_engineering: Optional[bool] = None,
                       min_confidence: float = 0.0) -> List[Dict[str, Any]]:
        """Filter projects by criteria
        
        Args:
            projects: List of projects to filter
            language: Filter by programming language
            framework: Filter by framework
            has_git: Filter by Git presence
            has_context_engineering: Filter by CLAUDE.md presence
            min_confidence: Minimum confidence score
            
        Returns:
            Filtered list of projects
        """
        filtered = []
        
        for project in projects:
            # Language filter
            if language and project.get('language', '').lower() != language.lower():
                continue
            
            # Framework filter
            if framework and project.get('framework', '').lower() != framework.lower():
                continue
            
            # Git filter
            if has_git is not None and project.get('has_git', False) != has_git:
                continue
            
            # Context Engineering filter
            if (has_context_engineering is not None and 
                project.get('has_context_engineering', False) != has_context_engineering):
                continue
            
            # Confidence filter
            if project.get('confidence', 0.0) < min_confidence:
                continue
            
            filtered.append(project)
        
        return filtered
    
    def export_projects_list(self, projects: List[Dict[str, Any]], file_path: Path):
        """Export projects list to JSON file
        
        Args:
            projects: List of projects to export
            file_path: Export file path
        """
        export_data = {
            'projects': projects,
            'exported_at': datetime.now().isoformat(),
            'total_projects': len(projects)
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"✅ Lista progetti esportata in: {file_path}", style="green")