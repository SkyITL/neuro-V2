from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    content: str
    timestamp: datetime = datetime.now()
    speaker: str = "user"  # "user" or "assistant"
    audio_path: Optional[str] = None