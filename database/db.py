"""
Database Manager - AI Chatbot for University Support
SQLite Database Layer - Phase 2 Implementation
Approved FYP Technology: SQLite
"""

import sys
import os
import sqlite3
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.db_path = DB_CONFIG['sqlite_path']
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
        self._create_tables()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _create_tables(self):
        conn = self._get_connection()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT DEFAULT '',
                role TEXT DEFAULT 'student' CHECK(role IN ('student','faculty','admin')),
                status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive','banned')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                tags TEXT DEFAULT '',
                category TEXT DEFAULT 'General',
                status TEXT DEFAULT 'published' CHECK(status IN ('published','draft','archived')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL DEFAULT 'General',
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                keywords TEXT DEFAULT '',
                status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department TEXT NOT NULL,
                person TEXT DEFAULT '',
                email TEXT DEFAULT '',
                phone TEXT DEFAULT '',
                office_location TEXT DEFAULT '',
                office_hours TEXT DEFAULT ''
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT DEFAULT 'New Conversation',
                mode TEXT NOT NULL DEFAULT 'mock' CHECK(mode IN ('mock','live')),
                status TEXT DEFAULT 'active' CHECK(status IN ('active','archived','deleted')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                sender TEXT NOT NULL CHECK(sender IN ('user','assistant','system')),
                message TEXT NOT NULL,
                mode TEXT NOT NULL DEFAULT 'mock' CHECK(mode IN ('mock','live')),
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT DEFAULT '',
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                confidence REAL DEFAULT 0.0,
                mode TEXT DEFAULT 'mock' CHECK(mode IN ('mock','live')),
                intent TEXT DEFAULT '',
                response_time_ms INTEGER DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                semester INTEGER DEFAULT 1,
                department TEXT DEFAULT '',
                credits INTEGER DEFAULT 3,
                description TEXT DEFAULT '',
                status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS academic_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                semester INTEGER DEFAULT NULL,
                status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT NOT NULL CHECK(type IN ('exam','assignment','general')),
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                reminder_date TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending','completed','cancelled')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS ai_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT DEFAULT '',
                model TEXT DEFAULT '',
                api_key_encrypted TEXT DEFAULT '',
                base_url TEXT DEFAULT '',
                temperature REAL DEFAULT 0.7,
                max_tokens INTEGER DEFAULT 500,
                enabled INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT DEFAULT '{}',
                user_id INTEGER DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        # Indexes
        c.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_faqs_category ON faqs(category)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_kb_category ON knowledge_base(category)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_kb_status ON knowledge_base(status)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_conv_user ON conversations(user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_conv_mode ON conversations(mode)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_msg_conv ON chat_messages(conversation_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_msg_mode ON chat_messages(mode)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_logs_mode ON chat_logs(mode)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_courses_sem ON courses(semester)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_reminders_user ON reminders(user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_analytics_type ON analytics(event_type)')

        conn.commit()
        conn.close()

    # ==================== USER METHODS ====================

    def add_user(self, email, password_hash, name="", role="student"):
        conn = self._get_connection()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (email, password_hash, name, role) VALUES (?, ?, ?, ?)",
                (email, password_hash, name, role)
            )
            conn.commit()
            uid = c.lastrowid
            conn.close()
            return uid
        except sqlite3.IntegrityError:
            conn.close()
            return None

    def get_user_by_email(self, email):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_id(self, user_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_users(self, limit=100, offset=0):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_total_users(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
        conn.close()
        return count

    def update_user(self, user_id, **kwargs):
        allowed = {"name", "role", "email", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [user_id]
        try:
            c.execute(f"UPDATE users SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", vals)
            conn.commit()
            ok = c.rowcount > 0
            conn.close()
            return ok
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def delete_user(self, user_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    # ==================== FAQ METHODS ====================

    def check_faq_duplicate(self, question, category):
        """Check if an FAQ with same question and category already exists."""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM faqs WHERE question = ? AND category = ?",
            (question, category)
        )
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def add_faq(self, question, answer, tags="", category="General"):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO faqs (question, answer, tags, category) VALUES (?, ?, ?, ?)",
            (question, answer, tags, category)
        )
        conn.commit()
        fid = c.lastrowid
        conn.close()
        return fid

    def get_all_faqs(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM faqs ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_faq_by_id(self, faq_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM faqs WHERE id = ?", (faq_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def search_faqs(self, query, limit=5):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM faqs WHERE question LIKE ? OR tags LIKE ? OR category LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", f"%{query}%", limit)
        )
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_faq(self, faq_id, **kwargs):
        allowed = {"question", "answer", "tags", "category", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [faq_id]
        c.execute(f"UPDATE faqs SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_faq(self, faq_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def get_total_faqs(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM faqs")
        count = c.fetchone()[0]
        conn.close()
        return count

    # ==================== KNOWLEDGE BASE METHODS ====================

    def check_knowledge_duplicate(self, category, question):
        """Check if a knowledge base entry with same category and question already exists."""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM knowledge_base WHERE category = ? AND question = ?",
            (category, question)
        )
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def add_knowledge(self, category, question, answer, keywords=""):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO knowledge_base (category, question, answer, keywords) VALUES (?, ?, ?, ?)",
            (category, question, answer, keywords)
        )
        conn.commit()
        kid = c.lastrowid
        conn.close()
        return kid

    def get_all_knowledge(self, category=None, status=None):
        conn = self._get_connection()
        c = conn.cursor()
        q = "SELECT * FROM knowledge_base WHERE 1=1"
        params = []
        if category:
            q += " AND category = ?"
            params.append(category)
        if status:
            q += " AND status = ?"
            params.append(status)
        q += " ORDER BY created_at DESC"
        c.execute(q, params)
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_knowledge_by_id(self, kb_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM knowledge_base WHERE id = ?", (kb_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def search_knowledge(self, query, limit=10):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM knowledge_base WHERE status = 'active' AND (question LIKE ? OR answer LIKE ? OR keywords LIKE ? OR category LIKE ?) LIMIT ?",
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", limit)
        )
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search_all_active(self, query, limit=10):
        """Search both knowledge_base and faqs for active entries.
        Returns combined results suitable for mock chatbot retrieval."""
        results = []
        # Search knowledge_base
        kb_results = self.search_knowledge(query, limit=limit)
        for r in kb_results:
            results.append({
                'source': 'knowledge_base',
                'question': r.get('question', ''),
                'answer': r.get('answer', ''),
                'category': r.get('category', ''),
                'keywords': r.get('keywords', ''),
            })
        # Search faqs
        faq_results = self.search_faqs(query, limit=limit)
        for r in faq_results:
            results.append({
                'source': 'faq',
                'question': r.get('question', ''),
                'answer': r.get('answer', ''),
                'category': r.get('category', ''),
                'keywords': r.get('tags', ''),
            })
        return results

    def update_knowledge(self, kb_id, **kwargs):
        allowed = {"category", "question", "answer", "keywords", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [kb_id]
        c.execute(f"UPDATE knowledge_base SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_knowledge(self, kb_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM knowledge_base WHERE id = ?", (kb_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def get_total_knowledge(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM knowledge_base")
        count = c.fetchone()[0]
        conn.close()
        return count

    # ==================== CONTACT METHODS ====================

    def add_contact(self, department, person="", email="", phone="", office_location="", office_hours=""):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO contacts (department, person, email, phone, office_location, office_hours) VALUES (?, ?, ?, ?, ?, ?)",
            (department, person, email, phone, office_location, office_hours)
        )
        conn.commit()
        cid = c.lastrowid
        conn.close()
        return cid

    def get_contacts(self, department=None):
        conn = self._get_connection()
        c = conn.cursor()
        if department:
            c.execute("SELECT * FROM contacts WHERE department LIKE ?", (f"%{department}%",))
        else:
            c.execute("SELECT * FROM contacts")
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_contact_by_id(self, contact_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_contact(self, contact_id, **kwargs):
        allowed = {"department", "person", "email", "phone", "office_location", "office_hours"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [contact_id]
        c.execute(f"UPDATE contacts SET {sets} WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_contact(self, contact_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def get_total_contacts(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM contacts")
        count = c.fetchone()[0]
        conn.close()
        return count

    # ==================== CONVERSATION METHODS ====================

    def create_conversation(self, user_id=None, title="New Conversation", mode="mock"):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO conversations (user_id, title, mode) VALUES (?, ?, ?)",
            (user_id, title, mode)
        )
        conn.commit()
        conv_id = c.lastrowid
        conn.close()
        return conv_id

    def get_conversations(self, user_id=None, mode=None, status="active"):
        conn = self._get_connection()
        c = conn.cursor()
        q = "SELECT * FROM conversations WHERE status = ?"
        params = [status]
        if user_id:
            q += " AND user_id = ?"
            params.append(user_id)
        if mode:
            q += " AND mode = ?"
            params.append(mode)
        q += " ORDER BY updated_at DESC"
        c.execute(q, params)
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_conversation_by_id(self, conv_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_conversation(self, conv_id, **kwargs):
        allowed = {"title", "mode", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [conv_id]
        c.execute(f"UPDATE conversations SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_conversation(self, conv_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("UPDATE conversations SET status = 'deleted' WHERE id = ?", (conv_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def get_total_conversations(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM conversations WHERE status = 'active'")
        count = c.fetchone()[0]
        conn.close()
        return count

    # ==================== CHAT MESSAGE METHODS ====================

    def add_message(self, conversation_id, sender, message, mode="mock", metadata=None):
        conn = self._get_connection()
        c = conn.cursor()
        meta_json = json.dumps(metadata or {})
        c.execute(
            "INSERT INTO chat_messages (conversation_id, sender, message, mode, metadata) VALUES (?, ?, ?, ?, ?)",
            (conversation_id, sender, message, mode, meta_json)
        )
        conn.commit()
        msg_id = c.lastrowid
        c.execute("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (conversation_id,))
        conn.commit()
        conn.close()
        return msg_id

    def get_messages(self, conversation_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,)
        )
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def delete_messages(self, conversation_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM chat_messages WHERE conversation_id = ?", (conversation_id,))
        conn.commit()
        conn.close()

    # ==================== CHAT LOG METHODS ====================

    def log_chat(self, user_email, user_message, bot_response,
                 confidence=0.0, mode="mock", intent="", response_time_ms=0):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO chat_logs (user_email, user_message, bot_response, confidence, mode, intent, response_time_ms) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_email, user_message, bot_response, confidence, mode, intent, response_time_ms)
        )
        conn.commit()
        conn.close()

    def get_chat_history(self, user_email, limit=50):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM chat_logs WHERE user_email = ? ORDER BY timestamp DESC LIMIT ?",
            (user_email, limit)
        )
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_recent_chats(self, limit=10):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_total_chats(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_logs")
        count = c.fetchone()[0]
        conn.close()
        return count

    def get_total_live_chats(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_logs WHERE mode = 'live'")
        count = c.fetchone()[0]
        conn.close()
        return count

    def get_total_mock_chats(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_logs WHERE mode = 'mock'")
        count = c.fetchone()[0]
        conn.close()
        return count

    # ==================== COURSE METHODS ====================

    def add_course(self, code, name, semester=1, department="", credits=3, description=""):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO courses (code, name, semester, department, credits, description) VALUES (?, ?, ?, ?, ?, ?)",
            (code, name, semester, department, credits, description)
        )
        conn.commit()
        cid = c.lastrowid
        conn.close()
        return cid

    def get_courses(self, semester=None, department=None):
        conn = self._get_connection()
        c = conn.cursor()
        q = "SELECT * FROM courses WHERE status = 'active'"
        params = []
        if semester:
            q += " AND semester = ?"
            params.append(semester)
        if department:
            q += " AND department LIKE ?"
            params.append(f"%{department}%")
        q += " ORDER BY semester, code"
        c.execute(q, params)
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_course(self, course_id, **kwargs):
        allowed = {"code", "name", "semester", "department", "credits", "description", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [course_id]
        c.execute(f"UPDATE courses SET {sets} WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_course(self, course_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("UPDATE courses SET status = 'inactive' WHERE id = ?", (course_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    # ==================== ACADEMIC INFO METHODS ====================

    def add_academic_info(self, category, title, content, semester=None):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO academic_info (category, title, content, semester) VALUES (?, ?, ?, ?)",
            (category, title, content, semester)
        )
        conn.commit()
        aid = c.lastrowid
        conn.close()
        return aid

    def get_academic_info(self, category=None, semester=None):
        conn = self._get_connection()
        c = conn.cursor()
        q = "SELECT * FROM academic_info WHERE status = 'active'"
        params = []
        if category:
            q += " AND category = ?"
            params.append(category)
        if semester:
            q += " AND (semester = ? OR semester IS NULL)"
            params.append(semester)
        q += " ORDER BY created_at DESC"
        c.execute(q, params)
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_academic_info(self, info_id, **kwargs):
        allowed = {"category", "title", "content", "semester", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [info_id]
        c.execute(f"UPDATE academic_info SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_academic_info(self, info_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("UPDATE academic_info SET status = 'inactive' WHERE id = ?", (info_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    # ==================== REMINDER METHODS ====================

    def add_reminder(self, user_id, type_, title, description="", reminder_date=""):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO reminders (user_id, type, title, description, reminder_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, type_, title, description, reminder_date)
        )
        conn.commit()
        rid = c.lastrowid
        conn.close()
        return rid

    def get_reminders(self, user_id=None, type_=None, status="pending"):
        conn = self._get_connection()
        c = conn.cursor()
        q = "SELECT * FROM reminders WHERE status = ?"
        params = [status]
        if user_id:
            q += " AND user_id = ?"
            params.append(user_id)
        if type_:
            q += " AND type = ?"
            params.append(type_)
        q += " ORDER BY reminder_date ASC"
        c.execute(q, params)
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_reminder(self, reminder_id, **kwargs):
        allowed = {"title", "description", "reminder_date", "status"}
        updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not updates:
            return False
        conn = self._get_connection()
        c = conn.cursor()
        sets = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [reminder_id]
        c.execute(f"UPDATE reminders SET {sets} WHERE id = ?", vals)
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    def delete_reminder(self, reminder_id):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("UPDATE reminders SET status = 'cancelled' WHERE id = ?", (reminder_id,))
        conn.commit()
        ok = c.rowcount > 0
        conn.close()
        return ok

    # ==================== AI CONFIG METHODS ====================

    def get_ai_config(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM ai_config ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def save_ai_config(self, provider="", model="", api_key="",
                       base_url="", temperature=0.7, max_tokens=500, enabled=False):
        conn = self._get_connection()
        c = conn.cursor()
        existing = self.get_ai_config()
        if existing:
            c.execute(
                "UPDATE ai_config SET provider=?, model=?, api_key_encrypted=?, base_url=?, temperature=?, max_tokens=?, enabled=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (provider, model, api_key, base_url, temperature,
                 max_tokens, 1 if enabled else 0, existing["id"])
            )
        else:
            c.execute(
                "INSERT INTO ai_config (provider, model, api_key_encrypted, base_url, temperature, max_tokens, enabled) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (provider, model, api_key, base_url, temperature,
                 max_tokens, 1 if enabled else 0)
            )
        conn.commit()
        conn.close()
        return True

    def get_ai_config_safe(self):
        cfg = self.get_ai_config()
        if cfg and cfg.get("api_key_encrypted"):
            key = cfg["api_key_encrypted"]
            if len(key) > 8:
                cfg["api_key_display"] = key[:4] + "*" * (len(key) - 8) + key[-4:]
            else:
                cfg["api_key_display"] = "****"
            cfg["api_key_encrypted"] = "***MASKED***"
        return cfg

    # ==================== ANALYTICS METHODS ====================

    def log_analytics(self, event_type, event_data=None, user_id=None):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO analytics (event_type, event_data, user_id) VALUES (?, ?, ?)",
            (event_type, json.dumps(event_data or {}), user_id)
        )
        conn.commit()
        conn.close()

    def get_analytics(self, event_type=None, limit=100):
        conn = self._get_connection()
        c = conn.cursor()
        q = "SELECT * FROM analytics"
        params = []
        if event_type:
            q += " WHERE event_type = ?"
            params.append(event_type)
        q += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        c.execute(q, params)
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_chat_stats(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_logs")
        total = c.fetchone()[0]
        c.execute("SELECT AVG(confidence) FROM chat_logs WHERE confidence > 0")
        avg_confidence = c.fetchone()[0] or 0
        c.execute(
            "SELECT intent, COUNT(*) as count FROM chat_logs WHERE intent != '' GROUP BY intent ORDER BY count DESC LIMIT 5"
        )
        top_intents = [{"intent": row[0], "count": row[1]} for row in c.fetchall()]
        c.execute("SELECT COUNT(*) FROM chat_logs WHERE mode = 'live'")
        live_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM chat_logs WHERE mode = 'mock'")
        mock_count = c.fetchone()[0]
        conn.close()
        return {
            "total_chats": total,
            "average_confidence": round(avg_confidence, 2),
            "top_intents": top_intents,
            "live_chats": live_count,
            "mock_chats": mock_count
        }

    def get_frequent_queries(self, limit=10):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT user_message, COUNT(*) as count FROM chat_logs GROUP BY user_message ORDER BY count DESC LIMIT ?",
            (limit,)
        )
        rows = c.fetchall()
        conn.close()
        return [{"query": row[0], "count": row[1]} for row in rows]
