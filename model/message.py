from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
	sender_id: int
	content: str
	chat_id: int = 0
	read: int = 0
	timeStamp: datetime = datetime.now()