# IIUI Smart Chatbot — AI Chatbot for University Support

**BS Final Year Project** — International Islamic University Islamabad (IIUI)

---

## Quick Start (One Click)

### Windows
1. Double-click **`RUN.bat`**
2. Wait for both servers to start (~30-60 seconds)
3. Browser opens automatically to `http://localhost:8501`
4. Login: `admin@iiu.edu.pk` / `admin123`

### Manual Start
```bash
# Terminal 1 — Flask Backend
python flask_server.py

# Terminal 2 — Streamlit Frontend
streamlit run app.py --server.port 8501
```

---

## Technology Stack

| Area | Technology |
|------|-----------|
| Language | Python 3.10+ |
| Frontend | Streamlit |
| Backend | Flask |
| NLP | NLTK + spaCy |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| Database | SQLite |
| Embeddings | Sentence Transformers + FAISS |
| Auth | bcrypt |

---

## Features

### Students/Faculty
- **Mock Data Assistant** — Answers from university knowledge base
- **Live AI Assistant** — AI-powered chat (requires provider config)
- **Chat History** — Review past conversations
- **University Info** — Admissions, fees, programs, calendar

### Admins
- **Dashboard** — Real-time system statistics
- **Knowledge Base** — Manage university information (CRUD)
- **FAQ Management** — Manage frequently asked questions
- **User Management** — View and manage users
- **Chat Logs** — Monitor all interactions
- **AI Settings** — Configure Live AI provider
- **ML Management** — View model status, retrain

---

## Project Structure

```
iiui-chatbot/
├── app.py                     # Streamlit frontend
├── flask_server.py            # Flask backend
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── RUN.bat                    # One-click launcher
├── start_flask.bat            # Start Flask only
├── start_streamlit.bat        # Start Streamlit only
├── run_tests.bat              # Run all tests
├── README.md                  # This file
│
├── auth/                      # Authentication
│   ├── login.py
│   └── session_manager.py
│
├── database/                  # Database
│   ├── db.py                  # SQLite manager
│   └── init_db.py             # DB init + seed data
│
├── models/                    # AI/NLP/ML
│   ├── nlp_processor.py       # NLP (NLTK + spaCy)
│   ├── ml_classifier.py       # ML classifier (Scikit-learn)
│   ├── response_generator.py  # Response generation
│   ├── chat_router.py         # Mock/Live mode routing
│   ├── generator.py           # Mock answer generator
│   ├── retriever.py           # FAISS FAQ retrieval
│   └── live_ai_service.py     # Live AI provider service
│
├── voice/                     # Voice features
├── mock_data/                 # Sample university data
├── models/ml_artifacts/       # Trained ML models
├── embeddings/                # FAISS cache
├── logs/                      # Chat logs DB
│
├── test_phase3.py             # Backend API tests
├── test_phase4.py             # Auth tests
├── test_phase5.py             # KB/FAQ tests
├── test_phase6.py             # Mock mode tests
├── test_phase7.py             # Live AI tests
├── test_phase8.py             # Mode router tests
├── test_phase9.py             # NLP tests
└── test_phase10_11.py         # ML + Response tests
```

---

## Manual Testing Guide

1. Start app with `RUN.bat`
2. Login as admin or register as student
3. Go to **Mock Data Assistant** → Ask "What is the admission process?"
4. Switch to **Live AI Assistant** → Verify mode switching works
5. Check **Chat History** → Verify conversations are recorded
6. As admin: Check **Settings → AI Configuration**

---

## Running Tests

```bash
python test_phase3.py     # 53 tests - Backend APIs
python test_phase4.py     # 41 tests - Authentication
python test_phase5.py     # 66 tests - Knowledge Base
python test_phase6.py     # 44 tests - Mock Mode
python test_phase7.py     # 67 tests - Live AI
python test_phase8.py     # 65 tests - Mode Router
python test_phase9.py     # NLP Processing
python test_phase10_11.py # ML + Response Gen
```

Or double-click `run_tests.bat` on Windows.

---

## Architecture

```
User Query → Streamlit → Flask → Chat Router
                                    ├── NLP Processor (Phase 9)
                                    ├── ML Classifier (Phase 10)
                                    ├── Response Generator (Phase 11)
                                    │
                                    ├── MOCK → Knowledge Base/FAISS → Response
                                    └── LIVE → AI Provider → Response
```

---

## FYP Compliance

- ✅ Python, Streamlit, Flask
- ✅ NLTK + spaCy (NLP)
- ✅ Scikit-learn (ML)
- ✅ SQLite (Database)
- ✅ Intent Detection + Entity Extraction
- ✅ Knowledge Base + Response Generation
- ✅ Admin Dashboard + Authentication
- ✅ Live AI + Mock Data modes

---

## Voice Interaction

### How to Use Voice Input
1. Open the Chat Assistant (Mock or Live mode)
2. Toggle the **🎤 Voice** switch ON
3. Click the microphone widget that appears
4. Speak your question clearly
5. The system converts speech to text and sends it through the chat pipeline
6. Response appears as text (same as typed input)

### Voice Requirements
- Microphone access in browser
- Internet connection (uses Google Speech Recognition)
- SpeechRecognition library (pre-installed)

### Voice Fallback
If voice is unavailable:
- Text input always works
- Voice errors show a warning message
- Application continues functioning normally

---

## Mock Data Documents

The `mock/` folder contains university PDF documents:

| Document | Description |
|----------|-------------|
| IIUI_Examination_and_Grading_Policy.pdf | Exam policies and grading |
| IIUI_Academic_Calendar.pdf | Academic calendar |
| IIUI_Admissions_Eligibility_Guide.pdf | Admission requirements |
| IIUI_Course_Catalog.pdf | Available courses |
| IIUI_Date_Sheet_Criteria.pdf | Exam date sheet |
| IIUI_Fee_Structure_FAQs.pdf | Fee information |
| IIUI_FYP_Guidelines_FCIT.pdf | FYP guidelines |
| IIUI_Hostel_and_Transport_Rules.pdf | Hostel/transport rules |
| IIUI_Scholarships_Financial_Aid.pdf | Scholarships info |
| IIUI_Student_Handbook.pdf | Student handbook |

These documents are for reference. Knowledge Base entries in the database power the chatbot responses.

---

## FYP Module Compliance

| Module | Status | Technology |
|--------|--------|-----------|
| User Interface | ✅ Implemented | Streamlit |
| Authentication | ✅ Implemented | bcrypt + Flask sessions |
| NLP Processing | ✅ Implemented | NLTK + spaCy |
| Knowledge Base | ✅ Implemented | SQLite + FAISS |
| ML Model | ✅ Implemented | Scikit-learn (TF-IDF + Logistic Regression) |
| Response Generation | ✅ Implemented | NLP + ML + KB integration |
| Admin Dashboard | ✅ Implemented | Streamlit + Flask |
| Academic Assistance | ✅ Implemented | SQLite + Streamlit |
| Voice Interaction | ✅ Implemented | SpeechRecognition + gTTS |
| Live AI | ✅ Implemented | Provider-agnostic (OpenAI/Anthropic/Custom) |
| Mock Data Mode | ✅ Implemented | Local KB + FAISS |
