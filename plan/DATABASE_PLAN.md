# Database Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Current Database Structure

### Database Files

| File | Purpose | Size |
|------|---------|------|
| `database/iiui_data.db` | Main database | 32KB |
| `logs/chat_logs.db` | Chat logs | 20KB |

### Existing Tables

#### Table: `faqs`
```sql
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    tags TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Status:** ✅ Exists  
**Data:** 2 records (from init_db.py)

#### Table: `contacts`
```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    person TEXT,
    email TEXT,
    phone TEXT,
    office_location TEXT,
    office_hours TEXT
)
```
**Status:** ✅ Exists  
**Data:** 0 records (empty)

#### Table: `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    role TEXT DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Status:** ✅ Exists  
**Data:** 1 record (admin)

#### Table: `chat_logs`
```sql
CREATE TABLE chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    confidence REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    intent TEXT
)
```
**Status:** ✅ Exists  
**Data:** 0 records

---

## 2. Missing Tables

### Table: `sessions`
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_email) REFERENCES users(email)
)
```
**Purpose:** Persistent session storage  
**Priority:** P1

### Table: `faq_categories`
```sql
CREATE TABLE faq_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Purpose:** Organize FAQs by category  
**Priority:** P2

### Table: `knowledge_base`
```sql
CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    tags TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Purpose:** Store detailed knowledge beyond FAQs  
**Priority:** P1

### Table: `analytics`
```sql
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    event_data TEXT,
    user_email TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Purpose:** Track user interactions  
**Priority:** P2

---

## 3. Required Changes to Existing Tables

### 3.1 `faqs` Table
**Add columns:**
```sql
ALTER TABLE faqs ADD COLUMN is_active BOOLEAN DEFAULT 1;
ALTER TABLE faqs ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE faqs ADD COLUMN created_by TEXT;
```

### 3.2 `users` Table
**Add columns:**
```sql
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ADD COLUMN department TEXT;
```

### 3.3 `contacts` Table
**Add columns:**
```sql
ALTER TABLE contacts ADD COLUMN is_active BOOLEAN DEFAULT 1;
ALTER TABLE contacts ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

---

## 4. Indexes for Performance

```sql
-- FAQs indexes
CREATE INDEX idx_faqs_category ON faqs(category);
CREATE INDEX idx_faqs_tags ON faqs(tags);
CREATE INDEX idx_faqs_active ON faqs(is_active);

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- Chat logs indexes
CREATE INDEX idx_chat_logs_user ON chat_logs(user_email);
CREATE INDEX idx_chat_logs_timestamp ON chat_logs(timestamp);
CREATE INDEX idx_chat_logs_intent ON chat_logs(intent);

-- Sessions indexes
CREATE INDEX idx_sessions_user ON sessions(user_email);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);
```

---

## 5. Sample Data Requirements

### 5.1 FAQs (100+ records)

**Categories:**
1. Admissions (15+ FAQs)
2. Fees (10+ FAQs)
3. Academic Programs (15+ FAQs)
4. Examinations (10+ FAQs)
5. Campus Life (10+ FAQs)
6. Facilities (10+ FAQs)
7. Contact Information (10+ FAQs)
8. Policies (10+ FAQs)
9. General (10+ FAQs)

**Sample FAQ Structure:**
```json
{
    "question": "What is the admission process at IIUI?",
    "answer": "IIUI admissions require: 1) Online application submission, 2) Entry test, 3) Interview. Weightage: 40% Entry Test, 40% Academic Qualification, 20% Interview.",
    "tags": "admission,application,process",
    "category": "Admissions"
}
```

### 5.2 Contacts (20+ records)

**Departments:**
1. Admissions Office
2. Registrar Office
3. Finance Office
4. IT Department
5. Student Affairs
6. Library
7. Hostel Administration
8. Examination Department
9. Academic Affairs
10. HR Department

**Sample Contact Structure:**
```json
{
    "department": "Admissions Office",
    "person": "Mr. Ahmad Khan",
    "email": "admissions@iiu.edu.pk",
    "phone": "+92-51-9011000",
    "office_location": "Admin Block, Room 101",
    "office_hours": "Monday-Friday, 9:00 AM - 4:00 PM"
}
```

### 5.3 Fee Structure

**Programs:**
1. BS Computer Science
2. BS Software Engineering
3. BS Data Science
4. BBA
5. MBA
6. B.Ed
7. MA English
8. BS Psychology
9. LLB
10. MBBS

---

## 6. Database Relationships

```
users (1) ──── (many) chat_logs
users (1) ──── (many) sessions
faqs (1) ──── (many) chat_logs (via intent/category)
```

**Note:** Currently no foreign key constraints defined. Should add for data integrity.

---

## 7. Improved Database Design

### Recommended Schema

```sql
-- Users table with full profile
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'student' CHECK(role IN ('student', 'admin')),
    phone TEXT,
    department TEXT,
    student_id TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Sessions table for persistence
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Enhanced FAQs
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category_id INTEGER,
    tags TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES faq_categories(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- FAQ Categories
CREATE TABLE faq_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    icon TEXT,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge Base
CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    tags TEXT,
    source TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Contacts
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    person TEXT,
    email TEXT,
    phone TEXT,
    office_location TEXT,
    office_hours TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Logs
CREATE TABLE chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_id TEXT,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    confidence REAL,
    intent TEXT,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Analytics
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    event_data TEXT,
    user_id INTEGER,
    session_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 8. Migration Plan

### Step 1: Backup existing databases
```bash
cp database/iiui_data.db database/iiui_data.db.backup
cp logs/chat_logs.db logs/chat_logs.db.backup
```

### Step 2: Create new tables
Run migration script to add new tables.

### Step 3: Migrate existing data
Transfer data from old tables to new schema.

### Step 4: Update application code
Modify DatabaseManager to use new schema.

### Step 5: Test
Verify all functionality works.

---

## 9. Data Validation Rules

| Table | Column | Rule |
|-------|--------|------|
| users | email | Unique, valid email format |
| users | password_hash | Not empty |
| users | role | Must be 'student' or 'admin' |
| faqs | question | Not empty, max 500 chars |
| faqs | answer | Not empty, max 2000 chars |
| contacts | department | Not empty |
| chat_logs | user_message | Not empty |
| chat_logs | bot_response | Not empty |
| chat_logs | confidence | Between 0 and 1 |

---

## 10. Backup Strategy

### Daily Backup
```bash
# Backup main database
cp database/iiui_data.db backups/iiui_data_$(date +%Y%m%d).db

# Backup chat logs
cp logs/chat_logs.db backups/chat_logs_$(date +%Y%m%d).db
```

### Weekly Cleanup
```sql
-- Remove old chat logs (keep 90 days)
DELETE FROM chat_logs WHERE created_at < DATE('now', '-90 days');

-- Remove expired sessions
DELETE FROM sessions WHERE expires_at < CURRENT_TIMESTAMP;
```
