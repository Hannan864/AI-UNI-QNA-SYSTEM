# Security Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Current Security Analysis

### 1.1 Security Features Present

| Feature | Status | Notes |
|---------|--------|-------|
| Password hashing | ✅ bcrypt | Good |
| Parameterized queries | ✅ SQLite | Prevents SQL injection |
| Session management | ⚠️ In-memory | Lost on restart |
| Input validation | ❌ Missing | Major risk |
| HTTPS | ❌ Missing | Plain HTTP |
| Rate limiting | ❌ Missing | Abuse potential |
| CORS | ✅ Flask-CORS | Configured |
| CSRF protection | ❌ Missing | Vulnerability |

### 1.2 Security Issues Found

#### Critical
1. **Hardcoded secrets** — Secret key in config.py
2. **No input validation** — API accepts any input
3. **No admin access control** — Any user can access admin endpoints
4. **In-memory sessions** — Lost on server restart

#### High
1. **No HTTPS** — Data transmitted in plain text
2. **No rate limiting** — Vulnerable to brute force
3. **No CSRF protection** — Cross-site request forgery possible
4. **Demo credentials visible** — Admin password shown in UI

#### Medium
1. **No password complexity** — Weak passwords allowed
2. **No account lockout** — Unlimited login attempts
3. **No audit logging** — Admin actions not tracked
4. **No session timeout enforcement** — Sessions may persist

#### Low
1. **No Content Security Policy** — XSS possible
2. **No HTTP security headers** — Missing protections
3. **Verbose error messages** — May leak information

---

## 2. Security Recommendations

### 2.1 Authentication Security

#### Password Policy
```python
PASSWORD_POLICY = {
    'min_length': 8,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_digit': True,
    'require_special': True,
    'max_length': 128
}

def validate_password(password):
    if len(password) < PASSWORD_POLICY['min_length']:
        return False, "Password must be at least 8 characters"
    if PASSWORD_POLICY['require_uppercase'] and not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if PASSWORD_POLICY['require_lowercase'] and not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    if PASSWORD_POLICY['require_digit'] and not any(c.isdigit() for c in password):
        return False, "Password must contain digit"
    if PASSWORD_POLICY['require_special'] and not any(not c.isalnum() for c in password):
        return False, "Password must contain special character"
    return True, "Valid"
```

#### Account Lockout
```python
LOGIN_ATTEMPTS = {
    'max_attempts': 5,
    'lockout_duration': 900,  # 15 minutes
    'window': 300  # 5 minutes
}

class AccountLockout:
    def __init__(self):
        self.attempts = {}
    
    def record_attempt(self, email):
        now = time.time()
        if email not in self.attempts:
            self.attempts[email] = []
        
        # Remove old attempts outside window
        self.attempts[email] = [
            t for t in self.attempts[email] 
            if now - t < LOGIN_ATTEMPTS['window']
        ]
        
        self.attempts[email].append(now)
    
    def is_locked(self, email):
        if email not in self.attempts:
            return False
        return len(self.attempts[email]) >= LOGIN_ATTEMPTS['max_attempts']
```

#### Email Validation
```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

---

### 2.2 Session Security

#### Environment Variables for Secrets
```python
# .env file
SECRET_KEY=your-secure-random-key-here
SESSION_TIMEOUT=3600

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY'),
    'session_timeout': int(os.getenv('SESSION_TIMEOUT', 3600))
}
```

#### Secure Session IDs
```python
import secrets

def create_session_id():
    return secrets.token_urlsafe(32)
```

#### Session Persistence
```python
# Store sessions in database
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    ip_address TEXT,
    user_agent TEXT
);
```

---

### 2.3 Input Validation

#### Request Validation Middleware
```python
from functools import wraps
from flask import request, jsonify

def validate_request(schema):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.json
            if not data:
                return jsonify({'success': False, 'message': 'No data provided'}), 400
            
            errors = []
            for field, rules in schema.items():
                value = data.get(field)
                
                # Required check
                if rules.get('required') and not value:
                    errors.append(f'{field} is required')
                    continue
                
                # Type check
                if value and rules.get('type') == 'email':
                    if not validate_email(value):
                        errors.append(f'{field} must be a valid email')
                
                # Length check
                if value and rules.get('max_length'):
                    if len(value) > rules['max_length']:
                        errors.append(f'{field} must be less than {rules["max_length"]} characters')
            
            if errors:
                return jsonify({'success': False, 'errors': errors}), 400
            
            return f(*args, **kwargs)
        return decorated
    return decorator

# Usage
@app.route('/api/register', methods=['POST'])
@validate_request({
    'email': {'required': True, 'type': 'email', 'max_length': 255},
    'password': {'required': True, 'min_length': 8, 'max_length': 128},
    'name': {'required': True, 'max_length': 100}
})
def register():
    # Registration logic
    pass
```

#### SQL Injection Prevention
```python
# Already using parameterized queries ✅
cursor.execute('SELECT * FROM users WHERE email = ?', (email,))

# Never do this ❌
cursor.execute(f'SELECT * FROM users WHERE email = "{email}"')
```

#### XSS Prevention
```python
import html

def sanitize_input(text):
    return html.escape(text)

def sanitize_output(text):
    # For display in HTML
    return html.escape(text)
```

---

### 2.4 API Security

#### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass

@app.route('/api/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    pass
```

#### CORS Configuration
```python
from flask_cors import CORS

# Restrict CORS in production
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8501"],  # Streamlit port
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

#### Security Headers
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

---

### 2.5 Admin Security

#### Admin Role Verification
```python
def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = session_manager.validate_session(session_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        if user.get('role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        
        return f(*args, user=user, **kwargs)
    return decorated
```

#### Audit Logging
```python
def log_admin_action(admin_email, action, target=None, details=None):
    conn = db._get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO audit_logs (admin_email, action, target, details, timestamp)
           VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''',
        (admin_email, action, target, details)
    )
    conn.commit()
    conn.close()
```

---

### 2.6 Environment Configuration

#### .env Template
```env
# Application
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secure-random-key-here

# Database
DATABASE_PATH=database/iiui_data.db
CHAT_LOG_PATH=logs/chat_logs.db

# Session
SESSION_TIMEOUT=3600

# API
API_HOST=0.0.0.0
API_PORT=5000

# Security
RATE_LIMIT_ENABLED=True
CORS_ORIGINS=http://localhost:8501
```

#### config.py Update
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/iiui_data.db')
    CHAT_LOG_PATH = os.getenv('CHAT_LOG_PATH', 'logs/chat_logs.db')
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

---

## 3. Security Checklist

### Authentication
- [ ] Password hashing with bcrypt
- [ ] Password complexity requirements
- [ ] Account lockout after failed attempts
- [ ] Email validation
- [ ] Secure session IDs
- [ ] Session timeout enforcement
- [ ] Session persistence in database

### Authorization
- [ ] Admin role verification
- [ ] Route protection middleware
- [ ] API endpoint authorization
- [ ] Resource-level access control

### Input Validation
- [ ] Request schema validation
- [ ] Parameterized SQL queries
- [ ] XSS prevention (input sanitization)
- [ ] File upload validation
- [ ] URL parameter validation

### API Security
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Security headers
- [ ] HTTPS (production)
- [ ] API key authentication (optional)

### Data Security
- [ ] Environment variables for secrets
- [ ] No hardcoded credentials
- [ ] Database encryption (optional)
- [ ] Backup encryption (optional)

### Monitoring
- [ ] Audit logging
- [ ] Error logging
- [ ] Login attempt logging
- [ ] Admin action logging

---

## 4. Security Testing

### 4.1 Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| SEC-001 | Login with SQL injection | Rejected |
| SEC-002 | Login with XSS payload | Sanitized |
| SEC-003 | Access admin route as student | 403 Forbidden |
| SEC-004 | Exceed rate limit | 429 Too Many Requests |
| SEC-005 | Use expired session | 401 Unauthorized |
| SEC-006 | Upload malicious file | Rejected |
| SEC-007 | Access without authentication | 401 Unauthorized |
| SEC-008 | Use weak password | Rejected |
| SEC-009 | Brute force login | Account locked |
| SEC-010 | Access other user's data | 403 Forbidden |

### 4.2 Testing Tools

1. **OWASP ZAP** — Web application security testing
2. **Burp Suite** — Vulnerability scanning
3. **Postman** — API security testing
4. **pytest** — Automated security tests

---

## 5. Production Security

### 5.1 Deployment Checklist

- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Set DEBUG=False
- [ ] Use environment variables
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Set security headers
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor for anomalies

### 5.2 Security Updates

```bash
# Check for vulnerable packages
pip audit

# Update packages
pip install --upgrade package-name

# Requirements with versions
pip freeze > requirements.txt
```

---

## 6. Incident Response

### 6.1 Security Incident Steps

1. **Identify** — Detect and confirm incident
2. **Contain** — Limit damage
3. **Eradicate** — Remove threat
4. **Recover** — Restore systems
5. **Learn** — Document and improve

### 6.2 Emergency Contacts

- **System Admin:** [Contact Info]
- **Security Team:** [Contact Info]
- **Management:** [Contact Info]

---

## 7. Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/patterns/)
- [Python Security](https://python-security.readthedocs.io/)
- [SQLite Security](https://www.sqlite.org/security.html)
