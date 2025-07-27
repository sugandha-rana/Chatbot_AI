from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = timedelta(hours=1)  # 1 hour timeout
        self.next_session_id = 1  # Simple counter for session IDs
    
    def create_session(self, user_type: str) -> str:
        """Create a new session and return session ID"""
        session_id = str(self.next_session_id)
        self.sessions[session_id] = {
            "user_type": user_type,
            "chat_history": [],
            "context": {},
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        self.next_session_id += 1
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data if it exists and is not expired"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        if datetime.now() - session["last_activity"] > self.session_timeout:
            # Session expired, remove it
            del self.sessions[session_id]
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now()
        return session
    
    def add_to_history(self, session_id: str, user_message: str, assistant_response: str):
        """Add a conversation turn to the session history"""
        session = self.get_session(session_id)
        if session:
            session["chat_history"].append({
                "user": user_message,
                "assistant": assistant_response,
                "timestamp": datetime.now()
            })
    
    def get_chat_history(self, session_id: str) -> List[Dict]:
        """Get formatted chat history for LangChain"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        # Format for LangChain ConversationalChatAgent
        history = []
        for turn in session["chat_history"]:
            history.append((turn["user"], turn["assistant"]))
        return history
    
    def update_context(self, session_id: str, key: str, value: any):
        """Update session context (e.g., lost item details)"""
        session = self.get_session(session_id)
        if session:
            session["context"][key] = value
    
    def get_context(self, session_id: str, key: str) -> any:
        """Get context value"""
        session = self.get_session(session_id)
        if session:
            return session["context"].get(key)
        return None
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session["last_activity"] > self.session_timeout
        ]
        for session_id in expired_sessions:
            del self.sessions[session_id]

# Global session manager instance
session_manager = SessionManager() 