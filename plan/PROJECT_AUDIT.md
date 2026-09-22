# Project Audit Report — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Auditor:** AI Assistant  
**Status:** Pre-Implementation Analysis

---

## 1. Current Architecture

The project uses a **dual-frontend architecture**:

```
Streamlit Frontend (app.py)  →  Flask API Backend (flask_server.py)  →  SQLite Database
```

### Technology Stack

| Layer | Technology | Status |
|-------|-----------|--------|
| Frontend | Streamlit | Functional (UI only) |
| Backend API | Flask + Flask-CORS | Functional (skeleton) |
| Database | SQLite | Functional (schema only) |
| NLP | NLTK + spaCy | Partially implemented |
| ML | Sentence Transformers + FAISS | Implemented but untested |
| Voice | SpeechRecognition + gTTS | Implemented but platform-dependent |
| Auth | bcrypt + in-memory sessions | Functional (basic) |

---

## 2. Folder Structure

```
IIUI_Smart_Chatbot/
├── app.py                          # Streamlit frontend (359 lines) ✅
├── config.py                       # Configuration (43 lines) ✅
├── flask_server.py                 # Flask API backend (123 lines) ✅
├── requirements.txt                # Dependencies (14 packages) ✅
├── README.md                       # Documentation (35 lines) ✅
├── auth/
│   ├── login.py                    # Auth manager (51 lines) ✅
│   └── session_manager.py          # Session manager (57 lines) ✅
├── data/
│   ├── contacts.csv                # EMPTY ❌
│   ├── faqs.csv                    # EMPTY ❌
│   ├── fee_structure.json          # EMPTY ❌
│   └── policies.json               # EMPTY ❌
├── database/
│   ├── db.py                       # Database manager (206 lines) ✅
│   ├── iiui_data.db                # SQLite database (32KB) ✅
│   └── init_db.py                  # DB initialization script (66 lines) ✅
├── embeddings/
│   └── faq_embeddings.pkl          # Pre-computed embeddings (36KB) ⚠️
├── logs/
│   └── chat_logs.db                # Chat logs database (20KB) ✅
├── models/
│   ├── generator.py                # Answer generator (137 lines) ✅
│   ├── intent_classifier.py        # EMPTY ❌
│   ├── nlp_processor.py            # NLP processor (80 lines) ✅
│   └── retriever.py                # FAQ retriever with FAISS (121 lines) ✅
├── static/
│   ├── css/
│   │   └── style.css               # EMPTY ❌
│   └── js/
│       └── voice.js                # EMPTY ❌
├── templates/
│   └── login.html                  # EMPTY ❌
└── voice/
    ├── speech_to_text.py           # STT module (61 lines) ✅
    └── text_to_speech.py           # TTS module (30 lines) ✅
```

---

## 3. File-by-File Analysis

### 3.1 `app.py` — Streamlit Frontend (359 lines)

**Status:** Partially functional

**What works:**
- Page configuration and layout
- Custom CSS styling (extensive)
- Login page UI
- Chat interface layout
- Sidebar with user info
- Session state management
- Message display (user/bot bubbles)
- Microphone button positioning
- Voice input handling logic

**What is broken/missing:**
- No registration page — only login exists
- No admin dashboard
- No chat history view
- No profile management
- No error boundaries
- Demo credentials hardcoded in UI
- No loading states for all operations
- No responsive design for mobile

**Dependencies:** Streamlit, requests, config, voice.speech_to_text

---

### 3.2 `config.py` — Configuration (43 lines)

**Status:** Functional

**What works:**
- Color theme definitions
- Database paths
- API config (embedding model, tokens, temperature)
- Auth config (secret key, session timeout)
- Voice config
- University info

**Issues:**
- Secret key is hardcoded (security risk)
- No environment variable support
- No `.env` file support

---

### 3.3 `flask_server.py` — Flask Backend (123 lines)

**Status:** Partially functional

**Endpoints defined:**
1. `POST /api/login` — Login ✅
2. `POST /api/chat` — Chat ✅
3. `POST /api/voice/transcribe` — Voice transcription ⚠️
4. `GET /api/faqs` — Get all FAQs ✅
5. `GET /api/contacts` — Get contacts ✅
6. `GET /api/history` — Get chat history ✅

**What is broken/missing:**
- No registration endpoint
- No admin endpoints
- No FAQ CRUD endpoints
- No user management endpoints
- No analytics endpoints
- No input validation middleware
- No error handling decorators
- No rate limiting
- No API documentation
- Voice endpoint saves to non-existent `temp/` directory

---

### 3.4 `auth/login.py` — Authentication (51 lines)

**Status:** Functional

**What works:**
- Password hashing with bcrypt
- Password verification
- User registration
- User authentication
- Default admin creation

**Issues:**
- No email validation
- No password strength requirements
- No account lockout
- No password reset

---

### 3.5 `auth/session_manager.py` — Session Management (57 lines)

**Status:** Partially functional

**What works:**
- Session creation
- Session validation
- Session expiration
- Session cleanup

**Critical issues:**
- Sessions stored in-memory only (lost on restart)
- No session persistence
- No concurrent session handling

---

### 3.6 `database/db.py` — Database Manager (206 lines)

**Status:** Functional

**Tables created:**
1. `faqs` — id, question, answer, tags, category, created_at
2. `contacts` — id, department, person, email, phone, office_location, office_hours
3. `users` — id, email, password_hash, name, role, created_at
4. `chat_logs` — id, user_email, user_message, bot_response, confidence, timestamp, intent

**Methods available:**
- `add_faq()`, `get_all_faqs()`, `search_faqs()`
- `add_contact()`, `get_contacts()`
- `add_user()`, `get_user_by_email()`
- `log_chat()`, `get_chat_history()`

**Issues:**
- No update/delete methods for FAQs
- No update/delete methods for users
- No admin-specific queries
- No analytics queries
- No foreign key relationships
- No indexes for performance

---

### 3.7 `database/init_db.py` — DB Initialization (66 lines)

**Status:** Functional

**What works:**
- Admin user creation
- Admin password reset
- FAQ seeding (only 2 FAQs)
- Database initialization

**Issues:**
- Only 2 sample FAQs
- No contacts seeded
- No fee structure data
- No policies data

---

### 3.8 `models/generator.py` — Answer Generator (137 lines)

**Status:** Partially functional

**What works:**
- Query preprocessing
- FAQ retrieval integration
- Confidence-based response selection
- Fallback responses
- Intent detection (basic keyword matching)
- Follow-up question generation
- Chat logging

**Issues:**
- No context handling
- No multi-turn conversation support
- Limited fallback responses
- Basic intent detection only

---

### 3.9 `models/retriever.py` — FAQ Retriever (121 lines)

**Status:** Implemented but untested

**What works:**
- Sentence Transformer model loading
- FAISS index building
- Embedding persistence
- Similarity search
- New FAQ addition with index rebuild

**Issues:**
- Model download required on first run
- Index rebuild on every new FAQ
- No incremental updates
- Pre-computed embeddings may be stale

---

### 3.10 `models/nlp_processor.py` — NLP Processor (80 lines)

**Status:** Implemented but untested

**What works:**
- Text preprocessing (tokenize, stopwords, lemmatize)
- Named entity extraction
- Keyword extraction
- Text similarity calculation

**Issues:**
- Requires spaCy model download
- No domain-specific NLP
- No Urdu language support

---

### 3.11 `voice/speech_to_text.py` — Speech to Text (61 lines)

**Status:** Platform-dependent

**What works:**
- Audio recording
- WAV file creation
- Google Speech Recognition transcription

**Issues:**
- Requires microphone hardware
- Requires internet for Google API
- No offline support
- No language selection

---

### 3.12 `voice/text_to_speech.py` — Text to Speech (30 lines)

**Status:** Partially implemented

**What works:**
- Text to speech conversion
- MP3 file generation

**Issues:**
- Not integrated with frontend
- No playback functionality
- No voice selection

---

### 3.13 Empty Files

| File | Status |
|------|--------|
| `data/contacts.csv` | Empty |
| `data/faqs.csv` | Empty |
| `data/fee_structure.json` | Empty |
| `data/policies.json` | Empty |
| `models/intent_classifier.py` | Empty |
| `static/css/style.css` | Empty |
| `static/js/voice.js` | Empty |
| `templates/login.html` | Empty |

---

## 4. Current Problems Summary

### 4.1 Critical Problems
1. **No admin dashboard** — Admin has no way to manage the system
2. **No registration endpoint** — Users cannot register
3. **Sessions lost on restart** — In-memory session storage
4. **Empty data files** — No actual university data
5. **Only 2 FAQs** — Insufficient knowledge base
6. **No FAQ management** — Cannot add/edit/delete FAQs

### 4.2 High Priority Problems
1. **No user management** — Admin cannot view/manage users
2. **No chat history UI** — History endpoint exists but no frontend
3. **No analytics** — No reporting or statistics
4. **No input validation** — API accepts any input
5. **Hardcoded secrets** — Security risk
6. **No error handling** — Crashes on errors

### 4.3 Medium Priority Problems
1. **No registration page** — Streamlit only has login
2. **No profile management** — Users cannot update profile
3. **No responsive design** — Mobile experience poor
4. **Voice integration incomplete** — STT/TTS not fully connected
5. **No FAQ categories management** — Categories hardcoded
6. **No knowledge base expansion** — Only FAQs in database

### 4.4 Low Priority Problems
1. **Empty static files** — CSS/JS not used (Streamlit handles styling)
2. **Empty templates** — HTML templates not used (Streamlit handles rendering)
3. **No API documentation** — No Swagger/OpenAPI
4. **No logging** — No application logging
5. **No deployment config** — No Docker/production setup

---

## 5. What Should Be Preserved

1. **Database schema** — Well-structured tables
2. **Authentication logic** — bcrypt hashing is correct
3. **FAISS retrieval system** — Good architecture for semantic search
4. **NLP preprocessing pipeline** — Proper text processing
5. **Streamlit UI structure** — Clean chat interface
6. **Config management** — Centralized configuration
7. **Chat logging** — Good for analytics

---

## 6. What Should Be Improved

1. **Add comprehensive admin dashboard**
2. **Add user registration**
3. **Expand knowledge base significantly**
4. **Add FAQ CRUD operations**
5. **Improve error handling**
6. **Add input validation**
7. **Implement persistent sessions**
8. **Add analytics and reporting**
9. **Improve UI/UX**
10. **Add proper security measures**

---

## 7. Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Sentence Transformer model too large | High | Medium | Use smaller model or API |
| spaCy model download fails | Medium | Low | Pre-download or use fallback |
| Google Speech API rate limits | Medium | High | Add offline fallback |
| SQLite concurrency issues | Low | Low | Use WAL mode |
| Memory usage with FAISS | Medium | Low | Optimize index size |

---

## 8. Recommendations

1. **Do NOT rebuild from scratch** — The core architecture is sound
2. **Focus on missing features** — Admin dashboard, registration, knowledge base
3. **Expand FAQ data** — Add 50+ university-specific FAQs
4. **Add proper error handling** — Prevent crashes
5. **Improve security** — Environment variables, input validation
6. **Add admin functionality** — Most critical missing piece
7. **Test the ML pipeline** — Verify embeddings and retrieval work
8. **Simplify voice features** — Make them optional/fallback

---

*This audit is based on code inspection only. Runtime testing has not been performed.*
