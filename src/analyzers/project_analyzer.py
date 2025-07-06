"""
Analizzatore struttura progetto
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    calculate_file_stats, 
    is_text_file, 
    get_file_extension,
    find_files_by_extension,
    detect_git_repo,
    get_project_name
)


class ProjectAnalyzer:
    """Analizza struttura e caratteristiche del progetto"""
    
    def __init__(self):
        self.ignored_dirs = {
            'node_modules', '.git', '__pycache__', '.pytest_cache',
            'venv', 'env', '.env', 'vendor', 'dist', 'build',
            '.next', '.nuxt', '.cache', 'coverage', '.coverage',
            '.tox', '.mypy_cache', '.DS_Store', 'Thumbs.db'
        }
        
        self.project_indicators = {
            'web': ['index.html', 'package.json', 'webpack.config.js', 'vite.config.js'],
            'api': ['api/', 'routes/', 'controllers/', 'app.py', 'server.js'],
            'mobile': ['android/', 'ios/', 'react-native/', 'flutter/'],
            'desktop': ['electron/', 'main.py', 'setup.py', 'Cargo.toml'],
            'library': ['lib/', 'src/lib/', 'setup.py', 'pyproject.toml', 'Cargo.toml'],
            'documentation': ['docs/', 'README.md', 'mkdocs.yml', 'docusaurus.config.js'],
            'data': ['notebooks/', '*.ipynb', 'data/', 'datasets/'],
            'game': ['unity/', 'godot/', 'assets/textures/', 'src/game/'],
            'blockchain': ['contracts/', 'truffle-config.js', 'hardhat.config.js'],
            'ai': ['models/', 'training/', 'ml/', 'ai/', '*.ipynb', 'requirements.txt']
        }
        
        self.complexity_indicators = {
            'high': ['microservices/', 'kubernetes/', 'docker-compose.yml', 'terraform/'],
            'medium': ['tests/', 'docs/', 'config/', 'scripts/'],
            'low': ['simple structure', 'single file']
        }
    
    def analyze_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analizza struttura completa del progetto"""
        
        # Statistiche base
        stats = calculate_file_stats(project_path)
        
        # Analisi directory
        directories = self._analyze_directories(project_path)
        
        # Rilevamento tipo progetto
        project_type = self._detect_project_type(project_path, directories)
        
        # Analisi complessità
        complexity = self._analyze_complexity(project_path, directories, stats)
        
        # Analisi architettura
        architecture = self._analyze_architecture(project_path, directories)
        
        # Analisi dipendenze
        dependencies = self._analyze_dependencies(project_path)
        
        return {
            'type': project_type,
            'complexity': complexity,
            'architecture': architecture,
            'directories': directories,
            'dependencies': dependencies,
            'stats': stats,
            'files_count': stats['total_files'],
            'has_tests': self._has_tests(project_path),
            'has_docs': self._has_docs(project_path),
            'has_config': self._has_config(project_path),
            'is_git_repo': detect_git_repo(project_path),
            'project_name': get_project_name(project_path)
        }
    
    def detect_languages(self, project_path: Path) -> List[str]:
        """Rileva linguaggi di programmazione utilizzati"""
        language_extensions = {
            'javascript': ['.js', '.jsx', '.mjs'],
            'typescript': ['.ts', '.tsx'],
            'python': ['.py', '.pyx'],
            'php': ['.php'],
            'java': ['.java'],
            'c#': ['.cs'],
            'c++': ['.cpp', '.cc', '.cxx'],
            'c': ['.c'],
            'go': ['.go'],
            'rust': ['.rs'],
            'ruby': ['.rb'],
            'swift': ['.swift'],
            'kotlin': ['.kt'],
            'dart': ['.dart'],
            'scala': ['.scala'],
            'r': ['.r'],
            'matlab': ['.m'],
            'shell': ['.sh', '.bash'],
            'powershell': ['.ps1'],
            'sql': ['.sql'],
            'html': ['.html', '.htm'],
            'css': ['.css', '.scss', '.sass'],
            'xml': ['.xml'],
            'json': ['.json'],
            'yaml': ['.yml', '.yaml'],
            'markdown': ['.md']
        }
        
        extension_counts = Counter()
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and not self._is_ignored_file(file_path):
                ext = get_file_extension(file_path)
                extension_counts[ext] += 1
        
        detected_languages = []
        for language, extensions in language_extensions.items():
            if any(ext in extension_counts for ext in extensions):
                detected_languages.append(language)
        
        # Ordina per frequenza
        language_scores = {}
        for language, extensions in language_extensions.items():
            if language in detected_languages:
                score = sum(extension_counts.get(ext, 0) for ext in extensions)
                language_scores[language] = score
        
        return sorted(detected_languages, key=lambda x: language_scores.get(x, 0), reverse=True)
    
    def _analyze_directories(self, project_path: Path) -> Dict[str, Any]:
        """Analizza struttura directory"""
        directories = {
            'root_dirs': [],
            'src_structure': {},
            'test_structure': {},
            'config_structure': {},
            'depth': 0
        }
        
        max_depth = 0
        
        for item in project_path.rglob('*'):
            if item.is_dir() and not self._is_ignored_dir(item):
                rel_path = item.relative_to(project_path)
                depth = len(rel_path.parts)
                max_depth = max(max_depth, depth)
                
                # Directory radice
                if depth == 1:
                    directories['root_dirs'].append(str(rel_path))
                
                # Struttura src
                if 'src' in str(rel_path).lower():
                    directories['src_structure'][str(rel_path)] = len(list(item.iterdir()))
                
                # Struttura test
                if any(test_word in str(rel_path).lower() for test_word in ['test', 'spec', '__tests__']):
                    directories['test_structure'][str(rel_path)] = len(list(item.iterdir()))
                
                # Struttura config
                if any(config_word in str(rel_path).lower() for config_word in ['config', 'conf', 'settings']):
                    directories['config_structure'][str(rel_path)] = len(list(item.iterdir()))
        
        directories['depth'] = max_depth
        return directories
    
    def _detect_project_type(self, project_path: Path, directories: Dict) -> str:
        """Rileva tipo di progetto"""
        type_scores = defaultdict(int)
        
        # Analizza file e directory indicatori
        for project_type, indicators in self.project_indicators.items():
            for indicator in indicators:
                if indicator.endswith('/'):
                    # Directory indicator
                    dir_name = indicator.rstrip('/')
                    if any(dir_name in d for d in directories['root_dirs']):
                        type_scores[project_type] += 2
                elif '*' in indicator:
                    # Pattern indicator
                    pattern = indicator.replace('*', '.*')
                    if any(re.match(pattern, str(f)) for f in project_path.rglob('*')):
                        type_scores[project_type] += 1
                else:
                    # File indicator
                    if (project_path / indicator).exists():
                        type_scores[project_type] += 3
        
        # Analisi specifica per tipo web
        if (project_path / 'package.json').exists():
            package_json = project_path / 'package.json'
            try:
                import json
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    
                    if any(key in deps for key in ['react', 'vue', 'angular', 'svelte']):
                        type_scores['web'] += 3
                    if any(key in deps for key in ['express', 'koa', 'fastify']):
                        type_scores['api'] += 3
                    if any(key in deps for key in ['electron', 'tauri']):
                        type_scores['desktop'] += 3
            except:
                pass
        
        # Analisi specifica per tipo API
        if any('api' in d.lower() for d in directories['root_dirs']):
            type_scores['api'] += 2
        
        # Restituisce tipo con score maggiore
        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        
        return 'unknown'
    
    def _analyze_complexity(self, project_path: Path, directories: Dict, stats: Dict) -> str:
        """Analizza complessità del progetto"""
        complexity_score = 0
        
        # Basato su numero di file
        if stats['total_files'] > 1000:
            complexity_score += 3
        elif stats['total_files'] > 100:
            complexity_score += 2
        elif stats['total_files'] > 20:
            complexity_score += 1
        
        # Basato su profondità directory
        if directories['depth'] > 8:
            complexity_score += 3
        elif directories['depth'] > 5:
            complexity_score += 2
        elif directories['depth'] > 3:
            complexity_score += 1
        
        # Basato su indicatori specifici
        for complexity_level, indicators in self.complexity_indicators.items():
            for indicator in indicators:
                if indicator.endswith('/'):
                    if any(indicator.rstrip('/') in d for d in directories['root_dirs']):
                        if complexity_level == 'high':
                            complexity_score += 3
                        elif complexity_level == 'medium':
                            complexity_score += 2
                else:
                    if (project_path / indicator).exists():
                        if complexity_level == 'high':
                            complexity_score += 3
                        elif complexity_level == 'medium':
                            complexity_score += 2
        
        # Determina livello complessità
        if complexity_score >= 8:
            return 'high'
        elif complexity_score >= 4:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_architecture(self, project_path: Path, directories: Dict) -> Dict[str, Any]:
        """Analizza architettura del progetto"""
        architecture = {
            'pattern': 'unknown',
            'layers': [],
            'has_separation': False,
            'has_modules': False
        }
        
        # Rilevamento pattern architetturali
        root_dirs = [d.lower() for d in directories['root_dirs']]
        
        # MVC Pattern
        if all(layer in root_dirs for layer in ['models', 'views', 'controllers']):
            architecture['pattern'] = 'mvc'
            architecture['layers'] = ['models', 'views', 'controllers']
            architecture['has_separation'] = True
        
        # Layered Architecture
        elif all(layer in ' '.join(root_dirs) for layer in ['controller', 'service', 'repository']):
            architecture['pattern'] = 'layered'
            architecture['layers'] = ['controller', 'service', 'repository']
            architecture['has_separation'] = True
        
        # Modular Architecture
        elif any(d in root_dirs for d in ['modules', 'components', 'features']):
            architecture['pattern'] = 'modular'
            architecture['has_modules'] = True
        
        # Microservices
        elif any(d in root_dirs for d in ['services', 'microservices']):
            architecture['pattern'] = 'microservices'
            architecture['has_modules'] = True
        
        return architecture
    
    def _analyze_dependencies(self, project_path: Path) -> Dict[str, Any]:
        """Analizza dipendenze del progetto"""
        dependencies = {
            'package_managers': [],
            'dependency_files': [],
            'total_dependencies': 0
        }
        
        # Controlla file di dipendenze
        dep_files = {
            'package.json': 'npm/yarn',
            'composer.json': 'composer',
            'requirements.txt': 'pip',
            'Pipfile': 'pipenv',
            'poetry.lock': 'poetry',
            'Cargo.toml': 'cargo',
            'go.mod': 'go modules',
            'Gemfile': 'bundler',
            'pom.xml': 'maven',
            'build.gradle': 'gradle'
        }
        
        for file_name, manager in dep_files.items():
            if (project_path / file_name).exists():
                dependencies['package_managers'].append(manager)
                dependencies['dependency_files'].append(file_name)
                
                # Conta dipendenze se possibile
                if file_name == 'package.json':
                    try:
                        import json
                        with open(project_path / file_name, 'r') as f:
                            data = json.load(f)
                            deps = len(data.get('dependencies', {}))
                            dev_deps = len(data.get('devDependencies', {}))
                            dependencies['total_dependencies'] += deps + dev_deps
                    except:
                        pass
        
        return dependencies
    
    def _has_tests(self, project_path: Path) -> bool:
        """Verifica presenza di test"""
        test_indicators = [
            'test/', 'tests/', '__tests__/', 'spec/', 'specs/',
            'test_*.py', '*_test.py', '*.test.js', '*.spec.js'
        ]
        
        for indicator in test_indicators:
            if indicator.endswith('/'):
                if (project_path / indicator.rstrip('/')).exists():
                    return True
            else:
                if list(project_path.rglob(indicator)):
                    return True
        
        return False
    
    def _has_docs(self, project_path: Path) -> bool:
        """Verifica presenza di documentazione"""
        doc_indicators = [
            'docs/', 'documentation/', 'README.md', 'readme.md',
            'CHANGELOG.md', 'API.md', 'mkdocs.yml'
        ]
        
        return any((project_path / indicator).exists() for indicator in doc_indicators)
    
    def _has_config(self, project_path: Path) -> bool:
        """Verifica presenza di configurazione"""
        config_indicators = [
            'config/', 'configuration/', '.env', '.env.example',
            'settings.py', 'config.js', 'app.config.js'
        ]
        
        return any((project_path / indicator).exists() for indicator in config_indicators)
    
    def _is_ignored_dir(self, path: Path) -> bool:
        """Verifica se directory deve essere ignorata"""
        return path.name in self.ignored_dirs
    
    def _is_ignored_file(self, path: Path) -> bool:
        """Verifica se file deve essere ignorato"""
        if path.name.startswith('.'):
            return True
        
        ignored_extensions = {'.pyc', '.pyo', '.log', '.tmp', '.temp'}
        return get_file_extension(path) in ignored_extensions