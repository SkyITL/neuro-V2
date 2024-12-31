# src/speech/test_tts.py
from pathlib import Path
import wave
import numpy as np
from .base import BaseTTS

class TestTTS(BaseTTS):
    """A simple test TTS that creates a sine wave audio file"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.output_dir = Path("output/audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize the test TTS system"""
        self.initialized = True
        return True
    
    def cleanup(self) -> None:
        """Cleanup any resources"""
        self.initialized = False
    
    def synthesize_speech(self, text: str) -> str:
        """
        Create a simple sine wave audio file as a test
        
        Args:
            text: Text to convert to speech (used for filename)
        
        Returns:
            str: Path to generated audio file
        """
        if not self.initialized:
            self.initialize()
            
        # Create a simple sine wave
        sample_rate = 44100
        duration = 1  # seconds
        frequency = 440  # Hz (A4 note)
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Scale to 16-bit integer range
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Generate filename from first few chars of text
        filename = self.output_dir / f"test_{text[:10].replace(' ', '_')}.wav"
        
        # Write WAV file
        with wave.open(str(filename), 'w') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print(f"Generated test audio file: {filename}")
        return str(filename)