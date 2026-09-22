# COMPLETE MASTER DEVELOPMENT ROADMAP
# AI Chatbot for University Support
# FYP-Compliant Phased Development

**Status:** ACTIVE — MASTER REFERENCE  
**Created:** August 18, 2026  
**Authority:** Approved FYP Proposal + Additional Implementation Requirements  
**Rule:** Follow this roadmap ONE PHASE AT A TIME

---

## OVERVIEW

This roadmap defines the complete development sequence for the AI Chatbot for University Support. It incorporates:

1. The approved FYP proposal requirements
2. The additional Live AI / Mock Data switching requirement
3. AI provider/model configuration from Settings
4. Full compliance with the approved technology stack

---

## ARCHITECTURE TARGET

```
                    UNIVERSITY AI CHATBOT
                           │
                    ┌──────┴──────┐
                    │             │
                 LIVE AI       MOCK DATA
                    │             │
             AI Provider      Knowledge Base
                    │             │
                    └──────┬──────┘
                           │
                     Response Layer
                           │
                     NLP Processing
                    NLTK + spaCy
                           │
                    ML Processing
              Scikit-learn / TF / PyTorch
                           │
                        Flask
                           │
                    SQLite / MySQL
                           │
                       Streamlit
                           │
        ┌──────────────────┼─────────────────┐
        │                  │                 │
     Student             Faculty           Admin
        │                                    │
  Academic Help                         Knowledge Base
  Chat Assistant                        FAQ Management
  Reminders                             Chat Logs
  Chat History                          Analytics
                                        Monitoring
                                        AI Settings
```

---

## PHASE 0 — PROJECT AUDIT & BASELINE

**Status:** COMPLETED ✅

```text
Proceed to PHASE 0 — COMPLETE PROJECT AUDIT.

Before changing any code, read:
1. APPROVED_PROJECT.md (Source of Truth)
2. PROJECT_RULES.md
3. DEVELOPMENT_ROADMAP.md
4. IMPLEMENTATION_STATUS.md

The approved proposal is the source of truth.

Inspect the COMPLETE existing project.

Audit:
- Project structure
- Frontend (Streamlit pages)
- Backend (Flask routes)
- Database (SQLite schema)
- Authentication
- User management
- Chatbot
- Existing mock data
- Existing live-data functionality
- NLP (NLTK + spaCy)
- ML (Sentence Transformers + FAISS)
- Admin functionality
- Knowledge base
- Chat history
- Analytics
- Configuration/settings
- Dependencies
- Environment variables
- API integrations
- Existing errors
- Broken buttons
- Dummy functionality
- Hard-coded data
- Missing functionality

Do NOT rewrite the project yet.

Create a detailed audit report:
| Area | Existing | Working | Broken | Missing | Proposal Requirement |

Also identify:
1. What can be reused?
2. What must be fixed?
3. What must be redesigned?
4. What is missing according to the FYP proposal?
5. What currently violates the approved technology stack?
6. What existing functionality should NOT be removed?

Perform a Proposal Compliance Check.

STOP after the audit.
Do not begin implementation until the audit is complete.
```

---

## PHASE 1 — PROFESSIONAL UI/UX

**Status:** COMPLETED ✅

```text
Proceed to PHASE 1 — FRONTEND/UI/UX.

IMPORTANT:
Only work on the frontend/UI/UX in this phase.
Do NOT implement database logic.
Do NOT implement Flask APIs.
Do NOT implement NLP.
Do NOT implement ML.
Do NOT implement actual AI API calls.

The frontend MUST remain Streamlit.

Create a consistent design system for:
- Typography (Inter font family)
- Spacing
- Navigation (role-aware sidebar)
- Cards, Buttons, Forms, Tables
- Chat messages (user/assistant)
- Alerts, Loading states, Empty states, Error states

Required UI structure:
AUTHENTICATION: Login, Register
MAIN APP: Dashboard, AI Assistant, Chat History, University Info, Academic Assistance, Profile, Settings
AI ASSISTANT: Live/Mock mode switch, Chat interface, Suggested questions, New/Clear conversation
ADMIN: Dashboard, Knowledge Base, FAQ Management, Chat Logs, Analytics, Monitoring, Users, Settings
SETTINGS: AI Provider configuration fields (placeholder for now)

Create clear visual distinction: LIVE AI vs MOCK DATA
Make the UI ready for backend integration.
Test all navigation and frontend states.
Perform Proposal Compliance Check.
STOP after Phase 1.
```

---

## PHASE 2 — DATABASE

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 2 — DATABASE.

Use only the approved database: SQLite (or MySQL if authorized).

Do NOT migrate to MongoDB, PostgreSQL, Firebase, Supabase, etc.

Design the database around the approved FYP requirements.

Required tables:

USERS:
- id, name, email, password_hash, role, status, created_at

KNOWLEDGE_BASE:
- id, category, question, answer, keywords, status, created_at, updated_at

FAQ:
- id, question, answer, category, status, created_at

CONVERSATIONS:
- id, user_id, mode (live/mock), title, created_at

MESSAGES:
- id, conversation_id, sender, content, mode, timestamp

CHAT_LOGS:
- id, user_email, query, response, mode, confidence, timestamp, intent

COURSES:
- id, semester, course_code, course_name, credits, description

ACADEMIC_INFO:
- id, category, title, content, semester, created_at

REMINDERS:
- id, user_id, type (exam/assignment), title, description, due_date, created_at

AI_CONFIG:
- id, provider, model, api_key_encrypted, base_url, temperature, max_tokens, enabled, updated_at

ANALYTICS:
- id, metric_name, metric_value, recorded_at

IMPORTANT:
- Never store plaintext API keys in chat logs
- Prefer environment variables for secrets
- Do not expose API keys in the frontend
- Use parameterized queries (prevent SQL injection)

Test the database thoroughly.
Perform Proposal Compliance Check.
STOP after Phase 2.
```

---

## PHASE 3 — FLASK BACKEND

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 3 — BACKEND.

Approved backend: Python + Flask.
Do not introduce Node.js/Express/FastAPI/Django.

Build/fix Flask APIs required by the approved project.

API areas:

AUTH:
- POST /api/register
- POST /api/login
- POST /api/logout
- GET /api/profile

USERS:
- GET /api/admin/users
- PUT /api/admin/users/<id>
- DELETE /api/admin/users/<id>

KNOWLEDGE BASE:
- GET /api/knowledge
- POST /api/knowledge
- PUT /api/knowledge/<id>
- DELETE /api/knowledge/<id>
- GET /api/knowledge/search

FAQ:
- GET /api/faqs
- POST /api/faqs
- PUT /api/faqs/<id>
- DELETE /api/faqs/<id>

CHAT:
- POST /api/chat (with mode parameter)
- GET /api/conversations
- POST /api/conversations
- GET /api/conversations/<id>/messages

AI CONFIG:
- GET /api/settings/ai
- PUT /api/settings/ai
- POST /api/settings/ai/test

ACADEMIC:
- GET /api/courses
- GET /api/reminders

ADMIN:
- GET /api/admin/analytics
- GET /api/admin/chat-logs
- GET /api/admin/monitoring

Implement proper:
- Validation
- Error handling
- Authentication
- Authorization
- Logging

Test all APIs.
Perform Proposal Compliance Check.
STOP after Phase 3.
```

---

## PHASE 4 — AUTHENTICATION & ROLE MANAGEMENT

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 4 — AUTHENTICATION & USER MANAGEMENT.

Implement the approved optional authentication system.

Roles:
1. Student
2. Faculty
3. Admin

Implement:
- Registration with role selection
- Login with session management
- Logout
- Secure password hashing (bcrypt)
- Protected pages
- Role-based authorization
- Profile management
- Account status

Students should not access Admin functionality.
Faculty should only access approved faculty functionality.
Admins should have full administrative functionality.

Connect: Streamlit → Flask → Database

Test all authentication scenarios.
Perform Proposal Compliance Check.
STOP after Phase 4.
```

---

## PHASE 5 — KNOWLEDGE BASE

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 5 — KNOWLEDGE BASE.

Implement the proposal's Knowledge Base Module.

The system must store university information including:
- Courses
- Rules
- Schedules
- FAQs
- Admissions
- Course registration
- Examination information
- Fee structure
- Academic policies
- University services

Admin must be able to:
- Add knowledge entries
- Edit knowledge entries
- Delete knowledge entries
- Search knowledge
- Filter by category
- Enable/disable entries
- Update knowledge dynamically

Connect: Admin UI → Flask → Database

Do not rely on permanent hard-coded answers.
Do not invent official university information.

Seed initial university data for demonstration.

Perform Proposal Compliance Check.
STOP after Phase 5.
```

---

## PHASE 6 — MOCK DATA MODE

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 6 — MOCK DATA MODE.

Implement a completely functional MOCK DATA mode.

The user must be able to switch to MOCK DATA from the AI Assistant interface.

The mode switch must be obvious:
[ LIVE AI ] [ MOCK DATA ]

When MOCK DATA is selected:
User → Streamlit → Flask → Knowledge Base → Matching/Retrieval → Response → Streamlit

The response must come from the configured project knowledge/mock data.
Do NOT call the Live AI provider while MOCK DATA mode is active.
Do NOT mix Live AI responses with Mock Data responses.

Display clear indicator: "Mock Data Mode"

Test:
- Known questions (should get answers from knowledge base)
- Different categories (admissions, fees, courses, etc.)
- Unknown questions (should get fallback response)
- Empty queries
- Multiple conversations
- Chat history
- Admin knowledge updates (should reflect in responses)

When admin changes knowledge, Mock Data responses should reflect updates.

Perform Proposal Compliance Check.
STOP after Phase 6.
```

---

## PHASE 7 — LIVE AI MODE

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 7 — LIVE AI MODE.

Implement the LIVE AI functionality.

The user must be able to switch between LIVE AI and MOCK DATA without leaving the chatbot.

When LIVE AI is selected:
User → Streamlit → Flask → Configured AI Provider → AI Response → Streamlit

The Live AI mode must be clearly labelled.

IMPORTANT:
The FYP proposal does not mandate one specific AI provider.
Therefore, implement provider/model configuration instead of hard-coding one provider.

The Settings area should allow authorized users/admins to configure:
- AI Provider (e.g., OpenAI, Anthropic, local model, etc.)
- Model name
- API Key (securely stored)
- Base URL/Endpoint if supported
- Temperature if supported
- Output token limit if supported
- Enable/disable provider

The architecture should be provider-configurable.

Security rules:
- Never display full saved API keys
- Never put keys in logs
- Never put keys in chat messages
- Use secure environment/secrets storage
- Do not expose keys to the frontend after saving

If no Live AI provider is configured, show:
"Live AI is not configured. Please configure an AI provider in Settings."
Do not crash.

Do not call Live AI when Mock Data mode is selected.

Perform Proposal Compliance Check.
STOP after Phase 7.
```

---

## PHASE 8 — LIVE/MOCK SWITCHING & CHAT ROUTER

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 8 — CHAT MODE ROUTING.

Create a reliable central routing mechanism for LIVE AI and MOCK DATA.

The selected mode must be stored with the conversation/message.
Every request must explicitly contain the selected mode.

Rules:
IF mode = MOCK:
    Use Knowledge Base / Mock Data.
    Do NOT call external Live AI.

IF mode = LIVE:
    Use configured Live AI provider.
    Do NOT silently fall back to Mock Data unless user explicitly chooses Mock Data.

The UI must show the current mode at all times.

Chat history must show whether a conversation was:
- Live AI
- Mock Data

Admin logs must also record the mode.

Test switching:
- Mock → Live
- Live → Mock
- Mock → Mock
- Live → Live

Make sure responses never cross modes.

Perform Proposal Compliance Check.
STOP after Phase 8.
```

---

## PHASE 9 — NLP PROCESSING

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 9 — NLP PROCESSING.

Use the approved NLP libraries:
- NLTK
- spaCy

Implement where appropriate:
- Text preprocessing (tokenization, normalization)
- Intent detection
- Entity extraction
- Query understanding

The NLP layer should help understand university queries:
- Admissions
- Course registration
- Examination schedules
- Fee structure
- Academic policies
- University services
- Course guidance

Connect NLP with the chatbot architecture.

Do not replace NLTK/spaCy with another NLP framework.

Test representative queries.

Perform Proposal Compliance Check.
STOP after Phase 9.
```

---

## PHASE 10 — MACHINE LEARNING

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 10 — MACHINE LEARNING.

Use approved ML technologies:
- Scikit-learn
- TensorFlow / PyTorch where required

Implement the Machine Learning Model Module from the proposal.

The system should be capable of training on historical queries/responses.

Implement:
- Dataset preparation
- Training pipeline
- Validation/testing
- Evaluation metrics
- Model saving/loading
- Prediction

Do not create unnecessary ML features.
Do not claim the model "improves over time" unless the retraining mechanism exists.

Perform Proposal Compliance Check.
STOP after Phase 10.
```

---

## PHASE 11 — RESPONSE GENERATION

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 11 — RESPONSE GENERATION.

Implement the complete response pipeline:

User Query → NLP → Intent Detection → Entity Extraction →
Knowledge Base / ML / Live AI (according to selected mode) →
Response Generation → User-Friendly Response

Responses should be:
- Meaningful
- Clear
- Relevant
- University-focused

If information is unavailable:
- Do not invent university facts
- Return appropriate fallback response

Test multiple query categories.

Perform Proposal Compliance Check.
STOP after Phase 11.
```

---

## PHASE 12 — ADMIN DASHBOARD

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 12 — ADMIN DASHBOARD.

Implement the approved Admin Dashboard Module.

Admin must be able to:
- Manage FAQs (CRUD)
- Manage chatbot responses
- Update system knowledge
- Manage Knowledge Base (CRUD)
- View chat logs
- View users where permitted
- View analytics
- Monitor system performance

Include AI configuration settings for authorized administrators:
- Provider selection
- Model configuration
- API configuration
- Enable/disable Live AI

Never display saved API secrets.
Use masked configuration indicators (e.g., ••••••••).

Perform Proposal Compliance Check.
STOP after Phase 12.
```

---

## PHASE 13 — STUDENT ACADEMIC ASSISTANCE

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 13 — STUDENT ACADEMIC ASSISTANCE.

Implement ONLY the features documented in the FYP:
1. Course guidance based on semester
2. Exam reminders
3. Assignment reminders

The UI should provide clear access to these features.
Connect them to the approved backend/database.

Do not invent unrelated student-management features.

Perform Proposal Compliance Check.
STOP after Phase 13.
```

---

## PHASE 14 — ADMIN ANALYTICS & MONITORING

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 14 — ADMIN ANALYTICS & MONITORING.

Implement the proposal's:
- Chat usage statistics
- Most frequent student issues
- System performance monitoring

Where useful, distinguish:
- Live AI usage
- Mock Data usage
- Query categories
- Response/error statistics

Only display data that actually exists.
Do not fabricate statistics.

Use Streamlit for visualization.

Perform Proposal Compliance Check.
STOP after Phase 14.
```

---

## PHASE 15 — CHAT HISTORY & LOGGING

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 15 — CHAT HISTORY & LOGGING.

Implement persistent chat history.

Users should be able to:
- View conversations
- Continue conversations
- Start new conversations
- Clear/delete conversations

Every conversation should preserve its mode: LIVE AI or MOCK DATA.

Admin logs should capture:
- User
- Query
- Response
- Mode
- Timestamp
- Status
- Performance information

IMPORTANT:
Never log API keys, passwords, or secrets.

Perform Proposal Compliance Check.
STOP after Phase 15.
```

---

## PHASE 16 — SETTINGS & CONFIGURATION

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 16 — SETTINGS & CONFIGURATION.

Create a professional Settings system.

Settings sections:

GENERAL:
- Application preferences
- User preferences

AI/LIVE MODEL:
- Provider: [ Dropdown ]
- Model: [ Text input ]
- API Key: [ Password field ] (masked after save)
- Base URL: [ Optional text field ]
- Temperature: [ Slider 0.0 - 2.0 ]
- Max Output Tokens: [ Number input ]
- Live AI: [ Enable/Disable toggle ]
- [ Test Connection ] button
- [ Save Configuration ] button

CHAT:
- Default mode (Live/Mock)
- Chat preferences

ADMIN:
- System configuration
- Knowledge configuration
- Monitoring configuration

SECURITY RULES:
- API keys are secrets
- Never display full saved API keys
- Never put keys in logs
- Never put keys in database records as plain text where avoidable
- Never send keys to the frontend unnecessarily
- Never commit keys to Git
- Use secure environment variables/secrets storage

When configuring a provider:
- Test connection
- Save configuration
- Validate settings
- Clear error messages

If configuration is missing:
Show: "Live AI is not configured. Please configure an AI provider in Settings."
Do not crash.

Perform Proposal Compliance Check.
STOP after Phase 16.
```

---

## PHASE 17 — FULL INTEGRATION

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 17 — FULL SYSTEM INTEGRATION.

Connect:
Streamlit → Flask → Database → Authentication → Knowledge Base →
Mock Data Engine → Live AI Provider → NLP → ML → Response Generation →
Analytics → Chat History

Verify complete user journeys:

STUDENT:
Register → Login → Dashboard → Choose Live/Mock → Ask question →
Receive response → View history → Academic assistance → Reminders

ADMIN:
Login → Dashboard → Knowledge Base → FAQs → Chat Logs →
Analytics → Monitoring → AI Settings

Test switching:
- LIVE → MOCK
- MOCK → LIVE

Ensure the selected mode is never confused.

Perform Proposal Compliance Check.
STOP after Phase 17.
```

---

## PHASE 18 — COMPLETE TESTING

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 18 — COMPLETE SYSTEM TESTING.

Test the complete application.

TEST AUTHENTICATION:
- Register, Login, Logout
- Wrong credentials, Duplicate users
- Role access (Student, Faculty, Admin)

TEST UI:
- Navigation, Forms, Chat, Settings, Dashboard, Admin

TEST MOCK DATA:
- Known query, Unknown query
- Knowledge update, Mode switching

TEST LIVE AI:
- Provider configuration
- API key validation
- Model selection
- Successful query
- Invalid key, Missing configuration, Provider error

TEST MODE SWITCHING:
- Live → Mock, Mock → Live
- History mode, Logs mode

TEST NLP:
- Intent detection, Entity extraction, Query processing

TEST ML:
- Training, Prediction, Evaluation, Model loading

TEST DATABASE:
- CRUD, Relationships, Persistence

TEST BACKEND:
- APIs, Authentication, Validation, Error handling

TEST ADMIN:
- Knowledge, FAQs, Logs, Analytics, Monitoring, Settings

Fix all discovered bugs.
Do not add unrelated features.

Perform Proposal Compliance Check.
STOP after Phase 18.
```

---

## PHASE 19 — FINAL FYP COMPLIANCE AUDIT

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 19 — FINAL FYP COMPLIANCE AUDIT.

Read APPROVED_PROJECT.md completely.

Compare the FINAL IMPLEMENTATION against EVERY requirement.

Create a compliance table:
| Proposal Requirement | Implemented? | Location | Technology | Tested? | Compliant? |

Check ALL:

PROJECT:
- AI Chatbot for University Support ✅

DOMAIN:
- AI, NLP, EdTech ✅

PURPOSE:
- Academic/administrative assistance ✅
- Reduce help-desk workload ✅
- Centralize university knowledge ✅

SCOPE:
- Instant university responses ✅
- Multiple users ✅
- 24/7 operation ✅

MODULES (all 7):
- User Interface ✅
- Authentication/User Management ✅
- NLP Processing ✅
- Knowledge Base ✅
- Machine Learning Model ✅
- Response Generation ✅
- Admin Dashboard ✅

TECHNOLOGY:
- Python ✅
- Streamlit ✅
- Flask ✅
- NLTK ✅
- spaCy ✅
- Scikit-learn ✅
- TensorFlow/PyTorch (if used) ✅
- SQLite/MySQL ✅

UNIQUE FEATURE:
- Automated University Support & Query Resolution ✅

SUPPORTED AREAS:
- Admissions, Course registration, Examination schedules ✅
- Fee structure, Academic policies, University services ✅

STUDENT FEATURES:
- Semester-based course guidance ✅
- Exam reminders ✅
- Assignment reminders ✅

ADMIN:
- Chat usage statistics ✅
- Most frequent student issues ✅
- System performance monitoring ✅
- FAQ management ✅
- Chat logs ✅
- Knowledge updates ✅

ADDITIONAL REQUIREMENTS:
- Clearly separated Live AI and Mock Data modes ✅
- User can switch between modes ✅
- Live AI configuration through Settings ✅
- Configurable provider/model/API key ✅
- Secure secret handling ✅
- No mixing between Live and Mock responses ✅

If anything is missing or non-compliant:
DO NOT mark the project as complete.
Report the exact problem and fix it.

Final result must be: COMPLIANT
```

---

## PHASE 20 — FINAL DOCUMENTATION & POLISH

**Status:** NOT STARTED ⬜

```text
Proceed to PHASE 20 — FINAL DOCUMENTATION & POLISH.

Create/update:
- README.md (comprehensive project documentation)
- API documentation
- Database schema documentation
- User guide
- Admin guide
- Deployment guide

Final UI polish:
- Consistent styling
- Responsive layout
- Professional appearance
- Loading states
- Error states
- Empty states

Performance optimization:
- Database query optimization
- API response times
- Frontend rendering

Final testing pass.

Prepare for FYP demonstration.

STOP after Phase 20.
```

---

## COMPLIANCE CHECKPOINTS

After EVERY phase, perform:

1. **Technology Compliance** — Still using approved stack?
2. **Module Compliance** — All required modules progressing?
3. **Proposal Compliance** — Meeting FYP requirements?
4. **Security Compliance** — No secrets exposed?
5. **Quality Compliance** — Code is clean and tested?

If any check fails, STOP and fix before proceeding.

---

## CURRENT STATUS

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0 — Audit | ✅ COMPLETED | Audit report created |
| Phase 1 — UI/UX | ✅ COMPLETED | Professional UI implemented |
| Phase 2 — Database | ⬜ NOT STARTED | Next phase |
| Phase 3 — Backend | ⬜ NOT STARTED | |
| Phase 4 — Auth | ⬜ NOT STARTED | |
| Phase 5 — Knowledge Base | ⬜ NOT STARTED | |
| Phase 6 — Mock Data | ⬜ NOT STARTED | |
| Phase 7 — Live AI | ⬜ NOT STARTED | |
| Phase 8 — Mode Router | ⬜ NOT STARTED | |
| Phase 9 — NLP | ⬜ NOT STARTED | |
| Phase 10 — ML | ⬜ NOT STARTED | |
| Phase 11 — Response Gen | ⬜ NOT STARTED | |
| Phase 12 — Admin Dashboard | ⬜ NOT STARTED | |
| Phase 13 — Academic | ⬜ NOT STARTED | |
| Phase 14 — Analytics | ⬜ NOT STARTED | |
| Phase 15 — Chat History | ⬜ NOT STARTED | |
| Phase 16 — Settings | ⬜ NOT STARTED | |
| Phase 17 — Integration | ⬜ NOT STARTED | |
| Phase 18 — Testing | ⬜ NOT STARTED | |
| Phase 19 — Final Audit | ⬜ NOT STARTED | |
| Phase 20 — Documentation | ⬜ NOT STARTED | |

**Next Action:** Proceed to Phase 2 — Database

---

**Document Version:** 1.0  
**Created:** August 18, 2026  
**Status:** ACTIVE — MASTER REFERENCE
