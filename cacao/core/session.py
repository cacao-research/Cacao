"""Session management for Cacao applications."""

import json
import os
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

class SessionManager:
    def __init__(self, 
                 storage_type: str = "memory", 
                 persist_on_refresh: bool = True,
                 storage_path: str = "./sessions",
                 session_expiry: int = 86400): # 24 hours by default
        """
        Initialize the session manager.
        
        Args:
            storage_type: Where to store sessions ("memory", "file", or "database")
            persist_on_refresh: Whether to maintain state on page refresh
            storage_path: Where to store session files (if using file storage)
            session_expiry: Session expiration time in seconds
        """
        self.storage_type = storage_type
        self.persist_on_refresh = persist_on_refresh
        self.storage_path = storage_path
        self.session_expiry = session_expiry
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        if storage_type == "file":
            os.makedirs(storage_path, exist_ok=True)
    
    def create_session(self) -> str:
        """Create a new session and return the session ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": time.time(),
            "last_accessed": time.time(),
            "state": {}
        }
        
        if self.storage_type == "file":
            self._save_session_to_file(session_id)
            
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a session by ID."""
        if self.storage_type == "memory":
            if session_id in self.sessions:
                self.sessions[session_id]["last_accessed"] = time.time()
                return self.sessions[session_id]
            return None
            
        elif self.storage_type == "file":
            session_file = Path(self.storage_path) / f"{session_id}.json"
            if not session_file.exists():
                return None
                
            with open(session_file, "r") as f:
                session = json.load(f)
                session["last_accessed"] = time.time()
                self._save_session_to_file(session_id, session)
                return session
    
    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the state for a given session."""
        session = self.get_session(session_id)
        if session:
            return session.get("state", {})
        return None
    
    def update_session_state(self, session_id: str, state: Dict[str, Any]) -> bool:
        """Update the state for a given session."""
        if self.storage_type == "memory":
            if session_id not in self.sessions:
                return False
                
            self.sessions[session_id]["state"] = state
            self.sessions[session_id]["last_accessed"] = time.time()
            return True
            
        elif self.storage_type == "file":
            session_file = Path(self.storage_path) / f"{session_id}.json"
            if not session_file.exists():
                return False
                
            with open(session_file, "r") as f:
                session = json.load(f)
                
            session["state"] = state
            session["last_accessed"] = time.time()
            
            with open(session_file, "w") as f:
                json.dump(session, f)
                
            return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        if self.storage_type == "memory":
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False
            
        elif self.storage_type == "file":
            session_file = Path(self.storage_path) / f"{session_id}.json"
            if session_file.exists():
                os.remove(session_file)
                return True
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of removed sessions."""
        now = time.time()
        count = 0
        
        if self.storage_type == "memory":
            expired_sessions = []
            for session_id, session in self.sessions.items():
                if now - session["last_accessed"] > self.session_expiry:
                    expired_sessions.append(session_id)
                    
            for session_id in expired_sessions:
                del self.sessions[session_id]
            
            return len(expired_sessions)
            
        elif self.storage_type == "file":
            for session_file in Path(self.storage_path).glob("*.json"):
                with open(session_file, "r") as f:
                    session = json.load(f)
                    
                if now - session["last_accessed"] > self.session_expiry:
                    os.remove(session_file)
                    count += 1
                    
            return count
    
    def _save_session_to_file(self, session_id: str, session=None) -> None:
        """Save a session to a file."""
        if session is None:
            session = self.sessions[session_id]
            
        session_file = Path(self.storage_path) / f"{session_id}.json"
        with open(session_file, "w") as f:
            json.dump(session, f)