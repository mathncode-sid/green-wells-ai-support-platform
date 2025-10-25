import json
import os
from datetime import datetime
from typing import List, Dict, Any

DATA_STORE_PATH = "app/static/data_store.json"

def initialize_data_store():
    """Initialize the JSON data store if it doesn't exist."""
    if not os.path.exists("app/static"):
        os.makedirs("app/static")
    
    if not os.path.exists(DATA_STORE_PATH):
        initial_data = {
            "feedbacks": [],
            "chats": [],
            "agents": []
        }
        with open(DATA_STORE_PATH, "w") as f:
            json.dump(initial_data, f, indent=4)

def load_data() -> Dict[str, Any]:
    """Load data from JSON store."""
    initialize_data_store()
    with open(DATA_STORE_PATH, "r") as f:
        return json.load(f)

def save_data(data: Dict[str, Any]):
    """Save data to JSON store."""
    with open(DATA_STORE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def save_feedback(feedback_data: Dict[str, Any], sentiment: str, summary: str) -> str:
    """Save feedback to the data store."""
    data = load_data()
    feedback_id = f"fb_{len(data['feedbacks']) + 1}"
    
    feedback_entry = {
        "id": feedback_id,
        "name": feedback_data.get("name"),
        "email": feedback_data.get("email"),
        "service": feedback_data.get("service"),
        "rating": feedback_data.get("rating"),
        "comment": feedback_data.get("comment"),
        "sentiment": sentiment,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }
    
    data["feedbacks"].append(feedback_entry)
    save_data(data)
    return feedback_id

def get_all_feedback() -> List[Dict[str, Any]]:
    """Retrieve all feedback."""
    data = load_data()
    return data.get("feedbacks", [])

def save_chat(chat_data: Dict[str, Any], reply: str) -> str:
    """Save chat message to the data store."""
    data = load_data()
    conversation_id = chat_data.get("conversation_id", f"conv_{len(data['chats']) + 1}")
    
    chat_entry = {
        "id": f"chat_{len(data['chats']) + 1}",
        "conversation_id": conversation_id,
        "user_id": chat_data.get("user_id"),
        "user_message": chat_data.get("message"),
        "ai_reply": reply,
        "timestamp": datetime.now().isoformat()
    }
    
    data["chats"].append(chat_entry)
    save_data(data)
    return conversation_id

def get_chat_history(conversation_id: str) -> List[Dict[str, Any]]:
    """Retrieve chat history for a conversation."""
    data = load_data()
    return [chat for chat in data.get("chats", []) if chat.get("conversation_id") == conversation_id]
