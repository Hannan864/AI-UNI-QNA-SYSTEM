# UI/UX Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Current UI Analysis

### 1.1 Existing Screens

| Screen | Status | Quality |
|--------|--------|---------|
| Login Page | ✅ Exists | Good |
| Chat Interface | ✅ Exists | Good |
| Sidebar | ✅ Exists | Good |
| Registration Page | ❌ Missing | - |
| Admin Dashboard | ❌ Missing | - |
| Chat History | ❌ Missing | - |
| Profile Page | ❌ Missing | - |

### 1.2 Current Strengths

1. **Clean Design** — Professional IIUI branding
2. **Consistent Theme** — Green/white color scheme
3. **Chat Bubbles** — Clear message distinction
4. **Responsive Layout** — Works on different screens
5. **Voice Button** — Integrated microphone

### 1.3 Current Weaknesses

1. **No Registration** — Only login available
2. **No Admin UI** — Admin has no interface
3. **No Navigation** — Limited menu options
4. **No Loading States** — Some operations lack feedback
5. **No Error Pages** — Errors shown inline
6. **No Mobile Optimization** — Basic responsive design

---

## 2. Design System

### 2.1 Color Palette

```python
COLORS = {
    'primary': '#06402B',      # IIUI Green
    'secondary': '#FFFFFF',    # White
    'accent': '#0A5C3E',       # Darker Green
    'background': '#F5F5F5',   # Light Gray
    'text_dark': '#1a1a1a',    # Dark Text
    'text_light': '#ffffff',   # Light Text
    'success': '#28a745',      # Green
    'warning': '#ffc107',      # Yellow
    'danger': '#dc3545',       # Red
    'info': '#17a2b8'          # Blue
}
```

### 2.2 Typography

```python
FONTS = {
    'heading': 'Inter, sans-serif',
    'body': 'Inter, sans-serif',
    'mono': 'Fira Code, monospace'
}
```

### 2.3 Spacing

```python
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px'
}
```

---

## 3. Screen Designs

### 3.1 Login Page

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              International Islamic University            │
│                  Smart Chatbot Support                   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │              🔐 Login to Continue                │   │
│  │                                                 │   │
│  │  Email Address                                  │   │
│  │  [your.email@iiu.edu.pk_______________]        │   │
│  │                                                 │   │
│  │  Password                                       │   │
│  │  [_____________________________________]        │   │
│  │                                                 │   │
│  │  [           Login            ]                 │   │
│  │                                                 │   │
│  │  Don't have an account? Register                │   │
│  │                                                 │   │
│  │  Demo Credentials:                              │   │
│  │  Email: admin@iiu.edu.pk                       │   │
│  │  Password: admin123                             │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Registration Page

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              International Islamic University            │
│                  Smart Chatbot Support                   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │              📝 Create Account                   │   │
│  │                                                 │   │
│  │  Full Name                                      │   │
│  │  [_____________________________________]        │   │
│  │                                                 │   │
│  │  Email Address                                  │   │
│  │  [your.email@iiu.edu.pk_______________]        │   │
│  │                                                 │   │
│  │  Password                                       │   │
│  │  [_____________________________________]        │   │
│  │                                                 │   │
│  │  Confirm Password                               │   │
│  │  [_____________________________________]        │   │
│  │                                                 │   │
│  │  Department (Optional)                          │   │
│  │  [Computer Science ▼]                           │   │
│  │                                                 │   │
│  │  [          Register          ]                 │   │
│  │                                                 │   │
│  │  Already have an account? Login                 │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Student Dashboard (Chat Interface)

```
┌──────────────────┬──────────────────────────────────────┐
│    SIDEBAR       │           MAIN CONTENT               │
├──────────────────┼──────────────────────────────────────┤
│                  │                                      │
│  👤 User Info    │  ╔══════════════════════════════════╗│
│  ────────────    │  ║  International Islamic University ║│
│  Email:          │  ║     AI Smart Chatbot Support      ║│
│  ali@student.pk  │  ║  Welcome, Ali!                    ║│
│  Role: Student   │  ╚══════════════════════════════════╝│
│                  │                                      │
│  [Logout]        │  ┌──────────────────────────────┐   │
│                  │  │ 🎓 You: What is the admission │   │
│  ────────────    │  │ process?                      │   │
│                  │  └──────────────────────────────┘   │
│  📚 Quick Links  │                                      │
│  ────────────    │  ┌──────────────────────────────┐   │
│  • IIUI Website  │  │ 🤖 IIUI Bot: IIUI admissions  │   │
│  • Fee Structure │  │ require online application...  │   │
│  • Admissions    │  │                               │   │
│                  │  │ ✅ Confidence: 85%            │   │
│  ────────────    │  └──────────────────────────────┘   │
│                  │                                      │
│  📜 Chat History │  ────────────────────────────────── │
│  [View History]  │                                      │
│                  │  [🎤 Type your question about IIUI...]│
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

### 3.4 Admin Dashboard

```
┌──────────────────┬──────────────────────────────────────┐
│    SIDEBAR       │           MAIN CONTENT               │
├──────────────────┼──────────────────────────────────────┤
│                  │                                      │
│  👤 Admin Info   │  ╔══════════════════════════════════╗│
│  ────────────    │  ║       Admin Dashboard             ║│
│  Email:          │  ╚══════════════════════════════════╝│
│  admin@iiu.pk    │                                      │
│  Role: Admin     │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐│
│                  │  │Users │ │ FAQs │ │ Chats│ │Active││
│  [Logout]        │  │ 150  │ │ 100  │ │ 1200 │ │  25  ││
│                  │  └──────┘ └──────┘ └──────┘ └──────┘│
│  ────────────    │                                      │
│                  │  ┌─────────────────┐ ┌─────────────┐│
│  📊 Management   │  │  Recent Chats   │ │Common Q's   ││
│  ────────────    │  │  • Question 1   │ │ 1. Admiss.  ││
│  • 📋 FAQs      │  │  • Question 2   │ │ 2. Fee      ││
│  • 👥 Users     │  │  • Question 3   │ │ 3. Exam     ││
│  • 📞 Contacts  │  └─────────────────┘ └─────────────┘│
│  • 📚 Knowledge │                                      │
│                  │  ──────────────────────────────────  │
│  ────────────    │                                      │
│                  │  📈 Analytics                         │
│  📈 Analytics    │  [Last 7 Days ▼]                     │
│  ────────────    │                                      │
│  • Overview      │  Chat Volume: ▁▃▅▇▅▃▁               │
│  • Chat Stats    │  Top Intent: Admission (45%)         │
│  • Common Q's    │  Avg Confidence: 82%                 │
│                  │                                      │
│  ────────────    │                                      │
│                  │                                      │
│  ⚙️ System      │                                      │
│  ────────────    │                                      │
│  • Status        │                                      │
│  • Logs          │                                      │
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

### 3.5 FAQ Management Page

```
┌──────────────────┬──────────────────────────────────────┐
│    SIDEBAR       │           MAIN CONTENT               │
├──────────────────┼──────────────────────────────────────┤
│                  │                                      │
│  👤 Admin Info   │  ╔══════════════════════════════════╗│
│                  │  ║       FAQ Management              ║│
│  [Logout]        │  ╚══════════════════════════════════╝│
│                  │                                      │
│  ────────────    │  [+ Add FAQ] [Import] [Export]       │
│                  │                                      │
│  📋 Management   │  Category: [All ▼]  Search: [_____] │
│  ────────────    │                                      │
│  • 📋 FAQs      │  ┌────┬─────────────────┬──────┬───┐│
│  • 👥 Users     │  │ ID │ Question        │ Categ│Act││
│  • 📞 Contacts  │  ├────┼─────────────────┼──────┼───┤│
│  • 📚 Knowledge │  │ 1  │ What is admis..?│Admiss│ ✏️🗑️││
│                  │  │ 2  │ What is fee..?  │ Fees │ ✏️🗑️││
│  ────────────    │  │ 3  │ When are exams? │ Exam │ ✏️🗑️││
│                  │  │ ...│ ...             │ ...  │ ...││
│  📈 Analytics    │  └────┴─────────────────┴──────┴───┘│
│  ────────────    │                                      │
│  • Overview      │  Page 1 of 5  [Previous] [Next]      │
│  • Chat Stats    │                                      │
│  • Common Q's    │                                      │
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

---

## 4. Navigation Structure

### 4.1 Student Navigation

```
Sidebar:
├── 👤 User Info
│   ├── Email
│   └── Role
├── [Logout]
├── ─────────────
├── 📚 Quick Links
│   ├── IIUI Website
│   ├── Fee Structure
│   └── Admissions
├── ─────────────
└── 📜 Chat History
    └── [View History]
```

### 4.2 Admin Navigation

```
Sidebar:
├── 👤 Admin Info
│   ├── Email
│   └── Role
├── [Logout]
├── ─────────────
├── 📋 Management
│   ├── 📋 FAQs
│   ├── 👥 Users
│   ├── 📞 Contacts
│   └── 📚 Knowledge Base
├── ─────────────
├── 📈 Analytics
│   ├── Overview
│   ├── Chat Stats
│   └── Common Questions
├── ─────────────
└── ⚙️ System
    ├── Status
    └── Logs
```

---

## 5. Components Library

### 5.1 Buttons

```python
# Primary Button
st.button("Login", type="primary")

# Secondary Button
st.button("Cancel", type="secondary")

# Danger Button
st.button("Delete", type="danger")
```

### 5.2 Forms

```python
# Text Input
name = st.text_input("Name", placeholder="Enter your name")

# Email Input
email = st.text_input("Email", placeholder="your.email@iiu.edu.pk")

# Password Input
password = st.text_input("Password", type="password")

# Select Box
role = st.selectbox("Role", ["Student", "Admin"])

# Text Area
answer = st.text_area("Answer", height=100)

# Checkbox
active = st.checkbox("Active", value=True)
```

### 5.3 Cards

```python
# Stat Card
with st.container():
    st.metric(label="Total Users", value="150", delta="+5")

# Content Card
with st.container():
    st.subheader("FAQ Title")
    st.write("FAQ content here...")
    st.button("Edit")
```

### 5.4 Tables

```python
# Data Table
import pandas as pd
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Custom Table
st.table(data)
```

### 5.5 Charts

```python
# Line Chart
st.line_chart(data)

# Bar Chart
st.bar_chart(data)

# Pie Chart (using plotly)
import plotly.express as px
fig = px.pie(values=[30, 40, 30], names=['Admission', 'Fee', 'Exam'])
st.plotly_chart(fig)
```

---

## 6. Responsive Design

### 6.1 Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
    .sidebar { display: none; }
    .main-content { width: 100%; }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
    .sidebar { width: 200px; }
    .main-content { width: calc(100% - 200px); }
}

/* Desktop */
@media (min-width: 1025px) {
    .sidebar { width: 250px; }
    .main-content { width: calc(100% - 250px); }
}
```

### 6.2 Mobile Considerations

1. **Stack columns** on mobile
2. **Hide sidebar** on mobile (use hamburger menu)
3. **Full-width forms** on mobile
4. **Larger touch targets** on mobile
5. **Simplified navigation** on mobile

---

## 7. Accessibility

### 7.1 Requirements

1. **Color contrast** — Minimum 4.5:1 ratio
2. **Font size** — Minimum 16px
3. **Keyboard navigation** — All elements focusable
4. **Screen reader** — Proper ARIA labels
5. **Error messages** — Clear and descriptive

### 7.2 Implementation

```python
# ARIA labels
st.button("Login", aria_label="Login to your account")

# Error messages
if not email:
    st.error("Please enter your email address")

# Focus management
st.text_input("Email", key="email_input")
```

---

## 8. Loading States

### 8.1 Spinners

```python
with st.spinner("Loading..."):
    # Long operation
    time.sleep(2)
```

### 8.2 Progress Bars

```python
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)
```

### 8.3 Skeleton Loading

```python
# Placeholder for content
placeholder = st.empty()
placeholder.text("Loading...")
# After loading
placeholder.empty()
```

---

## 9. Error Handling UI

### 9.1 Error Messages

```python
# Inline error
st.error("Invalid email or password")

# Warning
st.warning("Session expired. Please login again.")

# Success
st.success("FAQ saved successfully")

# Info
st.info("Demo credentials: admin@iiu.edu.pk / admin123")
```

### 9.2 Error Pages

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                      404                                │
│                   Page Not Found                        │
│                                                         │
│          The page you're looking for doesn't exist.     │
│                                                         │
│                    [Go Home]                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 10. Implementation Checklist

### Phase 1: Core UI (Days 1-2)
- [ ] Login page (exists)
- [ ] Registration page
- [ ] Chat interface (exists)
- [ ] Basic navigation

### Phase 2: Admin UI (Days 3-5)
- [ ] Admin dashboard
- [ ] FAQ management
- [ ] User management
- [ ] Contact management

### Phase 3: Enhancement (Days 6-7)
- [ ] Loading states
- [ ] Error handling
- [ ] Responsive design
- [ ] Accessibility

### Phase 4: Polish (Days 8-9)
- [ ] Animations
- [ ] Tooltips
- [ ] Keyboard shortcuts
- [ ] Final testing
