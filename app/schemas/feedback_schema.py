from pydantic import BaseModel, EmailStr
from typing import Optional

class FeedbackSchema(BaseModel):
    name: str
    email: EmailStr
    service: str
    rating: int
    comment: str

class FeedbackResponseSchema(BaseModel):
    message: str
    sentiment: str
    summary: str
    id: Optional[str] = None
