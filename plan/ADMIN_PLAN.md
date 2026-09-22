# Admin Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Current Admin Functionality

### 1.1 What Exists

| Feature | Status | Notes |
|---------|--------|-------|
| Admin login | ✅ Works | Uses same login as students |
| Default admin creation | ✅ Works | admin@iiu.edu.pk / admin123 |
| Role-based access | ⚠️ Partial | Role stored but not enforced |
| Admin dashboard | ❌ Missing | No UI for admin |
| FAQ management | ❌ Missing | No CRUD interface |
| User management | ❌ Missing | No user list/edit |
| Analytics | ❌ Missing | No reporting |
| System status | ❌ Missing | No monitoring |

### 1.2 Admin Detection

```python
# In login.py
def create_default_admin(self):
    # Creates admin with role='admin'
    
# Current issue: No endpoint checks admin role
```

---

## 2. Required Admin Features

### 2.1 Admin Authentication

**Priority:** P0

**Features:**
- Admin login (existing)
- Admin role verification
- Admin session management
- Admin-only route protection

**Implementation:**
```python
# Middleware to check admin role
def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.headers.get('Authorization')
        user = session_manager.validate_session(session_id)
        if not user or user.get('role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        return f(*args, user=user, **kwargs)
    return decorated
```

---

### 2.2 Admin Dashboard

**Priority:** P0

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                    Admin Dashboard                       │
├─────────────┬─────────────┬─────────────┬───────────────┤
│   Total     │   Total     │   Total     │    Active     │
│   Users     │   FAQs      │   Chats     │    Users      │
│    150      │    100      │   1200      │     25        │
├─────────────┴─────────────┴─────────────┴───────────────┤
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Recent Chats   │  │  Common Q's     │              │
│  │  - Question 1   │  │  1. Admission   │              │
│  │  - Question 2   │  │  2. Fee         │              │
│  │  - Question 3   │  │  3. Exam        │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  User Activity  │  │  System Status  │              │
│  │  - Online: 25   │  │  - DB: OK       │              │
│  │  - Today: 45    │  │  - API: OK      │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

**Data Required:**
- Total users count
- Total FAQs count
- Total chat count
- Active users today
- Recent chat messages
- Common questions
- System status

---

### 2.3 FAQ Management

**Priority:** P0

**Features:**
1. View all FAQs
2. Add new FAQ
3. Edit existing FAQ
4. Delete FAQ
5. Search FAQs
6. Filter by category
7. Bulk import/export

**Interface:**
```
┌─────────────────────────────────────────────────────────┐
│                    FAQ Management                        │
├─────────────────────────────────────────────────────────┤
│ [+ Add FAQ]  [Import CSV]  [Export CSV]  [Search...]   │
├─────────────────────────────────────────────────────────┤
│ Category: [All ▼]  Sort: [Newest ▼]                    │
├─────────────────────────────────────────────────────────┤
│ ID │ Question                    │ Category │ Actions   │
│----│-----------------------------│----------│-----------│
│ 1  │ What is the admission...?   │ Admission│ [Edit][Del]│
│ 2  │ What is the fee structure?  │ Fees     │ [Edit][Del]│
│ 3  │ When are exams scheduled?   │ Exam     │ [Edit][Del]│
│ ...│ ...                         │ ...      │ ...       │
└─────────────────────────────────────────────────────────┘
```

**Add/Edit Form:**
```
┌─────────────────────────────────────────────────────────┐
│                    Add New FAQ                           │
├─────────────────────────────────────────────────────────┤
│ Question: [_________________________________]           │
│                                                         │
│ Answer:                                                 │
│ [_____________________________________________]         │
│ [_____________________________________________]         │
│ [_____________________________________________]         │
│                                                         │
│ Category: [Admissions ▼]                                │
│ Tags: [admission, process, apply]                       │
│                                                         │
│ [Cancel]  [Save FAQ]                                    │
└─────────────────────────────────────────────────────────┘
```

---

### 2.4 Knowledge Base Management

**Priority:** P1

**Features:**
1. View knowledge base articles
2. Add new articles
3. Edit articles
4. Delete articles
5. Organize by category
6. Search articles

**Article Structure:**
```json
{
    "title": "Admission Requirements",
    "content": "Detailed admission requirements for IIUI...",
    "category": "Admissions",
    "tags": ["admission", "requirements", "documents"],
    "source": "IIUI Official Website"
}
```

---

### 2.5 User Management

**Priority:** P1

**Features:**
1. View all users
2. Search users
3. Filter by role
4. View user details
5. Edit user role
6. Deactivate user
7. Delete user

**Interface:**
```
┌─────────────────────────────────────────────────────────┐
│                    User Management                       │
├─────────────────────────────────────────────────────────┤
│ [Search users...]  Role: [All ▼]  Status: [All ▼]      │
├─────────────────────────────────────────────────────────┤
│ ID │ Name        │ Email              │ Role    │ Actions│
│----│-------------│--------------------|---------|--------│
│ 1  │ Admin User  │ admin@iiu.edu.pk   │ admin   │ [View] │
│ 2  │ Ali Ahmed   │ ali@student.edu.pk │ student │ [View] │
│ 3  │ Sara Khan   │ sara@student.edu.pk│ student │ [View] │
│ ...│ ...         │ ...                │ ...     │ ...    │
└─────────────────────────────────────────────────────────┘
```

**User Details View:**
```
┌─────────────────────────────────────────────────────────┐
│                    User Details                          │
├─────────────────────────────────────────────────────────┤
│ Name: Ali Ahmed                                         │
│ Email: ali@student.edu.pk                               │
│ Role: [Student ▼]                                       │
│ Department: Computer Science                            │
│ Joined: 2026-01-15                                      │
│ Last Login: 2026-08-18 10:30 AM                         │
│ Status: [Active ▼]                                      │
│                                                         │
│ Chat History:                                           │
│ - "What is the admission process?" (2026-08-18)         │
│ - "What is the fee structure?" (2026-08-17)             │
│                                                         │
│ [Edit]  [Deactivate]  [Delete]  [Back to List]         │
└─────────────────────────────────────────────────────────┘
```

---

### 2.6 Contact Management

**Priority:** P1

**Features:**
1. View all contacts
2. Add new contact
3. Edit contact
4. Delete contact
5. Filter by department

**Interface:**
```
┌─────────────────────────────────────────────────────────┐
│                   Contact Management                     │
├─────────────────────────────────────────────────────────┤
│ [+ Add Contact]  Department: [All ▼]                    │
├─────────────────────────────────────────────────────────┤
│ Dept            │ Person      │ Email                   │
│-----------------|-------------|-------------------------│
│ Admissions      │ Mr. Khan    │ admissions@iiu.edu.pk   │
│ IT Help Desk    │ Ali Ahmed   │ ithelp@iiu.edu.pk       │
│ Library         │ Sara Bibi   │ library@iiu.edu.pk      │
│ ...             │ ...         │ ...                     │
└─────────────────────────────────────────────────────────┘
```

---

### 2.7 Analytics Dashboard

**Priority:** P2

**Features:**
1. Overview statistics
2. Chat volume over time
3. Common questions
4. Intent distribution
5. Confidence scores
6. User activity
7. Peak hours

**Interface:**
```
┌─────────────────────────────────────────────────────────┐
│                   Analytics Dashboard                    │
├─────────────────────────────────────────────────────────┤
│ Period: [Last 7 Days ▼]  [Custom Range]                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Chat Volume    │  │  Top Intents    │              │
│  │  ▁▃▅▇▅▃▁      │  │  Admission: 45% │              │
│  │  Mon-Sun        │  │  Fee: 30%       │              │
│  │                 │  │  Exam: 25%      │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Confidence     │  │  User Activity  │              │
│  │  High: 70%      │  │  New Users: 15  │              │
│  │  Medium: 20%    │  │  Active: 45     │              │
│  │  Low: 10%       │  │  Returning: 30  │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  Most Common Questions:                                 │
│  1. What is the admission process? (45 times)           │
│  2. What is the fee structure? (38 times)               │
│  3. When are exams? (32 times)                          │
└─────────────────────────────────────────────────────────┘
```

---

### 2.8 Chat History Viewer

**Priority:** P1

**Features:**
1. View all chat logs
2. Filter by user
3. Filter by date
4. Filter by intent
5. View conversation threads
6. Export chat logs

**Interface:**
```
┌─────────────────────────────────────────────────────────┐
│                   Chat History                           │
├─────────────────────────────────────────────────────────┤
│ User: [All ▼]  Date: [All ▼]  Intent: [All ▼]          │
├─────────────────────────────────────────────────────────┤
│ Time        │ User              │ Message               │
│-------------|-------------------|-----------------------│
│ 10:30 AM    │ ali@student.edu   │ What is admission?    │
│ 10:30 AM    │ IIUI Bot          │ IIUI admissions...    │
│ 10:35 AM    │ sara@student.edu  │ Fee structure?        │
│ 10:35 AM    │ IIUI Bot          │ Fee varies by...      │
│ ...         │ ...               │ ...                   │
└─────────────────────────────────────────────────────────┘
```

---

### 2.9 System Status

**Priority:** P2

**Features:**
1. Database status
2. API status
3. Model status
4. Storage usage
5. Error logs

**Interface:**
```
┌─────────────────────────────────────────────────────────┐
│                   System Status                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Component          │ Status    │ Details               │
│  -------------------|-----------|-----------------------│
│  Database           │ ✅ OK     │ SQLite, 32KB          │
│  Chat Logs DB       │ ✅ OK     │ SQLite, 20KB          │
│  FAQ Embeddings     │ ✅ OK     │ 36KB, 100 FAQs       │
│  NLP Model          │ ✅ OK     │ en_core_web_sm        │
│  Sentence Model     │ ✅ OK     │ all-MiniLM-L6-v2     │
│  API Server         │ ✅ OK     │ Running on port 5000  │
│                                                         │
│  Storage:                                                │
│  - Database: 52KB                                        │
│  - Embeddings: 36KB                                      │
│  - Total: 88KB                                           │
│                                                         │
│  [Refresh Status]  [View Logs]                           │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Admin API Endpoints

### 3.1 Dashboard
- `GET /api/admin/dashboard` — Get dashboard data

### 3.2 FAQs
- `GET /api/admin/faqs` — Get all FAQs (with pagination)
- `POST /api/admin/faqs` — Create FAQ
- `PUT /api/admin/faqs/{id}` — Update FAQ
- `DELETE /api/admin/faqs/{id}` — Delete FAQ

### 3.3 Users
- `GET /api/admin/users` — Get all users
- `GET /api/admin/users/{id}` — Get user details
- `PUT /api/admin/users/{id}` — Update user
- `DELETE /api/admin/users/{id}` — Delete user

### 3.4 Contacts
- `GET /api/admin/contacts` — Get all contacts
- `POST /api/admin/contacts` — Create contact
- `PUT /api/admin/contacts/{id}` — Update contact
- `DELETE /api/admin/contacts/{id}` — Delete contact

### 3.5 Analytics
- `GET /api/admin/analytics/overview` — Get overview
- `GET /api/admin/analytics/chats` — Get chat analytics
- `GET /api/admin/analytics/common-questions` — Get common questions

### 3.6 Chat History
- `GET /api/admin/chats` — Get all chat logs
- `GET /api/admin/chats/{id}` — Get chat details

### 3.7 System
- `GET /api/admin/status` — Get system status

---

## 4. Implementation Priority

### Phase 1: Core Admin (Days 1-3)
1. Admin role verification
2. Admin dashboard layout
3. Basic statistics display

### Phase 2: Content Management (Days 4-6)
1. FAQ CRUD interface
2. Contact management
3. Knowledge base management

### Phase 3: User Management (Days 7-8)
1. User list view
2. User details view
3. User role management

### Phase 4: Analytics & Monitoring (Days 9-10)
1. Analytics dashboard
2. Chat history viewer
3. System status page

---

## 5. Security Requirements

1. **Admin-only access** — All admin endpoints require admin role
2. **Audit logging** — Track admin actions
3. **Input validation** — Validate all admin inputs
4. **CSRF protection** — Prevent cross-site request forgery
5. **Rate limiting** — Prevent abuse
6. **Session timeout** — Auto-logout after inactivity

---

## 6. Testing Checklist

- [ ] Admin can login
- [ ] Non-admin cannot access admin pages
- [ ] Dashboard displays correct statistics
- [ ] FAQ CRUD works correctly
- [ ] User management works correctly
- [ ] Contact management works correctly
- [ ] Analytics displays correct data
- [ ] Chat history loads correctly
- [ ] System status shows correct info
- [ ] All forms validate input
- [ ] Error messages are helpful
- [ ] Actions are logged
