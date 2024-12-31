import requests
from typing import Optional, Dict, Any
from .base import BaseLLM

class LlamaCpp(BaseLLM):
    def __init__(self, server_url: str, max_tokens: int = 2000, temperature: float = 0.7):
        self.server_url = server_url
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate_response(self, prompt: str, context: Optional[list[Dict[str, str]]] = None) -> str:
        """Generate a response using the llama.cpp server"""
        try:
            # Format context if provided
            if context:
                formatted_context = "\n".join([
                    f"{msg['role']}: {msg['content']}" 
                    for msg in context
                ])
                full_prompt = f"{formatted_context}\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = f"User: {prompt}\nAssistant:"
            
            # Prepare the request payload
            payload = {
                "prompt": full_prompt,
                "n_predict": self.max_tokens,
                "temperature": self.temperature,
                "stop": ["\nUser:", "\nAssistant:", "\n\n"],
                "stream": False
            }
            
            print(f"\nSending request to: {self.server_url}")
            print(f"Payload: {payload}")
            
            # Send request to the completion endpoint
            response = requests.post(f"{self.server_url}", json=payload)
            response.raise_for_status()
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            
            # Extract the generated text
            response_data = response.json()
            print(f"Response data: {response_data}")
            
            generated_text = response_data.get('content', '').strip()
            
            # Check for empty response
            if not generated_text:
                print(f"Warning: Empty response from server")
                return "I apologize, but I received an empty response. Please try again."
            
            return generated_text

        except requests.exceptions.RequestException as e:
            error_msg = f"Error communicating with llama.cpp server: {str(e)}"
            print(error_msg)
            return f"I apologize, but there was an error: {error_msg}"
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"I apologize, but there was an unexpected error: {str(e)}"