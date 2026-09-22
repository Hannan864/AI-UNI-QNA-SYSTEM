import hashlib
import time
from config import AUTH_CONFIG

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.timeout = AUTH_CONFIG['session_timeout']
    
    def create_session(self, user_email):
        """Create a new session for user"""
        session_id = hashlib.sha256(
            f"{user_email}{time.time()}".encode()
        ).hexdigest()
        
        self.sessions[session_id] = {
            'user_email': user_email,
            'created_at': time.time(),
            'last_active': time.time()
        }
        
        return session_id
    
    def validate_session(self, session_id):
        """Validate if session is active"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session expired
        if time.time() - session['last_active'] > self.timeout:
            del self.sessions[session_id]
            return None
        
        # Update last active time
        session['last_active'] = time.time()
        
        return session['user_email']
    
    def end_session(self, session_id):
        """End a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = time.time()
        expired = [
            sid for sid, session in self.sessions.items()
            if current_time - session['last_active'] > self.timeout
        ]
        
        for sid in expired:
            del self.sessions[sid]