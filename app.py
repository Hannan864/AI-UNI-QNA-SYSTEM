"""
IIUI Smart Chatbot - AI Chatbot for University Support
Professional Streamlit Frontend
"""
import streamlit as st
import requests
import time
from config import COLORS, UNIVERSITY_INFO

st.set_page_config(
    page_title="IIUI Smart Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

FLASK_API_URL = "http://localhost:5000/api"

# ============================================================
# CSS DESIGN SYSTEM
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root {{
    --primary: {COLORS['primary']};
    --primary-lighter: #E8F5EE;
    --accent: #D4A843;
    --surface: #FFFFFF;
    --surface-alt: #F0F2F5;
    --text: #1A1A2E;
    --text-secondary: #5F6B7A;
    --text-muted: #9CA3AF;
    --border: #E5E7EB;
    --success: #059669;
    --warning: #D97706;
    --danger: #DC2626;
    --info: #2563EB;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
    --radius-sm: 6px;
    --radius-md: 10px;
}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
h1,h2,h3,h4,h5,h6,p,div,span,label {{ font-family: 'Inter',-apple-system,sans-serif !important; }}
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg,{COLORS['primary']} 0%,#032A1A 100%) !important; }}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown li {{ color: #FFFFFF !important; }}
section[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255,255,255,0.1) !important; color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 8px !important;
    padding: 8px 16px !important; font-weight: 500 !important;
    text-align: left !important; width: 100% !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{ background: rgba(255,255,255,0.2) !important; }}
section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15) !important; margin: 8px 0 !important; }}
.card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; margin-bottom: 16px; box-shadow: var(--shadow-sm); }}
.stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; text-align: center; box-shadow: var(--shadow-sm); }}
.stat-card .stat-value {{ font-size: 2rem; font-weight: 700; color: var(--primary); }}
.stat-card .stat-label {{ font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }}
.badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
.badge-primary {{ background: var(--primary-lighter); color: var(--primary); }}
.badge-success {{ background: #D1FAE5; color: #065F46; }}
.badge-warning {{ background: #FEF3C7; color: #92400E; }}
.badge-danger {{ background: #FEE2E2; color: #991B1B; }}
.badge-info {{ background: #DBEAFE; color: #1E40AF; }}
.quick-action {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px; text-align: center; transition: all 0.2s; box-shadow: var(--shadow-sm); }}
.quick-action:hover {{ border-color: var(--primary); box-shadow: var(--shadow-md); transform: translateY(-2px); }}
.quick-action .qa-icon {{ font-size: 1.8rem; margin-bottom: 8px; }}
.quick-action .qa-title {{ font-size: 0.9rem; font-weight: 600; color: var(--text); }}
.quick-action .qa-desc {{ font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px; }}
.chat-msg {{ padding: 12px 16px; border-radius: 12px; margin: 8px 0; font-size: 0.95rem; line-height: 1.6; max-width: 85%; }}
.chat-user {{ background: var(--primary); color: #FFFFFF; margin-left: auto; border-bottom-right-radius: 4px; }}
.chat-bot {{ background: var(--surface); color: var(--text); border: 1px solid var(--border); border-bottom-left-radius: 4px; }}
.empty-state {{ text-align: center; padding: 48px 24px; color: var(--text-secondary); }}
.empty-state .empty-icon {{ font-size: 3rem; margin-bottom: 16px; opacity: 0.5; }}
.empty-state .empty-title {{ font-size: 1.1rem; font-weight: 600; color: var(--text); margin-bottom: 8px; }}
.empty-state .empty-desc {{ font-size: 0.9rem; color: var(--text-muted); }}
.data-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
.data-table th {{ background: var(--surface-alt); padding: 10px 12px; text-align: left; font-weight: 600; color: var(--text-secondary); border-bottom: 2px solid var(--border); }}
.data-table td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); color: var(--text); }}
.sidebar-user {{ background: rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; margin-bottom: 12px; }}
.sidebar-user .user-name {{ font-weight: 600; font-size: 0.95rem; color: #FFFFFF; }}
.sidebar-user .user-role {{ font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 2px; }}
.sidebar-user .user-email {{ font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 2px; }}
.sidebar-section {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.4) !important; margin-top: 12px; margin-bottom: 4px; padding-left: 12px; }}
.status-indicator {{ display: inline-flex; align-items: center; gap: 6px; font-size: 0.8rem; font-weight: 500; }}
.status-dot {{ width: 8px; height: 8px; border-radius: 50%; }}
.status-dot.online {{ background: var(--success); animation: pulse 2s infinite; }}
@keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
.nav-active {{ background: rgba(255,255,255,0.18) !important; font-weight: 700 !important; border-left: 3px solid rgba(255,255,255,0.8) !important; padding-left: 10px !important; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE & HELPERS
# ============================================================
def init_session():
    defaults = {'logged_in': False, 'session_id': None, 'user_info': None, 'current_page': 'dashboard', 'chat_mode': 'live', 'messages': [], 'auth_page': 'login', 'show_add_kb': False, 'show_add_faq': False, 'editing_kb_id': None, 'editing_faq_id': None}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_session()

def _auth_headers():
    """Return headers with session ID for authenticated requests."""
    headers = {}
    sid = st.session_state.get('session_id')
    if sid:
        headers['X-Session-Id'] = sid
    return headers

def _handle_auth_error(data):
    """Check if response indicates session expiry and auto-logout."""
    if not data.get('success') and data.get('message', '') in ('Session expired', 'Authentication required. Please login.'):
        st.session_state.logged_in = False
        st.session_state.session_id = None
        st.session_state.user_info = None
        st.session_state.messages = []
        st.session_state.auth_page = 'login'
        st.warning('Your session has expired. Please login again.')
        time.sleep(1)
        st.rerun()

def api_post(ep, d=None):
    try:
        resp = requests.post(f"{FLASK_API_URL}{ep}", json=d, headers=_auth_headers(), timeout=10)
        data = resp.json()
        if resp.status_code == 401:
            _handle_auth_error(data)
        return data
    except requests.ConnectionError:
        return {'success': False, 'message': 'Cannot connect to server. Is the Flask backend running?'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def api_put(ep, d=None):
    try:
        resp = requests.put(f"{FLASK_API_URL}{ep}", json=d, headers=_auth_headers(), timeout=10)
        data = resp.json()
        if resp.status_code == 401:
            _handle_auth_error(data)
        return data
    except requests.ConnectionError:
        return {'success': False, 'message': 'Cannot connect to server.'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def api_get(ep, p=None):
    try:
        resp = requests.get(f"{FLASK_API_URL}{ep}", params=p, headers=_auth_headers(), timeout=10)
        data = resp.json()
        if resp.status_code == 401:
            _handle_auth_error(data)
        return data
    except requests.ConnectionError:
        return {'success': False, 'message': 'Cannot connect to server.'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_role():
    return st.session_state.user_info.get('role', 'student') if st.session_state.user_info else 'student'

def is_admin():
    return get_role() == 'admin'

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def logout():
    # Call backend logout to invalidate session
    try:
        api_post('/logout', {'session_id': st.session_state.get('session_id')})
    except Exception:
        pass  # Proceed with local logout even if backend call fails
    st.session_state.logged_in = False
    st.session_state.session_id = None
    st.session_state.user_info = None
    st.session_state.messages = []
    st.session_state.current_page = 'dashboard'
    st.rerun()

# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""<div style="text-align:center;padding:12px 0 8px 0;">
        <div style="font-size:1.6rem;">🎓</div>
        <div style="color:#FFF;font-size:1rem;font-weight:700;margin-top:4px;">IIUI Smart Chatbot</div>
        <div style="color:rgba(255,255,255,0.5);font-size:0.7rem;margin-top:2px;">AI University Support</div></div>""", unsafe_allow_html=True)
        st.markdown("---")
        u = st.session_state.user_info
        if u:
            st.markdown(f"""<div class="sidebar-user">
            <div class="user-name">{u.get('name','User')}</div>
            <div class="user-role">{u.get('role','student').title()}</div>
            <div class="user-email">{u.get('email','')}</div></div>""", unsafe_allow_html=True)
        role = get_role()
        cp = st.session_state.current_page
        if role in ('student', 'faculty'):
            st.markdown('<div class="sidebar-section">Main</div>', unsafe_allow_html=True)
            for k, i, l in [('dashboard','📊','Dashboard'),('live_assistant','🤖','Live AI Assistant'),('mock_assistant','📋','Mock Data Assistant'),('chat_history','💬','Chat History')]:
                label = f"  {i}  {l}" + ("  ◀" if cp == k else "")
                if st.button(label, key=f"nav_{k}", use_container_width=True):
                    navigate_to(k)
            st.markdown('<div class="sidebar-section">Information</div>', unsafe_allow_html=True)
            for k, i, l in [('university_info','🏛️','University Info'),('academic','📚','Academic Assistance')]:
                label = f"  {i}  {l}" + ("  ◀" if cp == k else "")
                if st.button(label, key=f"nav_{k}", use_container_width=True):
                    navigate_to(k)
            st.markdown('<div class="sidebar-section">Account</div>', unsafe_allow_html=True)
            for k, i, l in [('profile','👤','Profile'),('settings','⚙️','Settings')]:
                label = f"  {i}  {l}" + ("  ◀" if cp == k else "")
                if st.button(label, key=f"nav_{k}", use_container_width=True):
                    navigate_to(k)
        elif role == 'admin':
            st.markdown('<div class="sidebar-section">Dashboard</div>', unsafe_allow_html=True)
            label = "  📊  Admin Dashboard" + ("  ◀" if cp == 'admin_dashboard' else "")
            if st.button(label, key="nav_admin_dashboard", use_container_width=True):
                navigate_to('admin_dashboard')
            st.markdown('<div class="sidebar-section">Management</div>', unsafe_allow_html=True)
            for k, i, l in [('admin_knowledge','📖','Knowledge Base'),('admin_faqs','❓','FAQ Management'),('admin_chatbot','🤖','Chatbot')]:
                label = f"  {i}  {l}" + ("  ◀" if cp == k else "")
                if st.button(label, key=f"nav_{k}", use_container_width=True):
                    navigate_to(k)
            st.markdown('<div class="sidebar-section">Monitoring</div>', unsafe_allow_html=True)
            for k, i, l in [('admin_users','👥','Users'),('admin_chat_logs','📝','Chat Logs'),('admin_analytics','📈','Analytics')]:
                label = f"  {i}  {l}" + ("  ◀" if cp == k else "")
                if st.button(label, key=f"nav_{k}", use_container_width=True):
                    navigate_to(k)
            st.markdown('<div class="sidebar-section">Account</div>', unsafe_allow_html=True)
            label = "  👤  Profile" + ("  ◀" if cp == 'profile' else "")
            if st.button(label, key="nav_profile_admin", use_container_width=True):
                navigate_to('profile')
            label = "  ⚙️  Settings" + ("  ◀" if cp == 'settings' else "")
            if st.button(label, key="nav_settings_admin", use_container_width=True):
                navigate_to('settings')
        st.markdown("---")
        if st.button("🚪  Logout", key="sidebar_logout", use_container_width=True):
            logout()
        st.markdown("""<div style="text-align:center;padding:8px 0;color:rgba(255,255,255,0.3);font-size:0.7rem;">
        IIUI Smart Chatbot v1.0<br>© 2026</div>""", unsafe_allow_html=True)

# ============================================================
# AUTH PAGES
# ============================================================
def page_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div style="text-align:center;margin-bottom:32px;">
        <div style="font-size:3rem;margin-bottom:8px;">🎓</div>
        <h1 style="margin:0;font-size:1.8rem;font-weight:700;color:{COLORS['primary']};">{UNIVERSITY_INFO['short_name']} Smart Chatbot</h1>
        <p style="color:#5F6B7A;font-size:0.9rem;margin-top:8px;">AI-Powered University Support System</p></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="padding:32px;">', unsafe_allow_html=True)
        st.markdown("""<div style="margin-bottom:24px;"><h2 style="margin:0;font-size:1.3rem;font-weight:600;">Welcome Back</h2>
        <p style="color:var(--text-secondary);font-size:0.85rem;margin-top:4px;">Sign in to continue to your account</p></div>""", unsafe_allow_html=True)
        email = st.text_input("Email Address", placeholder="your.email@iiu.edu.pk", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.checkbox("Remember me")
        with col_b:
            st.markdown('<div style="text-align:right;padding-top:8px;"><span style="color:var(--primary);font-size:0.85rem;">Forgot password?</span></div>', unsafe_allow_html=True)
        if st.button("Sign In", use_container_width=True, type="primary", key="login_btn"):
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                with st.spinner("Signing in..."):
                    data = api_post('/login', {'email': email, 'password': password})
                    if data.get('success'):
                        st.session_state.logged_in = True
                        st.session_state.session_id = data['session_id']
                        st.session_state.user_info = data['user']
                        st.session_state.current_page = 'dashboard'
                        st.success("Login successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(data.get('message', 'Login failed.'))
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center;margin-top:20px;padding:16px;background:var(--surface-alt);border-radius:10px;">
        <span style="color:var(--text-secondary);font-size:0.85rem;">Don't have an account?</span></div>""", unsafe_allow_html=True)
        if st.button("Create Account", use_container_width=True, key="goto_register"):
            st.session_state.auth_page = 'register'
            st.rerun()
        st.markdown(f"""<div style="margin-top:16px;padding:12px;background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;font-size:0.8rem;">
        <strong style="color:#92400E;">Demo Credentials:</strong><br>
        <span style="color:#78350F;">Admin: <code>admin@iiu.edu.pk</code> / <code>admin123</code><br>Student: Register a new account</span></div>""", unsafe_allow_html=True)

def page_register():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f"""<div style="text-align:center;margin-bottom:32px;">
        <div style="font-size:3rem;margin-bottom:8px;">🎓</div>
        <h1 style="margin:0;font-size:1.8rem;font-weight:700;color:{COLORS['primary']};">Create Account</h1>
        <p style="color:#5F6B7A;font-size:0.9rem;margin-top:8px;">Join the IIUI Smart Chatbot community</p></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="padding:32px;">', unsafe_allow_html=True)
        reg_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
        reg_email = st.text_input("University Email", placeholder="your.email@iiu.edu.pk", key="reg_email")
        reg_role = st.selectbox("Role", ["student", "faculty"], key="reg_role")
        reg_pass = st.text_input("Password", type="password", placeholder="Minimum 6 characters", key="reg_pass")
        reg_pass2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="reg_pass2")
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        if st.button("Create Account", use_container_width=True, type="primary", key="register_btn"):
            if not reg_name or not reg_email or not reg_pass:
                st.warning("Please fill in all fields.")
            elif reg_pass != reg_pass2:
                st.error("Passwords do not match.")
            elif len(reg_pass) < 6:
                st.error("Password must be at least 6 characters.")
            elif not terms:
                st.warning("Please agree to the terms.")
            else:
                with st.spinner("Creating account..."):
                    data = api_post('/register', {'name': reg_name, 'email': reg_email, 'password': reg_pass, 'role': reg_role})
                    if data.get('success'):
                        st.session_state.logged_in = True
                        st.session_state.session_id = data['session_id']
                        st.session_state.user_info = data['user']
                        st.session_state.current_page = 'dashboard'
                        st.success("Account created successfully!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(data.get('message', 'Registration failed.'))
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center;margin-top:20px;padding:16px;background:var(--surface-alt);border-radius:10px;">
        <span style="color:var(--text-secondary);font-size:0.85rem;">Already have an account?</span></div>""", unsafe_allow_html=True)
        if st.button("Sign In", use_container_width=True, key="goto_login"):
            st.session_state.auth_page = 'login'
            st.rerun()

# ============================================================
# STUDENT/FACULTY PAGES
# ============================================================
def page_dashboard():
    user = st.session_state.user_info
    name = user.get('name', 'User') if user else 'User'
    st.markdown(f"""<div style="background:linear-gradient(135deg,{COLORS['primary']} 0%,#0A5C3E 100%);color:white;padding:28px 32px;border-radius:12px;margin-bottom:24px;box-shadow:0 4px 15px rgba(6,64,43,0.3);">
    <h1 style="margin:0;font-size:1.6rem;font-weight:700;">Welcome, {name} 👋</h1>
    <p style="margin:6px 0 0 0;font-size:0.95rem;opacity:0.9;">How can we help you today?</p></div>""", unsafe_allow_html=True)
    st.markdown("### Quick Actions")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    for col, (icon, title, desc) in zip([qcol1, qcol2, qcol3, qcol4], [("🤖", "Live AI Assistant", "Chat with our AI-powered assistant"), ("📋", "Mock Data Assistant", "Get answers from university knowledge base"), ("💬", "Chat History", "Review your past conversations"), ("🏛️", "University Info", "Browse IIUI information and resources")]):
        with col:
            st.markdown(f'<div class="quick-action"><div class="qa-icon">{icon}</div><div class="qa-title">{title}</div><div class="qa-desc">{desc}</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("### 📌 Popular Questions")
        popular_qs = [("Admission process", "admission"), ("Fee structure", "fees"), ("Course registration", "courses"), ("Examination schedule", "exams"), ("Academic policies", "policies"), ("University services", "services"), ("Scholarships", "scholarships"), ("Campus facilities", "facilities")]
        for i in range(0, len(popular_qs), 2):
            row_cols = st.columns(2)
            for j, col in enumerate(row_cols):
                if i + j < len(popular_qs):
                    q, cat = popular_qs[i + j]
                    with col:
                        st.markdown(f'<div class="card" style="padding:12px 16px;"><div style="display:flex;align-items:center;gap:8px;"><span class="badge badge-primary">{cat}</span><span style="font-size:0.85rem;font-weight:500;">{q}</span></div></div>', unsafe_allow_html=True)
    with right:
        st.markdown("### 🕐 Recent Conversations")
        try:
            data = api_get('/history', {'session_id': st.session_state.session_id})
            hist = data.get('data', data.get('history', []))
            if data.get('success') and hist:
                for msg in hist[:5]:
                    st.markdown(f'<div class="card" style="padding:10px 14px;"><div style="font-size:0.85rem;font-weight:500;">{msg["user_message"][:60]}{"..." if len(msg["user_message"])>60 else ""}</div><div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px;">{msg.get("timestamp","N/A")}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state" style="padding:24px;"><div class="empty-icon">💬</div><div class="empty-title">No conversations yet</div><div class="empty-desc">Start a chat to see your history here</div></div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div class="empty-state" style="padding:24px;"><div class="empty-icon">💬</div><div class="empty-title">No conversations yet</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📚 Academic Assistance")
    acol1, acol2, acol3, acol4 = st.columns(4)
    for col, (icon, title, desc) in zip([acol1, acol2, acol3, acol4], [("📖", "Course Guidance", "Browse courses by semester"), ("📅", "Exam Schedule", "View upcoming examinations"), ("📝", "Assignment Reminders", "Track assignment deadlines"), ("🏆", "Scholarships", "Discover available scholarships")]):
        with col:
            st.markdown(f'<div class="card" style="text-align:center;padding:16px;"><div style="font-size:1.5rem;">{icon}</div><div style="font-size:0.85rem;font-weight:600;margin-top:6px;">{title}</div><div style="font-size:0.75rem;color:var(--text-muted);margin-top:2px;">{desc}</div></div>', unsafe_allow_html=True)

# ============================================================
# CHAT INTERFACE (shared by Live & Mock)
# ============================================================
def _render_chat_interface(mode='live'):
    # Require authentication for chat
    if not st.session_state.get('logged_in'):
        st.markdown('<div class="empty-state"><div class="empty-icon">🔒</div><div class="empty-title">Please login to use the chat assistant</div><div class="empty-desc">You need to be logged in to chat with the AI assistant.</div></div>', unsafe_allow_html=True)
        if st.button("Go to Login", type="primary"):
            st.session_state.auth_page = 'login'
            st.rerun()
        return

    mode_label = "LIVE AI" if mode == 'live' else "MOCK DATA"
    mode_color = "#059669" if mode == 'live' else "#D97706"
    mode_desc = "Powered by AI model" if mode == 'live' else "Powered by Knowledge Base"
    icon = '🤖' if mode == 'live' else '📋'

    # Check live AI configuration status
    ai_configured = False
    if mode == 'live':
        try:
            ai_status = api_get('/settings/ai/status')
            if ai_status.get('success'):
                ai_configured = ai_status.get('data', {}).get('status') == 'configured'
        except Exception:
            pass
    status_text = "Connected" if (mode == 'live' and ai_configured) else ("Not Configured" if mode == 'live' else "Available")
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 20px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;">
    <div style="display:flex;align-items:center;gap:12px;"><div style="font-size:1.5rem;">{icon}</div>
    <div><div style="font-weight:700;font-size:1rem;">{mode_label} Assistant</div><div style="font-size:0.8rem;color:var(--text-secondary);">{mode_desc}</div></div></div>
    <div><span class="status-indicator"><span class="status-dot {'online' if status_text == 'Connected' else ''}"></span><span style="color:{mode_color if status_text != 'Not Configured' else '#DC2626'};">{status_text}</span></span></div></div>""", unsafe_allow_html=True)
    lcol, rcol = st.columns(2)
    with lcol:
        live_type = "primary" if mode == 'live' else "secondary"
        if st.button("🤖  Live AI Assistant", use_container_width=True, key="mode_live_chat", type=live_type):
            st.session_state.chat_mode = 'live'; st.rerun()
    with rcol:
        mock_type = "primary" if mode == 'mock' else "secondary"
        if st.button("📋  Mock Data Assistant", use_container_width=True, key="mode_mock_chat", type=mock_type):
            st.session_state.chat_mode = 'mock'; st.rerun()
    # Show warning if live AI is not configured
    if mode == 'live' and not ai_configured:
        st.markdown('<div style="padding:12px 16px;background:#FEF3C7;border:1px solid #FDE68A;border-radius:8px;margin-bottom:16px;font-size:0.85rem;">⚠️ <strong>Live AI is not configured.</strong> Please configure an AI provider in Settings to use this mode. You can switch to Mock Data Assistant in the meantime.</div>', unsafe_allow_html=True)

    st.markdown("---")
    if not st.session_state.messages:
        st.markdown("#### 💡 Suggested Questions")
        suggestions = ["What is the admission process?", "How do I register for courses?", "What is the fee structure?", "When are examinations?", "Tell me about scholarships"] if mode == 'live' else ["What are the university hours?", "Where is the admissions office?", "What programs are offered?", "How can I contact support?", "What are the library hours?"]
        sug_cols = st.columns(len(suggestions))
        for i, (col, sug) in enumerate(zip(sug_cols, suggestions)):
            with col:
                if st.button(sug, key=f"sug_{mode}_{i}", use_container_width=True):
                    st.session_state.messages.append({'role': 'user', 'content': sug}); st.rerun()
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f'<div style="display:flex;justify-content:flex-end;margin:8px 0;"><div class="chat-msg chat-user"><strong>You</strong><br>{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="display:flex;justify-content:flex-start;margin:8px 0;"><div class="chat-msg chat-bot"><strong>{mode_label} Assistant</strong><br>{msg["content"]}</div></div>', unsafe_allow_html=True)
    st.markdown("---")

    # Voice input option
    voice_col1, voice_col2 = st.columns([1, 5])
    with voice_col1:
        voice_enabled = st.toggle("🎤 Voice", value=False, key=f"voice_toggle_{mode}", help="Enable voice input via microphone")

    if voice_enabled:
        audio_data = st.audio_input("🎤 Speak your question", key=f"voice_input_{mode}")
        if audio_data is not None:
            with st.spinner("🎤 Converting speech to text..."):
                try:
                    import io
                    audio_bytes = audio_data.read()
                    files = {'audio': ('voice_input.wav', audio_bytes, 'audio/wav')}
                    resp = requests.post(f"{FLASK_API_URL}/voice/transcribe", files=files, headers=_auth_headers(), timeout=15)
                    result = resp.json()
                    if result.get('success'):
                        transcribed = result.get('data', {}).get('text', '')
                        if transcribed and len(transcribed.strip()) > 1:
                            st.session_state.messages.append({'role': 'user', 'content': transcribed})
                            with st.spinner("Thinking..."):
                                data = api_post('/chat', {'message': transcribed, 'session_id': st.session_state.session_id, 'mode': mode})
                                if data.get('success'):
                                    resp_data = data.get('response', {})
                                    answer = resp_data.get('answer', 'No response received.')
                                    conf = resp_data.get('confidence', 0)
                                    ci = "✅" if conf > 0.7 else "⚠️" if conf > 0.4 else "❌"
                                    st.session_state.messages.append({'role': 'assistant', 'content': f"{answer}\n\n_{ci} Confidence: {int(conf*100)}%_"})
                                else:
                                    st.session_state.messages.append({'role': 'assistant', 'content': f"⚠️ {data.get('message', 'Error processing your request.')}"})
                            st.rerun()
                        else:
                            st.warning("Could not understand the audio. Please try again or type your question.")
                    else:
                        st.warning("Voice recognition failed. Please try again or type your question.")
                except Exception as e:
                    st.warning(f"Voice input error: {str(e)[:50]}. Please type your question.")

    # Text input
    user_input = st.chat_input("Ask about admissions, fees, courses, exams, policies...")
    if user_input:
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        with st.spinner("Thinking..."):
            data = api_post('/chat', {'message': user_input, 'session_id': st.session_state.session_id, 'mode': mode})
            if data.get('success'):
                resp = data.get('response', {})
                answer = resp.get('answer', 'No response received.')
                conf = resp.get('confidence', 0)
                ci = "✅" if conf > 0.7 else "⚠️" if conf > 0.4 else "❌"
                st.session_state.messages.append({'role': 'assistant', 'content': f"{answer}\n\n_{ci} Confidence: {int(conf*100)}%_"})
            else:
                st.session_state.messages.append({'role': 'assistant', 'content': f"⚠️ {data.get('message', 'Error processing your request.')}"})
        st.rerun()
    if st.session_state.messages:
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            if st.button("🗑️ Clear Chat", key=f"clear_{mode}"):
                st.session_state.messages = []; st.rerun()
        with c2:
            if st.button("🔄 New Conversation", key=f"new_{mode}"):
                st.session_state.messages = []; st.rerun()

def page_live_assistant(): _render_chat_interface(mode='live')
def page_mock_assistant(): _render_chat_interface(mode='mock')

# ============================================================
# CHAT HISTORY
# ============================================================
def page_chat_history():
    if not st.session_state.get('logged_in'):
        st.markdown('<div class="empty-state"><div class="empty-icon">🔒</div><div class="empty-title">Please login to view chat history</div></div>', unsafe_allow_html=True)
        if st.button("Go to Login", type="primary"):
            st.session_state.auth_page = 'login'
            st.rerun()
        return
    st.markdown("## 💬 Chat History")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">Review your past conversations with the AI assistant.</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([1, 1, 4])
    with fc1: st.selectbox("Mode", ["All", "Live AI", "Mock Data"], key="history_mode_filter")
    with fc2: st.date_input("From", key="history_date")
    st.markdown("---")
    try:
        data = api_get('/history', {'session_id': st.session_state.session_id})
        hist = data.get('data', data.get('history', []))
        if data.get('success') and hist:
            for msg in hist:
                st.markdown(f'<div class="card" style="padding:16px;"><div style="display:flex;justify-content:space-between;align-items:start;"><div><div style="font-weight:600;font-size:0.9rem;">{msg["user_message"][:80]}{"..." if len(msg["user_message"])>80 else ""}</div><div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">{msg["bot_response"][:100]}{"..." if len(msg["bot_response"])>100 else ""}</div></div><div style="text-align:right;min-width:120px;"><span class="badge badge-info">{msg.get("intent","general")}</span><div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px;">{msg.get("timestamp","")}</div></div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">💬</div><div class="empty-title">No conversations yet</div><div class="empty-desc">Start chatting and your history will appear here</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="empty-state"><div class="empty-icon">💬</div><div class="empty-title">No conversations yet</div><div class="empty-desc">Start chatting and your history will appear here</div></div>', unsafe_allow_html=True)

# ============================================================
# UNIVERSITY INFO
# ============================================================
def page_university_info():
    st.markdown("## 🏛️ University Information")
    st.markdown(f'<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">{UNIVERSITY_INFO["name"]}</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Admissions", "💰 Fee Structure", "📚 Programs", "📅 Academic Calendar", "🏆 Scholarships", "📞 Contact"])
    with tab1:
        st.markdown("### Admission Process")
        st.markdown('<div class="card"><h4 style="margin-top:0;">How to Apply</h4><ol style="font-size:0.9rem;line-height:1.8;"><li>Visit the IIUI admissions portal</li><li>Create an account and fill the online application</li><li>Upload required documents</li><li>Pay the application fee</li><li>Appear for the entry test</li><li>Attend the interview</li><li>Check results on the portal</li></ol><p style="font-size:0.85rem;color:var(--text-secondary);margin-top:12px;"><strong>Admission Weightage:</strong> 40% Entry Test + 40% Academic Qualification + 20% Interview</p></div>', unsafe_allow_html=True)
    with tab2:
        st.markdown("### Fee Structure")
        st.markdown('<div class="card"><p style="font-size:0.85rem;color:var(--text-secondary);">Fee structure varies by program and semester.</p><div class="data-table"><table><tr><th>Program</th><th>Admission Fee</th><th>Semester Fee</th></tr><tr><td>BS Computer Science</td><td>Rs. 102,000</td><td>Rs. 45,000 - 55,000</td></tr><tr><td>B.Ed Programs</td><td>Rs. 53,300</td><td>Rs. 25,000 - 35,000</td></tr><tr><td>BS Engineering</td><td>Rs. 95,000</td><td>Rs. 40,000 - 50,000</td></tr><tr><td>Masters Programs</td><td>Rs. 45,000</td><td>Rs. 20,000 - 30,000</td></tr></table></div><p style="font-size:0.8rem;color:var(--warning);margin-top:12px;">⚠️ These are approximate figures. Please verify with the official IIUI fee schedule.</p></div>', unsafe_allow_html=True)
    with tab3:
        st.markdown("### Academic Programs")
        for faculty, progs in [("Faculty of Computing & Mathematics", ["BS Computer Science", "BS Data Science", "BS Software Engineering", "BS Mathematics"]), ("Faculty of Engineering", ["BS Electrical Engineering", "BS Civil Engineering", "BS Mechanical Engineering"]), ("Faculty of Management Sciences", ["BBA", "MBA", "BS Accounting & Finance"]), ("Faculty of Social Sciences", ["BS Psychology", "BS Sociology", "BS International Relations"]), ("Faculty of Languages & Literature", ["BS English Literature", "BS Arabic", "BS Urdu"]), ("Faculty of Islamic Studies", ["BS Islamic Studies", "BS Shariah & Law"])]:
            with st.expander(f"🏛️ {faculty}"):
                for p in progs: st.markdown(f"• {p}")
    with tab4:
        st.markdown("### Academic Calendar")
        st.markdown('<div class="card"><p style="font-size:0.85rem;">📅 <strong>Fall Semester 2026</strong></p><ul style="font-size:0.85rem;line-height:1.8;"><li>Classes Begin: September 1, 2026</li><li>Mid-Term Exams: October 15-22, 2026</li><li>Final Exams: December 10-25, 2026</li><li>Results Announcement: January 10, 2027</li></ul><p style="font-size:0.8rem;color:var(--warning);">⚠️ This is indicative. Check official IIUI calendar for exact dates.</p></div>', unsafe_allow_html=True)
    with tab5:
        st.markdown("### Scholarships")
        st.markdown('<div class="card"><ul style="font-size:0.85rem;line-height:1.8;"><li><strong>Merit Scholarship:</strong> Based on academic performance</li><li><strong>Need-Based Financial Aid:</strong> For students from low-income families</li><li><strong>HEC Need-Based Scholarship:</strong> Government-funded assistance</li><li><strong>Alumni Scholarship:</strong> Funded by IIUI alumni association</li><li><strong>Sports Scholarship:</strong> For outstanding athletes</li></ul><p style="font-size:0.8rem;color:var(--warning);">⚠️ Verify availability and criteria with the IIUI scholarship office.</p></div>', unsafe_allow_html=True)
    with tab6:
        st.markdown("### Contact Information")
        st.markdown('<div class="card"><p style="font-size:0.85rem;line-height:2;">🌐 Website: <a href="https://www.iiu.edu.pk/" target="_blank">www.iiu.edu.pk</a><br>📍 Address: H-9, Islamabad, Pakistan<br>📞 Phone: +92-51-9018000<br>⏰ Office Hours: Monday to Friday, 8:00 AM to 5:00 PM</p></div>', unsafe_allow_html=True)

# ============================================================
# ACADEMIC
# ============================================================
def page_academic():
    st.markdown("## 📚 Academic Assistance")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">Access course guidance, exam schedules, and assignment reminders.</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 Course Guidance", "📅 Exam Schedule", "📝 Assignments"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            selected_sem = st.selectbox("Select Semester", ["All"] + [f"Semester {i}" for i in range(1, 9)], key="course_sem")
        with col2:
            selected_dept = st.text_input("Department Filter", placeholder="e.g., Computer Science", key="course_dept")
        try:
            params = {}
            if selected_sem != "All":
                sem_num = int(selected_sem.split()[-1])
                params['semester'] = sem_num
            if selected_dept:
                params['department'] = selected_dept
            data = api_get('/courses', params if params else None)
            if data.get('success') and data.get('data'):
                courses = data['data']
                if courses:
                    st.markdown(f"**{len(courses)} course(s) found**")
                    for course in courses:
                        st.markdown(f'<div class="card" style="padding:14px 18px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="font-weight:600;font-size:0.95rem;">{course.get("code","")} - {course.get("name","")}</div><div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">Semester {course.get("semester","?")} | {course.get("department","N/A")} | {course.get("credits","?")} Credits</div></div><span class="badge badge-success">Active</span></div>{"<div style='margin-top:8px;font-size:0.8rem;color:var(--text-secondary);'>" + course.get("description","") + "</div>" if course.get("description") else ""}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="empty-state"><div class="empty-icon">📖</div><div class="empty-title">No courses found for {selected_sem}</div><div class="empty-desc">Courses can be added by admin via Knowledge Base.</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state"><div class="empty-icon">📖</div><div class="empty-title">No course data available</div><div class="empty-desc">Ask your admin to add course information to the Knowledge Base.</div></div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load courses</div><div class="empty-desc">Make sure the Flask backend is running.</div></div>', unsafe_allow_html=True)
    with tab2:
        st.markdown("### 📅 Examination Information")
        try:
            data = api_get('/knowledge', {'category': 'Examinations'})
            if data.get('success') and data.get('data'):
                entries = data['data']
                if entries:
                    for entry in entries:
                        st.markdown(f'<div class="card" style="padding:14px 18px;"><div style="font-weight:600;font-size:0.9rem;">{entry.get("question","")}</div><div style="font-size:0.85rem;color:var(--text-secondary);margin-top:8px;line-height:1.6;">{entry.get("answer","")}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="empty-state"><div class="empty-icon">📅</div><div class="empty-title">No examination schedule configured</div><div class="empty-desc">Exam schedule information can be added by admin via Knowledge Base.</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state"><div class="empty-icon">📅</div><div class="empty-title">No examination data available</div><div class="empty-desc">Ask your admin to add examination information.</div></div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load exam data</div></div>', unsafe_allow_html=True)
    with tab3:
        st.markdown("### 📝 Assignment Reminders")
        if not st.session_state.get('logged_in'):
            st.markdown('<div class="empty-state"><div class="empty-icon">🔒</div><div class="empty-title">Please login to view reminders</div></div>', unsafe_allow_html=True)
        else:
            try:
                data = api_get('/reminders')
                if data.get('success') and data.get('data'):
                    reminders = data['data']
                    if reminders:
                        for r in reminders:
                            type_icon = '📅' if r.get('type') == 'exam' else '📝' if r.get('type') == 'assignment' else '📌'
                            status_badge = 'badge-warning' if r.get('status') == 'pending' else 'badge-success'
                            st.markdown(f'<div class="card" style="padding:14px 18px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="font-weight:600;font-size:0.9rem;">{type_icon} {r.get("title","")}</div><div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">Due: {r.get("reminder_date","N/A")}</div>{"<div style=\"font-size:0.8rem;color:var(--text-secondary);margin-top:4px;\">" + r.get("description","") + "</div>" if r.get("description") else ""}</div><span class="badge {status_badge}">{r.get("status","pending").title()}</span></div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="empty-state"><div class="empty-icon">📝</div><div class="empty-title">No assignment reminders yet</div><div class="empty-desc">Reminders will appear here when created.</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="empty-state"><div class="empty-icon">📝</div><div class="empty-title">No reminders configured</div><div class="empty-desc">Assignment and exam reminders can be set up via the API.</div></div>', unsafe_allow_html=True)
            except Exception:
                st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load reminders</div></div>', unsafe_allow_html=True)

# ============================================================
# PROFILE & SETTINGS
# ============================================================
def page_profile():
    if not st.session_state.get('logged_in'):
        st.markdown('<div class="empty-state"><div class="empty-icon">🔒</div><div class="empty-title">Please login to view your profile</div></div>', unsafe_allow_html=True)
        if st.button("Go to Login", type="primary"):
            st.session_state.auth_page = 'login'
            st.rerun()
        return
    st.markdown("## 👤 Profile")
    user = st.session_state.user_info
    if user:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f'<div class="card" style="text-align:center;padding:24px;"><div style="font-size:3rem;margin-bottom:8px;">👤</div><div style="font-size:1.1rem;font-weight:700;">{user.get("name","User")}</div><div style="font-size:0.85rem;color:var(--text-secondary);">{user.get("email","")}</div><div style="margin-top:8px;"><span class="badge badge-primary">{user.get("role","student").title()}</span></div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card"><h4 style="margin-top:0;">Account Information</h4></div>', unsafe_allow_html=True)
            st.text_input("Full Name", value=user.get('name',''), key="profile_name")
            st.text_input("Email", value=user.get('email',''), key="profile_email", disabled=True)
            st.text_input("Role", value=user.get('role','').title(), key="profile_role", disabled=True)
            st.markdown("---")
            st.markdown("#### Change Password")
            new_pass = st.text_input("New Password", type="password", key="profile_new_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="profile_confirm_pass")
            if st.button("Update Profile", type="primary", key="update_profile"):
                if new_pass and confirm_pass:
                    if new_pass != confirm_pass: st.error("Passwords do not match.")
                    elif len(new_pass) < 6: st.error("Password must be at least 6 characters.")
                    else: st.success("Profile updated successfully! (Backend integration pending)")
                else: st.info("Profile update will be connected in Phase 4.")

def _render_ai_configuration():
    """Render AI Configuration section for admin users."""
    st.markdown("### 🤖 AI Configuration")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:16px;">Configure the Live AI provider that powers the AI Assistant mode.</div>', unsafe_allow_html=True)

    # Load current config
    cfg_data = api_get('/settings/ai')
    cfg = cfg_data.get('data', {}) if cfg_data.get('success') else {}

    # Provider selection
    providers_data = api_get('/settings/ai/providers')
    providers = providers_data.get('data', []) if providers_data.get('success') else []
    provider_ids = [p['id'] for p in providers]
    provider_names = [p['name'] for p in providers]

    current_provider = cfg.get('provider', '')
    provider_index = provider_ids.index(current_provider) if current_provider in provider_ids else 0

    col1, col2 = st.columns(2)
    with col1:
        selected_provider = st.selectbox("AI Provider", provider_names, index=provider_index, key="ai_provider")
        selected_provider_id = provider_ids[provider_names.index(selected_provider)] if selected_provider in provider_names else provider_ids[0]
    with col2:
        model = st.text_input("Model", value=cfg.get('model', ''), placeholder="e.g., gpt-3.5-turbo, claude-3-haiku-20240307", key="ai_model")

    # API Key (masked display)
    api_key_display = cfg.get('api_key_display', '')
    api_key = st.text_input("API Key", value='', placeholder=f"Current: {api_key_display or 'Not set'}", type="password", key="ai_api_key", help="Your API key is stored securely and never displayed in full.")

    # Base URL (for custom providers)
    base_url = st.text_input("Base URL (optional)", value=cfg.get('base_url', ''), placeholder="e.g., http://localhost:11434/v1", key="ai_base_url", help="Required only for Custom/Local providers.")

    # Parameters
    col3, col4 = st.columns(2)
    with col3:
        temperature = st.slider("Temperature", 0.0, 2.0, float(cfg.get('temperature', 0.7)), 0.1, key="ai_temperature", help="Lower = more focused, Higher = more creative")
    with col4:
        max_tokens = st.number_input("Max Tokens", min_value=1, max_value=8192, value=int(cfg.get('max_tokens', 500)), key="ai_max_tokens", help="Maximum response length")

    # Enable/Disable
    enabled = st.toggle("Enable Live AI", value=bool(cfg.get('enabled', False)), key="ai_enabled", help="Enable or disable the Live AI mode for all users")

    # Status indicator
    if cfg.get('enabled') and cfg.get('provider'):
        st.markdown('<div style="padding:8px 12px;background:#D1FAE5;border-radius:8px;font-size:0.85rem;color:#065F46;">✅ Live AI is enabled</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:8px 12px;background:#FEF3C7;border-radius:8px;font-size:0.85rem;color:#92400E;">⚠️ Live AI is not configured or disabled</div>', unsafe_allow_html=True)

    # Buttons
    bc1, bc2, bc3 = st.columns([1, 1, 4])
    with bc1:
        if st.button("💾 Save Configuration", type="primary", key="save_ai_config"):
            payload = {
                'provider': selected_provider_id,
                'model': model,
                'base_url': base_url,
                'temperature': temperature,
                'max_tokens': max_tokens,
                'enabled': enabled,
            }
            if api_key:
                payload['api_key'] = api_key
            result = api_put('/settings/ai', payload)
            if result.get('success'):
                st.success("AI configuration saved successfully!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(result.get('message', 'Failed to save configuration.'))
    with bc2:
        if st.button("🔌 Test Connection", key="test_ai_connection"):
            with st.spinner("Testing connection..."):
                result = api_post('/settings/ai/test')
                if result.get('success'):
                    st.success(result.get('message', 'Connection successful!'))
                else:
                    st.error(result.get('message', 'Connection test failed.'))

    # Security notice
    st.markdown('---')
    st.markdown('<div style="padding:10px 14px;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;font-size:0.8rem;color:#1E40AF;">🔒 <strong>Security:</strong> API keys are stored securely in the database. Full keys are never displayed in the UI, logged, or returned in API responses.</div>', unsafe_allow_html=True)


def page_settings():
    st.markdown("## ⚙️ Settings")
    if is_admin():
        tab1, tab2, tab3, tab4 = st.tabs(["Account", "AI Configuration", "Preferences", "About"])
    else:
        tab1, tab3, tab4 = st.tabs(["Account", "Preferences", "About"])
        tab2 = None
    with tab1:
        st.markdown("### Account Settings")
        user = st.session_state.user_info
        if user:
            st.markdown(f'<div class="card"><p style="font-size:0.9rem;"><strong>Email:</strong> {user.get("email","")}</p><p style="font-size:0.9rem;"><strong>Role:</strong> {user.get("role","").title()}</p></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Danger Zone")
        st.markdown('<div style="border:1px solid var(--danger);border-radius:8px;padding:16px;background:#FEF2F2;"><p style="font-size:0.9rem;font-weight:600;color:var(--danger);">Delete Account</p><p style="font-size:0.8rem;color:var(--text-secondary);">This action cannot be undone.</p></div>', unsafe_allow_html=True)
        if st.button("Delete Account", key="delete_account", type="secondary"):
            st.warning("Account deletion will be available in Phase 4.")
    if tab2 is not None:
        with tab2:
            _render_ai_configuration()
    with tab3:
        st.markdown("### Preferences")
        st.checkbox("Email notifications", value=False, key="email_notif")
        st.checkbox("Browser notifications", value=False, key="browser_notif")
        st.checkbox("Show confidence scores", value=True, key="show_conf")
        st.checkbox("Auto-suggest questions", value=True, key="auto_suggest")
        st.info("Preference saving will be connected in Phase 4.")
    with tab4:
        st.markdown("### About")
        st.markdown(f'<div class="card"><h4 style="margin-top:0;">IIUI Smart Chatbot</h4><p style="font-size:0.85rem;line-height:1.8;"><strong>Version:</strong> 1.0<br><strong>University:</strong> {UNIVERSITY_INFO["name"]}<br><strong>Purpose:</strong> AI-Powered University Support<br><strong>Technology:</strong> Python, Streamlit, Flask, NLTK, spaCy, SQLite<br><strong>Project Type:</strong> BS Final Year Project</p></div>', unsafe_allow_html=True)

# ============================================================
# ADMIN PAGES
# ============================================================
def page_admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">System overview and management console.</div>', unsafe_allow_html=True)
    # Fetch real stats
    stats = {"users": "—", "chats": "—", "live": "—", "mock": "—", "kb": "—"}
    try:
        monitoring = api_get('/admin/monitoring')
        if monitoring.get('success') and monitoring.get('data'):
            d = monitoring['data']
            stats['users'] = d.get('total_users', '—')
            stats['chats'] = d.get('total_chats', '—')
            stats['live'] = d.get('total_live_chats', '—')
            stats['mock'] = d.get('total_mock_chats', '—')
            stats['kb'] = d.get('total_knowledge', '—')
    except Exception:
        pass
    s1, s2, s3, s4, s5 = st.columns(5)
    for col, (icon, label, value) in zip([s1, s2, s3, s4, s5], [("👥", "Total Users", stats['users']), ("💬", "Total Chats", stats['chats']), ("🤖", "Live AI Queries", stats['live']), ("📋", "Mock Queries", stats['mock']), ("📖", "KB Entries", stats['kb'])]):
        with col:
            st.markdown(f'<div class="stat-card"><div style="font-size:1.5rem;">{icon}</div><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    left, right = st.columns(2)
    with left:
        st.markdown("### 📈 Recent Activity")
        try:
            data = api_get('/faqs')
            if data.get('success') and data.get('faqs'):
                for faq in data['faqs'][:5]:
                    st.markdown(f'<div class="card" style="padding:10px 14px;"><div style="font-size:0.85rem;font-weight:500;">{faq["question"][:60]}{"..." if len(faq["question"])>60 else ""}</div><div style="font-size:0.75rem;color:var(--text-muted);margin-top:2px;"><span class="badge badge-primary">{faq.get("category","General")}</span></div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state" style="padding:24px;"><div class="empty-icon">📊</div><div class="empty-title">No activity data yet</div></div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div class="empty-state" style="padding:24px;"><div class="empty-icon">📊</div><div class="empty-title">No activity data yet</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown("### ⚙️ Quick Actions")
        for label, page_key in [("📖 Manage Knowledge Base", "admin_knowledge"), ("❓ Manage FAQs", "admin_faqs"), ("👥 Manage Users", "admin_users"), ("📝 View Chat Logs", "admin_chat_logs")]:
            if st.button(label, use_container_width=True, key=f"qa_{page_key}"):
                navigate_to(page_key)

KB_CATEGORIES = ["Admissions", "Courses", "Fees", "Examinations", "Scholarships", "Academic Policies", "Rules", "Schedules", "University Services", "Student Services", "General"]

def page_admin_knowledge():
    st.markdown("## 📖 Knowledge Base Management")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">Manage the knowledge base that powers the Mock Data Assistant. Only active entries are available to the chatbot.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: kb_search = st.text_input("🔍 Search entries...", key="kb_search")
    with c2: kb_category = st.selectbox("Category", ["All"] + KB_CATEGORIES, key="kb_category")
    with c3:
        if st.button("➕ Add Entry", type="primary", key="add_kb_entry"):
            st.session_state.show_add_kb = True
    st.markdown("---")

    # Handle edit mode
    editing_id = st.session_state.get('editing_kb_id')
    if editing_id:
        _render_kb_edit_form(editing_id)
        return

    try:
        # Use correct endpoint: /api/knowledge
        params = {}
        if kb_category and kb_category != "All":
            params['category'] = kb_category
        data = api_get('/knowledge', params if params else None)
        if data.get('success') and data.get('data'):
            entries = data['data']
            # Client-side search filter
            if kb_search:
                q = kb_search.lower()
                entries = [e for e in entries if q in (e.get('question','') + e.get('answer','') + e.get('keywords','') + e.get('category','')).lower()]
            if entries:
                st.markdown(f"**{len(entries)} entries found**")
                for entry in entries:
                    status_badge = 'badge-success' if entry.get('status') == 'active' else 'badge-warning'
                    status_label = entry.get('status', 'active').title()
                    with st.expander(f"**{entry['question'][:80]}**"):
                        st.markdown(f"**Answer:** {entry['answer']}")
                        if entry.get('keywords'):
                            st.markdown(f"**Keywords:** {entry['keywords']}")
                        st.markdown(f'<div style="margin-top:8px;display:flex;gap:8px;"><span class="badge badge-primary">{entry.get("category","General")}</span><span class="badge {status_badge}">{status_label}</span></div>', unsafe_allow_html=True)
                        st.caption(f"ID: {entry['id']} | Updated: {entry.get('updated_at', 'N/A')}")
                        ec1, ec2, ec3 = st.columns(3)
                        with ec1:
                            if st.button("✏️ Edit", key=f"edit_kb_{entry['id']}"):
                                st.session_state.editing_kb_id = entry['id']
                                st.rerun()
                        with ec2:
                            new_status = 'inactive' if entry.get('status') == 'active' else 'active'
                            label = '🔴 Deactivate' if entry.get('status') == 'active' else '🟢 Activate'
                            if st.button(label, key=f"toggle_kb_{entry['id']}"):
                                result = api_put(f"/knowledge/{entry['id']}", {'status': new_status})
                                if result.get('success'): st.success(f"Entry {new_status}"); st.rerun()
                                else: st.error(result.get('message', 'Failed'))
                        with ec3:
                            if st.button("🗑️ Delete", key=f"del_kb_{entry['id']}"):
                                if st.session_state.get(f'confirm_del_kb_{entry["id"]}'):
                                    result = api_post(f"/knowledge/{entry['id']}", None)
                                    # Use DELETE method via direct request
                                    import requests as _req
                                    try:
                                        _r = _req.delete(f"{FLASK_API_URL}/knowledge/{entry['id']}", headers=_auth_headers(), timeout=10)
                                        _d = _r.json()
                                        if _d.get('success'): st.success("Entry deleted"); st.rerun()
                                        else: st.error(_d.get('message', 'Failed'))
                                    except Exception as ex: st.error(str(ex))
                                else:
                                    st.session_state[f'confirm_del_kb_{entry["id"]}'] = True
                                    st.warning("Click Delete again to confirm.")
            else:
                st.markdown(f'<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-title">No entries match your search</div><div class="empty-desc">Try a different search term or category</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">📖</div><div class="empty-title">No knowledge base entries</div><div class="empty-desc">Add entries to power the Mock Data Assistant</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load knowledge base</div><div class="empty-desc">Make sure the Flask backend is running</div></div>', unsafe_allow_html=True)

    if st.session_state.get('show_add_kb', False):
        st.markdown("---")
        st.markdown("### ➕ Add New Knowledge Base Entry")
        new_q = st.text_area("Question", placeholder="e.g., What is the BSCS admission fee?", key="new_kb_q")
        new_a = st.text_area("Answer", placeholder="e.g., The BSCS admission fee is Rs. 85,000.", key="new_kb_a")
        new_cat = st.selectbox("Category", KB_CATEGORIES, key="new_kb_cat")
        new_kw = st.text_input("Keywords (comma-separated)", placeholder="e.g., admission, fee, bs cs", key="new_kb_kw")
        bc1, bc2 = st.columns([1, 4])
        with bc1:
            if st.button("Save Entry", type="primary", key="save_kb_entry"):
                if new_q and new_a:
                    result = api_post('/knowledge', {'question': new_q, 'answer': new_a, 'category': new_cat, 'keywords': new_kw})
                    if result.get('success'): st.success("Entry added successfully!"); st.session_state.show_add_kb = False; st.rerun()
                    else: st.error(result.get('message', 'Failed to add entry.'))
                else: st.warning("Please fill in both question and answer.")
        with bc2:
            if st.button("Cancel", key="cancel_kb_entry"):
                st.session_state.show_add_kb = False; st.rerun()


def _render_kb_edit_form(entry_id):
    """Render inline edit form for a knowledge base entry."""
    st.markdown("---")
    st.markdown(f"### ✏️ Edit Knowledge Base Entry (ID: {entry_id})")
    # Fetch current data
    data = api_get(f'/knowledge')
    entry = None
    if data.get('success') and data.get('data'):
        for e in data['data']:
            if e['id'] == entry_id:
                entry = e
                break
    # Also try fetching all entries (admin can see inactive)
    if not entry:
        import requests as _req
        try:
            _r = _req.get(f"{FLASK_API_URL}/knowledge", headers=_auth_headers(), timeout=10)
            _d = _r.json()
            if _d.get('success') and _d.get('data'):
                for e in _d['data']:
                    if e['id'] == entry_id:
                        entry = e
                        break
        except Exception:
            pass
    if not entry:
        st.error("Could not load entry for editing.")
        if st.button("Back to list", key="back_from_kb_edit"):
            st.session_state.editing_kb_id = None
            st.rerun()
        return

    edit_q = st.text_area("Question", value=entry.get('question', ''), key="edit_kb_q")
    edit_a = st.text_area("Answer", value=entry.get('answer', ''), key="edit_kb_a")
    edit_cat = st.selectbox("Category", KB_CATEGORIES, index=KB_CATEGORIES.index(entry['category']) if entry.get('category') in KB_CATEGORIES else 0, key="edit_kb_cat")
    edit_kw = st.text_input("Keywords", value=entry.get('keywords', ''), key="edit_kb_kw")
    status_options = ['active', 'inactive']
    edit_status = st.selectbox("Status", status_options, index=status_options.index(entry.get('status', 'active')) if entry.get('status') in status_options else 0, key="edit_kb_status")
    ec1, ec2, ec3 = st.columns([1, 1, 4])
    with ec1:
        if st.button("💾 Save", type="primary", key="save_kb_edit"):
            if edit_q and edit_a:
                result = api_put(f"/knowledge/{entry_id}", {
                    'question': edit_q, 'answer': edit_a, 'category': edit_cat,
                    'keywords': edit_kw, 'status': edit_status
                })
                if result.get('success'):
                    st.success("Entry updated!")
                    st.session_state.editing_kb_id = None
                    st.rerun()
                else: st.error(result.get('message', 'Failed to update.'))
            else: st.warning("Question and answer are required.")
    with ec2:
        if st.button("❌ Cancel", key="cancel_kb_edit"):
            st.session_state.editing_kb_id = None
            st.rerun()

FAQ_CATEGORIES = ["Admissions", "Courses", "Fees", "Examinations", "Scholarships", "Academic Policies", "Rules", "Schedules", "University Services", "Student Services", "General"]

def page_admin_faqs():
    st.markdown("## ❓ FAQ Management")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">Manage frequently asked questions for the chatbot.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1: faq_search = st.text_input("🔍 Search FAQs...", key="faq_search")
    with c2:
        if st.button("➕ Add FAQ", type="primary", key="add_faq"):
            st.session_state.show_add_faq = True
    st.markdown("---")

    # Handle edit mode
    editing_id = st.session_state.get('editing_faq_id')
    if editing_id:
        _render_faq_edit_form(editing_id)
        return

    try:
        data = api_get('/faqs')
        if data.get('success') and data.get('data'):
            entries = data['data']
            # Client-side search filter
            if faq_search:
                q = faq_search.lower()
                entries = [e for e in entries if q in (e.get('question','') + e.get('answer','') + e.get('tags','') + e.get('category','')).lower()]
            if entries:
                st.markdown(f"**{len(entries)} FAQs found**")
                for faq in entries:
                    status_label = faq.get('status', 'published').title()
                    status_badge = 'badge-success' if faq.get('status') == 'published' else 'badge-warning'
                    with st.expander(f"**{faq['question'][:80]}**"):
                        st.markdown(f"**Answer:** {faq['answer']}")
                        if faq.get('tags'):
                            st.markdown(f"**Tags:** {faq['tags']}")
                        st.markdown(f'<div style="margin-top:8px;display:flex;gap:8px;"><span class="badge badge-primary">{faq.get("category","General")}</span><span class="badge {status_badge}">{status_label}</span></div>', unsafe_allow_html=True)
                        st.caption(f"ID: {faq['id']} | Updated: {faq.get('updated_at', 'N/A')}")
                        ec1, ec2, ec3 = st.columns(3)
                        with ec1:
                            if st.button("✏️ Edit", key=f"edit_faq_{faq['id']}"):
                                st.session_state.editing_faq_id = faq['id']
                                st.rerun()
                        with ec2:
                            status_options = ['published', 'draft', 'archived']
                            new_status = 'draft' if faq.get('status') == 'published' else 'published'
                            label = '📝 Set Draft' if faq.get('status') == 'published' else '✅ Publish'
                            if st.button(label, key=f"toggle_faq_{faq['id']}"):
                                result = api_put(f"/faqs/{faq['id']}", {'status': new_status})
                                if result.get('success'): st.success(f"FAQ status updated"); st.rerun()
                                else: st.error(result.get('message', 'Failed'))
                        with ec3:
                            if st.button("🗑️ Delete", key=f"del_faq_{faq['id']}"):
                                if st.session_state.get(f'confirm_del_faq_{faq["id"]}'):
                                    import requests as _req
                                    try:
                                        _r = _req.delete(f"{FLASK_API_URL}/faqs/{faq['id']}", headers=_auth_headers(), timeout=10)
                                        _d = _r.json()
                                        if _d.get('success'): st.success("FAQ deleted"); st.rerun()
                                        else: st.error(_d.get('message', 'Failed'))
                                    except Exception as ex: st.error(str(ex))
                                else:
                                    st.session_state[f'confirm_del_faq_{faq["id"]}'] = True
                                    st.warning("Click Delete again to confirm.")
            else:
                st.markdown(f'<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-title">No FAQs match your search</div><div class="empty-desc">Try a different search term</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">❓</div><div class="empty-title">No FAQs yet</div><div class="empty-desc">Add FAQs to help students get answers</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load FAQs</div><div class="empty-desc">Make sure the Flask backend is running</div></div>', unsafe_allow_html=True)

    if st.session_state.get('show_add_faq', False):
        st.markdown("---")
        st.markdown("### ➕ Add New FAQ")
        new_q = st.text_area("Question", key="new_faq_q")
        new_a = st.text_area("Answer", key="new_faq_a")
        new_cat = st.selectbox("Category", FAQ_CATEGORIES, key="new_faq_cat")
        new_tags = st.text_input("Tags", key="new_faq_tags")
        bc1, bc2 = st.columns([1, 4])
        with bc1:
            if st.button("Save FAQ", type="primary", key="save_faq"):
                if new_q and new_a:
                    result = api_post('/faqs', {'question': new_q, 'answer': new_a, 'category': new_cat, 'tags': new_tags})
                    if result.get('success'): st.success("FAQ added!"); st.session_state.show_add_faq = False; st.rerun()
                    else: st.error(result.get('message', 'Failed.'))
                else: st.warning("Fill in question and answer.")
        with bc2:
            if st.button("Cancel", key="cancel_faq"):
                st.session_state.show_add_faq = False; st.rerun()


def _render_faq_edit_form(entry_id):
    """Render inline edit form for an FAQ entry."""
    st.markdown("---")
    st.markdown(f"### ✏️ Edit FAQ (ID: {entry_id})")
    data = api_get('/faqs')
    entry = None
    if data.get('success') and data.get('data'):
        for e in data['data']:
            if e['id'] == entry_id:
                entry = e
                break
    if not entry:
        st.error("Could not load FAQ for editing.")
        if st.button("Back to list", key="back_from_faq_edit"):
            st.session_state.editing_faq_id = None
            st.rerun()
        return

    edit_q = st.text_area("Question", value=entry.get('question', ''), key="edit_faq_q")
    edit_a = st.text_area("Answer", value=entry.get('answer', ''), key="edit_faq_a")
    edit_cat = st.selectbox("Category", FAQ_CATEGORIES, index=FAQ_CATEGORIES.index(entry['category']) if entry.get('category') in FAQ_CATEGORIES else 0, key="edit_faq_cat")
    edit_tags = st.text_input("Tags", value=entry.get('tags', ''), key="edit_faq_tags")
    status_options = ['published', 'draft', 'archived']
    edit_status = st.selectbox("Status", status_options, index=status_options.index(entry.get('status', 'published')) if entry.get('status') in status_options else 0, key="edit_faq_status")
    ec1, ec2, ec3 = st.columns([1, 1, 4])
    with ec1:
        if st.button("💾 Save", type="primary", key="save_faq_edit"):
            if edit_q and edit_a:
                result = api_put(f"/faqs/{entry_id}", {
                    'question': edit_q, 'answer': edit_a, 'category': edit_cat,
                    'tags': edit_tags, 'status': edit_status
                })
                if result.get('success'):
                    st.success("FAQ updated!")
                    st.session_state.editing_faq_id = None
                    st.rerun()
                else: st.error(result.get('message', 'Failed to update.'))
            else: st.warning("Question and answer are required.")
    with ec2:
        if st.button("❌ Cancel", key="cancel_faq_edit"):
            st.session_state.editing_faq_id = None
            st.rerun()

def page_admin_chatbot():
    st.markdown("## 🤖 Chatbot Management")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">Monitor and configure chatbot responses.</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Overview", "Response Settings", "Fallback Messages"])
    with tab1:
        st.markdown('<div class="card"><h4 style="margin-top:0;">Chatbot Status</h4><p style="font-size:0.85rem;"><span class="status-indicator"><span class="status-dot online"></span><span style="color:var(--success);">System Online</span></span></p><p style="font-size:0.85rem;color:var(--text-secondary);line-height:1.8;">• NLP Engine: NLTK + spaCy (Active)<br>• ML Model: Sentence Transformers + FAISS (Active)<br>• Knowledge Base: SQLite (Connected)<br>• Voice: SpeechRecognition + gTTS (Available)</p></div>', unsafe_allow_html=True)
    with tab2:
        st.slider("Confidence Threshold", 0.0, 1.0, 0.6, 0.05, key="conf_thresh")
        st.slider("Max Results per Query", 1, 10, 3, key="max_results")
        st.info("These settings will be connected in Phase 10.")
    with tab3:
        st.text_area("Fallback 1", value="I'm sorry, I couldn't find specific information about that.", key="fb1", height=68)
        st.text_area("Fallback 2", value="I don't have enough information. Check the IIUI website.", key="fb2", height=68)
        st.text_area("Fallback 3", value="For detailed information, please visit the IIUI administration office.", key="fb3", height=68)
        st.info("Fallback message editing will be connected in Phase 10.")

def page_admin_users():
    st.markdown("## 👥 User Management")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">View and manage user accounts.</div>', unsafe_allow_html=True)
    try:
        data = api_get('/admin/users')
        if data.get('success') and data.get('data'):
            users = data['data']
            st.markdown(f"**Total Users: {len(users)}**")
            for user in users:
                role_color = "badge-danger" if user.get('role') == 'admin' else "badge-info" if user.get('role') == 'faculty' else "badge-primary"
                status_color = "badge-success" if user.get('status') == 'active' else "badge-warning"
                st.markdown(f'<div class="card" style="padding:14px 18px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="font-weight:600;">{user.get("name","User")}</div><div style="font-size:0.8rem;color:var(--text-secondary);">{user.get("email","")}</div></div><div style="display:flex;gap:8px;"><span class="badge {role_color}">{user.get("role","student").title()}</span><span class="badge {status_color}">{user.get("status","active").title()}</span></div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">👥</div><div class="empty-title">No users found</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load users</div><div class="empty-desc">Make sure the Flask backend is running</div></div>', unsafe_allow_html=True)

def page_admin_chat_logs():
    st.markdown("## 📝 Chat Logs")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">View all chatbot interactions for monitoring and analysis.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1: log_search = st.text_input("🔍 Search logs...", key="log_search")
    with c2: log_filter = st.selectbox("Filter", ["All", "Live AI", "Mock Data"], key="log_filter")
    st.markdown("---")
    try:
        data = api_get('/admin/chat-logs')
        if data.get('success') and data.get('data'):
            logs = data['data']
            # Filter by mode
            if log_filter and log_filter != "All":
                mode = 'live' if 'Live' in log_filter else 'mock'
                logs = [l for l in logs if l.get('mode') == mode]
            # Client-side search
            if log_search:
                q = log_search.lower()
                logs = [l for l in logs if q in (l.get('user_message','') + l.get('bot_response','') + l.get('user_email','')).lower()]
            if logs:
                st.markdown(f"**{len(logs)} logs found**")
                for log in logs[:20]:
                    mode_badge = 'badge-success' if log.get('mode') == 'live' else 'badge-warning'
                    mode_label = log.get('mode', 'mock').upper()
                    st.markdown(f'<div class="card" style="padding:12px 16px;"><div style="display:flex;justify-content:space-between;align-items:start;"><div style="flex:1;"><div style="font-weight:600;font-size:0.85rem;">{log.get("user_message","")[:80]}{"..." if len(log.get("user_message",""))>80 else ""}</div><div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">{log.get("bot_response","")[:100]}{"..." if len(log.get("bot_response",""))>100 else ""}</div></div><div style="text-align:right;min-width:120px;"><span class="badge {mode_badge}">{mode_label}</span><div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px;">{log.get("timestamp","")}</div></div></div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state"><div class="empty-icon">📝</div><div class="empty-title">No logs found</div><div class="empty-desc">No chat logs match your filter criteria</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">📝</div><div class="empty-title">No chat logs yet</div><div class="empty-desc">Logs will appear as users interact with the chatbot</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-title">Unable to load chat logs</div><div class="empty-desc">Make sure the Flask backend is running</div></div>', unsafe_allow_html=True)

def page_admin_analytics():
    st.markdown("## 📈 Analytics & Monitoring")
    st.markdown('<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">System performance and usage analytics.</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Usage Analytics", "System Performance", "Student Issues"])
    with tab1:
        st.markdown("### Chat Usage Statistics")
        try:
            data = api_get('/admin/analytics')
            if data.get('success') and data.get('data'):
                d = data['data']
                chat_stats = d.get('chat_stats', {})
                cols = st.columns(3)
                for col, label, value in zip(cols, ["Total Conversations", "Live AI Queries", "Mock Data Queries"],
                    [chat_stats.get('total_chats', 0), chat_stats.get('live_chats', 0), chat_stats.get('mock_chats', 0)]):
                    with col:
                        st.markdown(f'<div class="stat-card"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
                # Additional stats
                cols2 = st.columns(3)
                for col, label, value in zip(cols2, ["Total Users", "Total KB Entries", "Total FAQs"],
                    [d.get('total_users', 0), d.get('total_knowledge_entries', 0), d.get('total_faqs', 0)]):
                    with col:
                        st.markdown(f'<div class="stat-card"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
            else:
                st.info("Analytics data will populate as users interact with the chatbot.")
        except Exception:
            st.info("Analytics data will populate as users interact with the chatbot.")
    with tab2:
        st.markdown('<div class="card"><h4 style="margin-top:0;">System Performance</h4><p style="font-size:0.85rem;line-height:2;"><strong>NLP Engine:</strong> <span class="badge badge-success">Active</span><br><strong>ML Model:</strong> <span class="badge badge-success">Loaded</span><br><strong>Database:</strong> <span class="badge badge-success">Connected</span><br><strong>Backend API:</strong> <span class="badge badge-success">Running</span></p></div>', unsafe_allow_html=True)
    with tab3:
        try:
            data = api_get('/admin/analytics')
            if data.get('success') and data.get('data'):
                frequent = data['data'].get('frequent_queries', [])
                if frequent:
                    st.markdown("### Most Frequent Queries")
                    for fq in frequent:
                        st.markdown(f'<div class="card" style="padding:10px 14px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="font-size:0.85rem;font-weight:500;">{fq["query"]}</div><span class="badge badge-primary">{fq["count"]}x</span></div></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">No query data yet</div><div class="empty-desc">Most frequent issues will be tracked as queries come in</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">No data yet</div><div class="empty-desc">Most frequent issues will be tracked as queries come in</div></div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">No data yet</div></div>', unsafe_allow_html=True)

# ============================================================
# PAGE ROUTER
# ============================================================
def main():
    if not st.session_state.logged_in:
        if st.session_state.auth_page == 'register':
            page_register()
        else:
            page_login()
        return
    render_sidebar()
    page = st.session_state.current_page
    role = get_role()
    pages = {
        'dashboard': page_dashboard if role != 'admin' else page_admin_dashboard,
        'live_assistant': page_live_assistant, 'mock_assistant': page_mock_assistant,
        'chat_history': page_chat_history, 'university_info': page_university_info,
        'academic': page_academic, 'profile': page_profile, 'settings': page_settings,
        'admin_dashboard': page_admin_dashboard, 'admin_knowledge': page_admin_knowledge,
        'admin_faqs': page_admin_faqs, 'admin_chatbot': page_admin_chatbot,
        'admin_users': page_admin_users, 'admin_chat_logs': page_admin_chat_logs,
        'admin_analytics': page_admin_analytics,
    }
    pages.get(page, page_dashboard)()

if __name__ == "__main__":
    main()
