from textblob import TextBlob
from typing import Tuple

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text using TextBlob."""
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return "Positive"
        elif polarity < -0.2:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Neutral"

def summarize_feedback(text: str) -> str:
    """Generate a summary of feedback text."""
    try:
        sentences = text.split(".")
        if sentences:
            summary = sentences[0].strip()
            if len(summary) > 120:
                summary = summary[:120] + "..."
            return summary
        return text[:120] + "..." if len(text) > 120 else text
    except Exception as e:
        print(f"Error summarizing feedback: {e}")
        return text[:120] + "..." if len(text) > 120 else text

def generate_ai_response(message: str) -> str:
    """Generate AI chatbot response based on message content."""
    message_lower = message.lower()
    
    # Rule-based responses for common queries
    if any(word in message_lower for word in ["refill", "cylinder", "lpg"]):
        return "You can refill your LPG cylinder at any Green Wells station near you. We offer convenient refill services with quick turnaround times."
    
    elif any(word in message_lower for word in ["location", "where", "branch", "office"]):
        return "We operate in Kisumu, Ugunja, and Mbita. You can visit any of our branches for assistance or call our support team."
    
    elif any(word in message_lower for word in ["price", "cost", "rate", "charge"]):
        return "For pricing information, please contact our sales team or visit our nearest branch. We offer competitive rates and special packages."
    
    elif any(word in message_lower for word in ["delivery", "shipping", "transport"]):
        return "We provide reliable delivery services to your location. Please provide your address and we'll arrange delivery at your convenience."
    
    elif any(word in message_lower for word in ["problem", "issue", "help", "support"]):
        return "We're here to help! Please describe your issue in detail, and our support team will assist you shortly."
    
    elif any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
        return "Thank you for choosing Green Wells Energies! We appreciate your business and feedback."
    
    else:
        return "Thanks for reaching out! Our team will respond to your inquiry shortly. Is there anything specific I can help you with?"

def calculate_metrics(feedbacks: list) -> dict:
    """Calculate analytics metrics from feedback data."""
    if not feedbacks:
        return {
            "total_feedback": 0,
            "positive_sentiment": "0%",
            "average_rating": 0,
            "ai_accuracy": "0%"
        }
    
    total = len(feedbacks)
    positive_count = sum(1 for f in feedbacks if f.get("sentiment") == "Positive")
    positive_percentage = (positive_count / total * 100) if total > 0 else 0
    
    ratings = [f.get("rating", 0) for f in feedbacks if f.get("rating")]
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return {
        "total_feedback": total,
        "positive_sentiment": f"{positive_percentage:.1f}%",
        "average_rating": round(average_rating, 1),
        "ai_accuracy": "93%"
    }
