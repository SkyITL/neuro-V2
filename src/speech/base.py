# src/speech/base.py

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseSpeech(ABC):
    """Base class for all speech-related functionality"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize with optional configuration
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config or {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize any necessary resources or connections
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup any resources"""
        pass

class BaseTTS(BaseSpeech):
    """Base class for text-to-speech implementations"""
    
    @abstractmethod
    def synthesize_speech(self, text: str) -> Optional[str]:
        """
        Convert text to speech
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            Optional[str]: Path to the generated audio file, if any
        """
        pass
    
    def adjust_voice(self, voice_id: str) -> bool:
        """
        Optional method to change voice
        
        Args:
            voice_id (str): Identifier for the desired voice
            
        Returns:
            bool: True if voice changed successfully
        """
        return False
    
    def get_available_voices(self) -> list[str]:
        """
        Optional method to list available voices
        
        Returns:
            list[str]: List of available voice identifiers
        """
        return []

class BaseSTT(BaseSpeech):
    """Base class for speech-to-text implementations"""
    
    @abstractmethod
    def transcribe_audio(self) -> str:
        """
        Transcribe audio input to text
        
        Returns:
            str: Transcribed text
        """
        pass
    
    def transcribe_file(self, file_path: str) -> str:
        """
        Optional method to transcribe audio from file
        
        Args:
            file_path (str): Path to audio file
            
        Returns:
            str: Transcribed text
        """
        raise NotImplementedError("File transcription not implemented")
    
    def start_continuous_recognition(self) -> None:
        """Optional method to start continuous recognition"""
        raise NotImplementedError("Continuous recognition not implemented")
    
    def stop_continuous_recognition(self) -> None:
        """Optional method to stop continuous recognition"""
        raise NotImplementedError("Continuous recognition not implemented")
