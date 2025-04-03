"""
Client for interacting with the Ollama API for text generation.
"""

import json
import requests


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gemma3:12b"):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Base URL for the Ollama API
            model: Ollama model to use
        """
        self.base_url = base_url
        self.model = model
    
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: Text prompt to feed to the model
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text as a string
            
        Raises:
            Exception: If there's an error communicating with Ollama
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "max_tokens": max_tokens
                }
            )
            response.raise_for_status()
            
            # Parse the streaming response
            generated_text = ""
            for line in response.iter_lines():
                if line:
                    response_obj = json.loads(line)
                    if 'response' in response_obj:
                        generated_text += response_obj['response']
                    
                    # Check if we've reached the end of the response
                    if response_obj.get('done', False):
                        break
                        
            return generated_text.strip()
        except Exception as e:
            raise Exception(f"Error generating text with Ollama: {str(e)}")