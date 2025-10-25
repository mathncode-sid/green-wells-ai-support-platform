from fastapi import APIRouter, HTTPException
from app.core.database import get_all_feedback
from app.core.ai_utils import calculate_metrics
import random

router = APIRouter()

@router.get("/metrics")
def get_metrics():
    """Get analytics metrics for admin dashboard."""
    try:
        feedbacks = get_all_feedback()
        metrics = calculate_metrics(feedbacks)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating metrics: {str(e)}")

@router.get("/insights")
def get_insights():
    """Get AI-generated operational insights."""
    try:
        feedbacks = get_all_feedback()
        
        if not feedbacks:
            return {
                "insights": ["No data available yet. Collect more feedback to generate insights."]
            }
        
        positive_count = sum(1 for f in feedbacks if f.get("sentiment") == "Positive")
        total = len(feedbacks)
        positive_percentage = (positive_count / total * 100) if total > 0 else 0
        
        insights = []
        
        if positive_percentage > 80:
            insights.append("Customer satisfaction is excellent! Keep up the great service.")
        elif positive_percentage > 60:
            insights.append("Customer satisfaction is good. Focus on addressing negative feedback.")
        else:
            insights.append("Customer satisfaction needs improvement. Review recent complaints.")
        
        avg_rating = sum(f.get("rating", 0) for f in feedbacks) / len(feedbacks) if feedbacks else 0
        if avg_rating >= 4.5:
            insights.append("Average rating is excellent. Customers are very satisfied.")
        elif avg_rating >= 3.5:
            insights.append("Average rating is good. Continue improving service quality.")
        else:
            insights.append("Average rating is below expectations. Immediate action needed.")
        
        if len(feedbacks) > 10:
            insights.append("You have sufficient feedback data for reliable analytics.")
        else:
            insights.append("Collect more feedback for more accurate insights.")
        
        return {
            "total_feedback": total,
            "positive_sentiment_percentage": positive_percentage,
            "average_rating": round(avg_rating, 1),
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@router.get("/chats")
def get_all_chats():
    """Fetch all conversations for admin monitoring."""
    try:
        from app.core.database import load_data
        data = load_data()
        chats = data.get("chats", [])
        
        return {
            "total_chats": len(chats),
            "chats": chats[-20:]  # Return last 20 chats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chats: {str(e)}")

@router.get("/team-performance")
def get_team_performance():
    """Get simulated team performance metrics."""
    try:
        return {
            "total_agents": 5,
            "active_agents": 4,
            "average_response_time": "2.3 minutes",
            "customer_satisfaction": "92%",
            "agents": [
                {"name": "Agent 1", "chats_handled": 45, "satisfaction": "94%"},
                {"name": "Agent 2", "chats_handled": 38, "satisfaction": "89%"},
                {"name": "Agent 3", "chats_handled": 52, "satisfaction": "95%"},
                {"name": "Agent 4", "chats_handled": 41, "satisfaction": "91%"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving team performance: {str(e)}")
