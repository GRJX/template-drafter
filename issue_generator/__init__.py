"""
Issue Generator - A tool for generating issues from templates using Ollama.
"""

from .template_manager import TemplateManager
from .ollama_client import OllamaClient
from .issue_generator import IssueGenerator

__all__ = ["TemplateManager", "OllamaClient", "IssueGenerator"]