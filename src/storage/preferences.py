"""
User preferences management system
Handles persistent storage of user settings and preferences
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from cryptography.fernet import Fernet
import base64

class PreferencesManager:
    """Manages user preferences with secure storage"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize preferences manager
        
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
        self.preferences_file = self.config_dir / 'preferences.json'
        self.secure_file = self.config_dir / 'secure.json'
        self.key_file = self.config_dir / '.key'
        
        # Initialize encryption key
        self._init_encryption()
        
        # Load existing preferences
        self.preferences = self._load_preferences()
        self.secure_data = self._load_secure_data()
    
    def _init_encryption(self):
        """Initialize encryption key for secure data"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
            # Hide key file on Unix systems
            if os.name == 'posix':
                os.chmod(self.key_file, 0o600)
        
        self.cipher = Fernet(self.key)
    
    def _load_preferences(self) -> Dict[str, Any]:
        """Load preferences from file"""
        if not self.preferences_file.exists():
            return self._get_default_preferences()
        
        try:
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return self._get_default_preferences()
    
    def _load_secure_data(self) -> Dict[str, Any]:
        """Load secure data from encrypted file"""
        if not self.secure_file.exists():
            return {}
        
        try:
            with open(self.secure_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception:
            return {}
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences"""
        return {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'user_info': {
                'name': '',
                'email': '',
                'github_username': ''
            },
            'programming': {
                'favorite_languages': [],
                'favorite_frameworks': [],
                'coding_style': 'pragmatic',
                'project_structure_preference': 'modular'
            },
            'interface': {
                'theme': 'default',
                'show_welcome_message': True,
                'auto_clear_screen': True
            },
            'integrations': {
                'auto_git_backup': True,
                'use_mcp_by_default': True,
                'backup_frequency': 'session'
            },
            'directories': {
                'default_project_paths': [
                    '/mnt/c/xampp/htdocs',
                    '/mnt/c/Users/*/Desktop',
                    '/mnt/c/progetti',
                    '~/projects'
                ],
                'scan_subdirectories': True
            },
            'notifications': {
                'show_suggestions': True,
                'show_next_steps': True,
                'show_tips': True
            }
        }
    
    def save_preferences(self):
        """Save preferences to file"""
        self.preferences['last_updated'] = datetime.now().isoformat()
        
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to save preferences: {str(e)}")
    
    def save_secure_data(self):
        """Save secure data to encrypted file"""
        try:
            data_str = json.dumps(self.secure_data, indent=2, ensure_ascii=False)
            encrypted_data = self.cipher.encrypt(data_str.encode('utf-8'))
            
            with open(self.secure_file, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            raise Exception(f"Failed to save secure data: {str(e)}")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a preference value using dot notation
        
        Args:
            key: Preference key (e.g., 'programming.favorite_languages')
            default: Default value if key doesn't exist
            
        Returns:
            Preference value
        """
        keys = key.split('.')
        value = self.preferences
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_preference(self, key: str, value: Any):
        """Set a preference value using dot notation
        
        Args:
            key: Preference key (e.g., 'programming.favorite_languages')
            value: Value to set
        """
        keys = key.split('.')
        current = self.preferences
        
        # Navigate to the parent dict
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the final value
        current[keys[-1]] = value
        self.save_preferences()
    
    def get_secure_data(self, key: str, default: Any = None) -> Any:
        """Get secure data (like tokens)
        
        Args:
            key: Data key
            default: Default value if key doesn't exist
            
        Returns:
            Secure data value
        """
        return self.secure_data.get(key, default)
    
    def set_secure_data(self, key: str, value: Any):
        """Set secure data (like tokens)
        
        Args:
            key: Data key
            value: Value to set
        """
        self.secure_data[key] = value
        self.save_secure_data()
    
    def update_preferences(self, updates: Dict[str, Any]):
        """Update multiple preferences at once
        
        Args:
            updates: Dictionary of preference updates
        """
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.preferences, updates)
        self.save_preferences()
    
    def add_favorite_language(self, language: str):
        """Add a programming language to favorites"""
        favorites = self.get_preference('programming.favorite_languages', [])
        if language not in favorites:
            favorites.append(language)
            self.set_preference('programming.favorite_languages', favorites)
    
    def add_favorite_framework(self, framework: str):
        """Add a framework to favorites"""
        favorites = self.get_preference('programming.favorite_frameworks', [])
        if framework not in favorites:
            favorites.append(framework)
            self.set_preference('programming.favorite_frameworks', favorites)
    
    def add_project_path(self, path: str):
        """Add a project path to scan directories"""
        paths = self.get_preference('directories.default_project_paths', [])
        if path not in paths:
            paths.append(path)
            self.set_preference('directories.default_project_paths', paths)
    
    def get_github_token(self) -> Optional[str]:
        """Get GitHub token from secure storage"""
        return self.get_secure_data('github_token')
    
    def set_github_token(self, token: str):
        """Set GitHub token in secure storage"""
        self.set_secure_data('github_token', token)
    
    def get_mcp_endpoints(self) -> List[str]:
        """Get MCP server endpoints"""
        return self.get_secure_data('mcp_endpoints', [])
    
    def add_mcp_endpoint(self, endpoint: str):
        """Add MCP server endpoint"""
        endpoints = self.get_mcp_endpoints()
        if endpoint not in endpoints:
            endpoints.append(endpoint)
            self.set_secure_data('mcp_endpoints', endpoints)
    
    def export_preferences(self, file_path: Path, include_secure: bool = False):
        """Export preferences to file
        
        Args:
            file_path: Path to export file
            include_secure: Whether to include secure data
        """
        export_data = {
            'preferences': self.preferences,
            'exported_at': datetime.now().isoformat(),
            'version': self.preferences.get('version', '1.0.0')
        }
        
        if include_secure:
            export_data['secure_data'] = self.secure_data
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def import_preferences(self, file_path: Path, merge: bool = True):
        """Import preferences from file
        
        Args:
            file_path: Path to import file
            merge: Whether to merge with existing preferences
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        if merge:
            self.update_preferences(import_data.get('preferences', {}))
            if 'secure_data' in import_data:
                self.secure_data.update(import_data['secure_data'])
                self.save_secure_data()
        else:
            self.preferences = import_data.get('preferences', self._get_default_preferences())
            if 'secure_data' in import_data:
                self.secure_data = import_data['secure_data']
                self.save_secure_data()
            self.save_preferences()
    
    def reset_preferences(self):
        """Reset preferences to defaults"""
        self.preferences = self._get_default_preferences()
        self.save_preferences()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of current preferences"""
        return {
            'languages': self.get_preference('programming.favorite_languages', []),
            'frameworks': self.get_preference('programming.favorite_frameworks', []),
            'coding_style': self.get_preference('programming.coding_style', 'pragmatic'),
            'git_backup': self.get_preference('integrations.auto_git_backup', True),
            'mcp_enabled': self.get_preference('integrations.use_mcp_by_default', True),
            'project_paths': self.get_preference('directories.default_project_paths', []),
            'github_configured': bool(self.get_github_token()),
            'mcp_endpoints': len(self.get_mcp_endpoints()),
            'last_updated': self.get_preference('last_updated', 'Never')
        }