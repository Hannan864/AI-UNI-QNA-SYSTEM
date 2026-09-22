# PROJECT MASTER CONSTITUTION

# AI CHATBOT FOR UNIVERSITY SUPPORT

**Purpose:** This document is the permanent project reference,
scope-control document, and technology/functionality compliance rulebook
for the Final Year Project.

------------------------------------------------------------------------

# PART 1 --- MASTER PROJECT RULES

## 1. SOURCE OF TRUTH

The approved Final Year Project Proposal included in **Part 2** of this
file is the **single source of truth** for the project's:

-   Purpose
-   Domain
-   Scope
-   Modules
-   Features
-   Frontend
-   Backend
-   NLP libraries
-   ML libraries
-   Database
-   Programming language
-   Unique feature
-   Functional requirements

The AI/developer must compare every implementation task against this
document before making changes.

## 2. EXACT PROJECT RULE

The objective is to build the **same project described in the approved
proposal**, not a different or expanded project.

Allowed:

-   Fixing broken functionality
-   Completing missing functionality explicitly described in the
    proposal
-   Improving UI/UX while keeping Streamlit
-   Connecting existing modules
-   Implementing the documented database/backend
-   Improving reliability, security, validation, and error handling
-   Adding implementation details required to make an explicitly
    documented feature work

Not allowed without explicit project-owner approval:

-   Changing the project domain
-   Replacing the approved technology stack
-   Removing approved modules
-   Turning the project into a generic AI chatbot
-   Adding unrelated major features
-   Introducing a different architecture just because it is easier
-   Adding technologies that contradict the proposal

## 3. TECHNOLOGY LOCK

The following stack is locked by the proposal:

  Area                   Approved Technology
  ---------------------- -------------------------------------
  Programming Language   Python
  Frontend               Streamlit
  Backend                Core Python + Flask
  NLP                    NLTK + spaCy
  ML                     Scikit-learn + TensorFlow / PyTorch
  Database               SQLite / MySQL

### Forbidden automatic replacements

Do not replace:

-   Python with JavaScript, TypeScript, Java, PHP, C#, etc.
-   Streamlit with React, Next.js, Vue, Angular, etc.
-   Flask with Node.js, Express.js, FastAPI, Django, etc.
-   SQLite/MySQL with MongoDB, PostgreSQL, Firebase, Supabase, etc.

If a technology conflict is found in the existing project, report it
first. Do not silently migrate the project.

## 4. DOCUMENT COMPLIANCE CHECK --- MANDATORY

Before implementing **any task**, the AI must answer internally and
record where appropriate:

1.  What requirement in the approved proposal does this task implement
    or support?
2.  Which approved module does it belong to?
3.  Which approved technology is being used?
4.  Does it change the project scope?
5.  Does it introduce a new technology?
6.  Does it introduce an unapproved feature?
7.  Does it remove or alter an approved feature?
8.  Does the implementation remain consistent with the proposal?

If the answer to #4, #5, or #6 indicates a scope/technology change, the
AI must **STOP and request approval** instead of silently proceeding.

## 5. BEFORE / AFTER COMPARISON RULE

For every completed task, the AI must perform a proposal-compliance
check.

Use this format:

### Proposal Compliance Check

**Task:**\
\[What was implemented\]

**Related Proposal Requirement:**\
\[Exact module/feature/technology from this document\]

**Implementation:**\
\[What was actually changed\]

**Technology Used:**\
\[Actual technology\]

**Scope Status:**\
PASS / WARNING / FAIL

**Technology Status:**\
PASS / WARNING / FAIL

**Feature Status:**\
PASS / WARNING / FAIL

**Unapproved Additions:**\
None / \[list\]

**Removed or Changed Approved Requirements:**\
None / \[list\]

**Final Verdict:**\
COMPLIANT / NEEDS REVIEW / NON-COMPLIANT

A task must not be marked complete if it is NON-COMPLIANT.

## 6. FINAL PROJECT AUDIT RULE

At the end of every major phase, compare the implementation against the
complete approved proposal.

The AI must verify:

-   Project title
-   Project purpose
-   Domain
-   Scope
-   Modules
-   Features
-   Frontend
-   Backend
-   NLP
-   ML
-   Database
-   Programming language
-   Unique feature

The AI must report any mismatch.

## 7. NO UNAUTHORIZED ADDITIONS

A small implementation detail may be added if it is necessary to make an
approved feature work.

Examples:

-   Form validation
-   Error messages
-   Loading states
-   Authentication session handling
-   Database constraints
-   API validation
-   UI navigation needed for an approved module

However, a new major product capability that is not in the proposal must
not be added automatically.

## 8. UI/UX RULE

The UI may be redesigned and improved substantially, but the frontend
technology must remain **Streamlit**.

The AI should make the application:

-   Professional
-   Clean
-   Modern
-   Consistent
-   Academic/EdTech appropriate
-   Easy to navigate
-   Functional

UI improvements must serve the documented project.

Do not use a UI redesign as an excuse to migrate to React or another
framework.

## 9. DEVELOPMENT ORDER

Build the project progressively:

1.  Project inspection
2.  Proposal/rules compliance setup
3.  Frontend/UI/UX
4.  Database
5.  Backend/Flask
6.  Authentication & user management
7.  Knowledge Base
8.  Mock-data functionality where required for development/testing
9.  Chatbot/response generation
10. NLP
11. Machine Learning
12. Admin Dashboard
13. Student Academic Assistance
14. Exam/assignment reminders
15. Admin Analytics & Monitoring
16. Full integration
17. Testing
18. Final compliance audit

Do not randomly jump between phases.

## 10. NO FAKE COMPLETION

A feature is not complete if:

-   It is only a visual button
-   It does not perform its intended function
-   It uses hard-coded data when real database functionality is required
-   The backend is missing
-   The database connection is missing
-   It has not been tested
-   It contradicts the proposal

Use labels such as `DEMO`, `MOCK`, `PENDING`, or `NOT IMPLEMENTED` where
appropriate.

## 11. PROJECT RULE FILE

This document should be retained as the project's master reference.

If a separate `PROJECT_RULES.md` is created in the codebase, it must
remain consistent with this document.

The AI must read and follow the rules before modifying the project.

------------------------------------------------------------------------

# PART 2 --- APPROVED FINAL YEAR PROJECT PROPOSAL

# ORIGINAL PROJECT DOCUMENT

## FINAL YEAR PROJECT PROPOSAL

### PROJECT TITLE

**AI CHATBOT FOR UNIVERSITY SUPPORT**

### SUBMITTED BY

**ASHARIB KHAN & KASHIF FAROOQ**

**909-FOC/BSIT/F22-(B) & 899-FOC/BSIT/F-22(B)**

------------------------------------------------------------------------

# INTRODUCTION

With the rapid growth of Artificial Intelligence, universities are
increasingly adopting intelligent systems to improve student support
services.

Students frequently face difficulties in getting timely information
regarding admissions, course registration, examinations, timetables,
fees, scholarships, and academic policies.

The AI chatbot for university support is designed to provide 24/7
automated assistance to students, faculty, and administrative staff.

------------------------------------------------------------------------

# PROJECT DOMAIN

-   Artificial Intelligence (AI)
-   Natural Language Processing (NLP)
-   Educational Technology (EdTech)

------------------------------------------------------------------------

# PURPOSE OF THE PROJECT

-   To assist students with academic and administrative information
-   To reduce workload on university help desks
-   To centralize university knowledge in one intelligent system

------------------------------------------------------------------------

# SCOPE OF THE PROJECT

-   Providing instant responses to common university-related queries
-   Supporting multiple users simultaneously
-   Operating 24/7 without human intervention

------------------------------------------------------------------------

# MODULES OF THIS PROJECT

## User Interface Module

Allows users to interact with the chatbot.

-   Text-based chat interface
-   Displays chatbot responses clearly

## Authentication & User Management Module

-   Optional login for students and staff
-   Role-based access (student, faculty, admin)

## NLP Processing Module

-   Intent detection and entity extraction
-   Converts user queries into machine-understandable form

## Knowledge Base Module

-   Stores university-related data (courses, rules, schedules, FAQs)
-   Can be updated dynamically by admin

## Machine Learning Model Module

-   Trains on historical queries and responses
-   Improves accuracy over time

## Response Generation Module

-   Matches user intent with best possible response
-   Generates meaningful and user-friendly replies

## Admin Dashboard Module

-   Manage FAQs and chatbot responses
-   View chat logs and update system knowledge

------------------------------------------------------------------------

# FRONT-END

The frontend is implemented using **Python-based frameworks**:

## Streamlit

-   Provides interactive input forms
-   Displays predictions, graphs, and recommendations

------------------------------------------------------------------------

# BACK-END

The backend is implemented using **core Python** and **FLASK**.

## NLP Libraries

-   NLTK
-   spaCy

## ML Libraries

-   Scikit-learn
-   TensorFlow / PyTorch

------------------------------------------------------------------------

# DATABASE

**SQLite/MySQL** for database management.

------------------------------------------------------------------------

# PROGRAMMING LANGUAGES

The language which was used in this project is:

**Python**

------------------------------------------------------------------------

# UNIQUE FEATURE

**Automated University Support & Query Resolution**

The chatbot automatically understands and responds to user queries
related to:

-   Admissions
-   Course registration
-   Examination schedules
-   Fee structure
-   Academic policies
-   University services

------------------------------------------------------------------------

# FEATURES / FUNCTIONALITIES

## Student Academic Assistance

-   Course guidance based on semester
-   Exam and assignment reminders

## Admin Analytics & Monitoring

-   Chat usage statistics
-   Most frequent student issues
-   System performance monitoring

------------------------------------------------------------------------

# PART 3 --- FEATURE TRACEABILITY MATRIX

Every implementation must be traceable to the approved proposal.

  -----------------------------------------------------------------------
  Proposal Requirement    Expected Implementation Status
                          Area                    
  ----------------------- ----------------------- -----------------------
  AI Chatbot for          Main application        NOT STARTED
  University Support                              

  AI / NLP / EdTech       Overall architecture    NOT STARTED
  domain                                          

  Instant university      Chatbot / Response      NOT STARTED
  query responses         Generation              

  Multiple users          Authentication/User     NOT STARTED
                          Management              

  24/7 assistance         Application             NOT STARTED
                          availability            

  Text-based chat         Streamlit UI            NOT STARTED

  Clear chatbot responses Response Generation/UI  NOT STARTED

  Optional login          Authentication          NOT STARTED

  Student/Faculty/Admin   User Management         NOT STARTED
  roles                                           

  Intent detection        NLP                     NOT STARTED

  Entity extraction       NLP                     NOT STARTED

  University knowledge    Knowledge Base          NOT STARTED
  base                                            

  Dynamic admin updates   Knowledge Base/Admin    NOT STARTED

  Historical              ML Model                NOT STARTED
  queries/responses                               

  Accuracy improvement    ML Model                NOT STARTED

  Intent-to-response      Response Generation     NOT STARTED
  matching                                        

  Meaningful replies      Response Generation     NOT STARTED

  FAQ management          Admin Dashboard         NOT STARTED

  Chat log viewing        Admin Dashboard         NOT STARTED

  System knowledge        Admin Dashboard         NOT STARTED
  updates                                         

  Streamlit frontend      Frontend                NOT STARTED

  Flask backend           Backend                 NOT STARTED

  NLTK                    NLP                     NOT STARTED

  spaCy                   NLP                     NOT STARTED

  Scikit-learn            ML                      NOT STARTED

  TensorFlow/PyTorch      ML where required       NOT STARTED

  SQLite/MySQL            Database                NOT STARTED

  Python                  Programming language    NOT STARTED

  Automated university    Core chatbot            NOT STARTED
  query resolution                                

  Admissions queries      Knowledge/Chatbot       NOT STARTED

  Course registration     Knowledge/Chatbot       NOT STARTED
  queries                                         

  Examination schedule    Knowledge/Chatbot       NOT STARTED
  queries                                         

  Fee structure queries   Knowledge/Chatbot       NOT STARTED

  Academic policy queries Knowledge/Chatbot       NOT STARTED

  University services     Knowledge/Chatbot       NOT STARTED
  queries                                         

  Semester-based course   Student Academic        NOT STARTED
  guidance                Assistance              

  Exam reminders          Student Academic        NOT STARTED
                          Assistance              

  Assignment reminders    Student Academic        NOT STARTED
                          Assistance              

  Chat usage statistics   Admin Analytics         NOT STARTED

  Most frequent student   Admin Analytics         NOT STARTED
  issues                                          

  System performance      Admin Monitoring        NOT STARTED
  monitoring                                      
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# PART 4 --- MASTER AI OPERATING RULE

Whenever a developer/user gives you a task, follow this sequence:

### STEP A --- UNDERSTAND THE TASK

Explain briefly what the task is asking for.

### STEP B --- MAP IT TO THE PROPOSAL

Identify the exact proposal section/module/feature that the task belongs
to.

### STEP C --- CHECK TECHNOLOGY

Confirm that the implementation uses the approved stack:

-   Python
-   Streamlit
-   Flask
-   NLTK
-   spaCy
-   Scikit-learn
-   TensorFlow/PyTorch
-   SQLite/MySQL

as applicable.

### STEP D --- CHECK SCOPE

Confirm that the task does not create a different project.

### STEP E --- IMPLEMENT

Only after the compliance check, implement the task.

### STEP F --- TEST

Actually test the result.

### STEP G --- COMPARE

Compare the completed work against the proposal.

### STEP H --- REPORT

Report:

-   What was implemented
-   Which proposal requirement it satisfies
-   What technology was used
-   What was tested
-   Whether any unapproved change was made
-   Final compliance status

------------------------------------------------------------------------

# PART 5 --- NON-COMPLIANCE HANDLING

If a requested task conflicts with this document:

DO NOT silently implement it.

Instead respond:

> "This request conflicts with the approved Final Year Project Proposal
> because \[reason\]. The approved requirement is \[requirement\]. I
> will not change the project scope or technology stack without explicit
> authorization."

Then provide the closest compliant alternative.

------------------------------------------------------------------------

# PART 6 --- FINAL ACCEPTANCE CRITERIA

The project can only be considered final when:

1.  All approved modules are implemented.
2.  All approved features/functions are implemented.
3.  The application uses the approved technology stack.
4.  The frontend remains Streamlit.
5.  The backend remains Python + Flask.
6.  NLP uses NLTK/spaCy as required.
7.  ML uses Scikit-learn and TensorFlow/PyTorch where required.
8.  Database remains SQLite/MySQL.
9.  The application remains an AI Chatbot for University Support.
10. The proposal traceability matrix has been reviewed.
11. All major functionality has been tested.
12. No unexplained scope changes remain.
13. No unauthorized technology replacements remain.
14. The final implementation has passed the proposal compliance audit.

------------------------------------------------------------------------

# FINAL COMMAND TO THE AI

Before every task:

**CHECK THE PROPOSAL.**

During every task:

**FOLLOW THE PROPOSAL.**

After every task:

**COMPARE THE IMPLEMENTATION WITH THE PROPOSAL.**

Before every major phase:

**AUDIT THE PROJECT AGAINST THE PROPOSAL.**

Before final delivery:

**PERFORM A COMPLETE PROPOSAL COMPLIANCE AUDIT.**

The goal is not to build a similar project.

The goal is to build the project defined by the approved proposal, with
its approved technologies, modules, features, and purpose, while fixing
and completing the existing implementation.
