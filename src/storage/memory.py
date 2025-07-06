"""
Memory management system for storing best practices and learned patterns
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

class PracticeCategory(Enum):
    """Categories for best practices"""
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    CI_CD = "ci_cd"
    CODE_QUALITY = "code_quality"
    UI_UX = "ui_ux"
    DATABASE = "database"
    API_DESIGN = "api_design"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"

@dataclass
class BestPractice:
    """Represents a best practice"""
    id: str
    title: str
    description: str
    category: PracticeCategory
    language: Optional[str] = None
    framework: Optional[str] = None
    tags: List[str] = None
    source: str = "manual"  # manual, mcp, analysis
    confidence: float = 1.0  # 0.0 to 1.0
    usage_count: int = 0
    last_used: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at

@dataclass
class ProjectPattern:
    """Represents a learned project pattern"""
    id: str
    project_type: str
    language: str
    framework: Optional[str]
    structure: Dict[str, Any]
    best_practices: List[str]  # IDs of related best practices
    success_rate: float = 1.0
    usage_count: int = 0
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at

class MemoryManager:
    """Manages persistent memory for best practices and patterns"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize memory manager
        
        Args:
            config_dir: Custom config directory path
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Use home directory for config
            home_dir = Path.home()
            self.config_dir = home_dir / '.context-engineer'
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.config_dir / 'memory.db'
        self.cache_file = self.config_dir / 'cache.json'
        
        # Initialize database
        self._init_database()
        
        # Load cache
        self.cache = self._load_cache()
    
    def _init_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS best_practices (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    language TEXT,
                    framework TEXT,
                    tags TEXT,  -- JSON array
                    source TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    last_used TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS project_patterns (
                    id TEXT PRIMARY KEY,
                    project_type TEXT NOT NULL,
                    language TEXT NOT NULL,
                    framework TEXT,
                    structure TEXT NOT NULL,  -- JSON
                    best_practices TEXT,  -- JSON array of IDs
                    success_rate REAL DEFAULT 1.0,
                    usage_count INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_practices_category 
                ON best_practices(category)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_practices_language 
                ON best_practices(language)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_patterns_type 
                ON project_patterns(project_type, language)
            ''')
            
            conn.commit()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache from file"""
        if not self.cache_file.exists():
            return {
                'mcp_responses': {},
                'analysis_results': {},
                'last_updated': datetime.now().isoformat()
            }
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return {
                'mcp_responses': {},
                'analysis_results': {},
                'last_updated': datetime.now().isoformat()
            }
    
    def _save_cache(self):
        """Save cache to file"""
        self.cache['last_updated'] = datetime.now().isoformat()
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to save cache: {str(e)}")
    
    def add_best_practice(self, practice: BestPractice) -> str:
        """Add a best practice to memory
        
        Args:
            practice: BestPractice instance
            
        Returns:
            Practice ID
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO best_practices 
                (id, title, description, category, language, framework, tags, 
                 source, confidence, usage_count, last_used, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                practice.id, practice.title, practice.description,
                practice.category.value, practice.language, practice.framework,
                json.dumps(practice.tags), practice.source, practice.confidence,
                practice.usage_count, practice.last_used, practice.created_at,
                practice.updated_at
            ))
            conn.commit()
        
        return practice.id
    
    def get_best_practice(self, practice_id: str) -> Optional[BestPractice]:
        """Get a best practice by ID
        
        Args:
            practice_id: Practice ID
            
        Returns:
            BestPractice instance or None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                'SELECT * FROM best_practices WHERE id = ?', 
                (practice_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return BestPractice(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                category=PracticeCategory(row['category']),
                language=row['language'],
                framework=row['framework'],
                tags=json.loads(row['tags']) if row['tags'] else [],
                source=row['source'],
                confidence=row['confidence'],
                usage_count=row['usage_count'],
                last_used=row['last_used'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
    
    def search_best_practices(
        self, 
        category: Optional[PracticeCategory] = None,
        language: Optional[str] = None,
        framework: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        limit: int = 50
    ) -> List[BestPractice]:
        """Search best practices with filters
        
        Args:
            category: Practice category filter
            language: Programming language filter
            framework: Framework filter
            tags: Tags filter (any of these tags)
            min_confidence: Minimum confidence score
            limit: Maximum results
            
        Returns:
            List of BestPractice instances
        """
        query = 'SELECT * FROM best_practices WHERE confidence >= ?'
        params = [min_confidence]
        
        if category:
            query += ' AND category = ?'
            params.append(category.value)
        
        if language:
            query += ' AND (language = ? OR language IS NULL)'
            params.append(language)
        
        if framework:
            query += ' AND (framework = ? OR framework IS NULL)'
            params.append(framework)
        
        # Order by usage count and confidence
        query += ' ORDER BY usage_count DESC, confidence DESC LIMIT ?'
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            practices = []
            for row in rows:
                practice = BestPractice(
                    id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    category=PracticeCategory(row['category']),
                    language=row['language'],
                    framework=row['framework'],
                    tags=json.loads(row['tags']) if row['tags'] else [],
                    source=row['source'],
                    confidence=row['confidence'],
                    usage_count=row['usage_count'],
                    last_used=row['last_used'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                
                # Filter by tags if specified
                if tags:
                    if any(tag in practice.tags for tag in tags):
                        practices.append(practice)
                else:
                    practices.append(practice)
            
            return practices
    
    def use_best_practice(self, practice_id: str):
        """Mark a best practice as used (increment usage count)
        
        Args:
            practice_id: Practice ID
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE best_practices 
                SET usage_count = usage_count + 1, 
                    last_used = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                practice_id
            ))
            conn.commit()
    
    def add_project_pattern(self, pattern: ProjectPattern) -> str:
        """Add a project pattern to memory
        
        Args:
            pattern: ProjectPattern instance
            
        Returns:
            Pattern ID
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO project_patterns 
                (id, project_type, language, framework, structure, best_practices,
                 success_rate, usage_count, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern.id, pattern.project_type, pattern.language,
                pattern.framework, json.dumps(pattern.structure),
                json.dumps(pattern.best_practices), pattern.success_rate,
                pattern.usage_count, pattern.created_at, pattern.updated_at
            ))
            conn.commit()
        
        return pattern.id
    
    def find_project_patterns(
        self,
        project_type: Optional[str] = None,
        language: Optional[str] = None,
        framework: Optional[str] = None,
        min_success_rate: float = 0.0,
        limit: int = 10
    ) -> List[ProjectPattern]:
        """Find project patterns with filters
        
        Args:
            project_type: Project type filter
            language: Programming language filter
            framework: Framework filter
            min_success_rate: Minimum success rate
            limit: Maximum results
            
        Returns:
            List of ProjectPattern instances
        """
        query = 'SELECT * FROM project_patterns WHERE success_rate >= ?'
        params = [min_success_rate]
        
        if project_type:
            query += ' AND project_type = ?'
            params.append(project_type)
        
        if language:
            query += ' AND language = ?'
            params.append(language)
        
        if framework:
            query += ' AND (framework = ? OR framework IS NULL)'
            params.append(framework)
        
        query += ' ORDER BY usage_count DESC, success_rate DESC LIMIT ?'
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            patterns = []
            for row in rows:
                pattern = ProjectPattern(
                    id=row['id'],
                    project_type=row['project_type'],
                    language=row['language'],
                    framework=row['framework'],
                    structure=json.loads(row['structure']),
                    best_practices=json.loads(row['best_practices']),
                    success_rate=row['success_rate'],
                    usage_count=row['usage_count'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                patterns.append(pattern)
            
            return patterns
    
    def cache_mcp_response(self, endpoint: str, query: str, response: Dict[str, Any]):
        """Cache MCP server response
        
        Args:
            endpoint: MCP endpoint
            query: Query string
            response: Response data
        """
        cache_key = f"{endpoint}:{hash(query)}"
        
        self.cache['mcp_responses'][cache_key] = {
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'query': query
        }
        
        # Clean old cache entries (keep last 100)
        if len(self.cache['mcp_responses']) > 100:
            # Remove oldest entries
            sorted_items = sorted(
                self.cache['mcp_responses'].items(),
                key=lambda x: x[1]['timestamp']
            )
            # Keep last 50
            self.cache['mcp_responses'] = dict(sorted_items[-50:])
        
        self._save_cache()
    
    def get_cached_mcp_response(
        self, 
        endpoint: str, 
        query: str, 
        max_age_hours: int = 24
    ) -> Optional[Dict[str, Any]]:
        """Get cached MCP response if available and not too old
        
        Args:
            endpoint: MCP endpoint
            query: Query string
            max_age_hours: Maximum age in hours
            
        Returns:
            Cached response or None
        """
        cache_key = f"{endpoint}:{hash(query)}"
        
        if cache_key not in self.cache['mcp_responses']:
            return None
        
        cached_item = self.cache['mcp_responses'][cache_key]
        
        # Check age
        cached_time = datetime.fromisoformat(cached_item['timestamp'])
        max_age = datetime.now() - timedelta(hours=max_age_hours)
        
        if cached_time < max_age:
            return None
        
        return cached_item['response']
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics
        
        Returns:
            Statistics dictionary
        """
        with sqlite3.connect(self.db_path) as conn:
            # Best practices stats
            cursor = conn.execute('SELECT COUNT(*) FROM best_practices')
            total_practices = cursor.fetchone()[0]
            
            cursor = conn.execute('''
                SELECT category, COUNT(*) 
                FROM best_practices 
                GROUP BY category
            ''')
            practices_by_category = dict(cursor.fetchall())
            
            cursor = conn.execute('''
                SELECT language, COUNT(*) 
                FROM best_practices 
                WHERE language IS NOT NULL
                GROUP BY language
            ''')
            practices_by_language = dict(cursor.fetchall())
            
            # Project patterns stats
            cursor = conn.execute('SELECT COUNT(*) FROM project_patterns')
            total_patterns = cursor.fetchone()[0]
            
            cursor = conn.execute('''
                SELECT project_type, COUNT(*) 
                FROM project_patterns 
                GROUP BY project_type
            ''')
            patterns_by_type = dict(cursor.fetchall())
        
        return {
            'best_practices': {
                'total': total_practices,
                'by_category': practices_by_category,
                'by_language': practices_by_language
            },
            'project_patterns': {
                'total': total_patterns,
                'by_type': patterns_by_type
            },
            'cache': {
                'mcp_responses': len(self.cache['mcp_responses']),
                'analysis_results': len(self.cache['analysis_results'])
            }
        }
    
    def export_data(self, file_path: Path):
        """Export all memory data to JSON file
        
        Args:
            file_path: Export file path
        """
        # Get all best practices
        practices = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM best_practices')
            for row in cursor.fetchall():
                practice_dict = dict(row)
                practice_dict['tags'] = json.loads(practice_dict['tags']) if practice_dict['tags'] else []
                practices.append(practice_dict)
        
        # Get all project patterns
        patterns = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM project_patterns')
            for row in cursor.fetchall():
                pattern_dict = dict(row)
                pattern_dict['structure'] = json.loads(pattern_dict['structure'])
                pattern_dict['best_practices'] = json.loads(pattern_dict['best_practices'])
                patterns.append(pattern_dict)
        
        export_data = {
            'best_practices': practices,
            'project_patterns': patterns,
            'cache': self.cache,
            'exported_at': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache = {
            'mcp_responses': {},
            'analysis_results': {},
            'last_updated': datetime.now().isoformat()
        }
        self._save_cache()