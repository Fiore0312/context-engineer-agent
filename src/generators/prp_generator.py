"""
Generatore PRP (Project Requirement Prompt) suggestions
"""

from typing import Dict, List, Any
from pathlib import Path


class PRPGenerator:
    """Genera suggerimenti PRP basati su analisi progetto e feature"""
    
    def __init__(self):
        self.prp_templates = {
            'crud': [
                "Implement CRUD operations with proper validation",
                "Create database migrations and models",
                "Build REST API endpoints with error handling",
                "Develop responsive UI forms and tables"
            ],
            'api': [
                "Design RESTful API architecture",
                "Implement authentication and authorization",
                "Create comprehensive API documentation",
                "Build automated API testing suite"
            ],
            'ui': [
                "Create responsive component library",
                "Implement accessible UI patterns",
                "Build interactive user interfaces",
                "Optimize frontend performance"
            ],
            'auth': [
                "Implement secure authentication system",
                "Build role-based access control",
                "Create user management interface",
                "Implement security audit logging"
            ],
            'integration': [
                "Design integration architecture",
                "Implement third-party API clients",
                "Build data synchronization system",
                "Create webhook handling system"
            ],
            'optimization': [
                "Analyze and optimize database queries",
                "Implement caching strategies",
                "Optimize frontend bundle size",
                "Improve application performance"
            ],
            'security': [
                "Conduct security vulnerability assessment",
                "Implement security hardening measures",
                "Build security monitoring system",
                "Create security incident response plan"
            ],
            'testing': [
                "Build comprehensive test suite",
                "Implement automated testing pipeline",
                "Create performance testing framework",
                "Build quality assurance process"
            ]
        }
    
    def suggest_prps(self, analysis: Dict[str, Any], feature_description: str) -> List[str]:
        """Genera suggerimenti PRP per feature e progetto"""
        
        # Classifica tipo di feature
        feature_type = self._classify_feature(feature_description)
        
        # Ottieni PRP base per tipo
        base_prps = self.prp_templates.get(feature_type, [])
        
        # Personalizza PRP basato su analisi progetto
        customized_prps = self._customize_prps(base_prps, analysis, feature_description)
        
        # Aggiungi PRP specifici per framework
        framework_prps = self._get_framework_specific_prps(analysis.get('framework', ''), feature_type)
        
        # Aggiungi PRP per architettura
        architecture_prps = self._get_architecture_prps(analysis.get('architecture', {}), feature_type)
        
        # Combina tutti i PRP
        all_prps = customized_prps + framework_prps + architecture_prps
        
        # Rimuovi duplicati e restituisci top 5
        unique_prps = list(dict.fromkeys(all_prps))
        return unique_prps[:5]
    
    def _classify_feature(self, description: str) -> str:
        """Classifica tipo di feature"""
        description_lower = description.lower()
        
        keywords = {
            'crud': ['create', 'read', 'update', 'delete', 'crud', 'gestione'],
            'api': ['api', 'endpoint', 'rest', 'service'],
            'ui': ['ui', 'interface', 'component', 'page', 'frontend'],
            'auth': ['auth', 'login', 'user', 'permission', 'security'],
            'integration': ['integrate', 'connect', 'sync', 'third-party'],
            'optimization': ['optimize', 'performance', 'speed', 'cache'],
            'security': ['security', 'secure', 'protect', 'vulnerability'],
            'testing': ['test', 'testing', 'quality', 'coverage']
        }
        
        scores = {}
        for feature_type, words in keywords.items():
            score = sum(1 for word in words if word in description_lower)
            if score > 0:
                scores[feature_type] = score
        
        return max(scores.items(), key=lambda x: x[1])[0] if scores else 'generic'
    
    def _customize_prps(self, base_prps: List[str], analysis: Dict[str, Any], description: str) -> List[str]:
        """Personalizza PRP basato su analisi progetto"""
        customized = []
        
        project_name = analysis.get('name', 'project')
        framework = analysis.get('framework', '')
        
        for prp in base_prps:
            # Sostituisci placeholder generici
            customized_prp = prp.replace('project', project_name)
            
            # Aggiungi contesto framework se appropriato
            if framework and framework != 'unknown':
                if 'API' in prp and framework in ['laravel', 'django', 'express']:
                    customized_prp = f"{prp} using {framework.title()}"
                elif 'UI' in prp and framework in ['react', 'vue', 'angular']:
                    customized_prp = f"{prp} with {framework.title()}"
            
            customized.append(customized_prp)
        
        return customized
    
    def _get_framework_specific_prps(self, framework: str, feature_type: str) -> List[str]:
        """Ottieni PRP specifici per framework"""
        framework_prps = {
            'laravel': {
                'crud': "Implement Laravel Eloquent models with relationships",
                'api': "Build Laravel API resources with validation",
                'auth': "Implement Laravel Sanctum authentication",
                'testing': "Create Laravel Feature and Unit tests"
            },
            'react': {
                'ui': "Build React components with hooks",
                'crud': "Implement React forms with validation",
                'testing': "Create React Testing Library tests"
            },
            'vue': {
                'ui': "Build Vue 3 components with Composition API",
                'crud': "Implement Vue forms with Pinia state management"
            },
            'django': {
                'crud': "Implement Django models and admin interface",
                'api': "Build Django REST Framework API",
                'auth': "Implement Django authentication system"
            },
            'express': {
                'api': "Build Express.js middleware and routes",
                'auth': "Implement Express authentication with JWT"
            },
            'next': {
                'ui': "Build Next.js pages with SSR/SSG",
                'api': "Implement Next.js API routes"
            }
        }
        
        if framework in framework_prps and feature_type in framework_prps[framework]:
            return [framework_prps[framework][feature_type]]
        
        return []
    
    def _get_architecture_prps(self, architecture: Dict[str, Any], feature_type: str) -> List[str]:
        """Ottieni PRP basati su architettura"""
        prps = []
        
        pattern = architecture.get('pattern', '')
        
        if pattern == 'mvc':
            if feature_type == 'crud':
                prps.append("Implement MVC pattern with proper separation of concerns")
        elif pattern == 'layered':
            prps.append("Follow layered architecture with service and repository layers")
        elif pattern == 'microservices':
            if feature_type == 'api':
                prps.append("Design microservice with proper API contracts")
        
        if architecture.get('has_modules'):
            prps.append("Implement modular architecture with clear boundaries")
        
        return prps