from fastapi import APIRouter, HTTPException
from app.schemas.chat_schema import ChatSchema, ChatResponseSchema
from app.core.database import save_chat, get_chat_history
from app.core.ai_utils import generate_ai_response
from datetime import datetime

router = APIRouter()

@router.post("/ai", response_model=ChatResponseSchema)
def ai_chat(query: ChatSchema):
    """Get AI-generated chatbot response."""
    try:
        reply = generate_ai_response(query.message)
        conversation_id = save_chat(query.dict(), reply)
        
        return ChatResponseSchema(
            reply=reply,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.post("/agent")
def agent_chat(query: ChatSchema):
    """Simulate live support agent reply."""
    try:
        agent_replies = [
            "Thank you for contacting us. A support agent will be with you shortly.",
            "I understand your concern. Let me connect you with a specialist.",
            "We appreciate your patience. Our team is reviewing your request.",
            "Your issue has been escalated to our support team for immediate attention."
        ]
        
        import random
        reply = random.choice(agent_replies)
        conversation_id = save_chat(query.dict(), reply)
        
        return {
            "reply": reply,
            "agent_id": "agent_001",
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent chat: {str(e)}")

@router.get("/history/{conversation_id}")
def get_conversation_history(conversation_id: str):
    """Fetch conversation history for a specific conversation."""
    try:
        history = get_chat_history(conversation_id)
        return {
            "conversation_id": conversation_id,
            "messages": history,
            "total_messages": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")
