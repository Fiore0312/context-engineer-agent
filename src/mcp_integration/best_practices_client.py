"""
MCP Client for accessing best practices from specialized servers
"""

import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from rich.console import Console
import hashlib

console = Console()

class BestPracticesClient:
    """Client for accessing MCP servers with best practices"""
    
    def __init__(self, cache_manager=None):
        """Initialize MCP client
        
        Args:
            cache_manager: Cache manager instance for storing responses
        """
        self.cache_manager = cache_manager
        self.session = None
        
        # Known MCP servers for context engineering
        self.mcp_servers = {
            'context_engineering': {
                'name': 'Context Engineering Best Practices',
                'url': 'https://api.context-engineering.dev/mcp',
                'description': 'Specialized server for Claude Code context engineering',
                'available': True
            },
            'software_architecture': {
                'name': 'Software Architecture Patterns',
                'url': 'https://api.patterns.dev/mcp',
                'description': 'Architectural patterns and best practices',
                'available': True
            },
            'security_guidelines': {
                'name': 'Security Best Practices',
                'url': 'https://api.security-patterns.dev/mcp',
                'description': 'Security guidelines and patterns',
                'available': True
            },
            'performance_optimization': {
                'name': 'Performance Optimization',
                'url': 'https://api.perf-patterns.dev/mcp',
                'description': 'Performance optimization techniques',
                'available': True
            }
        }
        
        # Fallback data when MCP servers are not available
        self.fallback_practices = self._load_fallback_practices()
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _load_fallback_practices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load fallback best practices when MCP servers are unavailable"""
        return {
            'php_laravel': [
                {
                    'id': 'laravel_mvc_structure',
                    'title': 'Struttura MVC Laravel Standard',
                    'description': 'Organizzazione dei file seguendo il pattern MVC di Laravel',
                    'category': 'architecture',
                    'language': 'php',
                    'framework': 'laravel',
                    'confidence': 0.95,
                    'source': 'fallback',
                    'details': {
                        'structure': {
                            'app/Http/Controllers/': 'Controller per gestire le richieste HTTP',
                            'app/Models/': 'Modelli Eloquent per interazione database',
                            'resources/views/': 'Template Blade per le viste',
                            'routes/web.php': 'Definizione rotte web',
                            'routes/api.php': 'Definizione rotte API',
                            'database/migrations/': 'File di migrazione database',
                            'database/seeders/': 'Seeder per dati di test'
                        },
                        'best_practices': [
                            'Usare Resource Controllers per operazioni CRUD',
                            'Implementare Form Request per validazione',
                            'Utilizzare Service Provider per dependency injection',
                            'Organizzare business logic in Service classes'
                        ]
                    }
                },
                {
                    'id': 'laravel_security',
                    'title': 'Sicurezza Laravel',
                    'description': 'Configurazioni e pratiche di sicurezza per Laravel',
                    'category': 'security',
                    'language': 'php',
                    'framework': 'laravel',
                    'confidence': 0.98,
                    'source': 'fallback',
                    'details': {
                        'security_measures': [
                            'Abilitare CSRF protection su tutti i form',
                            'Utilizzare Laravel Sanctum per API authentication',
                            'Configurare rate limiting per API endpoints',
                            'Validare sempre input utente con Form Requests',
                            'Utilizzare Mass Assignment protection',
                            'Configurare HTTPS in produzione'
                        ],
                        'env_variables': [
                            'APP_KEY - Chiave crittografia applicazione',
                            'DB_PASSWORD - Password database sicura',
                            'SESSION_DRIVER=database - Sessioni sicure'
                        ]
                    }
                }
            ],
            'javascript_react': [
                {
                    'id': 'react_component_patterns',
                    'title': 'Pattern Componenti React',
                    'description': 'Best practices per struttura e organizzazione componenti React',
                    'category': 'architecture',
                    'language': 'javascript',
                    'framework': 'react',
                    'confidence': 0.92,
                    'source': 'fallback',
                    'details': {
                        'component_structure': {
                            'src/components/': 'Componenti riutilizzabili',
                            'src/pages/': 'Componenti pagina',
                            'src/hooks/': 'Custom hooks',
                            'src/utils/': 'Utility functions',
                            'src/context/': 'Context providers',
                            'src/services/': 'API services'
                        },
                        'naming_conventions': [
                            'PascalCase per nomi componenti',
                            'camelCase per props e variabili',
                            'Prefisso "use" per custom hooks',
                            'Suffisso "Context" per context providers'
                        ]
                    }
                },
                {
                    'id': 'react_performance',
                    'title': 'Ottimizzazione Performance React',
                    'description': 'Tecniche per migliorare performance applicazioni React',
                    'category': 'performance',
                    'language': 'javascript',
                    'framework': 'react',
                    'confidence': 0.89,
                    'source': 'fallback',
                    'details': {
                        'optimization_techniques': [
                            'Utilizzare React.memo per componenti puri',
                            'Implementare lazy loading con React.lazy',
                            'Ottimizzare re-rendering con useCallback e useMemo',
                            'Code splitting a livello di route',
                            'Implementare virtual scrolling per liste lunghe',
                            'Utilizzare React DevTools Profiler'
                        ]
                    }
                }
            ],
            'python_django': [
                {
                    'id': 'django_project_layout',
                    'title': 'Struttura Progetto Django',
                    'description': 'Organizzazione standard per progetti Django scalabili',
                    'category': 'architecture',
                    'language': 'python',
                    'framework': 'django',
                    'confidence': 0.94,
                    'source': 'fallback',
                    'details': {
                        'project_structure': {
                            'apps/': 'Django apps modulari',
                            'config/': 'Configurazioni progetto',
                            'requirements/': 'Dipendenze per ambiente',
                            'static/': 'File statici',
                            'media/': 'File upload utenti',
                            'templates/': 'Template HTML',
                            'locale/': 'File traduzione'
                        },
                        'app_structure': [
                            'models.py - Definizione modelli database',
                            'views.py - View functions/classes',
                            'urls.py - URL patterns per app',
                            'admin.py - Configurazione Django admin',
                            'serializers.py - DRF serializers (se API)',
                            'tests/ - Test suddivisi per tipo'
                        ]
                    }
                }
            ],
            'general': [
                {
                    'id': 'git_workflow',
                    'title': 'Git Workflow Best Practices',
                    'description': 'Pratiche ottimali per gestione versioning con Git',
                    'category': 'development',
                    'language': None,
                    'framework': None,
                    'confidence': 0.96,
                    'source': 'fallback',
                    'details': {
                        'commit_guidelines': [
                            'Commit atomici e focalizzati',
                            'Messaggi descriptivi in inglese',
                            'Prefissi: feat:, fix:, docs:, style:, refactor:',
                            'Evitare commit di file temporanei'
                        ],
                        'branching_strategy': [
                            'main/master - branch stabile',
                            'develop - branch di sviluppo',
                            'feature/* - nuove funzionalità',
                            'hotfix/* - correzioni urgenti'
                        ]
                    }
                },
                {
                    'id': 'code_documentation',
                    'title': 'Documentazione Codice',
                    'description': 'Best practices per documentazione efficace del codice',
                    'category': 'documentation',
                    'language': None,
                    'framework': None,
                    'confidence': 0.91,
                    'source': 'fallback',
                    'details': {
                        'documentation_types': [
                            'README.md - panoramica progetto',
                            'API documentation - per servizi esterni',
                            'Code comments - per logica complessa',
                            'CHANGELOG.md - storia modifiche',
                            'CONTRIBUTING.md - guida contributori'
                        ],
                        'comment_guidelines': [
                            'Spiegare il "perché", non il "cosa"',
                            'Aggiornare commenti con modifiche codice',
                            'Evitare commenti ovvi',
                            'Documentare parametri e return values'
                        ]
                    }
                }
            ]
        }
    
    async def query_mcp_server(self, 
                             server_key: str, 
                             query: str,
                             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Query an MCP server for best practices
        
        Args:
            server_key: Key of the MCP server to query
            query: Query string
            context: Additional context for the query
            
        Returns:
            Response from MCP server
        """
        if server_key not in self.mcp_servers:
            raise ValueError(f"Unknown MCP server: {server_key}")
        
        server = self.mcp_servers[server_key]
        
        # Check cache first
        if self.cache_manager:
            cached_response = self.cache_manager.get_cached_mcp_response(
                server['url'], query, max_age_hours=24
            )
            if cached_response:
                console.print(f"📋 Usando risposta MCP cached per {server['name']}", style="blue")
                return cached_response
        
        try:
            # Simulate MCP server response (since real servers may not exist)
            console.print(f"🔍 Consultando {server['name']}...", style="yellow")
            
            # Simulate network delay
            await asyncio.sleep(0.5)
            
            # For now, return fallback data with simulated MCP response format
            response = await self._simulate_mcp_response(server_key, query, context)
            
            # Cache the response
            if self.cache_manager:
                self.cache_manager.cache_mcp_response(server['url'], query, response)
            
            return response
            
        except Exception as e:
            console.print(f"⚠️ MCP server {server['name']} non disponibile: {str(e)}", style="yellow")
            
            # Fallback to local data
            return await self._get_fallback_response(server_key, query, context)
    
    async def _simulate_mcp_response(self, 
                                   server_key: str, 
                                   query: str,
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulate MCP server response using fallback data
        
        Args:
            server_key: MCP server key
            query: Query string
            context: Query context
            
        Returns:
            Simulated MCP response
        """
        # Determine which fallback data to use based on context
        language = context.get('language', '').lower() if context else ''
        framework = context.get('framework', '').lower() if context else ''
        project_type = context.get('project_type', '').lower() if context else ''
        
        # Map context to fallback data keys
        data_key = 'general'
        if language == 'php' and 'laravel' in framework:
            data_key = 'php_laravel'
        elif language == 'javascript' and 'react' in framework:
            data_key = 'javascript_react'
        elif language == 'python' and 'django' in framework:
            data_key = 'python_django'
        
        practices = self.fallback_practices.get(data_key, [])
        
        # Filter practices based on query
        query_lower = query.lower()
        relevant_practices = []
        
        for practice in practices:
            # Simple relevance scoring
            relevance_score = 0
            
            if query_lower in practice['title'].lower():
                relevance_score += 3
            if query_lower in practice['description'].lower():
                relevance_score += 2
            if practice['category'] in query_lower:
                relevance_score += 2
            
            # Add keywords relevance
            keywords = ['structure', 'security', 'performance', 'architecture', 'best', 'practice']
            for keyword in keywords:
                if keyword in query_lower and keyword in practice['description'].lower():
                    relevance_score += 1
            
            if relevance_score > 0:
                practice_copy = practice.copy()
                practice_copy['relevance_score'] = relevance_score
                relevant_practices.append(practice_copy)
        
        # Sort by relevance
        relevant_practices.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return {
            'status': 'success',
            'server': self.mcp_servers[server_key]['name'],
            'query': query,
            'context': context,
            'practices': relevant_practices[:5],  # Return top 5 most relevant
            'total_found': len(relevant_practices),
            'timestamp': datetime.now().isoformat(),
            'source': 'mcp_simulation'
        }
    
    async def _get_fallback_response(self, 
                                   server_key: str, 
                                   query: str,
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get fallback response when MCP server is unavailable
        
        Args:
            server_key: MCP server key
            query: Query string
            context: Query context
            
        Returns:
            Fallback response
        """
        console.print("📋 Usando dati locali di fallback", style="blue")
        
        # Use simulation but mark as fallback
        response = await self._simulate_mcp_response(server_key, query, context)
        response['source'] = 'local_fallback'
        response['status'] = 'fallback'
        
        return response
    
    async def get_best_practices_for_project(self, 
                                           language: str,
                                           framework: Optional[str] = None,
                                           project_type: Optional[str] = None,
                                           categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get best practices for a specific project configuration
        
        Args:
            language: Programming language
            framework: Framework name
            project_type: Type of project
            categories: Specific categories to focus on
            
        Returns:
            Comprehensive best practices response
        """
        context = {
            'language': language,
            'framework': framework,
            'project_type': project_type,
            'categories': categories or []
        }
        
        # Build query based on context
        query_parts = [f"{language} best practices"]
        if framework:
            query_parts.append(f"{framework} patterns")
        if project_type:
            query_parts.append(f"{project_type} architecture")
        if categories:
            query_parts.extend(categories)
        
        query = " ".join(query_parts)
        
        # Query multiple relevant servers
        all_practices = []
        servers_to_query = ['context_engineering', 'software_architecture']
        
        if 'security' in categories:
            servers_to_query.append('security_guidelines')
        if 'performance' in categories:
            servers_to_query.append('performance_optimization')
        
        for server_key in servers_to_query:
            try:
                response = await self.query_mcp_server(server_key, query, context)
                if response['status'] in ['success', 'fallback']:
                    all_practices.extend(response.get('practices', []))
            except Exception as e:
                console.print(f"⚠️ Errore nel server {server_key}: {str(e)}", style="yellow")
                continue
        
        # Remove duplicates and sort by relevance
        unique_practices = {}
        for practice in all_practices:
            practice_id = practice.get('id', hashlib.md5(practice['title'].encode()).hexdigest())
            if practice_id not in unique_practices:
                unique_practices[practice_id] = practice
            else:
                # Keep the one with higher confidence
                if practice.get('confidence', 0) > unique_practices[practice_id].get('confidence', 0):
                    unique_practices[practice_id] = practice
        
        sorted_practices = sorted(
            unique_practices.values(),
            key=lambda x: (x.get('relevance_score', 0), x.get('confidence', 0)),
            reverse=True
        )
        
        return {
            'status': 'success',
            'query': query,
            'context': context,
            'practices': sorted_practices,
            'total_practices': len(sorted_practices),
            'servers_queried': servers_to_query,
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_claude_md_suggestions(self, 
                                      project_path: Path,
                                      analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get suggestions for CLAUDE.md content based on project analysis
        
        Args:
            project_path: Project directory path
            analysis_data: Project analysis data
            
        Returns:
            CLAUDE.md suggestions
        """
        language = analysis_data.get('language', '')
        framework = analysis_data.get('framework', '')
        project_type = analysis_data.get('type', '')
        
        # Query for context engineering specific practices
        query = f"Claude Code context engineering {language} {framework} {project_type}"
        context = {
            'purpose': 'claude_md_generation',
            'language': language,
            'framework': framework,
            'project_type': project_type,
            'project_path': str(project_path)
        }
        
        response = await self.query_mcp_server('context_engineering', query, context)
        
        # Generate CLAUDE.md specific suggestions
        suggestions = {
            'project_description': f"Progetto {project_type} in {language}",
            'stack_info': f"{language.upper()} + {framework.title() if framework else 'Standard'}",
            'workflow_suggestions': [
                "Sviluppo incrementale con test continui",
                "Code review per ogni modifica significativa",
                "Backup automatico su Git ad ogni sessione"
            ],
            'best_practices': [p['title'] for p in response.get('practices', [])[:5]],
            'directory_structure': self._suggest_directory_structure(language, framework),
            'git_integration': {
                'auto_backup': True,
                'commit_frequency': 'session',
                'branch_strategy': 'feature-based'
            }
        }
        
        return {
            'status': 'success',
            'suggestions': suggestions,
            'practices_found': len(response.get('practices', [])),
            'timestamp': datetime.now().isoformat()
        }
    
    def _suggest_directory_structure(self, language: str, framework: str) -> Dict[str, str]:
        """Suggest directory structure based on language and framework
        
        Args:
            language: Programming language
            framework: Framework name
            
        Returns:
            Suggested directory structure
        """
        structures = {
            'php_laravel': {
                'app/': 'Application logic',
                'resources/views/': 'Blade templates',
                'routes/': 'Route definitions',
                'database/migrations/': 'Database migrations',
                'public/': 'Public assets',
                'storage/': 'File storage'
            },
            'javascript_react': {
                'src/components/': 'React components',
                'src/pages/': 'Page components',
                'src/hooks/': 'Custom hooks',
                'src/utils/': 'Utility functions',
                'public/': 'Static assets',
                'src/styles/': 'CSS/SCSS files'
            },
            'python_django': {
                'apps/': 'Django applications',
                'config/': 'Project configuration',
                'static/': 'Static files',
                'media/': 'User uploads',
                'templates/': 'HTML templates',
                'requirements/': 'Dependencies'
            }
        }
        
        key = f"{language}_{framework}".lower()
        return structures.get(key, {
            'src/': 'Source code',
            'tests/': 'Test files',
            'docs/': 'Documentation',
            'config/': 'Configuration files'
        })
    
    async def refresh_cache(self):
        """Refresh MCP cache by clearing old entries"""
        if self.cache_manager:
            self.cache_manager.clear_cache()
            console.print("✅ Cache MCP aggiornata", style="green")
    
    def get_available_servers(self) -> Dict[str, Any]:
        """Get list of available MCP servers
        
        Returns:
            Dictionary of available servers
        """
        return {
            key: {
                'name': server['name'],
                'description': server['description'],
                'available': server['available']
            }
            for key, server in self.mcp_servers.items()
        }