"""
Git integration module for Context Engineer Agent
Provides automatic GitHub backup and repository management
"""

from .github_client import GitHubClient
from .auto_backup import AutoBackup

__all__ = [
    'GitHubClient',
    'AutoBackup'
]