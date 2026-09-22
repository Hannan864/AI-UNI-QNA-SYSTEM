"""
Flask Backend - AI Chatbot for University Support
Phase 3 Implementation - FYP Compliant
Approved Backend: Python + Flask
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from auth.login import AuthManager
from auth.session_manager import SessionManager
from models.generator import AnswerGenerator
from models.live_ai_service import LiveAIService
from models.chat_router import ChatRouter
from voice.speech_to_text import SpeechToText
from database.db import DatabaseManager
from config import SERVER_CONFIG
import json
import os
import re
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
os.makedirs("temp", exist_ok=True)

auth_manager = AuthManager()
session_manager = SessionManager()
answer_generator = AnswerGenerator()
live_ai_service = LiveAIService()
chat_router = ChatRouter()
speech_to_text = SpeechToText()
db = DatabaseManager()
auth_manager.create_default_admin()


def _ok(data=None, message="Success", status=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def _err(message="Error", status=400, code=None):
    body = {"success": False, "message": message}
    if code:
        body["error"] = {"code": code}
    return jsonify(body), status


def _get_session_email():
    session_id = request.headers.get("X-Session-Id") or request.args.get("session_id")
    if not session_id:
        return None
    return session_manager.validate_session(session_id)


def _require_auth():
    """Return (user_dict, error_response). user_dict includes id, email, role, etc."""
    email = _get_session_email()
    if not email:
        return None, _err("Authentication required. Please login.", 401)
    user = db.get_user_by_email(email)
    if not user:
        return None, _err("User not found.", 401)
    return user, None


def _require_role(allowed_roles):
    user, err = _require_auth()
    if err:
        return None, err
    if user["role"] not in allowed_roles:
        return None, _err("Access denied. Insufficient permissions.", 403)
    return user, None


@app.errorhandler(400)
def bad_request(error):
    return _err("Bad request. Please check your input.", 400)

@app.errorhandler(401)
def unauthorized(error):
    return _err("Authentication required. Please login.", 401)

@app.errorhandler(403)
def forbidden(error):
    return _err("Access denied. Insufficient permissions.", 403)

@app.errorhandler(404)
def not_found(error):
    return _err("Resource not found.", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return _err("Method not allowed.", 405)

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return _err("Internal server error. Please try again later.", 500)

@app.errorhandler(503)
def service_unavailable(error):
    return _err("Service temporarily unavailable.", 503)


@app.before_request
def handle_json_errors():
    if request.method in ("POST", "PUT", "PATCH"):
        ct = request.content_type or ""
        if "application/json" in ct:
            if not request.json and request.data:
                return _err("Invalid JSON format", 400)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    if not data:
        return _err("Request body required")
    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")
    name = (data.get("name") or "").strip()
    role = data.get("role", "student")
    if not email or not password:
        return _err("Email and password are required")
    if not name:
        return _err("Name is required")
    email_regex = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        return _err("Invalid email format")
    if len(password) < 6:
        return _err("Password must be at least 6 characters")
    # Prevent public admin registration - only allow student and faculty
    if role not in ("student", "faculty"):
        role = "student"
    existing = db.get_user_by_email(email)
    if existing:
        return _err("Email already registered", 409)
    user_id = auth_manager.register_user(email, password, name, role)
    if user_id:
        session_id = session_manager.create_session(email)
        db.log_analytics("user_registered", {"email": email, "role": role})
        return _ok(
            data={"id": user_id, "email": email, "name": name, "role": role, "session_id": session_id},
            message="Registration successful", status=201,
        )
    return _err("Registration failed", 500)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return _err("Request body required")
    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return _err("Email and password are required")
    user, message = auth_manager.authenticate_user(email, password)
    if user:
        session_id = session_manager.create_session(email)
        db.log_analytics("user_login", {"email": email})
        return _ok(data={
            "session_id": session_id,
            "user": {"email": user["email"], "name": user["name"], "role": user["role"]},
        }, message=message)
    return _err(message, 401)


@app.route("/api/logout", methods=["POST"])
def logout():
    session_id = request.headers.get("X-Session-Id") or (request.json or {}).get("session_id")
    if session_id:
        session_manager.end_session(session_id)
    return _ok(message="Logged out successfully")


@app.route("/api/profile", methods=["GET"])
def get_profile():
    user, err = _require_auth()
    if err:
        return err
    safe = {k: v for k, v in user.items() if k != "password_hash"}
    return _ok(data=safe)


@app.route("/api/profile", methods=["PUT"])
def update_profile():
    user, err = _require_auth()
    if err:
        return err
    data = request.json or {}
    name = (data.get("name") or "").strip()
    if not name:
        return _err("Name is required")
    ok = db.update_user(user["id"], name=name)
    if ok:
        return _ok(message="Profile updated")
    return _err("Update failed", 500)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    if not data:
        return _err("Request body required")
    message = (data.get("message") or "").strip()
    session_id = data.get("session_id")
    mode = data.get("mode", "mock")
    conversation_id = data.get("conversation_id")
    if not message:
        return _err("Message is required")
    if len(message) > 1000:
        return _err("Message too long (max 1000 characters)")
    if mode not in ("mock", "live"):
        mode = "mock"
    user_email = session_manager.validate_session(session_id) if session_id else "anonymous"
    if not user_email and session_id:
        return _err("Session expired", 401)

    # Centralized mode routing
    result = chat_router.route(
        message=message,
        mode=mode,
        user_email=user_email,
        conversation_id=conversation_id,
    )

    return _ok(data=result)


@app.route("/api/conversations", methods=["POST"])
def create_conversation():
    user, err = _require_auth()
    if err:
        return err
    data = request.json or {}
    title = (data.get("title") or "New Conversation").strip()
    mode = data.get("mode", "mock")
    if mode not in ("mock", "live"):
        mode = "mock"
    conv_id = db.create_conversation(user_id=user["id"], title=title, mode=mode)
    return _ok(data={"id": conv_id, "title": title, "mode": mode}, status=201)


@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    user, err = _require_auth()
    if err:
        return err
    mode = request.args.get("mode")
    convs = db.get_conversations(user_id=user["id"], mode=mode)
    return _ok(data=convs)


@app.route("/api/conversations/<int:conv_id>", methods=["GET"])
def get_conversation(conv_id):
    user, err = _require_auth()
    if err:
        return err
    conv = db.get_conversation_by_id(conv_id)
    if not conv:
        return _err("Conversation not found", 404)
    if conv.get("user_id") and conv["user_id"] != user["id"] and user["role"] != "admin":
        return _err("Access denied", 403)
    return _ok(data=conv)


@app.route("/api/conversations/<int:conv_id>/messages", methods=["GET"])
def get_conversation_messages(conv_id):
    user, err = _require_auth()
    if err:
        return err
    conv = db.get_conversation_by_id(conv_id)
    if not conv:
        return _err("Conversation not found", 404)
    if conv.get("user_id") and conv["user_id"] != user["id"] and user["role"] != "admin":
        return _err("Access denied", 403)
    return _ok(data=db.get_messages(conv_id))


@app.route("/api/conversations/<int:conv_id>", methods=["DELETE"])
def delete_conversation(conv_id):
    user, err = _require_auth()
    if err:
        return err
    conv = db.get_conversation_by_id(conv_id)
    if not conv:
        return _err("Conversation not found", 404)
    if conv.get("user_id") and conv["user_id"] != user["id"] and user["role"] != "admin":
        return _err("Access denied", 403)
    db.delete_conversation(conv_id)
    return _ok(message="Conversation deleted")


@app.route("/api/faqs", methods=["GET"])
def get_faqs():
    return _ok(data=db.get_all_faqs())


@app.route("/api/faqs/<int:faq_id>", methods=["GET"])
def get_faq(faq_id):
    entry = db.get_faq_by_id(faq_id)
    if not entry:
        return _err("FAQ not found", 404)
    return _ok(data=entry)


@app.route("/api/faqs/search", methods=["GET"])
def search_faqs():
    q = request.args.get("q", "").strip()
    if not q:
        return _err("Search query is required")
    return _ok(data=db.search_faqs(q))


@app.route("/api/faqs", methods=["POST"])
def create_faq():
    user, err = _require_role(["admin"])
    if err:
        return err
    data = request.json or {}
    question = (data.get("question") or "").strip()
    answer = (data.get("answer") or "").strip()
    if not question or not answer:
        return _err("Question and answer are required")
    category = (data.get("category") or "General").strip()
    tags = (data.get("tags") or "").strip()
    # Check for duplicate
    existing = db.check_faq_duplicate(question, category)
    if existing:
        return _err("A similar FAQ already exists in this category", 409)
    faq_id = db.add_faq(question, answer, tags, category)
    return _ok(data={"id": faq_id}, message="FAQ created", status=201)


@app.route("/api/faqs/<int:faq_id>", methods=["PUT"])
def update_faq(faq_id):
    user, err = _require_role(["admin"])
    if err:
        return err
    if not db.get_faq_by_id(faq_id):
        return _err("FAQ not found", 404)
    data = request.json or {}
    kwargs = {k: data[k] for k in ("question", "answer", "tags", "category", "status") if k in data}
    if not kwargs:
        return _err("No fields to update")
    db.update_faq(faq_id, **kwargs)
    return _ok(message="FAQ updated")


@app.route("/api/faqs/<int:faq_id>", methods=["DELETE"])
def delete_faq(faq_id):
    user, err = _require_role(["admin"])
    if err:
        return err
    if not db.get_faq_by_id(faq_id):
        return _err("FAQ not found", 404)
    db.delete_faq(faq_id)
    return _ok(message="FAQ deleted")


@app.route("/api/knowledge", methods=["GET"])
def list_knowledge():
    category = request.args.get("category")
    status_filter = request.args.get("status")
    email = _get_session_email()
    if email:
        user = db.get_user_by_email(email)
        if not (user and user["role"] == "admin"):
            status_filter = status_filter or "active"
    else:
        status_filter = status_filter or "active"
    return _ok(data=db.get_all_knowledge(category=category, status=status_filter))


@app.route("/api/knowledge/<int:kb_id>", methods=["GET"])
def get_knowledge(kb_id):
    entry = db.get_knowledge_by_id(kb_id)
    if not entry:
        return _err("Knowledge entry not found", 404)
    return _ok(data=entry)


@app.route("/api/knowledge/search", methods=["GET"])
def search_knowledge():
    q = request.args.get("q", "").strip()
    if not q:
        return _err("Search query is required")
    return _ok(data=db.search_knowledge(q))


@app.route("/api/knowledge", methods=["POST"])
def create_knowledge():
    user, err = _require_role(["admin"])
    if err:
        return err
    data = request.json or {}
    question = (data.get("question") or "").strip()
    answer = (data.get("answer") or "").strip()
    if not question or not answer:
        return _err("Question and answer are required")
    category = (data.get("category") or "General").strip()
    keywords = (data.get("keywords") or "").strip()
    # Check for duplicate
    existing = db.check_knowledge_duplicate(category, question)
    if existing:
        return _err("A similar knowledge entry already exists in this category", 409)
    kb_id = db.add_knowledge(category, question, answer, keywords)
    return _ok(data={"id": kb_id}, message="Knowledge entry created", status=201)


@app.route("/api/knowledge/<int:kb_id>", methods=["PUT"])
def update_knowledge(kb_id):
    user, err = _require_role(["admin"])
    if err:
        return err
    if not db.get_knowledge_by_id(kb_id):
        return _err("Knowledge entry not found", 404)
    data = request.json or {}
    kwargs = {k: data[k] for k in ("category", "question", "answer", "keywords", "status") if k in data}
    if not kwargs:
        return _err("No fields to update")
    db.update_knowledge(kb_id, **kwargs)
    return _ok(message="Knowledge entry updated")


@app.route("/api/knowledge/<int:kb_id>", methods=["DELETE"])
def delete_knowledge(kb_id):
    user, err = _require_role(["admin"])
    if err:
        return err
    if not db.get_knowledge_by_id(kb_id):
        return _err("Knowledge entry not found", 404)
    db.delete_knowledge(kb_id)
    return _ok(message="Knowledge entry deleted")


@app.route("/api/admin/users", methods=["GET"])
def admin_list_users():
    user, err = _require_role(["admin"])
    if err:
        return err
    users = db.get_all_users(limit=request.args.get("limit", 100, type=int), offset=request.args.get("offset", 0, type=int))
    return _ok(data=[{k: v for k, v in u.items() if k != "password_hash"} for u in users])


@app.route("/api/admin/users/<int:user_id>", methods=["PUT"])
def admin_update_user(user_id):
    user, err = _require_role(["admin"])
    if err:
        return err
    if not db.get_user_by_id(user_id):
        return _err("User not found", 404)
    data = request.json or {}
    kwargs = {k: data[k] for k in ("name", "role", "email", "status") if k in data}
    if not kwargs:
        return _err("No fields to update")
    if "role" in kwargs and kwargs["role"] not in ("student", "faculty", "admin"):
        return _err("Invalid role")
    if "status" in kwargs and kwargs["status"] not in ("active", "inactive", "banned"):
        return _err("Invalid status")
    if db.update_user(user_id, **kwargs):
        return _ok(message="User updated")
    return _err("Update failed", 500)


@app.route("/api/admin/users/<int:user_id>", methods=["DELETE"])
def admin_delete_user(user_id):
    user, err = _require_role(["admin"])
    if err:
        return err
    existing = db.get_user_by_id(user_id)
    if not existing:
        return _err("User not found", 404)
    if existing["id"] == user["id"]:
        return _err("Cannot delete your own account")
    if db.delete_user(user_id):
        return _ok(message="User deleted")
    return _err("Delete failed", 500)


@app.route("/api/admin/analytics", methods=["GET"])
def admin_analytics():
    user, err = _require_role(["admin"])
    if err:
        return err
    return _ok(data={
        "chat_stats": db.get_chat_stats(), "total_users": db.get_total_users(),
        "total_faqs": db.get_total_faqs(), "total_knowledge_entries": db.get_total_knowledge(),
        "total_conversations": db.get_total_conversations(), "frequent_queries": db.get_frequent_queries(limit=10),
    })


@app.route("/api/admin/chat-logs", methods=["GET"])
def admin_chat_logs():
    user, err = _require_role(["admin"])
    if err:
        return err
    return _ok(data=db.get_recent_chats(limit=request.args.get("limit", 50, type=int)))


@app.route("/api/admin/monitoring", methods=["GET"])
def admin_monitoring():
    user, err = _require_role(["admin"])
    if err:
        return err
    return _ok(data={
        "total_users": db.get_total_users(), "total_chats": db.get_total_chats(),
        "total_live_chats": db.get_total_live_chats(), "total_mock_chats": db.get_total_mock_chats(),
        "total_faqs": db.get_total_faqs(), "total_knowledge": db.get_total_knowledge(),
        "total_conversations": db.get_total_conversations(), "status": "operational",
    })


@app.route("/api/settings/ai", methods=["GET"])
def get_ai_config():
    user, err = _require_role(["admin"])
    if err:
        return err
    return _ok(data=db.get_ai_config_safe())


@app.route("/api/settings/ai", methods=["PUT"])
def update_ai_config():
    user, err = _require_role(["admin"])
    if err:
        return err
    data = request.json or {}
    try:
        temperature = float(data.get("temperature", 0.7))
        if temperature < 0 or temperature > 2.0:
            return _err("Temperature must be between 0.0 and 2.0")
    except (ValueError, TypeError):
        return _err("Invalid temperature value")
    try:
        max_tokens = int(data.get("max_tokens", 500))
        if max_tokens < 1 or max_tokens > 8192:
            return _err("Max tokens must be between 1 and 8192")
    except (ValueError, TypeError):
        return _err("Invalid max tokens value")
    db.save_ai_config(
        provider=(data.get("provider") or "").strip(), model=(data.get("model") or "").strip(),
        api_key=(data.get("api_key") or "").strip(), base_url=(data.get("base_url") or "").strip(),
        temperature=temperature, max_tokens=max_tokens, enabled=bool(data.get("enabled", False)),
    )
    db.log_analytics("ai_config_updated", {"provider": data.get("provider", ""), "model": data.get("model", "")})
    return _ok(message="AI configuration saved")


@app.route("/api/settings/ai/test", methods=["POST"])
def test_ai_config():
    user, err = _require_role(["admin"])
    if err:
        return err
    result = live_ai_service.test_connection()
    if result.get("success"):
        return _ok(data=result, message=result.get("message", "Connection successful"))
    return _err(result.get("message", "Connection test failed"))


@app.route("/api/settings/ai/providers", methods=["GET"])
def get_ai_providers():
    user, err = _require_role(["admin"])
    if err:
        return err
    return _ok(data=live_ai_service.get_provider_list())


@app.route("/api/settings/ai/status", methods=["GET"])
def get_ai_status():
    """Public endpoint for checking if live AI is available (no key exposure)."""
    is_cfg = live_ai_service.is_configured()
    cfg = db.get_ai_config()
    status = "configured" if is_cfg else "not_configured"
    if cfg and not cfg.get("enabled"):
        status = "disabled"
    return _ok(data={"status": status})


@app.route("/api/chat/modes", methods=["GET"])
def get_chat_modes():
    """Public endpoint returning available chat modes and their status."""
    return _ok(data=chat_router.get_mode_status())


@app.route("/api/courses", methods=["GET"])
def list_courses():
    return _ok(data=db.get_courses(semester=request.args.get("semester", type=int), department=request.args.get("department")))


@app.route("/api/courses", methods=["POST"])
def create_course():
    user, err = _require_role(["admin"])
    if err:
        return err
    data = request.json or {}
    code = (data.get("code") or "").strip()
    name = (data.get("name") or "").strip()
    if not code or not name:
        return _err("Course code and name are required")
    cid = db.add_course(code, name, data.get("semester", 1), (data.get("department") or "").strip(), data.get("credits", 3), (data.get("description") or "").strip())
    return _ok(data={"id": cid}, message="Course created", status=201)


@app.route("/api/reminders", methods=["GET"])
def list_reminders():
    user, err = _require_auth()
    if err:
        return err
    return _ok(data=db.get_reminders(user_id=user["id"], type_=request.args.get("type")))


@app.route("/api/reminders", methods=["POST"])
def create_reminder():
    user, err = _require_auth()
    if err:
        return err
    data = request.json or {}
    title = (data.get("title") or "").strip()
    reminder_date = (data.get("reminder_date") or "").strip()
    if not title:
        return _err("Title is required")
    if not reminder_date:
        return _err("Reminder date is required")
    type_ = data.get("type", "general")
    if type_ not in ("exam", "assignment", "general"):
        type_ = "general"
    rid = db.add_reminder(user["id"], type_, title, (data.get("description") or "").strip(), reminder_date)
    return _ok(data={"id": rid}, message="Reminder created", status=201)


@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    return _ok(data=db.get_contacts(request.args.get("department")))


@app.route("/api/history", methods=["GET"])
def get_history():
    user, err = _require_auth()
    if err:
        return err
    return _ok(data=db.get_chat_history(user["email"]))


@app.route("/api/voice/transcribe", methods=["POST"])
def voice_transcribe():
    if "audio" not in request.files:
        return _err("Audio file required")
    audio_file = request.files["audio"]
    temp_path = f"temp/{audio_file.filename}"
    audio_file.save(temp_path)
    text = speech_to_text.transcribe_audio_file(temp_path)
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return _ok(data={"text": text})


@app.route("/api/nlp/process", methods=["POST"])
def nlp_process():
    """NLP processing endpoint - returns structured NLP analysis of a query."""
    user, err = _require_role(["admin"])
    if err:
        return err
    data = request.json
    if not data:
        return _err("Request body required")
    message = (data.get("message") or "").strip()
    if not message:
        return _err("Message is required")
    from models.nlp_processor import NLPProcessor
    from models.ml_classifier import MLClassifier
    nlp = NLPProcessor()
    ml = MLClassifier()
    nlp_result = nlp.process_query(message)
    ml_result = ml.predict(message)
    return _ok(data={"nlp": nlp_result, "ml": ml_result})


@app.route("/api/ml/status", methods=["GET"])
def ml_status():
    """ML model status endpoint."""
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    return _ok(data=ml.get_status())


@app.route("/api/ml/retrain", methods=["POST"])
def ml_retrain():
    """Retrain the ML model (admin only)."""
    user, err = _require_role(["admin"])
    if err:
        return err
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    success = ml.retrain()
    if success:
        return _ok(data=ml.get_status(), message="Model retrained successfully")
    return _err("Retraining failed", 500)


@app.route("/api/health", methods=["GET"])
def health_check():
    return _ok(data={"status": "healthy", "version": "3.0.0"})


if __name__ == "__main__":
    app.run(debug=SERVER_CONFIG["debug"], host=SERVER_CONFIG["host"], port=SERVER_CONFIG["port"])
