"""
Interface module for Context Engineer Agent
Provides enhanced CLI interface with ASCII art and interactive prompts
"""

from .menu import show_main_menu, get_menu_choice
from .prompts import ask_new_project_questions, ask_existing_project_questions

__all__ = [
    'show_main_menu',
    'get_menu_choice', 
    'ask_new_project_questions',
    'ask_existing_project_questions'
]