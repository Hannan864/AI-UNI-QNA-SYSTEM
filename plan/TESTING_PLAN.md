# Testing Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Testing Strategy Overview

### 1.1 Testing Levels

1. **Unit Testing** — Individual functions
2. **Integration Testing** — Component interaction
3. **API Testing** — Endpoint verification
4. **Database Testing** — Data integrity
5. **UI Testing** — User interface
6. **Security Testing** — Vulnerability assessment
7. **Performance Testing** — Speed and scalability
8. **User Acceptance Testing** — Final validation

### 1.2 Testing Framework

```python
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-flask>=1.2.0
requests>=2.31.0
faker>=18.0.0
```

---

## 2. Unit Testing

### 2.1 NLP Processor Tests

```python
# tests/test_nlp_processor.py
import pytest
from models.nlp_processor import NLPProcessor

@pytest.fixture
def nlp():
    return NLPProcessor()

def test_preprocess_text(nlp):
    result = nlp.preprocess_text("What is the admission process?")
    assert isinstance(result, str)
    assert "admission" in result.lower()

def test_extract_entities(nlp):
    entities = nlp.extract_entities("IIUI is in Islamabad")
    assert 'organizations' in entities
    assert 'locations' in entities

def test_get_keywords(nlp):
    keywords = nlp.get_keywords("admission process at IIUI")
    assert isinstance(keywords, list)
    assert len(keywords) > 0

def test_calculate_similarity(nlp):
    score = nlp.calculate_similarity("admission process", "admission procedure")
    assert 0 <= score <= 1
    assert score > 0.5  # Should be similar
```

### 2.2 FAQ Retriever Tests

```python
# tests/test_retriever.py
import pytest
from models.retriever import FAQRetriever

@pytest.fixture
def retriever():
    return FAQRetriever()

def test_retrieve(retriever):
    results = retriever.retrieve("admission process")
    assert isinstance(results, list)
    assert len(results) > 0
    assert 'question' in results[0]
    assert 'answer' in results[0]
    assert 'confidence' in results[0]

def test_retrieve_confidence(retriever):
    results = retriever.retrieve("admission")
    for result in results:
        assert 0 <= result['confidence'] <= 1

def test_add_new_faq(retriever):
    faq_id = retriever.add_new_faq(
        question="Test question?",
        answer="Test answer",
        tags="test",
        category="Test"
    )
    assert faq_id is not None
```

### 2.3 Answer Generator Tests

```python
# tests/test_generator.py
import pytest
from models.generator import AnswerGenerator

@pytest.fixture
def generator():
    return AnswerGenerator()

def test_generate_answer(generator):
    response = generator.generate_answer("What is the admission process?")
    assert 'answer' in response
    assert 'confidence' in response
    assert 'source' in response
    assert isinstance(response['confidence'], float)

def test_generate_answer_fallback(generator):
    response = generator.generate_answer("xyz123 random")
    assert 'answer' in response
    assert response['confidence'] == 0.0

def test_detect_intent(generator):
    assert generator._detect_intent("What is the fee?") == 'fee'
    assert generator._detect_intent("How to apply?") == 'admission'
    assert generator._detect_intent("random question") == 'general'
```

### 2.4 Authentication Tests

```python
# tests/test_auth.py
import pytest
from auth.login import AuthManager
from auth.session_manager import SessionManager

@pytest.fixture
def auth():
    return AuthManager()

@pytest.fixture
def session_mgr():
    return SessionManager()

def test_hash_password(auth):
    hashed = auth.hash_password("testpass123")
    assert hashed != "testpass123"
    assert auth.verify_password("testpass123", hashed)

def test_verify_password(auth):
    hashed = auth.hash_password("mypassword")
    assert auth.verify_password("mypassword", hashed)
    assert not auth.verify_password("wrongpassword", hashed)

def test_authenticate_user(auth):
    # Create test user first
    auth.register_user("test@test.com", "pass123", "Test User")
    user, message = auth.authenticate_user("test@test.com", "pass123")
    assert user is not None
    assert message == "Authentication successful"

def test_authenticate_wrong_password(auth):
    auth.register_user("test@test.com", "pass123", "Test User")
    user, message = auth.authenticate_user("test@test.com", "wrongpass")
    assert user is None
    assert message == "Invalid password"

def test_create_session(session_mgr):
    session_id = session_mgr.create_session("test@test.com")
    assert session_id is not None
    assert len(session_id) > 0

def test_validate_session(session_mgr):
    session_id = session_mgr.create_session("test@test.com")
    email = session_mgr.validate_session(session_id)
    assert email == "test@test.com"

def test_validate_expired_session(session_mgr):
    session_id = session_mgr.create_session("test@test.com")
    # Manually expire session
    session_mgr.sessions[session_id]['last_active'] = 0
    email = session_mgr.validate_session(session_id)
    assert email is None
```

### 2.5 Database Tests

```python
# tests/test_database.py
import pytest
from database.db import DatabaseManager

@pytest.fixture
def db():
    return DatabaseManager()

def test_add_faq(db):
    faq_id = db.add_faq("Test Q?", "Test A", "test", "Test")
    assert faq_id is not None

def test_get_all_faqs(db):
    faqs = db.get_all_faqs()
    assert isinstance(faqs, list)

def test_search_faqs(db):
    results = db.search_faqs("admission")
    assert isinstance(results, list)

def test_add_user(db):
    user_id = db.add_user("test@test.com", "hash123", "Test User")
    assert user_id is not None

def test_get_user_by_email(db):
    db.add_user("test@test.com", "hash123", "Test User")
    user = db.get_user_by_email("test@test.com")
    assert user is not None
    assert user['email'] == "test@test.com"

def test_log_chat(db):
    db.log_chat("test@test.com", "Hello", "Hi there!", 0.8, "greeting")
    # Should not raise exception
```

---

## 3. API Testing

### 3.1 Authentication API Tests

```python
# tests/test_api_auth.py
import pytest
import json

def test_login_success(client):
    response = client.post('/api/login', 
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'session_id' in data

def test_login_invalid_credentials(client):
    response = client.post('/api/login',
        data=json.dumps({'email': 'wrong@email.com', 'password': 'wrong'}),
        content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['success'] == False

def test_login_missing_fields(client):
    response = client.post('/api/login',
        data=json.dumps({'email': 'test@test.com'}),
        content_type='application/json')
    assert response.status_code == 400

def test_register_success(client):
    response = client.post('/api/register',
        data=json.dumps({
            'email': 'new@student.edu.pk',
            'password': 'SecurePass123!',
            'name': 'New Student'
        }),
        content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['success'] == True

def test_register_duplicate_email(client):
    # Register first time
    client.post('/api/register',
        data=json.dumps({
            'email': 'test@student.edu.pk',
            'password': 'SecurePass123!',
            'name': 'Test Student'
        }),
        content_type='application/json')
    
    # Try again
    response = client.post('/api/register',
        data=json.dumps({
            'email': 'test@student.edu.pk',
            'password': 'SecurePass123!',
            'name': 'Test Student'
        }),
        content_type='application/json')
    assert response.status_code == 409
```

### 3.2 Chat API Tests

```python
# tests/test_api_chat.py
import pytest
import json

def test_chat_success(client):
    # Login first
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    # Chat
    response = client.post('/api/chat',
        data=json.dumps({
            'message': 'What is the admission process?',
            'session_id': session_id
        }),
        content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'response' in data
    assert 'answer' in data['response']

def test_chat_no_session(client):
    response = client.post('/api/chat',
        data=json.dumps({
            'message': 'Hello',
            'session_id': 'invalid-session'
        }),
        content_type='application/json')
    assert response.status_code == 401

def test_chat_empty_message(client):
    response = client.post('/api/chat',
        data=json.dumps({'message': ''}),
        content_type='application/json')
    assert response.status_code == 400
```

### 3.3 FAQ API Tests

```python
# tests/test_api_faqs.py
import pytest
import json

def test_get_faqs(client):
    response = client.get('/api/faqs')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True
    assert 'faqs' in data

def test_create_faq_admin(client):
    # Login as admin
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    # Create FAQ
    response = client.post('/api/faqs',
        data=json.dumps({
            'question': 'Test question?',
            'answer': 'Test answer',
            'tags': 'test',
            'category': 'Test'
        }),
        headers={'Authorization': f'Bearer {session_id}'},
        content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['success'] == True

def test_create_faq_non_admin(client):
    # Register as student
    client.post('/api/register',
        data=json.dumps({
            'email': 'student@test.edu.pk',
            'password': 'Pass123!',
            'name': 'Student'
        }),
        content_type='application/json')
    
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'student@test.edu.pk', 'password': 'Pass123!'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    # Try to create FAQ
    response = client.post('/api/faqs',
        data=json.dumps({
            'question': 'Test?',
            'answer': 'Answer'
        }),
        headers={'Authorization': f'Bearer {session_id}'},
        content_type='application/json')
    assert response.status_code == 403
```

### 3.4 Admin API Tests

```python
# tests/test_api_admin.py
import pytest
import json

def test_admin_dashboard(client):
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    response = client.get('/api/admin/dashboard',
        headers={'Authorization': f'Bearer {session_id}'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'analytics' in data

def test_admin_users(client):
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    response = client.get('/api/admin/users',
        headers={'Authorization': f'Bearer {session_id}'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'users' in data

def test_admin_access_denied(client):
    # Register as student
    client.post('/api/register',
        data=json.dumps({
            'email': 'student@test.edu.pk',
            'password': 'Pass123!',
            'name': 'Student'
        }),
        content_type='application/json')
    
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'student@test.edu.pk', 'password': 'Pass123!'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    response = client.get('/api/admin/dashboard',
        headers={'Authorization': f'Bearer {session_id}'})
    assert response.status_code == 403
```

---

## 4. Database Testing

### 4.1 Schema Tests

```python
# tests/test_db_schema.py
import pytest
import sqlite3

def test_tables_exist():
    conn = sqlite3.connect('database/iiui_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert 'users' in tables
    assert 'faqs' in tables
    assert 'contacts' in tables
    conn.close()

def test_chat_logs_exist():
    conn = sqlite3.connect('logs/chat_logs.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert 'chat_logs' in tables
    conn.close()
```

### 4.2 Data Integrity Tests

```python
# tests/test_db_integrity.py
import pytest

def test_admin_user_exists(db):
    admin = db.get_user_by_email('admin@iiu.edu.pk')
    assert admin is not None
    assert admin['role'] == 'admin'

def test_faqs_not_empty(db):
    faqs = db.get_all_faqs()
    assert len(faqs) > 0

def test_unique_email_constraint(db):
    db.add_user("unique@test.com", "hash", "User 1")
    result = db.add_user("unique@test.com", "hash", "User 2")
    assert result is None  # Should fail
```

---

## 5. UI Testing

### 5.1 Streamlit UI Tests

```python
# tests/test_ui.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestLoginUI:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8501")
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_login_page_loads(self):
        assert "IIUI" in self.driver.title
    
    def test_login_form_exists(self):
        email_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        assert email_input is not None
        assert password_input is not None
    
    def test_demo_credentials_visible(self):
        page_source = self.driver.page_source
        assert "admin@iiu.edu.pk" in page_source
```

---

## 6. Security Testing

### 6.1 SQL Injection Tests

```python
# tests/test_security.py
import pytest
import json

def test_sql_injection_login(client):
    response = client.post('/api/login',
        data=json.dumps({
            'email': "' OR '1'='1",
            'password': "' OR '1'='1"
        }),
        content_type='application/json')
    data = json.loads(response.data)
    assert data['success'] == False

def test_xss_in_chat(client):
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    response = client.post('/api/chat',
        data=json.dumps({
            'message': '<script>alert("xss")</script>',
            'session_id': session_id
        }),
        content_type='application/json')
    data = json.loads(response.data)
    # Should not contain unescaped script
    assert '<script>' not in data.get('response', {}).get('answer', '')
```

### 6.2 Authorization Tests

```python
def test_unauthorized_admin_access(client):
    response = client.get('/api/admin/dashboard')
    assert response.status_code == 401

def test_student_admin_access(client):
    # Register and login as student
    client.post('/api/register',
        data=json.dumps({
            'email': 'student@test.edu.pk',
            'password': 'Pass123!',
            'name': 'Student'
        }),
        content_type='application/json')
    
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'student@test.edu.pk', 'password': 'Pass123!'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    response = client.get('/api/admin/users',
        headers={'Authorization': f'Bearer {session_id}'})
    assert response.status_code == 403
```

---

## 7. Performance Testing

### 7.1 Response Time Tests

```python
# tests/test_performance.py
import pytest
import time

def test_chat_response_time(client):
    login_response = client.post('/api/login',
        data=json.dumps({'email': 'admin@iiu.edu.pk', 'password': 'admin123'}),
        content_type='application/json')
    session_id = json.loads(login_response.data)['session_id']
    
    start = time.time()
    response = client.post('/api/chat',
        data=json.dumps({
            'message': 'What is the admission process?',
            'session_id': session_id
        }),
        content_type='application/json')
    elapsed = time.time() - start
    
    assert elapsed < 3.0  # Should respond in under 3 seconds

def test_faqs_response_time(client):
    start = time.time()
    response = client.get('/api/faqs')
    elapsed = time.time() - start
    
    assert elapsed < 1.0
```

---

## 8. Test Configuration

### 8.1 conftest.py

```python
# tests/conftest.py
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_server import app
from database.db import DatabaseManager

@pytest.fixture
def app():
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    return DatabaseManager()
```

### 8.2 pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## 9. Test Execution

### 9.1 Run All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_hash_password
```

### 9.2 Test Report

```bash
# Generate HTML report
pytest --html=reports/test_report.html

# Generate XML report (for CI/CD)
pytest --junitxml=reports/test_results.xml
```

---

## 10. Test Checklist

### Before Each Release

- [ ] All unit tests pass
- [ ] All API tests pass
- [ ] Database tests pass
- [ ] Security tests pass
- [ ] Performance tests pass
- [ ] Manual UI testing complete
- [ ] Edge cases tested
- [ ] Error handling verified
- [ ] Cross-browser testing
- [ ] Mobile responsiveness tested
