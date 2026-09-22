# IIUI Smart Chatbot Configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Color Theme
COLORS = {
    'primary': '#06402B',      # Dark Green
    'secondary': '#FFFFFF',    # White
    'accent': '#0A5C3E',
    'text_dark': '#1a1a1a',
    'text_light': '#ffffff'
}

# Database Configuration
DB_CONFIG = {
    'sqlite_path': os.getenv('DATABASE_PATH', 'database/iiui_data.db'),
    'chat_log_path': os.getenv('CHAT_LOG_PATH', 'logs/chat_logs.db')
}

# API Configuration
API_CONFIG = {
    'embedding_model': os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2'),
    'max_tokens': int(os.getenv('MAX_TOKENS', 500)),
    'temperature': float(os.getenv('TEMPERATURE', 0.7))
}

# Authentication
AUTH_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY', 'iiui_smart_chatbot_2026_secret_change_in_production'),
    'session_timeout': int(os.getenv('SESSION_TIMEOUT', 3600))
}

# Voice Configuration
VOICE_CONFIG = {
    'language': os.getenv('VOICE_LANGUAGE', 'en-US'),
    'sample_rate': int(os.getenv('VOICE_SAMPLE_RATE', 16000))
}

# IIUI Information
UNIVERSITY_INFO = {
    'name': 'International Islamic University Islamabad',
    'short_name': 'IIUI',
    'website': 'https://www.iiu.edu.pk/',
    'general_hours': 'Monday to Friday, 8:00 AM to 5:00 PM'
}

# Server Configuration
SERVER_CONFIG = {
    'host': os.getenv('API_HOST', '0.0.0.0'),
    'port': int(os.getenv('API_PORT', 5000)),
    'debug': os.getenv('DEBUG', 'True').lower() == 'true'
}