import azure.cognitiveservices.speech as speechsdk
import sounddevice as sd
import numpy as np
from .base import BaseSpeechInterface

class SpeechToText(BaseSpeechInterface):
    def __init__(self, azure_key: str, azure_region: str):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=azure_key,
            region=azure_region
        )

    def transcribe_audio(self) -> str:
        """Record audio from microphone and transcribe"""
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )

        print("Listening... (Press Enter to stop)")
        
        # Start continuous recognition
        done = False
        transcript = []

        def handle_result(evt):
            transcript.append(evt.result.text)

        speech_recognizer.recognized.connect(handle_result)
        
        # Start recognition
        speech_recognizer.start_continuous_recognition()
        input()  # Wait for Enter key
        speech_recognizer.stop_continuous_recognition()
        
        return " ".join(transcript)