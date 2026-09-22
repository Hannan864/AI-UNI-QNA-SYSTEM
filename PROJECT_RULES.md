# PROJECT_RULES.md — AI Chatbot for University Support

**Status:** PERMANENT PROJECT CONSTITUTION
**Created:** August 18, 2026
**Authority:** Approved Project Proposal
**Rule:** NON-NEGOTIABLE — DO NOT OVERRIDE

---

## 1. PROJECT IDENTITY

| Field | Value |
|-------|-------|
| Project Name | AI Chatbot for University Support |
| Domain | Artificial Intelligence (AI), Natural Language Processing (NLP), Educational Technology (EdTech) |
| Purpose | To assist students with academic and administrative information; To reduce workload on university help desks; To centralize university knowledge in one intelligent system |
| Level | BS Final Year Project |
| University | International Islamic University Islamabad (IIUI) |
| Students | Asharib Khan (909-FOC/BSIT/F22-B), Kashif Farooq (899-FOC/BSIT/F-22B) |

---

## 2. TECHNOLOGY COMPLIANCE TABLE

Every implementation task MUST verify compliance against this table.

| Area | Approved Technology | Current Technology | Status |
|------|---------------------|-------------------|--------|
| Language | Python | Python 3.10 | COMPLIANT |
| Frontend | Streamlit | Streamlit >=1.38.0 | COMPLIANT |
| Backend | Python + Flask | Flask >=3.0.0 | COMPLIANT |
| NLP | NLTK + spaCy | NLTK >=3.9.1 + spaCy | COMPLIANT |
| ML | Scikit-learn + TensorFlow/PyTorch | Scikit-learn >=1.5.0 + Sentence Transformers | COMPLIANT |
| Database | SQLite/MySQL | SQLite | COMPLIANT |
| Vector Search | FAISS | FAISS >=1.8.0 | COMPLIANT |
| Voice | SpeechRecognition + gTTS | SpeechRecognition >=3.11.0 + gTTS >=2.5.1 | COMPLIANT |
| Auth | bcrypt | bcrypt >=4.2.0 | COMPLIANT |
| Live AI | Configurable Provider | Not yet configured | PENDING |

### 2.1 Live AI Configuration

The FYP proposal does NOT mandate a specific AI provider.
Therefore, the AI provider must be CONFIGURABLE, not hard-coded.

Approved configuration fields:
- AI Provider (OpenAI, Anthropic, local model, etc.)
- Model name
- API Key (stored securely)
- Base URL/Endpoint (where supported)
- Temperature (where supported)
- Max output tokens (where supported)
- Enable/Disable toggle

Security rules:
- Never display full saved API keys
- Never put keys in logs or chat messages
- Use secure environment variables/secrets storage
- Do not expose keys to the frontend after saving

---

## 3. ABSOLUTE TECHNOLOGY LOCKS

### 3.1 Programming Language Lock

**APPROVED:** Python

**FORBIDDEN replacements:**
- JavaScript / TypeScript
- Java
- C# / C++
- PHP
- Ruby
- Go
- Rust
- Any other language

**Rule:** Python is the ONLY acceptable programming language for this project.

### 3.2 Frontend Lock

**APPROVED:** Streamlit

**FORBIDDEN replacements:**
- React / Next.js
- Vue / Nuxt.js
- Angular
- Svelte
- Plain HTML/CSS/JavaScript as replacement frontend
- Bootstrap as standalone frontend
- Tailwind CSS framework switch
- Any other frontend framework

**Rule:** All UI MUST be built within Streamlit. UI improvement means improving Streamlit code, NOT switching frameworks.

### 3.3 Backend Lock

**APPROVED:** Python + Flask

**FORBIDDEN replacements:**
- Node.js / Express.js
- FastAPI (unless explicitly authorized)
- Django
- Spring Boot
- Laravel
- ASP.NET
- Any other backend framework

**Rule:** Flask is the ONLY acceptable backend framework.

### 3.4 NLP Lock

**APPROVED:** NLTK + spaCy

**FORBIDDEN replacements:**
- Hugging Face Transformers as primary NLP (can be used as supplementary only)
- OpenAI API as primary NLP
- Any other NLP framework as primary

**Rule:** NLTK and spaCy are the primary NLP technologies.

### 3.5 Machine Learning Lock

**APPROVED:** Scikit-learn + TensorFlow/PyTorch

**FORBIDDEN replacements:**
- JAX as primary ML
- Any other ML framework as primary

**Rule:** Use Scikit-learn for traditional ML. TensorFlow/PyTorch for deep learning if needed.

### 3.6 Database Lock

**APPROVED:** SQLite / MySQL

**Current:** SQLite

**FORBIDDEN replacements:**
- MongoDB
- PostgreSQL
- Firebase / Firestore
- Supabase
- Redis as primary database
- Oracle
- Any other database

**Rule:** SQLite is the approved database. Do NOT migrate without explicit authorization.

---

## 4. EXISTING PROJECT TECHNOLOGY INVENTORY

### 4.1 All Currently Used Technologies

| Technology | Purpose | File Location | Status |
|------------|---------|---------------|--------|
| Python 3.10 | Primary language | All files | APPROVED |
| Streamlit | Frontend UI | app.py | APPROVED |
| Flask | Backend API | flask_server.py | APPROVED |
| Flask-CORS | CORS handling | flask_server.py | APPROVED |
| NLTK | NLP processing | models/nlp_processor.py | APPROVED |
| spaCy | NLP processing | models/nlp_processor.py | APPROVED |
| Sentence Transformers | Embeddings | models/retriever.py | APPROVED |
| FAISS | Vector similarity search | models/retriever.py | APPROVED |
| Scikit-learn | ML utilities | requirements.txt | APPROVED |
| SQLite | Database | database/db.py | APPROVED |
| bcrypt | Password hashing | auth/login.py | APPROVED |
| SpeechRecognition | Voice input | voice/speech_to_text.py | APPROVED |
| gTTS | Text-to-speech | voice/text_to_speech.py | APPROVED |
| NumPy | Numerical computing | models/retriever.py | APPROVED |
| Pandas | Data manipulation | requirements.txt | APPROVED |
| python-dotenv | Environment config | config.py | APPROVED |
| requests | HTTP client | app.py | APPROVED |

### 4.2 Technology Compliance Verdict

**ALL technologies currently used in the project are APPROVED and COMPLIANT.**

No technology conflicts detected.

---

## 5. ARCHITECTURE RULES

### 5.1 Current Architecture (APPROVED)

```
Streamlit Frontend (app.py)
        |
        | HTTP API calls
        v
Flask Backend (flask_server.py)
        |
        | Database queries
        v
SQLite Database (database/iiui_data.db)
        |
        | Embeddings
        v
FAISS Index (embeddings/faq_embeddings.pkl)
```

### 5.2 Architecture Change Rules

- Do NOT introduce microservices architecture
- Do NOT introduce message queues
- Do NOT introduce separate frontend server
- Do NOT introduce containerization unless explicitly required
- Keep the architecture simple and understandable for a BS project

### 5.3 Communication Pattern

- Frontend communicates with Backend via HTTP REST API
- Backend communicates with Database via SQLite Python API
- Backend uses FAISS for vector similarity search
- All communication stays within the approved stack

---

## 6. MODULE RULES

### 6.1 Approved Modules (from Proposal)

| # | Module | Description | Status |
|---|--------|-------------|--------|
| 1 | User Interface Module | Allows users to interact with the chatbot | EXISTS |
| 2 | Authentication & User Management | Optional login, role-based access (student, faculty, admin) | EXISTS |
| 3 | NLP Processing | Intent detection and entity extraction | EXISTS |
| 4 | Knowledge Base | Stores university-related data, updatable by admin | EXISTS |
| 5 | Machine Learning Model | Trains on historical queries, improves accuracy | EXISTS |
| 6 | Response Generation | Matches intent with best response | EXISTS |
| 7 | Admin Dashboard | Manage FAQs, chatbot responses, chat logs | UI EXISTS |

Additional modules in project:
| Module | Description | Status |
|--------|-------------|--------|
| Chat History | Conversation logging | EXISTS |
| Voice Input | Speech-to-text | EXISTS |
| Voice Output | Text-to-speech | EXISTS |

### 6.2 Module Development Rules

- Each module must use approved technologies only
- Modules must communicate through well-defined interfaces
- Do not create inter-module dependencies that violate architecture
- Each module must be independently testable

---

## 7. DEVELOPMENT RULES

### 7.1 Before Any Change

1. Read this PROJECT_RULES.md
2. Verify technology compliance
3. Inspect affected files
4. Understand existing functionality
5. Make minimal necessary changes
6. Test the change
7. Verify no technology violations

### 7.2 Code Quality Rules

- Follow existing code conventions
- Use meaningful variable/function names
- Avoid code duplication
- Keep functions manageable (< 50 lines ideal)
- Add comments only where truly necessary
- Do not leave debug code or temporary hacks
- Do not leave unused imports

### 7.3 File Management Rules

- Do NOT delete existing files without explicit justification
- Do NOT rename files without checking all references
- Do NOT create files that violate the approved architecture
- Prefer editing existing files over creating new ones

### 7.4 Dependency Rules

- Do NOT add new dependencies without checking approval
- Do NOT add JavaScript/Node.js packages
- Do NOT add frontend framework packages
- Do NOT add non-Python backend packages
- All new packages must be approved or genuinely necessary

---

## 8. UI/UX RULES

### 8.1 Frontend Technology

**MUST use:** Streamlit

**Improvement goal:** Make Streamlit look professional

**NOT allowed:**
- Switching to React/Vue/Angular
- Using Streamlit as "wrapper" for another frontend
- Embedding React components in Streamlit

### 8.2 UI Quality Standards

The Streamlit UI must be:
- Professional and clean
- Modern looking
- Academic in tone
- Responsive where possible
- User-friendly
- Consistent in design
- Well-organized

### 8.3 UI Screens Required

| Screen | Purpose | Priority |
|--------|---------|----------|
| Login | User authentication | P0 |
| Registration | New user signup | P0 |
| Student Dashboard | Chat interface | P0 |
| Admin Dashboard | System management | P0 |
| Chat History | View past conversations | P1 |
| FAQ Management | CRUD for FAQs (admin) | P0 |
| Knowledge Base | View/manage KB | P1 |
| User Management | Admin user control | P1 |
| Analytics | Basic statistics | P2 |

### 8.4 UI Connection Rule

Every UI element must connect to actual backend functionality.

**FORBIDDEN:**
- Fake login that doesn't authenticate
- Fake chatbot responses from hard-coded data
- Buttons that do nothing
- Analytics showing fake data
- Database operations that don't actually execute

If functionality is not implemented, clearly mark it as:
- "Coming Soon"
- "Planned"
- "Demo Mode"

---

## 9. BACKEND RULES

### 9.1 Backend Framework

**MUST use:** Flask

**NOT allowed:**
- FastAPI
- Django
- Node.js/Express
- Any other backend framework

### 9.2 API Design Rules

- Use RESTful API patterns
- Use JSON for data exchange
- Use proper HTTP status codes
- Implement proper error handling
- Use consistent response format

### 9.3 API Response Format

```json
{
    "success": true/false,
    "message": "Description",
    "data": {},
    "error": {}
}
```

### 9.4 Authentication Rules

- Use bcrypt for password hashing
- Use session-based authentication
- Implement role-based access control
- Protect admin endpoints
- Validate sessions on every request

---

## 10. DATABASE RULES

### 10.1 Database Engine

**MUST use:** SQLite

**NOT allowed:**
- MongoDB
- PostgreSQL
- MySQL migration (unless explicitly authorized)
- Firebase
- Any other database

### 10.2 Database Operations

- Use parameterized queries (prevent SQL injection)
- Use context managers for connections
- Close connections after use
- Handle database errors gracefully
- Do not expose database errors to users

### 10.3 Schema Changes

- Do not drop tables without backup
- Do not delete columns without migration plan
- Add new tables/columns as needed
- Maintain backward compatibility
- Document all schema changes

---

## 11. NLP RULES

### 11.1 NLP Technologies

**MUST use:** NLTK + spaCy

**Current usage:**
- NLTK: Tokenization, stopwords, lemmatization
- spaCy: Named entity extraction, keyword extraction

### 11.2 NLP Responsibilities

- Text preprocessing (tokenization, normalization)
- Intent detection (keyword + pattern matching)
- Entity extraction (spaCy NER)
- Text similarity (spaCy similarity)
- Query processing

### 11.3 NLP Performance Rules

- NLP processing should not block the main thread
- Cache NLP model loading
- Handle model download failures gracefully
- Provide fallback for NLP failures

---

## 12. ML RULES

### 12.1 ML Technologies

**MUST use:** Scikit-learn + Sentence Transformers

**Current usage:**
- Sentence Transformers: Text embeddings
- FAISS: Vector similarity search
- Scikit-learn: Available for traditional ML if needed

### 12.2 ML Model Rules

- Use pre-trained models where possible
- Cache model loading
- Handle model download failures
- Do not train models from scratch unless necessary
- Keep models lightweight for BS project scope

---

## 13. CHATBOT RULES

### 13.1 Chatbot Architecture

The chatbot MUST support TWO modes:

**MODE 1: MOCK DATA**
- Uses Knowledge Base / configured university data
- Does NOT call external AI providers
- Responses come from stored information

**MODE 2: LIVE AI**
- Uses configured AI provider/model
- Requires valid API configuration
- Falls back gracefully if not configured

The mode switch MUST be:
- Clearly visible in the UI
- Stored with conversations/messages
- Never confused between modes

### 13.2 Response Quality Rules

- Responses must be accurate
- Responses must be helpful
- Never fabricate university information
- Provide fallback for uncertain answers
- Indicate confidence level
- Show which mode generated the response

### 13.3 Chatbot Scope

The chatbot MUST focus on university-related queries:
- Admissions
- Course registration
- Examination schedules
- Fee structure
- Academic policies
- University services
- General university information

**Unique Feature:** Automated University Support & Query Resolution

**NOT allowed:**
- General-purpose chatbot functionality
- Unrelated topics
- Fabricated information
- ChatGPT clone behavior
- Mixing Live AI and Mock Data responses

---

## 14. SECURITY RULES

### 14.1 Never Expose

- Passwords (use hashing)
- Database credentials
- API keys
- Secret keys
- Internal configuration
- Stack traces to users

### 14.2 Always Implement

- Password hashing (bcrypt)
- Input validation
- SQL injection prevention
- XSS prevention
- Session management
- Role-based access control

### 14.3 Configuration Security

- Use environment variables for secrets
- Do not hardcode credentials
- Use .env files (not committed to git)
- Different configs for dev/production

---

## 15. TESTING RULES

### 15.1 Test Requirements

Every major change MUST be tested:

| Test Type | Required | Priority |
|-----------|----------|----------|
| Import test | Yes | P0 |
| Syntax test | Yes | P0 |
| API endpoint test | Yes | P0 |
| Database CRUD test | Yes | P0 |
| Authentication test | Yes | P0 |
| Chatbot test | Yes | P0 |
| Integration test | Yes | P1 |
| UI test | Yes | P1 |
| Error handling test | Yes | P1 |
| Security test | Yes | P2 |

### 15.2 Test Documentation

- Record test results in IMPLEMENTATION_STATUS.md
- Mark task as COMPLETED only after testing
- Document any test failures
- Document remaining issues

---

## 16. DOCUMENTATION RULES

### 16.1 Required Documents

| Document | Purpose | Required |
|----------|---------|----------|
| PROJECT_RULES.md | Project constitution | YES |
| PROJECT_AUDIT.md | Current state analysis | YES |
| REQUIREMENTS.md | Functional requirements | YES |
| IMPLEMENTATION_PLAN.md | Development plan | YES |
| DATABASE_PLAN.md | Database design | YES |
| API_PLAN.md | API specification | YES |
| CHATBOT_PLAN.md | Chatbot architecture | YES |
| ADMIN_PLAN.md | Admin features | YES |
| UI_UX_PLAN.md | UI/UX design | YES |
| SECURITY_PLAN.md | Security measures | YES |
| TESTING_PLAN.md | Testing strategy | YES |
| ROADMAP.md | Development roadmap | YES |
| MASTER_TASK_LIST.md | Task tracking | YES |
| IMPLEMENTATION_STATUS.md | Progress tracking | YES |

### 16.2 Documentation Rules

- Do not create unnecessary documentation
- Keep documentation accurate and up-to-date
- Reference actual code, not assumptions
- Document conflicts and issues clearly

---

## 17. CHANGE CONTROL RULES

### 17.1 Minor Changes (No Approval Required)

- Bug fixes
- UI styling improvements within Streamlit
- Adding new Streamlit widgets
- Adding new API endpoints (non-architectural)
- Database schema additions
- Adding new FAQs/knowledge base entries
- Code refactoring (no architecture change)
- Documentation updates

### 17.2 Major Changes (Approval Required)

- Changing frontend framework
- Changing backend framework
- Changing programming language
- Changing database engine
- Changing NLP framework
- Changing ML framework
- Adding major external services
- Replacing project architecture
- Migrating entire application

### 17.3 Change Request Process

1. Identify the change needed
2. Check against PROJECT_RULES.md
3. If compliant: proceed with implementation
4. If conflicting: STOP and report conflict
5. Document the change request
6. Wait for explicit authorization
7. Only proceed after approval

---

## 18. FORBIDDEN TECHNOLOGIES

The following technologies are FORBIDDEN unless explicitly authorized:

### Frontend
- React / Next.js / Remix
- Vue / Nuxt.js / SvelteKit
- Angular
- Svelte
- HTML/CSS/JS as replacement frontend
- jQuery as frontend framework
- Bootstrap as primary UI framework

### Backend
- Node.js / Express.js
- FastAPI (unless explicitly authorized)
- Django
- Spring Boot
- Laravel / PHP
- ASP.NET / C#
- Go / Rust backends

### Database
- MongoDB
- PostgreSQL
- Firebase / Firestore
- Supabase
- Redis as primary database
- Cassandra
- DynamoDB

### NLP/AI
- OpenAI API as primary NLP (unless explicitly authorized)
- Google Cloud NLP as primary
- AWS Comprehend as primary
- Any paid NLP API as primary

### Other
- Docker (unless explicitly required for deployment)
- Kubernetes
- Microservices architecture
- GraphQL (use REST instead)
- WebSockets (unless explicitly required)

---

## 19. QUALITY STANDARDS

### 9.1 Code Quality

- Clean, readable code
- Consistent naming conventions
- Proper error handling
- No hardcoded values (use config)
- No debug code in production
- No unused imports/variables

### 9.2 Application Quality

- Functional (all features work)
- Stable (no crashes)
- Professional appearance
- Fast response times (< 3 seconds)
- Graceful error handling
- User-friendly interface

### 9.3 Project Quality

- Complete documentation
- All tests passing
- No known critical bugs
- Suitable for BS project demonstration
- Suitable for viva presentation

---

## 20. COMPLIANCE VERIFICATION

Before completing any task, verify:

- [ ] Technology stack compliance
- [ ] Architecture compliance
- [ ] Module compliance
- [ ] UI/UX compliance
- [ ] Backend compliance
- [ ] Database compliance
- [ ] NLP compliance
- [ ] ML compliance
- [ ] Security compliance
- [ ] Testing compliance
- [ ] Documentation compliance

---

## 21. VIOLATION REPORTING

If any code or change violates this PROJECT_RULES.md:

1. STOP implementation immediately
2. Document the violation
3. Report the violation
4. Wait for resolution
5. Do NOT proceed until compliant

**Example violation:**
```
VIOLATION DETECTED:
- Current code uses: MongoDB
- Approved technology: SQLite
- Conflict type: Database technology violation
- Action required: Report to project owner
- Status: BLOCKED until resolved
```

---

## 22. EMERGENCY CONTACT

If PROJECT_RULES.md conflicts with user instructions:

1. Follow PROJECT_RULES.md
2. Report the conflict to the user
3. Request explicit authorization
4. Do NOT silently change the architecture

---

## 23. RULES MODIFICATION

This PROJECT_RULES.md can ONLY be modified by:

1. Explicit request from project owner
2. Documented and approved change
3. Updated with version control
4. All changes logged

Do NOT modify this file:
- To make implementation easier
- Because another AI tool recommends it
- Because a technology is popular
- Because the current code is poor
- Without explicit authorization

---

## 24. FINAL RULE

> **THE PROJECT TECHNOLOGY STACK IS LOCKED.**
>
> **Python. Streamlit. Flask. NLTK. spaCy. Scikit-learn. SQLite.**
>
> **Do not change these without explicit authorization.**
>
> **A UI redesign, bug fix, feature request, or performance improvement is NOT permission to change the technology stack.**

---

**Document Version:** 1.0
**Created:** August 18, 2026
**Status:** ACTIVE — MANDATORY COMPLIANCE
