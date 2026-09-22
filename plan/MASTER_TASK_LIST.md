# Master Task List — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## Priority Legend

- **P0** = Critical / Must fix first
- **P1** = High
- **P2** = Medium
- **P3** = Optional

---

## Phase 1: Project Setup & Dependencies

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T1.1 | Fix dependencies and create requirements-dev.txt | P0 | NOT_STARTED | None | requirements.txt |
| T1.2 | Create .env file and update config.py for environment variables | P0 | NOT_STARTED | None | .env, config.py |
| T1.3 | Run database initialization and verify | P0 | NOT_STARTED | T1.1 | database/init_db.py, database/iiui_data.db |

---

## Phase 2: Database Improvements

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T2.1 | Add missing database CRUD methods (update/delete for FAQs, users, contacts) | P0 | NOT_STARTED | T1.3 | database/db.py |
| T2.2 | Add admin-specific queries (analytics, statistics) | P1 | NOT_STARTED | T2.1 | database/db.py |
| T2.3 | Seed comprehensive knowledge base data (50+ FAQs, contacts, fee structure) | P0 | NOT_STARTED | T2.1 | database/init_db.py |
| T2.4 | Add database indexes for performance | P2 | NOT_STARTED | T2.1 | database/db.py |

---

## Phase 3: Backend API

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T3.1 | Add user registration endpoint (POST /api/register) | P0 | NOT_STARTED | T2.1 | flask_server.py |
| T3.2 | Add FAQ CRUD endpoints (POST/PUT/DELETE /api/faqs) | P0 | NOT_STARTED | T2.1 | flask_server.py |
| T3.3 | Add admin endpoints with role checking | P0 | NOT_STARTED | T3.2 | flask_server.py |
| T3.4 | Add user management endpoints (GET/PUT/DELETE /api/admin/users) | P1 | NOT_STARTED | T2.1 | flask_server.py |
| T3.5 | Add analytics endpoints | P2 | NOT_STARTED | T2.2 | flask_server.py |
| T3.6 | Add input validation middleware | P1 | NOT_STARTED | None | flask_server.py |
| T3.7 | Add global error handling | P0 | NOT_STARTED | None | flask_server.py |

---

## Phase 4: Authentication & Security

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T4.1 | Add admin role verification middleware | P0 | NOT_STARTED | T3.3 | flask_server.py, auth/login.py |
| T4.2 | Implement session persistence in database | P1 | NOT_STARTED | T2.1 | auth/session_manager.py, database/db.py |
| T4.3 | Add input sanitization for XSS prevention | P1 | NOT_STARTED | None | flask_server.py |
| T4.4 | Add rate limiting | P2 | NOT_STARTED | None | flask_server.py |

---

## Phase 5: Frontend - Registration

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T5.1 | Create registration page in Streamlit | P0 | NOT_STARTED | T3.1 | app.py |
| T5.2 | Add form validation feedback | P1 | NOT_STARTED | T5.1 | app.py |

---

## Phase 6: Frontend - Admin Dashboard

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T6.1 | Create admin dashboard layout | P0 | NOT_STARTED | T4.1 | app.py |
| T6.2 | Create FAQ management UI (CRUD) | P0 | NOT_STARTED | T3.2, T6.1 | app.py |
| T6.3 | Create user management UI | P1 | NOT_STARTED | T3.4, T6.1 | app.py |
| T6.4 | Create contact management UI | P1 | NOT_STARTED | T3.2, T6.1 | app.py |
| T6.5 | Create analytics dashboard | P2 | NOT_STARTED | T3.5, T6.1 | app.py |
| T6.6 | Create chat history viewer | P1 | NOT_STARTED | T3.3, T6.1 | app.py |

---

## Phase 7: Knowledge Base Expansion

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T7.1 | Create comprehensive FAQ dataset (100+ FAQs) | P0 | NOT_STARTED | T2.3 | database/init_db.py |
| T7.2 | Add contact directory data | P1 | NOT_STARTED | T2.3 | database/init_db.py |
| T7.3 | Add fee structure data | P1 | NOT_STARTED | T2.3 | database/init_db.py |
| T7.4 | Add academic policies data | P2 | NOT_STARTED | T2.3 | database/init_db.py |

---

## Phase 8: Chatbot Improvements

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T8.1 | Improve intent detection with better patterns | P1 | NOT_STARTED | None | models/generator.py |
| T8.2 | Add conversation context handling | P2 | NOT_STARTED | None | models/generator.py |
| T8.3 | Improve fallback responses | P1 | NOT_STARTED | None | models/generator.py |
| T8.4 | Add response templates | P2 | NOT_STARTED | None | models/generator.py |

---

## Phase 9: Voice Integration

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T9.1 | Fix voice input for web browser | P2 | NOT_STARTED | None | voice/speech_to_text.py, app.py |
| T9.2 | Integrate text-to-speech with UI | P2 | NOT_STARTED | T9.1 | app.py, voice/text_to_speech.py |

---

## Phase 10: Testing & Bug Fixing

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T10.1 | Write unit tests for core modules | P1 | NOT_STARTED | All previous | tests/ |
| T10.2 | Write integration tests | P1 | NOT_STARTED | T10.1 | tests/ |
| T10.3 | Security testing | P2 | NOT_STARTED | T10.1 | tests/ |
| T10.4 | Performance testing | P2 | NOT_STARTED | T10.1 | tests/ |

---

## Phase 11: UI Polish

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T11.1 | Improve styling and consistency | P2 | NOT_STARTED | All UI tasks | app.py |
| T11.2 | Add loading states for all operations | P1 | NOT_STARTED | None | app.py |
| T11.3 | Add user-friendly error displays | P1 | NOT_STARTED | None | app.py |

---

## Phase 12: Deployment

| Task ID | Description | Priority | Status | Dependencies | Files Involved |
|---------|-------------|----------|--------|--------------|----------------|
| T12.1 | Create startup script (run both servers) | P1 | NOT_STARTED | All previous | run.py |
| T12.2 | Update README documentation | P2 | NOT_STARTED | All previous | README.md |
| T12.3 | Final end-to-end testing | P0 | NOT_STARTED | All previous | All |

---

## Execution Order

```
T1.1 → T1.2 → T1.3 → T2.1 → T2.2 → T2.3
                                    ↓
                              T3.1 → T3.2 → T3.3 → T3.4 → T3.5
                              T3.6 → T3.7
                                    ↓
                              T4.1 → T4.2 → T4.3 → T4.4
                                    ↓
                              T5.1 → T5.2
                                    ↓
                              T6.1 → T6.2 → T6.3 → T6.4 → T6.5 → T6.6
                                    ↓
                              T7.1 → T7.2 → T7.3 → T7.4
                                    ↓
                              T8.1 → T8.2 → T8.3 → T8.4
                                    ↓
                              T9.1 → T9.2
                                    ↓
                              T10.1 → T10.2 → T10.3 → T10.4
                                    ↓
                              T11.1 → T11.2 → T11.3
                                    ↓
                              T12.1 → T12.2 → T12.3
```

---

## Current Status

**Next Task:** T1.1 — Fix dependencies and create requirements-dev.txt  
**Phase:** 1 — Project Setup & Dependencies  
**Progress:** 0% complete
