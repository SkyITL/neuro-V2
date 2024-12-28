import requests
from typing import Optional, Dict, Any
from .base import BaseLLM

class LlamaCpp(BaseLLM):
    def __init__(self, server_url: str, max_tokens: int = 2000, temperature: float = 0.7):
        self.server_url = server_url
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response using the llama.cpp server"""
        full_prompt = f"{context}\n{prompt}" if context else prompt
        
        payload = {
            "prompt": full_prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stop": ["\n\nUser:", "\n\nAssistant:"]
        }
        
        try:
            response = requests.post(self.server_url, json=payload)
            response.raise_for_status()
            return response.json()["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error communicating with llama.cpp server: {str(e)}")