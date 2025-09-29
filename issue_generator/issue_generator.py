"""
Issue generator module for creating issues from templates using AI.
"""

import re
from typing import Dict, List, Any

from .template_manager import TemplateManager
from .ollama_client import OllamaClient
from .placeholder_types import PlaceholderTypes


class IssueGenerator:
    """Generates issue descriptions from templates using AI."""
    
    def __init__(self, template_manager: TemplateManager, ollama_client: OllamaClient, output_format: str = 'jira'):
        """
        Initialize the IssueGenerator.
        
        Args:
            template_manager: Manager for loading and rendering templates
            ollama_client: Pre-initialized client for generating text with Ollama
            output_format: The desired output format ('jira' or 'adoc')
        """
        self.template_manager = template_manager
        self.ollama_client = ollama_client
        self.prompts = self.template_manager.get_template_prompts()
        self.output_format = output_format
        self.placeholder_types = PlaceholderTypes(ollama_client, output_format)

    def _extract_template_fields(self, template_content: str) -> List[str]:
        """
        Extract fields (placeholders) from a template file.
        
        Args:
            template_content: The content of the template file
            
        Returns:
            List of field names extracted from the template
        """
        # Regular expression to find all placeholders like {{ field_name }}
        fields = re.findall(r'{{\s*(\w+)\s*}}', template_content)
        
        # Return unique field names
        return list(set(fields))

    def generate_issue_content(self, context: str, field: str) -> str:
        """
        Generate content for a specific field of an issue.
        
        Args:
            context: User-provided context for the issue
            field: Field to generate content for (e.g., 'description', 'acceptance_criteria')
            
        Returns:
            Generated content for the field
        """
        # self.prompts now correctly points to the 'template_prompts' dictionary
        if field not in self.prompts:
            raise ValueError(f"Unknown field in template_prompts: {field}")
        
        # Get the prompt configuration for the specific field
        prompt_config = self.prompts[field]
        
        # Check if the prompt has a type and use the appropriate generation function
        if "type" in prompt_config:
            generation_type = prompt_config["type"]
            additional_info = prompt_config.get("additional_info", '')
            
            if generation_type == "header":
                word_limit = prompt_config.get("args", {}).get("word_limit", 7)
                return self.placeholder_types.generate_header(context, word_limit, additional_info)
            
            elif generation_type == "sentence":
                word_limit = prompt_config.get("args", {}).get("word_limit", 50)
                return self.placeholder_types.generate_sentence(context, word_limit, additional_info)
            
            elif generation_type == "bullets":
                bullet_limit = prompt_config.get("args", {}).get("bullet_limit", 5)
                return self.placeholder_types.generate_bullets(context, bullet_limit, additional_info)
            
            elif generation_type == "numbered":
                step_limit = prompt_config.get("args", {}).get("step_limit", 5)
                return self.placeholder_types.generate_numbered(context, step_limit, additional_info)
            
            elif generation_type == "selection":
                options = prompt_config.get("args", {}).get("options", [])
                if not options:
                    raise ValueError("Options list is required for 'selection' generation type")
                return self.placeholder_types.select_from_list(context, options, additional_info)
            
            elif generation_type == "tables":
                table_limit = prompt_config.get("args", {}).get("table_limit", 1)
                # Process table_title format - replace placeholders like <abbreviation> if needed later
                raw_title_format = prompt_config.get("args", {}).get("table_title", "") 
                # Simple placeholder replacement for now, might need refinement
                processed_title = raw_title_format # Placeholder for potential future logic
                
                table_headers = prompt_config.get("args", {}).get("table_headers", ["Header1", "Header2"])
                
                return self.placeholder_types.generate_tables(context, table_limit, processed_title, table_headers, additional_info)
            
            else:
                raise ValueError(f"Unsupported generation type: {generation_type}")
        
        return self.ollama_client.generate_text(prompt_config)
    
    def generate_full_issue(self, context: str, template_name: str) -> str:
        """
        Generate a complete issue from a template.
        
        Args:
            context: User-provided context for the issue
            template_name: Name of the template file to use
            
        Returns:
            Fully rendered issue content
        """
        # Load the template
        template_content = self.template_manager.load_template(template_name)
        
        # Extract fields from the template
        fields = self._extract_template_fields(template_content)
        
        # Generate content for each field
        issue_data = {}
        
        # Generate standard fields first
        for field in fields:
            print(f"\033[94mGenerating {field}...\033[0m")
            try:
                issue_data[field] = self.generate_issue_content(context, field)
            except ValueError as e:
                print(f"\033[93mWarning: Could not generate content for {field}: {str(e)}\033[0m")
                issue_data[field] = f"<!-- Missing content for {field} -->"
        
        # Render the template with the generated content
        return self.template_manager.render_template(template_content, issue_data)
