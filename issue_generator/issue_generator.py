"""
Issue generator module for creating issues from templates using AI.
"""

import json
import os
import re
from typing import Dict, List, Any

from .template_manager import TemplateManager
from .ollama_client import OllamaClient


class IssueGenerator:
    """Generates issue descriptions from templates using AI."""
    
    def __init__(self, template_manager: TemplateManager, ollama_client: OllamaClient):
        """
        Initialize the IssueGenerator.
        
        Args:
            template_manager: Manager for loading and rendering templates
            ollama_client: Client for generating text with Ollama
        """
        self.template_manager = template_manager
        self.ollama_client = ollama_client
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """
        Load prompts from the JSON configuration file.
        
        Returns:
            Dictionary containing the prompt templates
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompts_path = os.path.join(script_dir, 'prompts-config.json')
        
        with open(prompts_path, 'r') as f:
            return json.load(f)
    
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
    
    def generate_header(self, context: str, word_limit: int = 7, additional_info: str = '') -> str:
        """
        Generate a concise header/title with a limited number of words.
        
        Args:
            context: User-provided context for the header
            word_limit: Maximum number of words in the header (default: 7)
            additional_info: Additional prompt information (optional)
            
        Returns:
            Generated header as a string
        """
        prompt = f"""
            Create a brief, concise title (maximum {word_limit} words) about this topic in Dutch. 

            {additional_info}

            Return without any additional text or punctuation. 

            This is the context: {context}
        """
        
        return self.ollama_client.generate_text(prompt)

    def generate_sentence(self, context: str, word_limit: int = 50, additional_info: str = '') -> str:
        """
        Generate descriptive, functional, and clear sentences.
        
        Args:
            context: User-provided context for the sentence
            word_limit: Maximum number of words in the sentence (default: 50)
            additional_info: Additional prompt information (optional)
            
        Returns:
            Generated sentence as a string
        """
        prompt = f"""
            Write a single clear and descriptive sentence(s) (maximum {word_limit} words) about this topic in Dutch. Make it functional and direct. 
                
            {additional_info}

            Return without any explanation, additional text or newline characters.

            This is the context: {context}
        """
        return self.ollama_client.generate_text(prompt)

    def generate_bullets(self, context: str, bullet_limit: int = 5, additional_info: str = '') -> str:
        """
        Generate a list of bullet points.
        
        Args:
            context: User-provided context for the bullet points
            bullet_limit: Maximum number of bullet points to generate (default: 5)
            additional_info: Additional prompt information (optional)
            
        Returns:
            Generated bullet points as a string
        """
        prompt = f"""
            Create a list of maximum {bullet_limit} bullet points about this topic in Dutch. 
            
            {additional_info}

            Return only the bulleted list like: '* bullet item', without explanation, additional text or characters.

            This is the context: {context}
        """
        return self.ollama_client.generate_text(prompt)

    def select_from_list(self, context: str, options: List[str], additional_info: str = '') -> str:
        """
        Select a single item from a predefined list based on the context.
        
        Args:
            context: User-provided context for the selection
            options: List of options to choose from
            additional_info: Additional prompt information (optional)
            
        Returns:
            Selected item as a string
        """
        options_str = ", ".join([f"'{option}'" for option in options])
        prompt = f"""
            Select ONE of the following options: {options_str}. Return ONLY the selected option without the explanation 
            between the brackets or additional text.
            
            {additional_info}

            This is the context: {context}
        """
        return self.ollama_client.generate_text(prompt)
    
    def generate_issue_content(self, context: str, field: str) -> str:
        """
        Generate content for a specific field of an issue.
        
        Args:
            context: User-provided context for the issue
            field: Field to generate content for (e.g., 'description', 'acceptance_criteria')
            
        Returns:
            Generated content for the field
        """
        if field not in self.prompts:
            raise ValueError(f"Unknown field: {field}")
        
        # Get the prompt configuration
        prompt_config = self.prompts[field]
        
        # Check if the prompt has a type and use the appropriate generation function
        if "type" in prompt_config:
            generation_type = prompt_config["type"]
            additional_info = prompt_config.get("additional_info", '')
            
            if generation_type == "header":
                word_limit = prompt_config.get("args", {}).get("word_limit", 7)
                return self.generate_header(context, word_limit, additional_info)
            
            elif generation_type == "sentence":
                word_limit = prompt_config.get("args", {}).get("word_limit", 50)
                return self.generate_sentence(context, word_limit, additional_info)
            
            elif generation_type == "bullets":
                bullet_limit = prompt_config.get("args", {}).get("bullet_limit", 5)
                return self.generate_bullets(context, bullet_limit, additional_info)
            
            elif generation_type == "selection":
                options = prompt_config.get("args", {}).get("options", [])
                if not options:
                    raise ValueError("Options list is required for 'selection' generation type")
                return self.select_from_list(context, options, additional_info)
            
            elif generation_type == "custom":
                # For custom types, use the standard prompt approach
                pass
            
            else:
                raise ValueError(f"Unsupported generation type: {generation_type}")
        
        # Get the prompt template
        prompt_template = prompt_config["prompt"]
        
        # Replace argument placeholders if present
        if "args" in prompt_config:
            for arg_name, arg_value in prompt_config["args"].items():
                prompt_template = prompt_template.replace(f"{{{arg_name}}}", str(arg_value))
        
        # Replace the context placeholder
        formatted_prompt = prompt_template.replace("{context}", context)
        
        return self.ollama_client.generate_text(formatted_prompt)
    
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
        
        # Check if this is an epic template to handle special cases
        is_epic_template = "epic_template" in template_name
        
        # Generate standard fields first
        for field in fields:
            # Skip special handling fields for epics that will be processed separately
            if is_epic_template and field in ["bf_table_rows", "af_table_rows", "business_rules"]:
                continue
                
            print(f"\033[94mGenerating {field}...\033[0m")
            try:
                issue_data[field] = self.generate_issue_content(context, field)
            except ValueError as e:
                print(f"\033[93mWarning: Could not generate content for {field}: {str(e)}\033[0m")
                issue_data[field] = f"<!-- Missing content for {field} -->"
        
        # For epic templates, handle special cases
        if is_epic_template:
            # Generate and process basic flow steps
            if "bf_table_rows" in fields:
                print("\033[94mGenerating basic flow steps...\033[0m")
                bf_table_rows = self.generate_issue_content(context, "bf_table_rows")
                issue_data.update(self._format_table_steps(bf_table_rows, "bf_table_rows"))
            
            # Generate and process alternative flow steps
            if "af_table_rows" in fields:
                print("\033[94mGenerating alternative flow steps...\033[0m")
                af_table_rows = self.generate_issue_content(context, "af_table_rows")
                issue_data.update(self._format_table_steps(af_table_rows, "af_table_rows"))
            
            # Generate and process business rules
            if "business_rules" in fields:
                print("\033[94mGenerating business rules...\033[0m")
                business_rules = self.generate_issue_content(context, "business_rules")
                issue_data.update(self._process_business_rules(business_rules))
        
        # Render the template with the generated content
        return self.template_manager.render_template(template_content, issue_data)