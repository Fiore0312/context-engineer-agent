"""
Rilevatore framework e tecnologie
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_json, read_file


class FrameworkDetector:
    """Rileva framework e tecnologie utilizzate nel progetto"""
    
    def __init__(self):
        self.framework_patterns = {
            # Frontend Frameworks
            'react': {
                'files': ['package.json'],
                'dependencies': ['react', 'react-dom'],
                'patterns': ['import.*from.*react', 'jsx', 'tsx'],
                'config_files': ['webpack.config.js', 'vite.config.js', 'craco.config.js']
            },
            'vue': {
                'files': ['package.json'],
                'dependencies': ['vue', '@vue/cli'],
                'patterns': ['<template>', '<script>', '<style>'],
                'config_files': ['vue.config.js', 'vite.config.js']
            },
            'angular': {
                'files': ['package.json', 'angular.json'],
                'dependencies': ['@angular/core', '@angular/cli'],
                'patterns': ['@Component', '@Injectable', '@NgModule'],
                'config_files': ['angular.json', 'tsconfig.json']
            },
            'svelte': {
                'files': ['package.json'],
                'dependencies': ['svelte'],
                'patterns': ['<script>', '<style>', '<div>'],
                'config_files': ['svelte.config.js', 'vite.config.js']
            },
            'next': {
                'files': ['package.json'],
                'dependencies': ['next'],
                'patterns': ['pages/', 'app/', 'getServerSideProps'],
                'config_files': ['next.config.js']
            },
            'nuxt': {
                'files': ['package.json'],
                'dependencies': ['nuxt'],
                'patterns': ['pages/', 'layouts/', 'plugins/'],
                'config_files': ['nuxt.config.js']
            },
            
            # Backend Frameworks
            'express': {
                'files': ['package.json'],
                'dependencies': ['express'],
                'patterns': ['app.use', 'app.get', 'app.post', 'require.*express'],
                'config_files': ['server.js', 'app.js', 'index.js']
            },
            'fastify': {
                'files': ['package.json'],
                'dependencies': ['fastify'],
                'patterns': ['fastify.register', 'fastify.get', 'fastify.post'],
                'config_files': ['server.js', 'app.js']
            },
            'koa': {
                'files': ['package.json'],
                'dependencies': ['koa'],
                'patterns': ['app.use', 'ctx.body', 'require.*koa'],
                'config_files': ['app.js', 'server.js']
            },
            'nestjs': {
                'files': ['package.json'],
                'dependencies': ['@nestjs/core', '@nestjs/common'],
                'patterns': ['@Controller', '@Injectable', '@Module'],
                'config_files': ['nest-cli.json', 'main.ts']
            },
            
            # PHP Frameworks
            'laravel': {
                'files': ['composer.json', 'artisan'],
                'dependencies': ['laravel/framework'],
                'patterns': ['<?php', 'namespace App', 'use Illuminate'],
                'config_files': ['config/app.php', 'routes/web.php', '.env']
            },
            'symfony': {
                'files': ['composer.json'],
                'dependencies': ['symfony/framework-bundle'],
                'patterns': ['namespace App', 'use Symfony'],
                'config_files': ['config/services.yaml', 'bin/console']
            },
            'codeigniter': {
                'files': ['composer.json'],
                'dependencies': ['codeigniter4/framework'],
                'patterns': ['class.*extends.*Controller', 'CI_Controller'],
                'config_files': ['app/Config/', 'system/']
            },
            
            # Python Frameworks
            'django': {
                'files': ['requirements.txt', 'manage.py'],
                'dependencies': ['Django'],
                'patterns': ['from django', 'import django', 'INSTALLED_APPS'],
                'config_files': ['settings.py', 'urls.py', 'wsgi.py']
            },
            'flask': {
                'files': ['requirements.txt'],
                'dependencies': ['Flask'],
                'patterns': ['from flask', 'app = Flask', '@app.route'],
                'config_files': ['app.py', 'main.py', 'run.py']
            },
            'fastapi': {
                'files': ['requirements.txt'],
                'dependencies': ['fastapi'],
                'patterns': ['from fastapi', 'app = FastAPI', '@app.get'],
                'config_files': ['main.py', 'app.py']
            },
            'tornado': {
                'files': ['requirements.txt'],
                'dependencies': ['tornado'],
                'patterns': ['import tornado', 'tornado.web'],
                'config_files': ['app.py', 'main.py']
            },
            
            # Mobile Frameworks
            'react-native': {
                'files': ['package.json'],
                'dependencies': ['react-native'],
                'patterns': ['import.*react-native', 'AppRegistry'],
                'config_files': ['metro.config.js', 'index.js']
            },
            'flutter': {
                'files': ['pubspec.yaml'],
                'dependencies': ['flutter'],
                'patterns': ['import.*flutter', 'StatelessWidget', 'StatefulWidget'],
                'config_files': ['pubspec.yaml', 'analysis_options.yaml']
            },
            
            # Desktop Frameworks
            'electron': {
                'files': ['package.json'],
                'dependencies': ['electron'],
                'patterns': ['require.*electron', 'BrowserWindow'],
                'config_files': ['main.js', 'preload.js']
            },
            'tauri': {
                'files': ['Cargo.toml', 'tauri.conf.json'],
                'dependencies': ['tauri'],
                'patterns': ['#[tauri::command]', 'tauri::'],
                'config_files': ['tauri.conf.json']
            },
            
            # CSS Frameworks
            'tailwind': {
                'files': ['package.json'],
                'dependencies': ['tailwindcss'],
                'patterns': ['@tailwind', 'tailwind.config'],
                'config_files': ['tailwind.config.js']
            },
            'bootstrap': {
                'files': ['package.json'],
                'dependencies': ['bootstrap'],
                'patterns': ['import.*bootstrap', 'class.*btn'],
                'config_files': []
            },
            
            # Build Tools
            'webpack': {
                'files': ['package.json'],
                'dependencies': ['webpack'],
                'patterns': ['module.exports', 'entry:', 'output:'],
                'config_files': ['webpack.config.js']
            },
            'vite': {
                'files': ['package.json'],
                'dependencies': ['vite'],
                'patterns': ['import.meta.env', 'defineConfig'],
                'config_files': ['vite.config.js', 'vite.config.ts']
            },
            'rollup': {
                'files': ['package.json'],
                'dependencies': ['rollup'],
                'patterns': ['export default', 'input:', 'output:'],
                'config_files': ['rollup.config.js']
            }
        }
    
    def detect(self, project_path: Path) -> Dict[str, Any]:
        """Rileva framework utilizzati nel progetto"""
        detected_frameworks = {}
        confidence_scores = {}
        
        for framework, config in self.framework_patterns.items():
            score = self._calculate_framework_score(project_path, framework, config)
            if score > 0:
                detected_frameworks[framework] = score
                confidence_scores[framework] = self._calculate_confidence(score)
        
        # Ordina per score
        sorted_frameworks = sorted(detected_frameworks.items(), key=lambda x: x[1], reverse=True)
        
        primary_framework = sorted_frameworks[0][0] if sorted_frameworks else 'unknown'
        
        return {
            'primary': primary_framework,
            'all': dict(sorted_frameworks),
            'confidence_scores': confidence_scores,
            'categories': self._categorize_frameworks(detected_frameworks.keys()),
            'tech_stack': self._build_tech_stack(detected_frameworks.keys())
        }
    
    def _calculate_framework_score(self, project_path: Path, framework: str, config: Dict) -> int:
        """Calcola score per un framework specifico"""
        score = 0
        
        # Controlla file richiesti
        for file_name in config.get('files', []):
            if (project_path / file_name).exists():
                score += 3
        
        # Controlla dipendenze
        for dep_file in ['package.json', 'composer.json', 'requirements.txt', 'Cargo.toml']:
            if (project_path / dep_file).exists():
                dependencies = self._extract_dependencies(project_path / dep_file)
                for dep in config.get('dependencies', []):
                    if dep in dependencies:
                        score += 5
        
        # Controlla pattern nel codice
        for pattern in config.get('patterns', []):
            if self._find_pattern_in_project(project_path, pattern):
                score += 2
        
        # Controlla file di configurazione
        for config_file in config.get('config_files', []):
            if (project_path / config_file).exists():
                score += 2
        
        return score
    
    def _extract_dependencies(self, file_path: Path) -> Set[str]:
        """Estrae dipendenze da file di configurazione"""
        dependencies = set()
        
        if file_path.name == 'package.json':
            try:
                data = load_json(file_path)
                dependencies.update(data.get('dependencies', {}).keys())
                dependencies.update(data.get('devDependencies', {}).keys())
            except:
                pass
        
        elif file_path.name == 'composer.json':
            try:
                data = load_json(file_path)
                dependencies.update(data.get('require', {}).keys())
                dependencies.update(data.get('require-dev', {}).keys())
            except:
                pass
        
        elif file_path.name == 'requirements.txt':
            try:
                content = read_file(file_path)
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Estrae nome package (prima di ==, >=, etc.)
                        dep_name = re.split(r'[=<>!]', line)[0].strip()
                        dependencies.add(dep_name)
            except:
                pass
        
        elif file_path.name == 'Cargo.toml':
            try:
                content = read_file(file_path)
                # Parsing semplificato di TOML
                in_dependencies = False
                for line in content.split('\n'):
                    line = line.strip()
                    if line == '[dependencies]':
                        in_dependencies = True
                    elif line.startswith('[') and line != '[dependencies]':
                        in_dependencies = False
                    elif in_dependencies and '=' in line:
                        dep_name = line.split('=')[0].strip()
                        dependencies.add(dep_name)
            except:
                pass
        
        return dependencies
    
    def _find_pattern_in_project(self, project_path: Path, pattern: str) -> bool:
        """Cerca pattern nel codice del progetto"""
        # Se il pattern è un path/directory
        if pattern.endswith('/'):
            return (project_path / pattern.rstrip('/')).exists()
        
        # Se il pattern è un file specifico
        if not any(char in pattern for char in ['*', '?', '[', ']', '(', ')']):
            return (project_path / pattern).exists()
        
        # Pattern regex nel codice
        try:
            pattern_regex = re.compile(pattern, re.IGNORECASE)
            
            # Cerca in file di codice comuni
            search_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.php', '.vue', '.svelte'}
            
            for file_path in project_path.rglob('*'):
                if (file_path.is_file() and 
                    file_path.suffix in search_extensions and
                    file_path.stat().st_size < 1024 * 1024):  # Max 1MB
                    
                    try:
                        content = read_file(file_path)
                        if pattern_regex.search(content):
                            return True
                    except:
                        continue
            
            return False
            
        except re.error:
            return False
    
    def _calculate_confidence(self, score: int) -> str:
        """Calcola livello di confidenza"""
        if score >= 10:
            return 'very_high'
        elif score >= 7:
            return 'high'
        elif score >= 4:
            return 'medium'
        elif score >= 2:
            return 'low'
        else:
            return 'very_low'
    
    def _categorize_frameworks(self, frameworks: List[str]) -> Dict[str, List[str]]:
        """Categorizza framework rilevati"""
        categories = {
            'frontend': [],
            'backend': [],
            'mobile': [],
            'desktop': [],
            'css': [],
            'build_tools': [],
            'testing': [],
            'database': []
        }
        
        framework_categories = {
            'react': 'frontend',
            'vue': 'frontend',
            'angular': 'frontend',
            'svelte': 'frontend',
            'next': 'frontend',
            'nuxt': 'frontend',
            'express': 'backend',
            'fastify': 'backend',
            'koa': 'backend',
            'nestjs': 'backend',
            'laravel': 'backend',
            'symfony': 'backend',
            'codeigniter': 'backend',
            'django': 'backend',
            'flask': 'backend',
            'fastapi': 'backend',
            'tornado': 'backend',
            'react-native': 'mobile',
            'flutter': 'mobile',
            'electron': 'desktop',
            'tauri': 'desktop',
            'tailwind': 'css',
            'bootstrap': 'css',
            'webpack': 'build_tools',
            'vite': 'build_tools',
            'rollup': 'build_tools'
        }
        
        for framework in frameworks:
            category = framework_categories.get(framework, 'other')
            if category in categories:
                categories[category].append(framework)
            else:
                categories.setdefault('other', []).append(framework)
        
        # Rimuovi categorie vuote
        return {k: v for k, v in categories.items() if v}
    
    def _build_tech_stack(self, frameworks: List[str]) -> Dict[str, Any]:
        """Costruisce descrizione tech stack"""
        categories = self._categorize_frameworks(frameworks)
        
        stack = {
            'description': self._generate_stack_description(categories),
            'complexity': self._assess_stack_complexity(categories),
            'modern_score': self._calculate_modern_score(frameworks),
            'recommendations': self._generate_recommendations(categories, frameworks)
        }
        
        return stack
    
    def _generate_stack_description(self, categories: Dict[str, List[str]]) -> str:
        """Genera descrizione tech stack"""
        descriptions = []
        
        if categories.get('frontend'):
            descriptions.append(f"Frontend: {', '.join(categories['frontend'])}")
        
        if categories.get('backend'):
            descriptions.append(f"Backend: {', '.join(categories['backend'])}")
        
        if categories.get('mobile'):
            descriptions.append(f"Mobile: {', '.join(categories['mobile'])}")
        
        if categories.get('desktop'):
            descriptions.append(f"Desktop: {', '.join(categories['desktop'])}")
        
        return "; ".join(descriptions) if descriptions else "Stack non identificato"
    
    def _assess_stack_complexity(self, categories: Dict[str, List[str]]) -> str:
        """Valuta complessità tech stack"""
        total_frameworks = sum(len(frameworks) for frameworks in categories.values())
        
        if total_frameworks >= 8:
            return 'very_high'
        elif total_frameworks >= 5:
            return 'high'
        elif total_frameworks >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_modern_score(self, frameworks: List[str]) -> int:
        """Calcola score di modernità (1-10)"""
        modern_frameworks = {
            'react', 'vue', 'angular', 'svelte', 'next', 'nuxt',
            'fastapi', 'nestjs', 'vite', 'tailwind', 'tauri'
        }
        
        modern_count = sum(1 for fw in frameworks if fw in modern_frameworks)
        total_count = len(frameworks)
        
        if total_count == 0:
            return 5
        
        ratio = modern_count / total_count
        return min(10, max(1, int(ratio * 10)))
    
    def _generate_recommendations(self, categories: Dict[str, List[str]], frameworks: List[str]) -> List[str]:
        """Genera raccomandazioni per il tech stack"""
        recommendations = []
        
        # Raccomandazioni per frontend
        if not categories.get('frontend'):
            recommendations.append("Considerare aggiungere framework frontend moderno")
        
        # Raccomandazioni per build tools
        if not categories.get('build_tools'):
            recommendations.append("Considerare aggiungere build tool come Vite o Webpack")
        
        # Raccomandazioni per CSS
        if not categories.get('css'):
            recommendations.append("Considerare framework CSS come Tailwind")
        
        # Raccomandazioni specifiche
        if 'react' in frameworks and 'typescript' not in frameworks:
            recommendations.append("Considerare migrazione a TypeScript per React")
        
        if len(frameworks) > 6:
            recommendations.append("Stack complesso: considerare semplificazione")
        
        return recommendations