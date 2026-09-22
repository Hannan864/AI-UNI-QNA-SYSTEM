"""
Phase 3 Backend Test Suite
AI Chatbot for University Support
Tests all API endpoints
"""
import sys
import json
import time

sys.path.insert(0, '.')

from flask_server import app

# Test client
client = app.test_client()
PASSED = 0
FAILED = 0

def test(name, func):
    global PASSED, FAILED
    try:
        result = func()
        if result:
            PASSED += 1
            print(f"  PASS: {name}")
        else:
            FAILED += 1
            print(f"  FAIL: {name}")
    except Exception as e:
        FAILED += 1
        print(f"  ERROR: {name} - {e}")

def post_json(url, data, headers=None):
    return client.post(url, json=data, headers=headers or {})

def put_json(url, data, headers=None):
    return client.put(url, json=data, headers=headers or {})

def get_json(url, headers=None):
    return client.get(url, headers=headers or {})

def del_json(url, headers=None):
    return client.delete(url, headers=headers or {})


# ==================== 1. HEALTH CHECK ====================
print("\n=== 1. HEALTH CHECK ===")

def test_health():
    r = get_json("/api/health")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["status"] == "healthy"
test("Health check", test_health)


# ==================== 2. AUTH - REGISTER ====================
print("\n=== 2. AUTH - REGISTER ===")

def test_register_missing_fields():
    r = post_json("/api/register", {})
    d = r.get_json()
    return r.status_code == 400 and not d["success"]
test("Register missing fields", test_register_missing_fields)

def test_register_invalid_email():
    r = post_json("/api/register", {"email": "bad", "password": "test123", "name": "Test"})
    d = r.get_json()
    return r.status_code == 400 and not d["success"]
test("Register invalid email", test_register_invalid_email)

def test_register_short_password():
    r = post_json("/api/register", {"email": "test@test.com", "password": "123", "name": "Test"})
    d = r.get_json()
    return r.status_code == 400 and not d["success"]
test("Register short password", test_register_short_password)

def test_register_student():
    r = post_json("/api/register", {"email": "teststudent@test.com", "password": "test123", "name": "Test Student", "role": "student"})
    d = r.get_json()
    return r.status_code == 201 and d["success"]
test("Register student", test_register_student)

def test_register_faculty():
    r = post_json("/api/register", {"email": "testfaculty@test.com", "password": "test123", "name": "Test Faculty", "role": "faculty"})
    d = r.get_json()
    return r.status_code == 201 and d["success"] and d["data"]["role"] == "faculty"
test("Register faculty", test_register_faculty)

def test_register_duplicate():
    r = post_json("/api/register", {"email": "teststudent@test.com", "password": "test123", "name": "Duplicate", "role": "student"})
    d = r.get_json()
    return r.status_code == 409 and not d["success"]
test("Register duplicate email", test_register_duplicate)


# ==================== 3. AUTH - LOGIN ====================
print("\n=== 3. AUTH - LOGIN ===")

admin_session = None

def test_login_admin():
    global admin_session
    r = post_json("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        admin_session = d["data"]["session_id"]
        return True
    return False
test("Login admin", test_login_admin)

student_session = None

def test_login_student():
    global student_session
    r = post_json("/api/login", {"email": "teststudent@test.com", "password": "test123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        student_session = d["data"]["session_id"]
        return True
    return False
test("Login student", test_login_student)

def test_login_invalid():
    r = post_json("/api/login", {"email": "wrong@test.com", "password": "wrong"})
    d = r.get_json()
    return r.status_code == 401 and not d["success"]
test("Login invalid credentials", test_login_invalid)

def test_login_missing_fields():
    r = post_json("/api/login", {})
    d = r.get_json()
    return r.status_code == 400 and not d["success"]
test("Login missing fields", test_login_missing_fields)


# ==================== 4. PROFILE ====================
print("\n=== 4. PROFILE ===")

def test_get_profile():
    r = get_json("/api/profile", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "password_hash" not in d["data"]
test("Get profile", test_get_profile)

def test_profile_no_auth():
    r = get_json("/api/profile")
    return r.status_code == 401
test("Profile no auth", test_profile_no_auth)

def test_update_profile():
    r = put_json("/api/profile", {"name": "Admin Updated"}, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]
test("Update profile", test_update_profile)


# ==================== 5. FAQ ====================
print("\n=== 5. FAQ ===")

def test_get_faqs():
    r = get_json("/api/faqs")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0
test("Get FAQs", test_get_faqs)

def test_search_faqs():
    r = get_json("/api/faqs/search?q=admission")
    d = r.get_json()
    return r.status_code == 200 and d["success"]
test("Search FAQs", test_search_faqs)

def test_search_faqs_missing_query():
    r = get_json("/api/faqs/search")
    return r.status_code == 400
test("Search FAQs missing query", test_search_faqs_missing_query)

new_faq_id = None

def test_create_faq():
    global new_faq_id
    r = post_json("/api/faqs", {"question": "Test FAQ?", "answer": "Test answer", "category": "Test"}, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        new_faq_id = d["data"]["id"]
        return True
    return False
test("Create FAQ (admin)", test_create_faq)

def test_create_faq_unauthorized():
    r = post_json("/api/faqs", {"question": "No?", "answer": "No"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Create FAQ unauthorized", test_create_faq_unauthorized)

def test_update_faq():
    r = put_json(f"/api/faqs/{new_faq_id}", {"answer": "Updated answer"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Update FAQ (admin)", test_update_faq)

def test_delete_faq():
    r = del_json(f"/api/faqs/{new_faq_id}", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Delete FAQ (admin)", test_delete_faq)

def test_delete_faq_not_found():
    r = del_json("/api/faqs/99999", headers={"X-Session-Id": admin_session})
    return r.status_code == 404
test("Delete FAQ not found", test_delete_faq_not_found)


# ==================== 6. KNOWLEDGE BASE ====================
print("\n=== 6. KNOWLEDGE BASE ===")

def test_list_knowledge():
    r = get_json("/api/knowledge")
    d = r.get_json()
    return r.status_code == 200 and d["success"]
test("List knowledge", test_list_knowledge)

def test_search_knowledge():
    r = get_json("/api/knowledge/search?q=admission")
    d = r.get_json()
    return r.status_code == 200 and d["success"]
test("Search knowledge", test_search_knowledge)

new_kb_id = None

def test_create_knowledge():
    global new_kb_id
    r = post_json("/api/knowledge", {"category": "Test", "question": "Test KB?", "answer": "Test KB answer"}, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        new_kb_id = d["data"]["id"]
        return True
    return False
test("Create knowledge (admin)", test_create_knowledge)

def test_create_knowledge_unauthorized():
    r = post_json("/api/knowledge", {"question": "No?", "answer": "No"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Create knowledge unauthorized", test_create_knowledge_unauthorized)

def test_update_knowledge():
    r = put_json(f"/api/knowledge/{new_kb_id}", {"answer": "Updated KB"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 200
test("Update knowledge (admin)", test_update_knowledge)

def test_delete_knowledge():
    r = del_json(f"/api/knowledge/{new_kb_id}", headers={"X-Session-Id": admin_session})
    return r.status_code == 200
test("Delete knowledge (admin)", test_delete_knowledge)


# ==================== 7. CHAT ====================
print("\n=== 7. CHAT ===")

def test_chat_mock():
    r = post_json("/api/chat", {"message": "What is the admission process?"})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "data" in d
test("Chat mock mode", test_chat_mock)

def test_chat_empty_message():
    r = post_json("/api/chat", {"message": ""})
    return r.status_code == 400
test("Chat empty message", test_chat_empty_message)

def test_chat_missing_message():
    r = post_json("/api/chat", {})
    return r.status_code == 400
test("Chat missing message", test_chat_missing_message)

def test_chat_long_message():
    r = post_json("/api/chat", {"message": "x" * 1001})
    return r.status_code == 400
test("Chat long message", test_chat_long_message)

def test_chat_live_not_configured():
    r = post_json("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    # Live mode returns placeholder — either "not configured" or "Phase 7" message
    answer = d["data"]["answer"]
    return r.status_code == 200 and ("not currently configured" in answer or "Phase 7" in answer)
test("Chat live mode placeholder response", test_chat_live_not_configured)


# ==================== 8. CONVERSATIONS ====================
print("\n=== 8. CONVERSATIONS ===")

new_conv_id = None

def test_create_conversation():
    global new_conv_id
    r = post_json("/api/conversations", {"title": "Test Chat", "mode": "mock"}, headers={"X-Session-Id": student_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        new_conv_id = d["data"]["id"]
        return True
    return False
test("Create conversation", test_create_conversation)

def test_list_conversations():
    r = get_json("/api/conversations", headers={"X-Session-Id": student_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]
test("List conversations", test_list_conversations)

def test_get_conversation():
    r = get_json(f"/api/conversations/{new_conv_id}", headers={"X-Session-Id": student_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Get conversation", test_get_conversation)

def test_get_conversation_messages():
    r = get_json(f"/api/conversations/{new_conv_id}/messages", headers={"X-Session-Id": student_session})
    return r.status_code == 200
test("Get conversation messages", test_get_conversation_messages)

def test_chat_with_conversation():
    r = post_json("/api/chat", {"message": "What are the fees?", "conversation_id": new_conv_id}, headers={"X-Session-Id": student_session})
    return r.status_code == 200
test("Chat with conversation_id", test_chat_with_conversation)

def test_delete_conversation():
    r = del_json(f"/api/conversations/{new_conv_id}", headers={"X-Session-Id": student_session})
    return r.status_code == 200
test("Delete conversation", test_delete_conversation)


# ==================== 9. ADMIN - USERS ====================
print("\n=== 9. ADMIN - USERS ===")

def test_admin_list_users():
    r = get_json("/api/admin/users", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0
test("Admin list users", test_admin_list_users)

def test_admin_list_users_unauthorized():
    r = get_json("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Admin list users unauthorized", test_admin_list_users_unauthorized)


# ==================== 10. ADMIN - ANALYTICS ====================
print("\n=== 10. ADMIN - ANALYTICS ===")

def test_admin_analytics():
    r = get_json("/api/admin/analytics", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "chat_stats" in d["data"]
test("Admin analytics", test_admin_analytics)

def test_admin_chat_logs():
    r = get_json("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Admin chat logs", test_admin_chat_logs)

def test_admin_monitoring():
    r = get_json("/api/admin/monitoring", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["status"] == "operational"
test("Admin monitoring", test_admin_monitoring)


# ==================== 11. AI CONFIGURATION ====================
print("\n=== 11. AI CONFIGURATION ===")

def test_get_ai_config():
    r = get_json("/api/settings/ai", headers={"X-Session-Id": admin_session})
    return r.status_code == 200
test("Get AI config", test_get_ai_config)

def test_update_ai_config():
    r = put_json("/api/settings/ai", {
        "provider": "openai", "model": "gpt-4", "api_key": "sk-test123",
        "temperature": 0.7, "max_tokens": 500, "enabled": True
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 200
test("Update AI config", test_update_ai_config)

def test_ai_config_no_raw_key():
    r = get_json("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    # API key should be masked
    return "api_key_encrypted" not in d["data"] or d["data"].get("api_key_encrypted") == "***MASKED***"
test("AI config masked key", test_ai_config_no_raw_key)

def test_ai_config_invalid_temp():
    r = put_json("/api/settings/ai", {"temperature": 5.0}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400
test("AI config invalid temperature", test_ai_config_invalid_temp)

def test_ai_config_unauthorized():
    r = get_json("/api/settings/ai", headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("AI config unauthorized", test_ai_config_unauthorized)


# ==================== 12. COURSES ====================
print("\n=== 12. COURSES ===")

def test_list_courses():
    r = get_json("/api/courses")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0
test("List courses", test_list_courses)

def test_list_courses_by_semester():
    r = get_json("/api/courses?semester=1")
    d = r.get_json()
    return r.status_code == 200 and d["success"]
test("List courses by semester", test_list_courses_by_semester)


# ==================== 13. CONTACTS ====================
print("\n=== 13. CONTACTS ===")

def test_list_contacts():
    r = get_json("/api/contacts")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0
test("List contacts", test_list_contacts)


# ==================== 14. LOGOUT ====================
print("\n=== 14. LOGOUT ===")

def test_logout():
    r = post_json("/api/logout", {"session_id": student_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Logout", test_logout)


# ==================== RESULTS ====================
print("\n" + "=" * 50)
print(f"PHASE 3 TEST RESULTS")
print(f"=" * 50)
print(f"  Total:  {PASSED + FAILED}")
print(f"  Passed: {PASSED}")
print(f"  Failed: {FAILED}")
print(f"=" * 50)

if FAILED > 0:
    print("\nSome tests failed. Review output above.")
    sys.exit(1)
else:
    print("\nAll tests passed!")
    sys.exit(0)
