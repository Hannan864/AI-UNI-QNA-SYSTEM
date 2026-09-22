# Requirements Document — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Functional Requirements

### 1.1 Authentication & User Management

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| FR-AUTH-01 | User login with email/password | ✅ Existing | P0 |
| FR-AUTH-02 | User registration | ❌ Missing | P0 |
| FR-AUTH-03 | Password hashing (bcrypt) | ✅ Existing | P0 |
| FR-AUTH-04 | Session management | ✅ Existing (in-memory) | P1 |
| FR-AUTH-05 | Logout functionality | ✅ Existing | P0 |
| FR-AUTH-06 | Role-based access (student/admin) | ⚠️ Partially implemented | P1 |
| FR-AUTH-07 | Admin default account creation | ✅ Existing | P1 |
| FR-AUTH-08 | Password strength validation | ❌ Missing | P2 |
| FR-AUTH-09 | Session timeout | ✅ Existing | P1 |
| FR-AUTH-10 | Session persistence | ❌ Missing | P1 |

### 1.2 Chatbot Functionality

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| FR-CHAT-01 | Text-based chat input | ✅ Existing | P0 |
| FR-CHAT-02 | AI-powered responses | ✅ Existing | P0 |
| FR-CHAT-03 | FAQ retrieval using embeddings | ✅ Existing | P0 |
| FR-CHAT-04 | Confidence scoring | ✅ Existing | P1 |
| FR-CHAT-05 | Fallback responses | ✅ Existing | P1 |
| FR-CHAT-06 | Follow-up suggestions | ✅ Existing | P2 |
| FR-CHAT-07 | Voice input (speech-to-text) | ⚠️ Partially implemented | P2 |
| FR-CHAT-08 | Voice output (text-to-speech) | ⚠️ Partially implemented | P2 |
| FR-CHAT-09 | Multi-turn conversation | ❌ Missing | P2 |
| FR-CHAT-10 | Context awareness | ❌ Missing | P2 |
| FR-CHAT-11 | Intent detection | ✅ Existing (basic) | P1 |
| FR-CHAT-12 | Entity extraction | ✅ Existing | P2 |
| FR-CHAT-13 | Urdu language support | ❌ Missing | P3 |

### 1.3 Knowledge Base

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| FR-KB-01 | FAQ storage in database | ✅ Existing | P0 |
| FR-KB-02 | FAQ retrieval by similarity | ✅ Existing | P0 |
| FR-KB-03 | FAQ CRUD operations (admin) | ❌ Missing | P0 |
| FR-KB-04 | FAQ categories | ✅ Existing | P1 |
| FR-KB-05 | FAQ tags | ✅ Existing | P1 |
| FR-KB-06 | Contact directory | ✅ Existing (empty data) | P1 |
| FR-KB-07 | Fee structure information | ❌ Missing | P1 |
| FR-KB-08 | Academic policies | ❌ Missing | P2 |
| FR-KB-09 | Admission information | ❌ Missing | P1 |
| FR-KB-10 | Course catalog | ❌ Missing | P2 |
| FR-KB-11 | Knowledge base expansion | ❌ Missing | P1 |

### 1.4 Chat History & Logging

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| FR-HIST-01 | Chat logging to database | ✅ Existing | P0 |
| FR-HIST-02 | User chat history retrieval | ✅ Existing | P1 |
| FR-HIST-03 | Chat history UI | ❌ Missing | P1 |
| FR-HIST-04 | Admin chat history view | ❌ Missing | P1 |
| FR-HIST-05 | Chat export | ❌ Missing | P3 |

### 1.5 Admin Dashboard

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| FR-ADMIN-01 | Admin login | ✅ Existing (same as user) | P0 |
| FR-ADMIN-02 | Admin dashboard UI | ❌ Missing | P0 |
| FR-ADMIN-03 | FAQ management (CRUD) | ❌ Missing | P0 |
| FR-ADMIN-04 | Knowledge base management | ❌ Missing | P1 |
| FR-ADMIN-05 | User management | ❌ Missing | P1 |
| FR-ADMIN-06 | Chat history view | ❌ Missing | P1 |
| FR-ADMIN-07 | Basic analytics | ❌ Missing | P2 |
| FR-ADMIN-08 | System status | ❌ Missing | P2 |
| FR-ADMIN-09 | Contact management | ❌ Missing | P1 |
| FR-ADMIN-10 | Data import/export | ❌ Missing | P3 |

### 1.6 User Interface

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| FR-UI-01 | Login page | ✅ Existing | P0 |
| FR-UI-02 | Chat interface | ✅ Existing | P0 |
| FR-UI-03 | Sidebar navigation | ✅ Existing | P1 |
| FR-UI-04 | Responsive design | ⚠️ Partially implemented | P2 |
| FR-UI-05 | IIUI branding/theme | ✅ Existing | P1 |
| FR-UI-06 | Registration page | ❌ Missing | P0 |
| FR-UI-07 | Admin dashboard page | ❌ Missing | P0 |
| FR-UI-08 | Chat history page | ❌ Missing | P1 |
| FR-UI-09 | Profile page | ❌ Missing | P3 |
| FR-UI-10 | Error pages | ❌ Missing | P2 |

---

## 2. Non-Functional Requirements

### 2.1 Usability

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| NFR-USE-01 | Intuitive interface | ✅ Existing | P1 |
| NFR-USE-02 | Clear error messages | ⚠️ Partially implemented | P1 |
| NFR-USE-03 | Loading indicators | ⚠️ Partially implemented | P2 |
| NFR-USE-04 | Input validation feedback | ❌ Missing | P2 |
| NFR-USE-05 | Help/documentation | ❌ Missing | P3 |

### 2.2 Performance

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| NFR-PERF-01 | Response time < 3 seconds | ⚠️ Unverified | P1 |
| NFR-PERF-02 | Database query optimization | ❌ Missing | P2 |
| NFR-PERF-03 | Embedding caching | ✅ Existing | P1 |
| NFR-PERF-04 | Concurrent user support | ❌ Missing | P2 |

### 2.3 Security

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| NFR-SEC-01 | Password hashing | ✅ Existing | P0 |
| NFR-SEC-02 | Session management | ✅ Existing | P0 |
| NFR-SEC-03 | Input validation | ❌ Missing | P0 |
| NFR-SEC-04 | SQL injection prevention | ✅ Existing (parameterized queries) | P0 |
| NFR-SEC-05 | XSS prevention | ⚠️ Partially implemented | P1 |
| NFR-SEC-06 | CSRF protection | ❌ Missing | P1 |
| NFR-SEC-07 | Rate limiting | ❌ Missing | P2 |
| NFR-SEC-08 | Environment variable usage | ❌ Missing | P1 |
| NFR-SEC-09 | Admin access control | ⚠️ Partially implemented | P0 |

### 2.4 Reliability

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| NFR-REL-01 | Error handling | ❌ Missing | P0 |
| NFR-REL-02 | Graceful degradation | ⚠️ Partially implemented | P1 |
| NFR-REL-03 | Data backup | ❌ Missing | P2 |
| NFR-REL-04 | Session persistence | ❌ Missing | P1 |

### 2.5 Maintainability

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| NFR-MAINT-01 | Code documentation | ⚠️ Partially implemented | P2 |
| NFR-MAINT-02 | Modular architecture | ✅ Existing | P1 |
| NFR-MAINT-03 | Configuration management | ✅ Existing | P1 |
| NFR-MAINT-04 | Logging | ❌ Missing | P2 |

### 2.6 Scalability

| ID | Requirement | Status | Priority |
|----|-------------|--------|----------|
| NFR-SCALE-01 | Database scalability | ⚠️ SQLite limited | P2 |
| NFR-SCALE-02 | API scalability | ⚠️ Single-threaded Flask | P2 |
| NFR-SCALE-03 | Knowledge base expansion | ⚠️ Partially implemented | P1 |

---

## 3. Requirements Summary

| Category | Existing | Partial | Missing | Total |
|----------|----------|---------|---------|-------|
| Authentication | 4 | 2 | 4 | 10 |
| Chatbot | 8 | 3 | 4 | 15 |
| Knowledge Base | 3 | 0 | 7 | 10 |
| Chat History | 2 | 0 | 3 | 5 |
| Admin Dashboard | 1 | 0 | 9 | 10 |
| User Interface | 4 | 1 | 5 | 10 |
| Non-Functional | 6 | 6 | 12 | 24 |
| **Total** | **28** | **12** | **44** | **84** |

---

## 4. Priority Matrix

### P0 — Critical (Must Have)
- User registration
- Admin dashboard
- FAQ management
- Input validation
- Error handling
- Admin access control

### P1 — High (Should Have)
- Session persistence
- Chat history UI
- User management
- Knowledge base expansion
- Contact management
- Performance optimization

### P2 — Medium (Nice to Have)
- Voice features
- Multi-turn conversation
- Analytics
- Responsive design
- Data import/export

### P3 — Optional (Future)
- Urdu support
- Profile management
- Chat export
- Help documentation
