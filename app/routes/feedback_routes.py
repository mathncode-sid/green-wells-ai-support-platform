from fastapi import APIRouter, HTTPException
from app.schemas.feedback_schema import FeedbackSchema, FeedbackResponseSchema
from app.core.database import save_feedback, get_all_feedback
from app.core.ai_utils import analyze_sentiment, summarize_feedback

router = APIRouter()

@router.post("/submit", response_model=FeedbackResponseSchema)
def submit_feedback(feedback: FeedbackSchema):
    """Submit user feedback with AI sentiment analysis and summarization."""
    try:
        sentiment = analyze_sentiment(feedback.comment)
        summary = summarize_feedback(feedback.comment)
        feedback_id = save_feedback(feedback.dict(), sentiment, summary)
        
        return FeedbackResponseSchema(
            message="Feedback received successfully",
            sentiment=sentiment,
            summary=summary,
            id=feedback_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")

@router.get("/all")
def get_all_feedbacks():
    """Retrieve all stored feedback (admin endpoint)."""
    try:
        feedbacks = get_all_feedback()
        return {
            "total": len(feedbacks),
            "feedbacks": feedbacks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedback: {str(e)}")

@router.get("/summary")
def get_feedback_summary():
    """Get AI-generated summary of all feedback."""
    try:
        feedbacks = get_all_feedback()
        if not feedbacks:
            return {"message": "No feedback available yet"}
        
        positive_count = sum(1 for f in feedbacks if f.get("sentiment") == "Positive")
        negative_count = sum(1 for f in feedbacks if f.get("sentiment") == "Negative")
        neutral_count = sum(1 for f in feedbacks if f.get("sentiment") == "Neutral")
        
        return {
            "total_feedback": len(feedbacks),
            "sentiment_breakdown": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            },
            "recent_summaries": [f.get("summary") for f in feedbacks[-5:]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
