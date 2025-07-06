"""
MCP (Model Context Protocol) integration module
Provides access to specialized MCP servers for best practices and context engineering
"""

from .best_practices_client import BestPracticesClient

__all__ = [
    'BestPracticesClient'
]