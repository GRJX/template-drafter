"""
Client for interacting with the Ollama API for text generation.
"""

import json
import requests
import time


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
            
            payload = {
                "model": self.model,
                "prompt": cleaned_prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
            }
            
            # Make the API request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True
            )
            response.raise_for_status()
            
            # Process the response
            result = self._process_streaming_response(response)
            
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
            
            return result["text"]
        except Exception as e:
            # Print error in red
            print(f"\033[91mError: {str(e)}\033[0m")
            raise Exception(f"Error generating text with Ollama: {str(e)}")
    
    def _process_streaming_response(self, response):
        """Process the streaming response from Ollama API."""
        generated_text = ""
        total_prompt_tokens = 0
        total_completion_tokens = 0
        first_token_time = None
        token_times = []
        
        for line in response.iter_lines():
            if not line:
                continue
                
            current_time = time.time()
            
            try:
                response_obj = json.loads(line)
                
                if 'response' in response_obj:
                    if first_token_time is None:
                        first_token_time = current_time
                    
                    generated_text += response_obj['response']
                    token_times.append(current_time)
                
                # Extract token counts if available
                if 'prompt_eval_count' in response_obj:
                    total_prompt_tokens = response_obj['prompt_eval_count']
                if 'eval_count' in response_obj:
                    total_completion_tokens = response_obj['eval_count']
                
                # Check if we've reached the end of the response
                if response_obj.get('done', False):
                    break
            except json.JSONDecodeError:
                # Skip lines that aren't valid JSON
                continue
        
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
