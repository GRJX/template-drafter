"""
Client for interacting with the Ollama API for text generation.
"""

import time
import ollama
import re


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gemma3:12b", 
                 system_prompt: str = "You are a helpful AI assistant."):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Base URL for the Ollama API
            model: Ollama model to use
            system_prompt: The system prompt to guide the AI model
        """
        self.base_url = base_url
        self.model = model
        self.system_prompt = system_prompt
        self.ollama_sdk_client = ollama.Client(host=self.base_url)
    
    def generate_text(self, prompt: str, max_tokens: int = 300, 
                      temperature: float = 0.1, top_p: float = 0.1, 
                      top_k: int = 20, presence_penalty: float = 0.1,
                      frequency_penalty: float = 0.1) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: Text prompt to feed to the model
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0.0-1.0, lower is more deterministic)
            top_p: Nucleus sampling parameter (0.0-1.0)
            top_k: Limits token selection to k most likely tokens
            presence_penalty: Penalizes repeated tokens (0.0-1.0)
            frequency_penalty: Penalizes frequent tokens (0.0-1.0)
            
        Returns:
            Generated text as a string
            
        Raises:
            Exception: If there's an error communicating with Ollama
        """
        try:
            # Start timing
            start_time = time.time()
            
            # Clean up prompt by removing newlines and excessive spaces
            cleaned_prompt = " ".join(prompt.replace("\n", " ").split())
            
            # Prepare generation parameters
            params = {
                "model": self.model,
                "prompt": cleaned_prompt,
                "system": self.system_prompt,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "presence_penalty": presence_penalty,
                    "frequency_penalty": frequency_penalty,
                }
            }
            
            # Using ollama library for streaming generation
            result = self._process_streaming_generation(params)
            
            # Log metrics
            self._log_metrics(
                start_time=start_time,
                end_time=time.time(),
                first_token_time=result["first_token_time"],
                token_times=result["token_times"],
                total_prompt_tokens=result["total_prompt_tokens"],
                total_completion_tokens=result["total_completion_tokens"]
            )
            
            # Print success message in green
            print("\033[92mGeneration completed successfully\033[0m")
            
            # Clean the response to remove any thinking tags
            cleaned_text = self._clean_response(result["text"])
            
            return cleaned_text
        except Exception as e:
            # Print error in red
            print(f"\033[91mError: {str(e)}\033[0m")
            raise Exception(f"Error generating text with Ollama: {str(e)}")
    
    def _process_streaming_generation(self, params):
        """Process the streaming generation using ollama library."""
        generated_text = ""
        total_prompt_tokens = 0
        total_completion_tokens = 0
        first_token_time = None
        token_times = []
        
        # Use the instance's ollama.Client to get streaming response
        for chunk in self.ollama_sdk_client.generate(**params, stream=True):
            current_time = time.time()
            
            if 'response' in chunk:
                if first_token_time is None:
                    first_token_time = current_time
                
                generated_text += chunk['response']
                token_times.append(current_time)
            
            # Extract token counts if available
            if 'prompt_eval_count' in chunk:
                total_prompt_tokens = chunk['prompt_eval_count']
            if 'eval_count' in chunk:
                total_completion_tokens = chunk['eval_count']
        
        return {
            "text": generated_text.strip(),
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "first_token_time": first_token_time,
            "token_times": token_times
        }
    
    def _log_metrics(self, start_time, end_time, first_token_time, token_times, 
                     total_prompt_tokens, total_completion_tokens):
        """Log performance metrics for the generation process."""
        # Calculate token timing metrics
        tokens_per_second = None
        if first_token_time and token_times:
            generation_time = token_times[-1] - first_token_time if len(token_times) > 1 else 0.001
            
            if generation_time > 0.05 and total_completion_tokens > 0:
                tokens_per_second = total_completion_tokens / generation_time
        
        total_time = end_time - start_time
        
        # Print metrics with muted color
        print("\n\t\033[90m--- LLM Request Metrics ---")
        print(f"\tPrompt tokens: {total_prompt_tokens}")
        print(f"\tCompletion tokens: {total_completion_tokens}")
        print(f"\tTotal time: {total_time:.3f}s")
        if tokens_per_second is not None:
            print(f"\tSpeed: {tokens_per_second:.2f} tokens/second")
        else:
            print("\tSpeed: N/A tokens/second")
        print("\t---------------------------\033[0m\n")
    
    def _clean_response(self, text: str) -> str:
        """Remove thinking tags and other unwanted elements from the response."""
        # Remove <think>...</think> tags and their content
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove any standalone <think> or </think> tags
        text = re.sub(r'</?think>', '', text, flags=re.IGNORECASE)
        
        # Clean up any extra whitespace that might be left
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Replace multiple newlines with double newlines
        text = text.strip()
        
        return text
