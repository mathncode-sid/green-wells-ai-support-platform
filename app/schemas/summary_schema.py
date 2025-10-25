from pydantic import BaseModel

class SummarySchema(BaseModel):
    total_feedback: int
    positive_sentiment: str
    average_rating: float
    ai_accuracy: str
