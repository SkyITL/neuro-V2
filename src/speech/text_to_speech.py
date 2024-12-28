import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime
from typing import Optional
from .base import BaseSpeechInterface

class TextToSpeech(BaseSpeechInterface):
    def __init__(
        self,
        azure_key: str,
        azure_region: str,
        voice_name: str = "en-US-JennyNeural"
    ):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=azure_key,
            region=azure_region
        )
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.output_dir = "output/audio"
        os.makedirs(self.output_dir, exist_ok=True)

    def synthesize_speech(self, text: str) -> str:
        """Synthesize text to speech and save to file"""
        filename = f"{self.output_dir}/response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )

        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return filename
        else:
            raise Exception(
                f"Speech synthesis failed: {result.reason}\n"
                f"Detailed error: {result.error_details}"
            )