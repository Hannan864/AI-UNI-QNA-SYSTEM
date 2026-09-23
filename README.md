# 🎓 IIUI Smart Chatbot — AI-Powered University Support System

<div align="center">

# 🤖 IIUI Smart Chatbot

### Intelligent University Assistance • NLP • Machine Learning • Semantic Search • Gemini AI • Voice Interaction

**BS Final Year Project — International Islamic University Islamabad (IIUI)**

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python AI](https://img.shields.io/badge/AI-Powered-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Scikit Learn](https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge)](https://spacy.io/)
[![FAISS](https://img.shields.io/badge/FAISS-Semantic_Search-0468D7?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br>

**An AI-assisted university support platform combining traditional NLP, machine learning, semantic retrieval, knowledge-base search, Gemini/live AI integration, authentication, administration, and voice interaction.**

</div>

---

## 🖼️ AI & System Showcase

<div align="center">

### 🧠 AI-Powered University Assistance

```text
                    ┌─────────────────────────┐
                    │       👨‍🎓 USER          │
                    │  Student / Faculty      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    💬 CHAT INTERFACE    │
                    │       Streamlit         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      🧠 AI PIPELINE     │
                    │   NLP + ML + Retrieval  │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
              ▼                                     ▼
     ┌──────────────────┐                 ┌──────────────────┐
     │   📚 KNOWLEDGE   │                 │   ✨ GEMINI AI   │
     │      BASE        │                 │   LIVE AI MODE   │
     │  SQLite + FAISS  │                 │  External Model  │
     └────────┬─────────┘                 └────────┬─────────┘
              │                                    │
              └────────────────┬───────────────────┘
                               ▼
                    ┌─────────────────────────┐
                    │      🤖 RESPONSE        │
                    │ University Assistance   │
                    └─────────────────────────┘
````

</div>

---

# 📌 What Is IIUI Smart Chatbot?

**IIUI Smart Chatbot** is a university-focused AI and NLP application developed as a **BS Final Year Project** for **International Islamic University Islamabad (IIUI)**.

The system provides students and faculty with a conversational interface for accessing university-related information including:

* 🎓 Admissions and eligibility
* 📚 Academic programs and courses
* 💰 Fees and financial information
* 📝 Examination and grading policies
* 📅 Academic calendar
* 🧑‍💻 FYP guidelines
* 🏠 Hostel and transport information
* 🎓 Scholarships and financial aid
* 📖 Student policies and university guidance

The project combines **traditional NLP, machine learning, semantic search, local knowledge retrieval, and live AI integration** into one application.

The key idea is:

> **Don't rely on one AI technique — combine deterministic university knowledge with ML, semantic retrieval, and modern generative AI.**

---

# ✨ AI Architecture at a Glance

```text
                         USER QUESTION
                              │
                              ▼
                    ┌───────────────────┐
                    │  Streamlit Chat   │
                    │     Interface     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Flask Backend   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Chat Router    │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌──────────────────┐
        │   MOCK MODE     │       │    LIVE AI MODE  │
        │                 │       │                  │
        │ NLTK + spaCy    │       │  Gemini / AI     │
        │ TF-IDF + ML     │       │    Provider      │
        │ FAISS + KB      │       │                  │
        └────────┬────────┘       └────────┬─────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    ┌───────────────────┐
                    │ Response Generator│
                    └─────────┬─────────┘
                              │
                              ▼
                    🤖 FINAL RESPONSE
```

---

# 🎯 Core Features

## 👨‍🎓 Student & Faculty Features

### 💬 University AI Assistant

Ask natural-language questions about university-related information.

### 📚 Knowledge-Based Assistant

Answers can be generated using locally maintained university information.

### ✨ Live AI Assistant

Supports integration with an external AI provider, including Gemini-compatible AI configuration.

### 🔎 Semantic Search

Uses embeddings and FAISS to retrieve semantically relevant information.

### 🧠 Intent Detection

Machine-learning classification identifies the likely intent behind a user's query.

### 💾 Chat History

Users can review previous conversations stored by the application.

### 🎙️ Voice Interaction

Users can provide questions through microphone input instead of typing.

---

# 👨‍💼 Administrator Features

The administrator interface provides management capabilities for the complete chatbot ecosystem.

| Module             | Function                                         |
| ------------------ | ------------------------------------------------ |
| 📊 Dashboard       | System statistics and overview                   |
| 📚 Knowledge Base  | Create, update and manage university information |
| ❓ FAQ Management   | Manage frequently asked questions                |
| 👥 User Management | View and manage registered users                 |
| 💬 Chat Logs       | Review chatbot interactions                      |
| ⚙️ AI Settings     | Configure live AI provider                       |
| 🧠 ML Management   | View model status and retraining functionality   |

---

# 🤖 AI & Machine Learning Stack

The project demonstrates several different approaches to AI rather than depending entirely on a single LLM.

## 🧠 Natural Language Processing

Implemented using:

* **NLTK**
* **spaCy**
* Text preprocessing
* Linguistic processing
* Intent-oriented feature preparation

---

## 📈 Traditional Machine Learning

The intent-classification pipeline uses:

```text
User Query
     ↓
Text Processing
     ↓
TF-IDF Vectorization
     ↓
Logistic Regression
     ↓
Intent Classification
```

### Why this matters

This gives the project an actual **machine-learning classification layer** instead of making the application simply an API wrapper around a generative AI model.

---

# ✨ Gemini / Generative AI Integration

The project includes a **Live AI layer** designed to communicate with an external AI provider.

Where Gemini is configured as the provider, the flow becomes:

```text
                  User Question
                        │
                        ▼
                ┌───────────────┐
                │ Chat Router   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Live AI       │
                │ Service       │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Google Gemini │
                │      ✨       │
                └───────┬───────┘
                        │
                        ▼
                AI-Generated Response
```

The AI service is separated from the rest of the application so that the chatbot architecture is not tightly coupled to one specific provider.

### AI responsibilities

Depending on the configured provider, the Live AI layer can support:

* Natural-language conversation
* Flexible question answering
* AI-generated responses
* Context-aware conversational interaction
* Provider-specific AI configuration

> **Important:** The local Mock mode remains independent of external AI services, allowing the project to demonstrate its own NLP, ML, retrieval, and knowledge-base pipeline.

---

# 🔎 Semantic Search & Knowledge Retrieval

The project uses:

* **Sentence Transformers**
* **Embeddings**
* **FAISS**
* **SQLite knowledge base**

The retrieval process can be represented as:

```text
University Information
        │
        ▼
 Knowledge Base
        │
        ▼
Sentence Transformer
        │
        ▼
   Embeddings
        │
        ▼
      FAISS
        │
        ▼
Relevant Information
        │
        ▼
Response Generator
```

This allows the system to retrieve information based on **semantic similarity**, rather than depending exclusively on exact keyword matching.

---

# 🧩 Hybrid AI Architecture

One of the main technical aspects of the project is that different technologies perform different jobs.

| Component                | Responsibility               |
| ------------------------ | ---------------------------- |
| 🧹 NLTK                  | NLP processing               |
| 🧠 spaCy                 | Linguistic processing        |
| 📈 TF-IDF                | Text feature extraction      |
| 🤖 Logistic Regression   | Intent classification        |
| 🔎 Sentence Transformers | Semantic embeddings          |
| ⚡ FAISS                  | Vector similarity search     |
| 📚 SQLite                | University knowledge storage |
| ✨ Gemini / AI Provider   | Generative AI responses      |
| 🧩 Response Generator    | Final response construction  |

This creates a **hybrid conversational architecture** combining traditional ML, retrieval-based methods, and generative AI.

---

# 🏗️ Full System Architecture

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                              │
│                                                                              │
│                              Streamlit UI                                    │
│                                                                              │
│       Student / Faculty                         Administrator               │
│              │                                          │                    │
│              └────────────────────┬─────────────────────┘                    │
└───────────────────────────────────┼──────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND LAYER                                   │
│                                                                              │
│                                Flask                                         │
│                                                                              │
│       Authentication │ Sessions │ Chat APIs │ Admin APIs │ AI Settings      │
└───────────────────────────────────┼──────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CHAT ROUTER                                     │
│                                                                              │
│                         ┌────────┴────────┐                                  │
│                         ▼                 ▼                                  │
│                     MOCK MODE         LIVE AI MODE                           │
└─────────────────────────┼─────────────────┼──────────────────────────────────┘
                          │                 │
                          ▼                 ▼
              ┌──────────────────┐   ┌────────────────────┐
              │ NLP + ML Pipeline│   │ AI Provider Layer │
              └────────┬─────────┘   └─────────┬──────────┘
                       │                       │
                       ▼                       ▼
              ┌──────────────────┐     ┌──────────────────┐
              │ SQLite + FAISS   │     │ Gemini / External │
              │ Knowledge Base   │     │ AI Provider       │
              └────────┬─────────┘     └─────────┬──────────┘
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Response Generation  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Chat Response    │
                         └──────────────────────┘
```

---

# 🔐 Authentication & Security

Authentication is implemented through the Flask backend.

### Security Components

* 🔑 Password hashing with bcrypt
* 👤 User authentication
* 🛡️ Session management
* 👨‍💼 Role-aware administration
* 🔒 Separation of user/admin functionality

The system distinguishes normal users from administrators so management functions remain separated from the student/faculty experience.

---

# 🎙️ Voice Interaction

The chatbot supports voice input as an additional interaction method.

## Voice Pipeline

```text
🎤 Microphone
      │
      ▼
Speech Recognition
      │
      ▼
Text Query
      │
      ▼
NLP / AI Pipeline
      │
      ▼
Chat Response
```

## How I Use It

1. Open the Chat Assistant.
2. Select Mock or Live mode.
3. Enable the **🎤 Voice** option.
4. Allow microphone access.
5. Speak the university-related question.
6. Speech is converted to text.
7. The text enters the normal chatbot pipeline.
8. The response is displayed to the user.

### Voice Requirements

* Browser microphone permission
* SpeechRecognition library
* Internet connection for the configured Google Speech Recognition service

If voice recognition fails, normal text input remains available.

---

# 🗄️ Database & Data Layer

The project uses **SQLite** for local persistent storage.

The database supports application data such as:

* Users
* Knowledge-base records
* FAQs
* Chat history
* Administrative data
* Application-related records

The project also maintains supporting artifacts for machine-learning and retrieval components.

---

# 🛠️ Technology Stack

| Layer             | Technology            | Purpose                     |
| ----------------- | --------------------- | --------------------------- |
| 💻 Language       | Python 3.10+          | Core development            |
| 🖥️ Frontend      | Streamlit             | Interactive web interface   |
| 🌐 Backend        | Flask                 | API and application backend |
| 🧠 NLP            | NLTK                  | Natural-language processing |
| 🧠 NLP            | spaCy                 | Linguistic processing       |
| 📈 ML             | Scikit-learn          | Machine learning            |
| 🔢 Features       | TF-IDF                | Text vectorization          |
| 🤖 Classifier     | Logistic Regression   | Intent classification       |
| 🔎 Embeddings     | Sentence Transformers | Semantic representation     |
| ⚡ Vector Search   | FAISS                 | Similarity retrieval        |
| 🗄️ Database      | SQLite                | Persistent storage          |
| 🔐 Authentication | bcrypt                | Password hashing            |
| ✨ Generative AI   | Gemini / AI Provider  | Live AI responses           |
| 🎙️ Speech        | SpeechRecognition     | Voice input                 |
| 🔊 TTS            | gTTS                  | Text-to-speech              |

---

# 📂 Project Structure

```text
iiui-chatbot/
│
├── app.py                         # Streamlit frontend
├── flask_server.py                # Flask backend
├── config.py                      # Application configuration
├── requirements.txt               # Dependencies
│
├── RUN.bat                        # One-click Windows launcher
├── start_flask.bat                # Flask launcher
├── start_streamlit.bat            # Streamlit launcher
├── run_tests.bat                  # Complete test launcher
├── README.md                      # Project documentation
│
├── auth/
│   ├── login.py                   # Authentication
│   └── session_manager.py         # Session management
│
├── database/
│   ├── db.py                      # SQLite manager
│   └── init_db.py                 # Initialization + seed data
│
├── models/
│   ├── nlp_processor.py           # NLTK + spaCy processing
│   ├── ml_classifier.py            # ML intent classifier
│   ├── response_generator.py      # Response generation
│   ├── chat_router.py             # Mock / Live routing
│   ├── generator.py               # Mock answer generator
│   ├── retriever.py               # FAISS retrieval
│   └── live_ai_service.py         # Live AI provider service
│
├── voice/                          # Voice functionality
├── mock_data/                      # Sample university data
├── models/ml_artifacts/            # Trained ML artifacts
├── embeddings/                     # FAISS embedding/cache data
├── logs/                           # Application/chat logs
│
├── test_phase3.py                  # Backend API tests
├── test_phase4.py                  # Authentication tests
├── test_phase5.py                  # Knowledge Base tests
├── test_phase6.py                  # Mock mode tests
├── test_phase7.py                  # Live AI tests
├── test_phase8.py                  # Router tests
├── test_phase9.py                  # NLP tests
└── test_phase10_11.py              # ML + response tests
```

---

# 🚀 Quick Start

## 🪟 Windows — One Click

The easiest way to launch the complete application is:

```text
RUN.bat
```

### Steps

1. Double-click **`RUN.bat`**
2. Wait for the backend and frontend to start
3. The browser should open automatically
4. Open:

```text
http://localhost:8501
```

### 🔐 Local Demo Account

```text
Email:    admin@iiu.edu.pk
Password: admin123
```

> ⚠️ These credentials are intended for local/demo use. Replace seeded credentials before any real deployment.

---

# 🖥️ Manual Startup

### Terminal 1 — Flask Backend

```bash
python flask_server.py
```

### Terminal 2 — Streamlit Frontend

```bash
streamlit run app.py --server.port 8501
```

Then visit:

```text
http://localhost:8501
```

---

# 🧪 Testing

The project contains phase-based test suites covering different parts of the system.

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

Or on Windows:

```text
run_tests.bat
```

## Test Coverage

| Test File            | Coverage                 |
| -------------------- | ------------------------ |
| `test_phase3.py`     | Backend APIs             |
| `test_phase4.py`     | Authentication           |
| `test_phase5.py`     | Knowledge Base / FAQ     |
| `test_phase6.py`     | Mock AI mode             |
| `test_phase7.py`     | Live AI integration      |
| `test_phase8.py`     | Mode routing             |
| `test_phase9.py`     | NLP processing           |
| `test_phase10_11.py` | ML + response generation |

---

# 🧪 Manual Testing Flow

## 👨‍🎓 Student / Faculty

1. Start the application using `RUN.bat`.
2. Register or log in.
3. Open **Mock Data Assistant**.
4. Ask:

```text
What is the admission process?
```

5. Verify the response.
6. Open **Chat History**.
7. Confirm the conversation is recorded.

## ✨ Live AI

1. Open **Live AI Assistant**.
2. Verify that an AI provider is configured.
3. Submit a question.
4. Verify the AI response.
5. Switch between Mock and Live modes.

## 👨‍💼 Administrator

1. Log in using an administrator account.
2. Open the dashboard.
3. Test Knowledge Base management.
4. Test FAQ management.
5. Review users and chat logs.
6. Open AI configuration.
7. Check ML model status.

---

# 📚 University Knowledge Base

The project includes reference documents covering major areas of university information.

| Document                                  | Information                    |
| ----------------------------------------- | ------------------------------ |
| `IIUI_Examination_and_Grading_Policy.pdf` | Examination and grading        |
| `IIUI_Academic_Calendar.pdf`              | Academic calendar              |
| `IIUI_Admissions_Eligibility_Guide.pdf`   | Admission requirements         |
| `IIUI_Course_Catalog.pdf`                 | Course information             |
| `IIUI_Date_Sheet_Criteria.pdf`            | Date-sheet criteria            |
| `IIUI_Fee_Structure_FAQs.pdf`             | Fee information                |
| `IIUI_FYP_Guidelines_FCIT.pdf`            | FYP guidelines                 |
| `IIUI_Hostel_and_Transport_Rules.pdf`     | Hostel and transport           |
| `IIUI_Scholarships_Financial_Aid.pdf`     | Scholarships and financial aid |
| `IIUI_Student_Handbook.pdf`               | Student policies               |

These documents provide reference material for the project's university knowledge base.

The chatbot's responses depend on the information actually stored, indexed, and retrieved by the application.

---

# 🎓 FYP Module Coverage

| FYP Module               | Status | Technology / Implementation   |
| ------------------------ | :----: | ----------------------------- |
| User Interface           |    ✅   | Streamlit                     |
| Authentication           |    ✅   | bcrypt + Flask sessions       |
| NLP Processing           |    ✅   | NLTK + spaCy                  |
| Knowledge Base           |    ✅   | SQLite + FAISS                |
| ML Model                 |    ✅   | TF-IDF + Logistic Regression  |
| Intent Detection         |    ✅   | NLP + ML                      |
| Entity / Text Processing |    ✅   | NLTK + spaCy                  |
| Response Generation      |    ✅   | NLP + ML + Knowledge Base     |
| Admin Dashboard          |    ✅   | Streamlit + Flask             |
| Academic Assistance      |    ✅   | University Knowledge Base     |
| Voice Interaction        |    ✅   | SpeechRecognition + gTTS      |
| Live AI                  |    ✅   | Provider-agnostic AI service  |
| Gemini Integration       |    ✅   | Configurable Live AI provider |
| Mock Data Mode           |    ✅   | Local KB + FAISS              |
| Chat History             |    ✅   | Database-backed storage       |
| FAQ Management           |    ✅   | Admin CRUD                    |
| User Management          |    ✅   | Admin interface               |
| AI Configuration         |    ✅   | Admin settings                |
| ML Management            |    ✅   | Model status / retraining     |

---

# 📊 Engineering Domains Demonstrated

## 🤖 Artificial Intelligence

* Generative AI integration
* Gemini-compatible live AI architecture
* AI provider abstraction
* Conversational AI

## 🧠 Natural Language Processing

* NLTK
* spaCy
* Text preprocessing
* Intent-oriented processing

## 📈 Machine Learning

* TF-IDF
* Logistic Regression
* Intent classification
* Model artifacts
* Retraining workflow

## 🔎 Information Retrieval

* Sentence Transformers
* Embeddings
* FAISS
* Semantic similarity search
* Knowledge-base retrieval

## 🌐 Software Engineering

* Frontend/backend separation
* Flask backend
* Streamlit interface
* Modular Python architecture
* Authentication
* Session management
* Administrative workflows

## 🧪 Testing

* Backend testing
* Authentication testing
* NLP testing
* ML testing
* Mock-mode testing
* Live-AI testing
* Phase-based test organization

---

# 💡 Why This Project Is Technically Interesting

The project is not simply a **"chatbot connected to an AI API."**

It demonstrates a layered approach:

```text
                 ┌──────────────────────────┐
                 │       User Interface     │
                 │        Streamlit         │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │      Flask Backend       │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │      Chat Router         │
                 └────────────┬─────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
         🧠 NLP/ML       🔎 Retrieval       ✨ Gemini
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    🤖 Response Layer
                              │
                              ▼
                         👨‍🎓 User
```

This separation makes it possible to demonstrate **traditional AI/ML techniques alongside modern generative AI** within the same application.

---

# 🧠 QNA (About This Project)

### 1. Why did I build IIUI Smart Chatbot?

I built IIUI Smart Chatbot as my BS Final Year Project to explore how AI, NLP, machine learning, information retrieval, and software engineering can be combined to solve a practical university-support problem.

I wanted to build more than a basic chatbot. I designed the system around university knowledge, intent detection, semantic retrieval, administration, authentication, voice interaction, and optional generative AI.

### 2. Why did I use both traditional ML and Generative AI?

I used traditional machine learning for structured tasks such as intent classification and generative AI for flexible conversational interaction.

This allowed me to separate deterministic or classification-oriented tasks from open-ended language generation instead of using an LLM for every part of the system.

### 3. Why did I integrate Gemini?

I integrated Gemini through the Live AI layer to provide a modern generative-AI capability within the chatbot.

I kept the AI provider behind a separate service layer so the rest of the application does not have to depend directly on one provider implementation.

### 4. Why did I use Streamlit?

I used Streamlit because it allowed me to develop an interactive Python-based interface while keeping the project focused on the AI, NLP, ML, retrieval, and backend components.

For an FYP, this also reduced frontend complexity while still providing a functional web application.

### 5. Why did I use Flask?

I used Flask to provide a dedicated backend layer for API handling, authentication, sessions, administrative functionality, and communication between application components.

This separates backend responsibilities from the Streamlit presentation layer.

### 6. How does my machine-learning pipeline work?

I designed the intent-classification pipeline as:

```text
User Query
    ↓
NLP Processing
    ↓
TF-IDF Feature Extraction
    ↓
Logistic Regression
    ↓
Intent Classification
```

The predicted intent can then be used by the rest of the chatbot pipeline for retrieval and response generation.

### 7. Why did I use TF-IDF and Logistic Regression?

I used TF-IDF to transform text into numerical features and Logistic Regression for intent classification.

This is a lightweight and practical approach for a structured classification problem such as categorizing common university-related questions.

### 8. Why did I use Sentence Transformers and FAISS?

I used Sentence Transformers to create semantic representations of text and FAISS to perform similarity-based retrieval.

This allows the knowledge-base system to search for information based on semantic similarity rather than relying entirely on exact keyword matching.

### 9. How does my Mock Data Assistant work?

I designed Mock mode around local university information.

The general flow is:

```text
User Question
     ↓
NLP Processing
     ↓
Intent / Query Analysis
     ↓
Knowledge Retrieval
     ↓
FAISS Similarity Search
     ↓
Response Generation
     ↓
University Answer
```

This mode does not require every response to be generated by an external AI service.

### 10. How does my Live AI Assistant work?

The Live AI Assistant routes the conversation through the application's AI service layer.

When Gemini or another configured provider is enabled, the service communicates with that provider and returns the generated response to the application.

The provider-specific implementation remains separated from the main chatbot architecture.

### 11. Why did I create Mock and Live modes separately?

I separated the modes so that the project can demonstrate both:

* A controlled local knowledge/retrieval system
* A modern generative-AI integration

This also makes development and testing easier because the local mode does not depend entirely on external AI availability.

### 12. Why did I use SQLite?

I used SQLite because this is primarily a local FYP application and SQLite provides simple persistent storage without requiring a separate database server.

It is suitable for storing application data such as users, FAQs, knowledge-base records, and chat-related information within the project's current scope.

### 13. How did I implement authentication?

I implemented authentication through Flask sessions and bcrypt password hashing.

I also separated administrator functionality from normal user functionality so that management operations remain within the administrative interface.

### 14. Why did I add voice interaction?

I added voice interaction to provide an alternative way for users to submit questions.

The important part of the design is that voice input eventually becomes text and enters the same chatbot pipeline as a typed question.

### 15. What makes this more than a simple AI chatbot?

I combined several engineering layers:

* NLP processing
* Traditional machine learning
* Semantic retrieval
* FAISS vector search
* SQLite knowledge storage
* Flask backend
* Streamlit frontend
* Authentication
* Administration
* Voice interaction
* Live generative AI
* Gemini integration
* Automated testing

The project therefore demonstrates both **AI concepts and general software-engineering practices**.

### 16. What was the main engineering challenge?

One of the main challenges was coordinating different processing approaches within a single conversational flow.

The system has to handle user input, NLP processing, intent classification, retrieval, response generation, database operations, and optional live AI integration without making every component tightly dependent on another.

I addressed this by separating responsibilities into modules such as the NLP processor, ML classifier, retriever, response generator, chat router, and live AI service.

### 17. What would I improve for a larger production deployment?

For a larger deployment, I would consider:

* Moving from SQLite to a production-oriented database where appropriate
* More comprehensive automated testing
* Stronger authorization controls
* Secure secrets management
* API rate limiting
* Centralized logging and monitoring
* Formal observability
* Better deployment infrastructure
* More extensive AI response validation
* Improved retrieval evaluation
* Stronger protection against prompt injection and malicious input

---

# 📬 Contact & Hire Me

<div align="center">

## 💼 Let's Build Something With AI

### **Abdul Hannan Shahid**

**Software Development • AI Applications • Full-Stack Development • NLP/ML • IT Systems**

<br>

📧 **Email**

**[iamhannanshahid@gmail.com](mailto:iamhannanshahid@gmail.com)**

<br>

💻 **GitHub**

**github.com/Hannan864**

<br>

🔗 **LinkedIn**

**linkedin.com/in/hanstudio**

<br>

### Open to opportunities involving

**AI Applications · Software Development · Full-Stack Development · NLP/ML · Python · Backend Engineering · IT Systems**

</div>

---

<div align="center">

### 🤖 IIUI Smart Chatbot

**AI + NLP + Machine Learning + Semantic Search + Gemini + University Knowledge**

Built as a **BS Final Year Project** at **International Islamic University Islamabad**

<br>

[![Python](https://img.shields.io/badge/Built_With-Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Powered_by-Gemini_AI-8E75B2?style=for-the-badge\&logo=google\&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br>

**© 2026 Abdul Hannan Shahid • International Islamic University Islamabad**

</div>
