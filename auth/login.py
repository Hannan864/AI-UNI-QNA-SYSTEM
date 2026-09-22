import bcrypt
from database.db import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    def register_user(self, email, password, name='', role='student'):
        """Register a new user"""
        hashed_password = self.hash_password(password)
        user_id = self.db.add_user(email, hashed_password, name, role)
        return user_id
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password.
        Uses generic error messages to prevent user enumeration."""
        user = self.db.get_user_by_email(email)

        if user is None:
            return None, "Invalid email or password."

        if not self.verify_password(password, user['password_hash']):
            return None, "Invalid email or password."

        # Check account status
        status = user.get('status', 'active')
        if status != 'active':
            return None, "Your account is currently disabled."

        return user, "Authentication successful"
    
    def create_default_admin(self):
        """Create default admin user for testing"""
        # Check if admin exists
        admin = self.db.get_user_by_email('admin@iiu.edu.pk')
        
        if admin is None:
            self.register_user(
                email='admin@iiu.edu.pk',
                password='admin123',
                name='Admin User',
                role='admin'
            )
            print("Default admin created: admin@iiu.edu.pk / admin123")