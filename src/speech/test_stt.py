# src/speech/test_stt.py
from .base import BaseSTT

class TestSTT(BaseSTT):
    """A simple test STT that returns predefined responses"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.test_responses = [
            "This is a test transcription",
            "Hello, how can I help you today?",
            "I'm a test speech to text implementation"
        ]
        self.response_index = 0
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize the test STT system"""
        self.initialized = True
        return True
    
    def cleanup(self) -> None:
        """Cleanup any resources"""
        self.initialized = False
        self.response_index = 0
    
    def transcribe_audio(self) -> str:
        """
        Return a test transcription
        
        Returns:
            str: Test transcription text
        """
        if not self.initialized:
            self.initialize()
            
        # Cycle through test responses
        response = self.test_responses[self.response_index]
        self.response_index = (self.response_index + 1) % len(self.test_responses)
        
        print(f"Test STT returning: {response}")
        return response