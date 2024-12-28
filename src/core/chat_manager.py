import logging
from typing import List
from .message import Message
from ..llm.base import BaseLLM
from ..speech.text_to_speech import TextToSpeech
from ..speech.speech_to_text import SpeechToText

class ChatManager:
    def __init__(
        self,
        llm: BaseLLM,
        tts: TextToSpeech,
        stt: SpeechToText
    ):
        self.llm = llm
        self.tts = tts
        self.stt = stt
        self.conversation_history: List[Message] = []
        self.logger = logging.getLogger(__name__)

    def process_voice_input(self) -> Message:
        """Record and transcribe user's voice input"""
        text = self.stt.transcribe_audio()
        message = Message(content=text, speaker="user")
        self.conversation_history.append(message)
        return message

    def generate_response(self, user_message: Message) -> Message:
        """Generate LLM response and convert to speech"""
        # Format conversation history for LLM context
        context = self._format_conversation_history()
        
        # Get LLM response
        response_text = self.llm.generate_response(
            user_message.content,
            context=context
        )
        
        # Convert to speech
        audio_path = self.tts.synthesize_speech(response_text)
        
        # Create and store message
        response = Message(
            content=response_text,
            speaker="assistant",
            audio_path=audio_path
        )
        self.conversation_history.append(response)
        
        return response

    def _format_conversation_history(self) -> str:
        """Format conversation history for LLM context"""
        formatted = []
        for msg in self.conversation_history[-5:]:  # Last 5 messages
            speaker = "User" if msg.speaker == "user" else "Assistant"
            formatted.append(f"{speaker}: {msg.content}")
        return "\n".join(formatted)