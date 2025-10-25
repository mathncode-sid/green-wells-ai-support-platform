from pydantic import BaseModel
from typing import Optional

class ChatSchema(BaseModel):
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponseSchema(BaseModel):
    reply: str
    conversation_id: str
    timestamp: str
