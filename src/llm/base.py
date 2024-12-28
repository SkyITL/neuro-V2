from abc import ABC, abstractmethod
from typing import Optional

class BaseLLM(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response to the given prompt"""
        pass