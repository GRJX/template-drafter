"""
Issue generator module for creating issues from templates using AI.
"""

from typing import Dict

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
    
    def generate_issue_content(self, context: str, field: str) -> str:
        """
        Generate content for a specific field of an issue.
        
        Args:
            context: User-provided context for the issue
            field: Field to generate content for (e.g., 'description', 'acceptance_criteria')
            
        Returns:
            Generated content for the field
        """
        prompts = {
            "title": f"Create a brief, concise title (maximum 10 words) for this issue in Dutch. Only return the title without any explanation or additional text: {context}",
            "stakeholder": f"Identify the stakeholder or end-user for this issue. Return ONLY the role or type of user, without any explanation, additional text, or formatting, in 1-3 words: {context}",
            "doel": f"Write a VERY concise statement in Dutch about what the user wants to accomplish (WIL IK part of the user story). Keep it under 15 words. Return only the statement without WIL IK, any explanation or formatting: {context}",
            "waarde": f"Write a VERY concise statement in Dutch about the business value or benefit (ZODAT part of the user story). Keep it under 15 words. Return only the statement without ZODAT, any explanation or formatting: {context}",
            "huidige_situatie": f"Describe the current problem or situation in Dutch in 1-2 short sentences. Return only the description without any explanation or additional text: {context}",
            "gewenste_situatie": f"Describe the desired solution in Dutch in 1-2 short sentences. Return only the description without any explanation or additional text: {context}",
            "acceptatie_criteria": f"Generate 1-6 concise acceptance criteria for this issue. Format each item with an asterisk prefix. Return only the list in Dutch without any explanation or additional text: {context}"
        }
        
        if field not in prompts:
            raise ValueError(f"Unknown field: {field}")
        
        return self.ollama_client.generate_text(prompts[field])
    
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
        
        # Generate content for each field
        issue_data = {}
        fields = [
            "title", "stakeholder", "doel", "waarde", "huidige_situatie", 
            "gewenste_situatie", "acceptatie_criteria"
        ]
        
        for field in fields:
            print(f"Generating {field}...")
            issue_data[field] = self.generate_issue_content(context, field)
        
        # Render the template with the generated content
        return self.template_manager.render_template(template_content, issue_data)