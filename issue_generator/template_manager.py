"""
Template manager for loading and rendering templates and managing prompt configurations.
"""

import os
import json
from typing import Dict, Any
from jinja2 import Template


class TemplateManager:
    """Manages loading templates and prompt configurations."""
    
    def __init__(self, template_dir: str, prompts_config_path: str):
        """
        Initialize the TemplateManager.
        
        Args:
            template_dir: Directory containing template files (.txt)
            prompts_config_path: Path to the prompts configuration JSON file
        """
        self.template_dir = template_dir
        self.prompts_config_path = prompts_config_path
        self._load_prompts_config()

    def _load_prompts_config(self):
        """Load the prompts configuration from the JSON file."""
        if not os.path.exists(self.prompts_config_path):
            raise FileNotFoundError(f"Prompts configuration file '{self.prompts_config_path}' not found")
        
        with open(self.prompts_config_path, 'r') as f:
            full_config = json.load(f)
            
        self.system_prompt = full_config.get("system_prompt", "You are a helpful AI assistant.") # Default fallback
        self.template_prompts = full_config.get("template_prompts", {})

    def get_system_prompt(self) -> str:
        """Returns the loaded system prompt."""
        return self.system_prompt
    
    def get_template_prompts(self) -> str:
        """Returns the loaded system prompt."""
        return self.template_prompts
    
    def load_template(self, template_name: str) -> str:
        """
        Load a template file.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Template content as a string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        template_path = os.path.join(self.template_dir, template_name)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{template_path}' not found")
        
        with open(template_path, 'r') as f:
            return f.read()
    
    def render_template(self, template_content: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context.
        
        Args:
            template_content: Template content as a string
            context: Dictionary of variables to render in the template
            
        Returns:
            Rendered template as a string
        """
        template = Template(template_content)
        return template.render(**context)