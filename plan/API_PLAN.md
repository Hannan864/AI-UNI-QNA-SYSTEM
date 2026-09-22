# API Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Current API Endpoints

| Method | Endpoint | Status | Purpose |
|--------|----------|--------|---------|
| POST | `/api/login` | ✅ Working | User login |
| POST | `/api/chat` | ✅ Working | Send chat message |
| POST | `/api/voice/transcribe` | ⚠️ Partial | Voice transcription |
| GET | `/api/faqs` | ✅ Working | Get all FAQs |
| GET | `/api/contacts` | ✅ Working | Get contacts |
| GET | `/api/history` | ✅ Working | Get chat history |

---

## 2. Required New Endpoints

### 2.1 Authentication Endpoints

#### POST /api/register
**Purpose:** Register new user  
**Authentication:** Not required  
**Request:**
```json
{
    "email": "student@iiu.edu.pk",
    "password": "securepass123",
    "name": "John Doe",
    "role": "student"
}
```
**Response (201):**
```json
{
    "success": true,
    "message": "Registration successful",
    "user": {
        "id": 1,
        "email": "student@iiu.edu.pk",
        "name": "John Doe",
        "role": "student"
    }
}
```
**Error Responses:**
- 400: Missing required fields
- 409: Email already exists
- 422: Invalid email format

#### POST /api/logout
**Purpose:** End user session  
**Authentication:** Required  
**Request:**
```json
{
    "session_id": "abc123..."
}
```
**Response (200):**
```json
{
    "success": true,
    "message": "Logged out successfully"
}
```

#### GET /api/profile
**Purpose:** Get current user profile  
**Authentication:** Required  
**Response (200):**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "email": "student@iiu.edu.pk",
        "name": "John Doe",
        "role": "student",
        "created_at": "2026-01-01T00:00:00"
    }
}
```

#### PUT /api/profile
**Purpose:** Update user profile  
**Authentication:** Required  
**Request:**
```json
{
    "name": "John Smith",
    "phone": "+92-300-1234567",
    "department": "Computer Science"
}
```
**Response (200):**
```json
{
    "success": true,
    "message": "Profile updated"
}
```

---

### 2.2 FAQ Management Endpoints (Admin)

#### POST /api/faqs
**Purpose:** Create new FAQ  
**Authentication:** Admin required  
**Request:**
```json
{
    "question": "What is the admission deadline?",
    "answer": "The admission deadline for Fall 2026 is August 15, 2026.",
    "tags": "admission,deadline",
    "category": "Admissions"
}
```
**Response (201):**
```json
{
    "success": true,
    "message": "FAQ created",
    "faq": {
        "id": 3,
        "question": "What is the admission deadline?",
        "answer": "The admission deadline for Fall 2026 is August 15, 2026.",
        "tags": "admission,deadline",
        "category": "Admissions",
        "created_at": "2026-08-18T12:00:00"
    }
}
```

#### PUT /api/faqs/{id}
**Purpose:** Update existing FAQ  
**Authentication:** Admin required  
**Request:**
```json
{
    "question": "What is the admission deadline for Fall 2026?",
    "answer": "The admission deadline for Fall 2026 is August 20, 2026.",
    "tags": "admission,deadline,fall2026",
    "category": "Admissions"
}
```
**Response (200):**
```json
{
    "success": true,
    "message": "FAQ updated"
}
```

#### DELETE /api/faqs/{id}
**Purpose:** Delete FAQ  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "message": "FAQ deleted"
}
```

#### GET /api/faqs/{id}
**Purpose:** Get single FAQ  
**Authentication:** Required  
**Response (200):**
```json
{
    "success": true,
    "faq": {
        "id": 1,
        "question": "What is the admission process?",
        "answer": "...",
        "tags": "admission",
        "category": "Admissions",
        "created_at": "2026-01-01T00:00:00"
    }
}
```

---

### 2.3 User Management Endpoints (Admin)

#### GET /api/admin/users
**Purpose:** Get all users  
**Authentication:** Admin required  
**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 20)
- `role` (optional filter)
- `search` (optional search)

**Response (200):**
```json
{
    "success": true,
    "users": [
        {
            "id": 1,
            "email": "admin@iiu.edu.pk",
            "name": "Admin User",
            "role": "admin",
            "is_active": true,
            "created_at": "2026-01-01T00:00:00",
            "last_login": "2026-08-18T10:00:00"
        }
    ],
    "total": 1,
    "page": 1,
    "pages": 1
}
```

#### PUT /api/admin/users/{id}
**Purpose:** Update user (admin)  
**Authentication:** Admin required  
**Request:**
```json
{
    "role": "admin",
    "is_active": true
}
```
**Response (200):**
```json
{
    "success": true,
    "message": "User updated"
}
```

#### DELETE /api/admin/users/{id}
**Purpose:** Delete/deactivate user  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "message": "User deleted"
}
```

---

### 2.4 Analytics Endpoints (Admin)

#### GET /api/admin/analytics/overview
**Purpose:** Get analytics overview  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "analytics": {
        "total_users": 150,
        "total_chats": 1200,
        "total_faqs": 100,
        "active_users_today": 25,
        "average_confidence": 0.82,
        "top_intents": [
            {"intent": "admission", "count": 450},
            {"intent": "fee", "count": 300}
        ]
    }
}
```

#### GET /api/admin/analytics/chats
**Purpose:** Get chat analytics  
**Authentication:** Admin required  
**Query Parameters:**
- `period` (day/week/month)
- `start_date` (optional)
- `end_date` (optional)

**Response (200):**
```json
{
    "success": true,
    "analytics": {
        "total_chats": 150,
        "daily_average": 10,
        "peak_hours": [10, 11, 14, 15],
        "confidence_distribution": {
            "high": 80,
            "medium": 40,
            "low": 30
        }
    }
}
```

#### GET /api/admin/analytics/common-questions
**Purpose:** Get most common questions  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "questions": [
        {
            "question": "What is the admission process?",
            "count": 45,
            "intent": "admission"
        },
        {
            "question": "What is the fee structure?",
            "count": 38,
            "intent": "fee"
        }
    ]
}
```

---

### 2.5 Knowledge Base Endpoints

#### GET /api/knowledge
**Purpose:** Get knowledge base articles  
**Authentication:** Required  
**Query Parameters:**
- `category` (optional)
- `search` (optional)
- `page` (default: 1)
- `limit` (default: 20)

**Response (200):**
```json
{
    "success": true,
    "articles": [
        {
            "id": 1,
            "title": "Admission Requirements",
            "content": "...",
            "category": "Admissions",
            "tags": "admission,requirements"
        }
    ],
    "total": 50,
    "page": 1,
    "pages": 3
}
```

#### POST /api/knowledge (Admin)
**Purpose:** Create knowledge base article  
**Authentication:** Admin required  
**Request:**
```json
{
    "title": "Admission Requirements for BS Programs",
    "content": "Detailed admission requirements...",
    "category": "Admissions",
    "tags": "admission,bs,requirements"
}
```
**Response (201):**
```json
{
    "success": true,
    "message": "Article created",
    "article": {
        "id": 1,
        "title": "Admission Requirements for BS Programs",
        "content": "Detailed admission requirements...",
        "category": "Admissions",
        "tags": "admission,bs,requirements",
        "created_at": "2026-08-18T12:00:00"
    }
}
```

#### PUT /api/knowledge/{id} (Admin)
**Purpose:** Update knowledge base article  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "message": "Article updated"
}
```

#### DELETE /api/knowledge/{id} (Admin)
**Purpose:** Delete knowledge base article  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "message": "Article deleted"
}
```

---

### 2.6 Contact Management Endpoints

#### POST /api/contacts (Admin)
**Purpose:** Add new contact  
**Authentication:** Admin required  
**Request:**
```json
{
    "department": "IT Help Desk",
    "person": "Ali Ahmed",
    "email": "ithelp@iiu.edu.pk",
    "phone": "+92-51-9011234",
    "office_location": "IT Block, Room 201",
    "office_hours": "Monday-Friday, 9:00 AM - 5:00 PM"
}
```
**Response (201):**
```json
{
    "success": true,
    "message": "Contact added",
    "contact": {
        "id": 1,
        "department": "IT Help Desk",
        "person": "Ali Ahmed",
        "email": "ithelp@iiu.edu.pk",
        "phone": "+92-51-9011234",
        "office_location": "IT Block, Room 201",
        "office_hours": "Monday-Friday, 9:00 AM - 5:00 PM"
    }
}
```

#### PUT /api/contacts/{id} (Admin)
**Purpose:** Update contact  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "message": "Contact updated"
}
```

#### DELETE /api/contacts/{id} (Admin)
**Purpose:** Delete contact  
**Authentication:** Admin required  
**Response (200):**
```json
{
    "success": true,
    "message": "Contact deleted"
}
```

---

### 2.7 Chat History Endpoints

#### GET /api/history
**Purpose:** Get user's chat history  
**Authentication:** Required  
**Query Parameters:**
- `session_id` (required)
- `limit` (default: 50)
- `offset` (default: 0)

**Response (200):**
```json
{
    "success": true,
    "history": [
        {
            "id": 1,
            "user_message": "What is the admission process?",
            "bot_response": "IIUI admissions require...",
            "confidence": 0.85,
            "intent": "admission",
            "timestamp": "2026-08-18T10:30:00"
        }
    ],
    "total": 25
}
```

#### DELETE /api/history/{id}
**Purpose:** Delete chat history entry  
**Authentication:** Required  
**Response (200):**
```json
{
    "success": true,
    "message": "History entry deleted"
}
```

#### DELETE /api/history
**Purpose:** Clear all chat history  
**Authentication:** Required  
**Response (200):**
```json
{
    "success": true,
    "message": "History cleared"
}
```

---

## 3. API Authentication Flow

### Request Headers
```
Content-Type: application/json
Authorization: Bearer <session_id>
```

### Authentication Middleware
```python
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = session_manager.validate_session(session_id)
        if not user:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        return f(*args, user=user, **kwargs)
    return decorated

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

---

## 4. Error Response Format

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "field": "email",
            "issue": "Invalid email format"
        }
    }
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid input |
| UNAUTHORIZED | 401 | Authentication required |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource already exists |
| RATE_LIMITED | 429 | Too many requests |
| SERVER_ERROR | 500 | Internal server error |

---

## 5. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| POST /api/login | 5 requests | 1 minute |
| POST /api/register | 3 requests | 1 minute |
| POST /api/chat | 30 requests | 1 minute |
| GET /api/faqs | 60 requests | 1 minute |
| All other GET | 60 requests | 1 minute |
| All other POST/PUT/DELETE | 30 requests | 1 minute |

---

## 6. API Testing Checklist

- [ ] Registration with valid data
- [ ] Registration with duplicate email
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Chat with valid session
- [ ] Chat with expired session
- [ ] FAQ CRUD as admin
- [ ] FAQ CRUD as non-admin (should fail)
- [ ] User management as admin
- [ ] User management as non-admin (should fail)
- [ ] Analytics retrieval as admin
- [ ] Analytics retrieval as non-admin (should fail)
- [ ] Rate limiting enforcement
- [ ] Error handling for all endpoints
