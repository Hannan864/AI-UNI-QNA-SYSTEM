````markdown
# 🎓 IIUI Smart Chatbot — AI-Powered University Support System

<div align="center">

### Intelligent Academic Assistance, NLP, Machine Learning & AI Chat

**BS Final Year Project — International Islamic University Islamabad (IIUI)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge)](https://spacy.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-0468D7?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p>
  <b>A full-stack university support chatbot combining NLP, traditional machine learning, semantic retrieval, local knowledge-base responses, live AI integration, authentication, administration, and voice interaction.</b>
</p>

</div>

---

## 📌 Project Overview

**IIUI Smart Chatbot** is a university-focused AI and NLP application developed as a **BS Final Year Project** for **International Islamic University Islamabad (IIUI)**.

The system is designed to provide students and faculty with a centralized conversational interface for accessing university-related information such as:

- Admissions and eligibility
- Academic programs and courses
- Fees and financial information
- Examination and grading policies
- Academic calendar information
- FYP guidelines
- Hostel and transport information
- Scholarships and financial aid
- Student policies and general university information

Rather than relying on a single chatbot mechanism, the project combines multiple approaches:

**User Query → NLP Processing → Intent Classification → Retrieval / Response Generation → Mock or Live AI Response**

The project demonstrates practical implementation of **AI, NLP, machine learning, information retrieval, backend APIs, authentication, database design, testing, and user-facing application development**.

---

## 🧭 Navigation

- [🎯 Core Capabilities](#-core-capabilities)
- [🏗️ System Architecture](#️-system-architecture)
- [🤖 AI, NLP & ML Pipeline](#-ai-nlp--ml-pipeline)
- [🔎 Knowledge Retrieval](#-knowledge-retrieval)
- [🔐 Authentication & Administration](#-authentication--administration)
- [🎙️ Voice Interaction](#️-voice-interaction)
- [🛠️ Technology Stack](#️-technology-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [🧪 Testing](#-testing)
- [📚 Knowledge Base Documents](#-knowledge-base-documents)
- [🎓 FYP Module Coverage](#-fyp-module-coverage)
- [🧠 QNA](#-qna-about-this-project)
- [📬 Contact & Hire Me](#-contact--hire-me)

---

# 🎯 Core Capabilities

| Area | Implementation | What It Demonstrates |
|------|----------------|----------------------|
| 💬 Conversational UI | Streamlit | Interactive application development |
| 🧠 NLP | NLTK + spaCy | Text preprocessing and language analysis |
| 🤖 Machine Learning | TF-IDF + Logistic Regression | Intent classification |
| 🔎 Semantic Retrieval | Sentence Transformers + FAISS | Knowledge retrieval |
| 📚 Knowledge Base | SQLite | Structured university information |
| 🧩 Response Generation | Custom response pipeline | Context-aware answer generation |
| 🔀 Chat Routing | Mock / Live modes | Modular AI architecture |
| 🌐 Backend APIs | Flask | REST-style backend development |
| 🔐 Authentication | bcrypt + sessions | User authentication |
| 👨‍💼 Administration | Admin dashboard | System and content management |
| 🎙️ Voice | SpeechRecognition + gTTS | Voice-based interaction |
| 🧪 Testing | Phase-based test suites | Software verification |
| 🤖 Live AI | Provider-agnostic integration | External AI service integration |

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                   │
│                         Streamlit Application                                 │
│                                                                              │
│       Student / Faculty                     Administrator                    │
│              │                                     │                         │
│              └──────────────────┬──────────────────┘                         │
│                                 ▼                                            │
│                         Chat / Dashboard UI                                  │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FLASK BACKEND                                   │
│                                                                              │
│   Authentication │ Sessions │ Chat APIs │ Admin APIs │ AI Configuration      │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           CHAT ROUTER                                        │
│                                                                              │
│                    ┌──────────────┴──────────────┐                           │
│                    ▼                             ▼                           │
│               MOCK MODE                     LIVE MODE                       │
│                    │                             │                           │
│                    ▼                             ▼                           │
│          NLP / ML / Retrieval             AI Provider Service               │
│                    │                             │                           │
│                    ▼                             ▼                           │
│        Knowledge Base + FAISS          External AI Provider                 │
└────────────────────┬────────────────────────────┬────────────────────────────┘
                     │                            │
                     └─────────────┬──────────────┘
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE PIPELINE                                    │
│                                                                              │
│     NLP Processing → Intent Detection → Retrieval → Response Generation     │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
│                                                                              │
│     SQLite Database │ FAQ / KB Data │ Chat History │ ML Artifacts │ Logs     │
└──────────────────────────────────────────────────────────────────────────────┘
````

---

# 🤖 AI, NLP & ML Pipeline

The chatbot uses multiple AI/NLP components rather than treating every query as a direct LLM request.

### 1. Text Processing

User input is processed through NLP components using:

* **NLTK**
* **spaCy**
* Text normalization
* Tokenization / linguistic processing
* Intent-related feature preparation

### 2. Intent Classification

The project uses a traditional machine-learning pipeline based on:

```text
User Query
    ↓
Text Preprocessing
    ↓
TF-IDF Feature Extraction
    ↓
Logistic Regression
    ↓
Predicted Intent
```

This provides a lightweight approach for classifying common university-related query types.

### 3. Retrieval

For knowledge-base questions, the system can use semantic retrieval through:

* Sentence Transformers
* FAISS
* FAQ / knowledge-base content

This allows the application to search for semantically relevant information instead of relying only on exact keyword matching.

### 4. Response Generation

The response-generation layer combines the available information sources and produces the final chatbot response.

The architecture separates:

* Query processing
* Classification
* Retrieval
* Response generation
* AI provider integration

This makes individual components easier to modify and test.

---

# 🔎 Knowledge Retrieval

The **Mock Data Assistant** is designed to answer questions using locally available university information.

```text
University Documents
        ↓
Knowledge Base
        ↓
Embedding / Retrieval Layer
        ↓
FAISS Semantic Search
        ↓
Relevant Information
        ↓
Response Generator
        ↓
Chatbot Response
```

This approach is particularly useful for university information because the chatbot can operate using a controlled knowledge source instead of requiring every response to come directly from an external AI service.

---

# 🔀 Mock AI vs Live AI

The project supports two conversational modes.

| Mode                    | Data Source            | External AI Required | Purpose                             |
| ----------------------- | ---------------------- | -------------------- | ----------------------------------- |
| 🗃️ Mock Data Assistant | Local KB + FAISS       | No                   | Controlled university information   |
| 🤖 Live AI Assistant    | Configured AI provider | Yes                  | AI-powered conversational responses |

### Mock Mode

Mock mode is designed around the project's local university knowledge base and retrieval pipeline.

It is useful for:

* Offline/local demonstrations
* Predictable university information
* Testing NLP and retrieval components
* Reducing dependency on external AI APIs

### Live AI Mode

Live mode provides integration with an external AI provider through the project's AI service layer.

The architecture is designed to keep the provider implementation separate from the rest of the chatbot pipeline.

---

# 🔐 Authentication & Administration

The system includes separate user-facing and administrative functionality.

### Authentication

Authentication is implemented using:

* Flask backend
* Password hashing with bcrypt
* Session management
* Role-aware access

### Administrator Capabilities

Administrators can access functionality for:

* 📊 System dashboard
* 📚 Knowledge-base management
* ❓ FAQ management
* 👥 User management
* 💬 Chat-log monitoring
* ⚙️ AI provider configuration
* 🧠 ML model management

This gives the project an operational layer beyond the chatbot interface itself.

---

# 🎙️ Voice Interaction

The chatbot also supports voice-based input.

### Voice Flow

```text
🎤 Microphone
      ↓
Speech Recognition
      ↓
Text Query
      ↓
Chat Pipeline
      ↓
Response
```

### How to Use

1. Open the Chat Assistant.
2. Select Mock or Live mode.
3. Enable the **🎤 Voice** option.
4. Use the microphone widget.
5. Speak the question.
6. The speech input is converted to text.
7. The resulting text is processed through the normal chatbot pipeline.

### Requirements

* Browser microphone permission
* SpeechRecognition library
* Internet connection for the configured Google Speech Recognition service

If voice input is unavailable, normal text-based chat remains available.

---

# 🛠️ Technology Stack

| Layer              | Technology            | Role                        |
| ------------------ | --------------------- | --------------------------- |
| Language           | Python 3.10+          | Application development     |
| Frontend           | Streamlit             | Web UI                      |
| Backend            | Flask                 | Backend/API layer           |
| NLP                | NLTK + spaCy          | Text processing             |
| Machine Learning   | Scikit-learn          | Intent classification       |
| Feature Extraction | TF-IDF                | ML text representation      |
| ML Algorithm       | Logistic Regression   | Intent classification       |
| Embeddings         | Sentence Transformers | Semantic representation     |
| Vector Search      | FAISS                 | Similarity retrieval        |
| Database           | SQLite                | Persistent application data |
| Authentication     | bcrypt                | Password hashing            |
| Voice Input        | SpeechRecognition     | Speech-to-text              |
| Voice Output       | gTTS                  | Text-to-speech              |
| AI Integration     | Provider-agnostic     | Live AI responses           |

---

# 📂 Project Structure

```text
iiui-chatbot/
│
├── app.py                         # Streamlit frontend
├── flask_server.py                # Flask backend
├── config.py                      # Application configuration
├── requirements.txt               # Python dependencies
│
├── RUN.bat                        # One-click Windows launcher
├── start_flask.bat                # Backend launcher
├── start_streamlit.bat            # Frontend launcher
├── run_tests.bat                  # Test-suite launcher
├── README.md                      # Project documentation
│
├── auth/
│   ├── login.py                   # Authentication logic
│   └── session_manager.py         # Session management
│
├── database/
│   ├── db.py                      # SQLite database manager
│   └── init_db.py                 # Database initialization + seed data
│
├── models/
│   ├── nlp_processor.py           # NLTK + spaCy processing
│   ├── ml_classifier.py           # ML intent classifier
│   ├── response_generator.py      # Response generation
│   ├── chat_router.py             # Mock / Live routing
│   ├── generator.py               # Mock response generation
│   ├── retriever.py               # FAISS retrieval
│   └── live_ai_service.py         # Live AI provider service
│
├── voice/                          # Voice-related functionality
├── mock_data/                      # Sample university data
├── models/ml_artifacts/            # Trained ML artifacts
├── embeddings/                     # FAISS embedding/cache data
├── logs/                           # Application/chat logs
│
├── test_phase3.py                  # Backend API tests
├── test_phase4.py                  # Authentication tests
├── test_phase5.py                  # Knowledge Base / FAQ tests
├── test_phase6.py                  # Mock mode tests
├── test_phase7.py                  # Live AI tests
├── test_phase8.py                  # Chat mode router tests
├── test_phase9.py                  # NLP tests
└── test_phase10_11.py              # ML + response-generation tests
```

---

# 🚀 Quick Start

## Windows — One-Click Launch

The project includes a Windows launcher:

```text
RUN.bat
```

### Steps

1. Double-click **`RUN.bat`**.
2. Wait for the backend and frontend services to start.
3. The application should open in the browser.
4. Open:

```text
http://localhost:8501
```

### Demo Credentials

```text
Email:    admin@iiu.edu.pk
Password: admin123
```

> ⚠️ These credentials are intended for local/demo use. Change or remove seeded credentials before deploying an application outside the development environment.

---

## Manual Startup

### Terminal 1 — Flask Backend

```bash
python flask_server.py
```

### Terminal 2 — Streamlit Frontend

```bash
streamlit run app.py --server.port 8501
```

Then open:

```text
http://localhost:8501
```

---

# 🧪 Testing

The project includes phase-based test suites covering major system components.

```bash
python test_phase3.py
python test_phase4.py
python test_phase5.py
python test_phase6.py
python test_phase7.py
python test_phase8.py
python test_phase9.py
python test_phase10_11.py
```

### Test Coverage

| Test Suite           | Focus                    |
| -------------------- | ------------------------ |
| `test_phase3.py`     | Backend APIs             |
| `test_phase4.py`     | Authentication           |
| `test_phase5.py`     | Knowledge Base / FAQ     |
| `test_phase6.py`     | Mock mode                |
| `test_phase7.py`     | Live AI                  |
| `test_phase8.py`     | Mode routing             |
| `test_phase9.py`     | NLP processing           |
| `test_phase10_11.py` | ML + response generation |

On Windows, the complete suite can also be launched using:

```text
run_tests.bat
```

---

# 🧪 Manual Testing Guide

A basic end-to-end verification flow:

### Student / Faculty Flow

1. Start the application using `RUN.bat`.
2. Register or log in.
3. Open **Mock Data Assistant**.
4. Ask:

```text
What is the admission process?
```

5. Verify that the chatbot processes the question and returns university-related information.
6. Open **Chat History**.
7. Confirm that the conversation is recorded.

### Live AI Flow

1. Open **Live AI Assistant**.
2. Verify that the configured provider is available.
3. Submit a test question.
4. Verify that mode switching and response handling work correctly.

### Administrator Flow

1. Log in using an administrator account.
2. Open the admin dashboard.
3. Test Knowledge Base and FAQ management.
4. Review user records and chat logs.
5. Open AI configuration.
6. Check ML model status.

---

# 📚 Knowledge Base Documents

The project includes university reference documents intended to support the chatbot's knowledge base.

| Document                                  | Coverage                         |
| ----------------------------------------- | -------------------------------- |
| `IIUI_Examination_and_Grading_Policy.pdf` | Examination and grading policies |
| `IIUI_Academic_Calendar.pdf`              | Academic calendar                |
| `IIUI_Admissions_Eligibility_Guide.pdf`   | Admission requirements           |
| `IIUI_Course_Catalog.pdf`                 | Course information               |
| `IIUI_Date_Sheet_Criteria.pdf`            | Date-sheet criteria              |
| `IIUI_Fee_Structure_FAQs.pdf`             | Fee-related information          |
| `IIUI_FYP_Guidelines_FCIT.pdf`            | FYP guidelines                   |
| `IIUI_Hostel_and_Transport_Rules.pdf`     | Hostel and transport rules       |
| `IIUI_Scholarships_Financial_Aid.pdf`     | Scholarships and financial aid   |
| `IIUI_Student_Handbook.pdf`               | Student policies and guidance    |

These documents provide reference material for the project's university knowledge base. The chatbot's actual responses depend on the information stored and indexed by the application's database and retrieval pipeline.

---

# 🎓 FYP Module Coverage

| FYP Module          | Status | Implementation               |
| ------------------- | :----: | ---------------------------- |
| User Interface      |    ✅   | Streamlit                    |
| Authentication      |    ✅   | bcrypt + Flask sessions      |
| NLP Processing      |    ✅   | NLTK + spaCy                 |
| Knowledge Base      |    ✅   | SQLite + FAISS               |
| ML Model            |    ✅   | TF-IDF + Logistic Regression |
| Response Generation |    ✅   | NLP + ML + Knowledge Base    |
| Admin Dashboard     |    ✅   | Streamlit + Flask            |
| Academic Assistance |    ✅   | University KB + Streamlit    |
| Voice Interaction   |    ✅   | SpeechRecognition + gTTS     |
| Live AI             |    ✅   | Provider-agnostic AI service |
| Mock Data Mode      |    ✅   | Local KB + FAISS             |
| Chat History        |    ✅   | Database-backed storage      |
| FAQ Management      |    ✅   | Admin CRUD                   |
| User Management     |    ✅   | Admin interface              |
| AI Configuration    |    ✅   | Admin settings               |
| ML Management       |    ✅   | Model status / retraining    |

---

# 📊 Engineering Concepts Demonstrated

This project brings together several areas of software and AI engineering:

### 🤖 Artificial Intelligence

* Live AI provider integration
* AI-assisted conversational responses
* Provider abstraction

### 🧠 Natural Language Processing

* NLTK
* spaCy
* Text preprocessing
* Intent-oriented language processing

### 📈 Machine Learning

* TF-IDF feature extraction
* Logistic Regression
* Intent classification
* Model artifacts and management

### 🔎 Information Retrieval

* Sentence Transformers
* Embeddings
* FAISS vector search
* Knowledge-base retrieval

### 🌐 Backend Engineering

* Flask
* Backend API architecture
* Authentication/session handling
* Modular service components

### 🗄️ Data Management

* SQLite
* Knowledge-base storage
* FAQ management
* Chat history
* Logs

### 🧪 Software Testing

* Phase-based test organization
* Backend testing
* Authentication testing
* NLP/ML testing
* Mock/Live mode testing

---

# 🧠 QNA (About This Project)

### 1. Why did I build IIUI Smart Chatbot?

I built IIUI Smart Chatbot as my BS Final Year Project to explore how AI, NLP, machine learning, information retrieval, and web application development can be combined to solve a practical university-support problem.

The idea was to create a centralized conversational system where students and faculty could access university-related information through a chatbot interface instead of manually searching through different sources.

### 2. Why did I use both Mock AI and Live AI modes?

I used two modes because they solve different requirements.

The **Mock Data Assistant** works around the project's local university knowledge base and retrieval system, making it useful for controlled demonstrations and university-specific information.

The **Live AI Assistant** provides integration with an external AI provider for more flexible conversational responses.

Separating the two modes also made the architecture easier to test and maintain.

### 3. Why did I use Streamlit for the frontend?

I used Streamlit because it allowed me to build an interactive Python-based web interface quickly while keeping the frontend closely integrated with the AI and data-processing components.

For this FYP, it also allowed me to focus more heavily on the chatbot, NLP, machine-learning, retrieval, and backend functionality without introducing a separate JavaScript frontend framework.

### 4. Why did I use Flask for the backend?

I used Flask to provide a dedicated backend layer for API handling, authentication, sessions, administrative functionality, and communication between the application components.

Separating backend responsibilities from the Streamlit interface also gave the project a clearer application structure.

### 5. How does my NLP and ML pipeline work?

I designed the processing pipeline around traditional NLP and machine-learning techniques.

The general flow is:

```text
User Query
    ↓
NLP Processing
    ↓
TF-IDF Feature Extraction
    ↓
Logistic Regression
    ↓
Intent Detection
    ↓
Retrieval / Response Generation
```

This gives the project an actual machine-learning component instead of relying entirely on an external LLM.

### 6. Why did I use TF-IDF and Logistic Regression?

I used TF-IDF to convert text into numerical features and Logistic Regression as the intent-classification model.

This combination is lightweight, interpretable, relatively simple to train, and suitable for a structured classification problem such as identifying common categories of university questions.

### 7. Why did I use FAISS and Sentence Transformers?

I used Sentence Transformers to generate semantic representations and FAISS to perform efficient similarity-based retrieval.

This allows the system to find relevant information based on semantic similarity rather than depending only on exact keyword matches.

### 8. Why did I use SQLite?

I used SQLite because the project is primarily a local FYP application and does not require the operational complexity of a large database server.

SQLite provides persistent storage for application data such as users, knowledge-base information, FAQs, and chat-related records while keeping the project easy to run locally.

### 9. How did I handle authentication?

I implemented authentication using Flask-based session handling and bcrypt for password hashing.

The application also separates administrative functionality from normal user functionality so that management operations such as knowledge-base and user administration are not exposed as normal user features.

### 10. How does the admin dashboard help the project?

I included an administrative layer so the chatbot is not just a static question-answering interface.

Administrators can manage university information, FAQs, users, chat records, AI configuration, and ML-related functionality through the application.

This makes the system more representative of a maintainable software application.

### 11. Why did I add voice interaction?

I added voice interaction to provide an alternative input method for users.

The voice pipeline converts speech into text and then sends the resulting text through the same chatbot processing pipeline used for typed questions.

This keeps voice interaction as an additional interface rather than creating a completely separate chatbot system.

### 12. What software-engineering concepts does this project demonstrate?

This project demonstrates:

* Full-stack Python application development
* Streamlit UI development
* Flask backend architecture
* REST-style API integration
* NLP processing
* Machine-learning classification
* Semantic information retrieval
* FAISS vector search
* Database design with SQLite
* Authentication and session management
* Role-aware administration
* Modular service architecture
* Automated and phase-based testing
* Voice-enabled interaction
* External AI provider integration

### 13. What would I improve for a larger production deployment?

For a larger deployment, I would consider moving from SQLite to a production-oriented database where appropriate, adding more comprehensive automated testing, strengthening authorization and secrets management, introducing centralized logging and monitoring, improving deployment infrastructure, adding stronger input validation and rate limiting, and establishing formal observability around the AI and retrieval pipelines.

---

# 📬 Contact & Hire Me

<div align="center">

### 💼 Interested in working with me?

**Abdul Hannan Shahid**

**Software Development • AI Applications • Full-Stack Development • NLP/ML • IT Systems**

📧 **Email:** [iamhannanshahid@gmail.com](mailto:iamhannanshahid@gmail.com)

💻 **GitHub:** [github.com/Hannan864](https://github.com/Hannan864)

🔗 **LinkedIn:** [linkedin.com/in/hanstudio](https://linkedin.com/in/hanstudio)

</div>

---

<div align="center">

### 🎓 IIUI Smart Chatbot

**A BS Final Year Project demonstrating practical integration of AI, NLP, machine learning, information retrieval, backend engineering, and university-focused software development.**

**© 2026 Abdul Hannan Shahid • International Islamic University Islamabad**

</div>
```
