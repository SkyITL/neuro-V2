# src/core/chat_manager.py

from typing import List, Dict, Optional
from ..llm.base import BaseLLM
from ..speech.base import BaseTTS, BaseSTT

class ChatManager:
    def __init__(
        self,
        llm: BaseLLM,
        tts: Optional[BaseTTS] = None,
        stt: Optional[BaseSTT] = None
    ):
        self.llm = llm
        self.tts = tts
        self.stt = stt
        self.conversation_history: List[Dict[str, str]] = []

    def add_message(self, content: str, role: str = "user") -> None:
        """Add a message to the conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def get_response(self, text_input: str) -> Dict[str, str]:
        """Get response from LLM and optionally convert to speech"""
        # Add user input to history
        self.add_message(text_input, "user")
        
        # Generate LLM response
        response_text = self.llm.generate_response(
            text_input,
            context=self.conversation_history[:-1]  # Exclude latest message
        )
        
        # Add response to history
        self.add_message(response_text, "assistant")
        
        result = {"text": response_text}
        
        # Synthesize speech if TTS is available
        if self.tts:
            audio_path = self.tts.synthesize_speech(response_text)
            if audio_path:
                result["audio_path"] = audio_path
                
        return result