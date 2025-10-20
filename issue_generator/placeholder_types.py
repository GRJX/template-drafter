"""
Placeholder type generators for different content generation strategies.
"""

from typing import List
from .ollama_client import OllamaClient


class PlaceholderTypes:
    """Handles different types of content generation for template placeholders."""
    
    def __init__(self, ollama_client: OllamaClient, output_format: str = 'jira'):
        """
        Initialize the PlaceholderTypes.
        
        Args:
            ollama_client: Pre-initialized client for generating text with Ollama
            output_format: The desired output format ('jira' or 'adoc')
        """
        self.ollama_client = ollama_client
        self.output_format = output_format

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
            - Return without any additional text or punctuations.

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
        
        prompt = f"""
            Create a list of bullet points. 
            
            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - Maximum {bullet_limit} bullet points.
            - "Bullet format: '* <bullet_item>'."
            - Return without any explanation, additional text or special characters beyond the bullet format.

            This is the context: {context}
        """
        return self.ollama_client.generate_text(prompt)

    def generate_numbered(self, context: str, step_limit: int = 5, additional_info: str = '') -> str:
        """
        Generate a numbered list of sequential steps.
        
        Args:
            context: User-provided context for the numbered steps
            step_limit: Maximum number of steps to generate (default: 5)
            additional_info: Additional prompt information (optional)
            
        Returns:
            Generated numbered steps as a string
        """

        # Define format-specific rules
        if self.output_format == 'adoc':
            number_format = "'. <step_item>'."
        else: # Default to Jira
            number_format = "'# <step_item>'."
        
        prompt = f"""
            Create a list of sequential steps or items. 
            
            Additional information that overrules the rules if contradicting: {additional_info}

            Rules:
            - Maximum {step_limit} numbered items.
            - Each step should be clear and actionable.
            - Don't use number to sequence steps, but this format: {number_format}.
            - Return without any explanation, additional text or special characters beyond the number format.

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
            header_format_rule = f"Table headers: {table_headers}. Start table with '|===\n'. Formatted the headers like: '|*header1* |*header2* |...'"
            row_format_rule = "Table rows format: '|row1 |row2 |...'. Start each data row with '|'. End table with '|==='."
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
