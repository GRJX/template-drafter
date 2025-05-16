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
            Create a brief, concise title.

            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - Maximum {word_limit} words.
            - Return without any additional text or punctuation.

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
            Write clear and descriptive sentence(s) about the topic.

            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - The sentence should be functional and direct.
            - Maximum {word_limit} words.
            - Return without any explanation, additional text or newline characters.

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

         # Define format-specific rules
        if self.output_format == 'adoc':
            bullet_format = "Bullet format: '- <bullet_item> +'."
        else: # Default to Jira
            bullet_format = "Bullet format: '* <bullet_item>'."
        
        prompt = f"""
            Create a list of bullet points. 
            
            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - Maximum {bullet_limit} bullet points.
            - {bullet_format}
            - Return without any explanation, additional text or special characters beyond the bullet format.

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
            Select ONE option from the provided list.
            
            Available options: {options_str}

            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - Return ONLY the selected option.
            - Remove the information between brackets.
            - Return without any explanation or additional text.
            
            This is the context: {context}
        """
        return self.ollama_client.generate_text(prompt)

    def generate_tables(self, context: str, table_limit: int = 1, table_title: str = 'Table: <title>', table_headers: list = [], additional_info: str = '') -> str:
        """
        Generate tables in the specified format (Markdown or AsciiDoc).
        
        Args:
            context: User-provided context for the tables
            table_limit: Maximum number of tables to generate
            table_title: Title format string (e.g., "BF{n}: {title}")
            table_headers: List of header strings
            additional_info: Additional prompt information (optional)
            
        Returns:
            Generated tables as a structured string in the correct format.
        """
        
        # Define format-specific rules
        if self.output_format == 'adoc':
            title_format_rule = f"Table title format: '===== {{title}}' (e.g., '===== {table_title}'). If title is empty, omit this line. Include the attribute line '[cols=\"1,9\",options=\"header\"]' directly below the title and before the table start."
            header_format_rule = f"Table headers: {table_headers}. Start table with '|===\n'. Formatted the headers like: '|header1 |header2 |...'"
            row_format_rule = "Table rows format: 'a|row1 |row2 |...'. Start each data row with 'a|'. End table with '|==='."
        else: # Default to Markdown
            title_format_rule = f"Table tile is short, action-based and in format: {table_title}. If title is empty, omit this line."
            header_format_rule = f"Table headers are: {table_headers} in the format '||header1||header2||...||'."
            row_format_rule = "Table rows are in the format '|row1|row2|...|'."

        prompt = f"""
            Create one or more tables based on the context.

            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - Generate {table_limit} table(s).
            - Table text is in Dutch.
            - {title_format_rule}
            - {header_format_rule}
            - {row_format_rule}
            - Return only the title and table output, no extra text, newlines or code blocks.

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
            
            elif generation_type == "tables":
                table_limit = prompt_config.get("args", {}).get("table_limit", 1)
                # Process table_title format - replace placeholders like <abbreviation> if needed later
                raw_title_format = prompt_config.get("args", {}).get("table_title", "") 
                # Simple placeholder replacement for now, might need refinement
                processed_title = raw_title_format # Placeholder for potential future logic
                
                table_headers = prompt_config.get("args", {}).get("table_headers", ["Header1", "Header2"])
                
                return self.generate_tables(context, table_limit, processed_title, table_headers, additional_info)
            
            else:
                raise ValueError(f"Unsupported generation type: {generation_type}")
        
        return self.ollama_client.generate_text(prompt)
    
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
