"""
Phase 7 Live AI Integration Test Suite
AI Chatbot for University Support
Tests AI configuration, mode isolation, security, error handling, and regressions
"""
import sys
import json
import time

sys.path.insert(0, '.')

from flask_server import app

client = app.test_client()
PASSED = 0
FAILED = 0
TEST_SUFFIX = str(int(time.time()))[-4:]


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


def post(url, data, headers=None):
    return client.post(url, json=data, headers=headers or {})


def put(url, data, headers=None):
    return client.put(url, json=data, headers=headers or {})


def get(url, headers=None):
    return client.get(url, headers=headers or {})


def delete(url, headers=None):
    return client.delete(url, headers=headers or {})


# ==================== SETUP ====================
print("\n=== SETUP: AUTHENTICATION ===")

admin_session = None
student_session = None
faculty_session = None


def test_login_admin():
    global admin_session
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        admin_session = d["data"]["session_id"]
        return True
    return False


test("Login as admin", test_login_admin)


def test_login_student():
    global student_session
    r = post("/api/login", {"email": "student@iiu.edu.pk", "password": "student123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        student_session = d["data"]["session_id"]
        return True
    return False


test("Login as student", test_login_student)


def test_register_faculty():
    global faculty_session
    email = f"test_p7fac_{TEST_SUFFIX}@test.com"
    r = post("/api/register", {"email": email, "password": "test123", "name": "Phase7 Faculty", "role": "faculty"})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        faculty_session = d["data"]["session_id"]
        return True
    r2 = post("/api/login", {"email": email, "password": "test123"})
    d2 = r2.get_json()
    if r2.status_code == 200 and d2["success"]:
        faculty_session = d2["data"]["session_id"]
        return True
    return False


test("Setup faculty session", test_register_faculty)


# ==================== TEST 1: LIVE AI CONFIGURATION ====================
print("\n=== TEST 1: LIVE AI CONFIGURATION ===")


def test_admin_can_get_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Admin can get AI configuration", test_admin_can_get_ai_config)


def test_admin_can_save_ai_config():
    r = put("/api/settings/ai", {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": f"sk-test-key-{TEST_SUFFIX}",
        "base_url": "",
        "temperature": 0.7,
        "max_tokens": 500,
        "enabled": False,
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Admin can save AI configuration", test_admin_can_save_ai_config)


def test_config_saved_with_correct_values():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    cfg = d.get("data", {})
    return (cfg.get("provider") == "openai" and
            cfg.get("model") == "gpt-3.5-turbo" and
            cfg.get("enabled") in (0, False))


test("Configuration saved with correct values", test_config_saved_with_correct_values)


def test_providers_list_endpoint():
    r = get("/api/settings/ai/providers", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        providers = d["data"]
        ids = [p["id"] for p in providers]
        return "openai" in ids and "anthropic" in ids and "custom" in ids
    return False


test("Providers list returns supported providers", test_providers_list_endpoint)


def test_temperature_validation_high():
    r = put("/api/settings/ai", {"temperature": 3.0}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("Temperature > 2.0 rejected", test_temperature_validation_high)


def test_temperature_validation_low():
    r = put("/api/settings/ai", {"temperature": -0.5}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("Temperature < 0.0 rejected", test_temperature_validation_low)


def test_max_tokens_validation_high():
    r = put("/api/settings/ai", {"max_tokens": 10000}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("Max tokens > 8192 rejected", test_max_tokens_validation_high)


def test_max_tokens_validation_low():
    r = put("/api/settings/ai", {"max_tokens": 0}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("Max tokens < 1 rejected", test_max_tokens_validation_low)


# ==================== TEST 2: ADMIN AUTHORIZATION ====================
print("\n=== TEST 2: ADMIN AUTHORIZATION ===")


def test_admin_can_access_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin can access AI config endpoint", test_admin_can_access_ai_config)


def test_admin_can_update_ai_config():
    r = put("/api/settings/ai", {"model": "gpt-4"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin can update AI config", test_admin_can_update_ai_config)


# ==================== TEST 3: STUDENT CANNOT MODIFY SETTINGS ====================
print("\n=== TEST 3: STUDENT CANNOT MODIFY SETTINGS ===")


def test_student_blocked_ai_config_get():
    r = get("/api/settings/ai", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from reading AI config", test_student_blocked_ai_config_get)


def test_student_blocked_ai_config_update():
    r = put("/api/settings/ai", {"provider": "openai"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from updating AI config", test_student_blocked_ai_config_update)


def test_student_blocked_ai_test():
    r = client.post("/api/settings/ai/test", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from testing AI connection", test_student_blocked_ai_test)


def test_student_blocked_providers_list():
    r = get("/api/settings/ai/providers", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from listing AI providers", test_student_blocked_providers_list)


# ==================== TEST 4: FACULTY CANNOT MODIFY SETTINGS ====================
print("\n=== TEST 4: FACULTY CANNOT MODIFY SETTINGS ===")


def test_faculty_blocked_ai_config_get():
    r = get("/api/settings/ai", headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from reading AI config", test_faculty_blocked_ai_config_get)


def test_faculty_blocked_ai_config_update():
    r = put("/api/settings/ai", {"provider": "openai"}, headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from updating AI config", test_faculty_blocked_ai_config_update)


def test_faculty_blocked_ai_test():
    r = client.post("/api/settings/ai/test", headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from testing AI connection", test_faculty_blocked_ai_test)


# ==================== TEST 5: API KEY MASKING ====================
print("\n=== TEST 5: API KEY MASKING ===")


def test_api_key_masked_in_config_response():
    """API key should never be returned in full."""
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    cfg = d.get("data", {})
    # The encrypted key should be masked
    if cfg.get("api_key_encrypted") and cfg["api_key_encrypted"] != "***MASKED***":
        return False
    # If there's a display key, it should be masked
    display = cfg.get("api_key_display", "")
    if display and display != "****":
        # Should have asterisks in the middle
        return "*" in display and len(display) < 40
    return True


test("API key is masked in config response", test_api_key_masked_in_config_response)


# ==================== TEST 6: NO API KEY EXPOSURE ====================
print("\n=== TEST 6: NO API KEY EXPOSURE ===")


def test_no_full_api_key_in_any_response():
    """Full API key should never appear in any admin endpoint response."""
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    response_str = json.dumps(d)
    # The test key we saved
    full_key = f"sk-test-key-{TEST_SUFFIX}"
    return full_key not in response_str


test("Full API key not exposed in config response", test_no_full_api_key_in_any_response)


def test_no_api_key_in_chat_logs():
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    response_str = json.dumps(d)
    full_key = f"sk-test-key-{TEST_SUFFIX}"
    return full_key not in response_str


test("Full API key not exposed in chat logs", test_no_api_key_in_chat_logs)


def test_no_api_key_in_status_endpoint():
    r = get("/api/settings/ai/status")
    d = r.get_json()
    response_str = json.dumps(d)
    full_key = f"sk-test-key-{TEST_SUFFIX}"
    return full_key not in response_str


test("Full API key not exposed in status endpoint", test_no_api_key_in_status_endpoint)


def test_no_api_key_in_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    response_str = json.dumps(d)
    full_key = f"sk-test-key-{TEST_SUFFIX}"
    return full_key not in response_str


test("Full API key not exposed in profile", test_no_api_key_in_profile)


# ==================== TEST 7: MOCK MODE DOES NOT CALL LIVE AI ====================
print("\n=== TEST 7: MOCK MODE DOES NOT CALL LIVE AI ===")


def test_mock_mode_no_live_ai_call():
    """Mock mode should use knowledge base, not the AI provider."""
    # First enable AI to make sure mock still doesn't use it
    put("/api/settings/ai", {"enabled": True}, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    # Mode must be mock, not live
    return resp.get("mode") == "mock" and "AI (" not in resp.get("source", "")


test("Mock mode does not call Live AI provider", test_mock_mode_no_live_ai_call)


def test_mock_mode_uses_knowledge_base():
    r = post("/api/chat", {"message": "What are the university hours?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    # Should return a response from knowledge base (confidence > 0 or fallback)
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"


test("Mock mode uses knowledge base", test_mock_mode_uses_knowledge_base)


# Disable AI again for subsequent tests
put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})


# ==================== TEST 8: LIVE MODE CALLS CONFIGURED PROVIDER ====================
print("\n=== TEST 8: LIVE MODE CALLS CONFIGURED PROVIDER ===")


def test_live_mode_unconfigured_returns_message():
    """When AI is not configured, live mode should return a helpful message."""
    # Disable AI
    put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return (r.status_code == 200 and d["success"] and
            resp.get("mode") == "live" and
            "not" in resp.get("answer", "").lower() or "configure" in resp.get("answer", "").lower())


test("Live mode returns helpful message when not configured", test_live_mode_unconfigured_returns_message)


def test_live_mode_disabled_returns_message():
    """When AI is disabled, live mode should indicate it."""
    # Configure but disable
    put("/api/settings/ai", {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": "sk-test",
        "enabled": False,
    }, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live"


test("Live mode returns message when AI is disabled", test_live_mode_disabled_returns_message)


# ==================== TEST 9: INVALID API KEY HANDLED SAFELY ====================
print("\n=== TEST 9: INVALID API KEY HANDLED SAFELY ===")


def test_invalid_api_key_safe_error():
    """With a fake API key, live mode should fail gracefully without crashing."""
    put("/api/settings/ai", {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": "sk-invalid-key-for-testing",
        "enabled": True,
    }, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})

    # Should return a 200 with an error message, NOT crash
    if r.status_code != 200:
        return False
    # The response should contain a user-friendly error, not a traceback
    answer = resp.get("answer", "")
    traceback_indicators = ["traceback", "exception", "file \"", "line ", "import ", "stack trace"]
    has_traceback = any(ind in answer.lower() for ind in traceback_indicators)
    # Should not expose the actual API key in the error
    return not has_traceback and "sk-invalid-key" not in answer


test("Invalid API key handled safely without traceback", test_invalid_api_key_safe_error)


def test_invalid_api_key_no_key_exposure():
    """The API key should never appear in the error response."""
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    response_str = json.dumps(d)
    return "sk-invalid-key-for-testing" not in response_str


test("Invalid API key not exposed in error response", test_invalid_api_key_no_key_exposure)


# ==================== TEST 10: PROVIDER UNAVAILABLE HANDLED SAFELY ====================
print("\n=== TEST 10: PROVIDER UNAVAILABLE HANDLED SAFELY ===")


def test_provider_unavailable_safe():
    """When provider is unreachable, it should fail gracefully."""
    put("/api/settings/ai", {
        "provider": "custom",
        "model": "test-model",
        "api_key": "test-key",
        "base_url": "http://localhost:19999/v1",
        "enabled": True,
    }, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})

    # Should return gracefully, not crash
    return r.status_code == 200 and d["success"] and resp.get("mode") == "live"


test("Provider unavailable handled safely", test_provider_unavailable_safe)


# Reset config
put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})


# ==================== TEST 11: UNCONFIGURED LIVE AI HANDLED SAFELY ====================
print("\n=== TEST 11: UNCONFIGURED LIVE AI HANDLED SAFELY ===")


def test_unconfigured_live_ai_no_crash():
    """When no AI is configured at all, live mode should not crash."""
    # Clear config by setting empty
    put("/api/settings/ai", {
        "provider": "",
        "model": "",
        "api_key": "",
        "enabled": False,
    }, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "What is admission process?", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})

    return (r.status_code == 200 and d["success"] and
            resp.get("mode") == "live" and
            "configure" in resp.get("answer", "").lower() or "not" in resp.get("answer", "").lower())


test("Unconfigured live AI handled safely with message", test_unconfigured_live_ai_no_crash)


def test_ai_status_endpoint_unconfigured():
    r = get("/api/settings/ai/status")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["status"] in ("not_configured", "disabled")


test("AI status endpoint returns correct status when unconfigured", test_ai_status_endpoint_unconfigured)


# ==================== TEST 12: CHAT HISTORY STORES MODE ====================
print("\n=== TEST 12: CHAT HISTORY STORES MODE ===")


def test_mock_chat_stores_mode():
    """Mock mode chats should be stored with mode=mock."""
    msg = f"Phase7 mode test mock {TEST_SUFFIX}"
    post("/api/chat", {"message": msg, "mode": "mock", "session_id": student_session})

    r = get("/api/history", headers={"X-Session-Id": student_session})
    d = r.get_json()
    entries = d.get("data") or d.get("history") or []
    if d.get("success") and entries:
        for h in entries:
            if msg in h.get("user_message", ""):
                return h.get("mode") == "mock"
    return False


test("Mock chat stored with mode=mock in history", test_mock_chat_stores_mode)


def test_live_chat_stores_mode():
    """Live mode chats should be stored with mode=live."""
    msg = f"Phase7 mode test live {TEST_SUFFIX}"
    post("/api/chat", {"message": msg, "mode": "live", "session_id": student_session})

    r = get("/api/history", headers={"X-Session-Id": student_session})
    d = r.get_json()
    entries = d.get("data") or d.get("history") or []
    if d.get("success") and entries:
        for h in entries:
            if msg in h.get("user_message", ""):
                return h.get("mode") == "live"
    return False


test("Live chat stored with mode=live in history", test_live_chat_stores_mode)


def test_chat_logs_store_mode_live():
    """Admin chat logs should show mode=live for live chats."""
    msg = f"Phase7 log test {TEST_SUFFIX}"
    post("/api/chat", {"message": msg, "mode": "live", "session_id": student_session})

    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for log in d["data"]:
            if msg in log.get("user_message", ""):
                return log.get("mode") == "live"
    return False


test("Chat logs correctly record live mode", test_chat_logs_store_mode_live)


# ==================== TEST 13: EXISTING AUTHENTICATION WORKS ====================
print("\n=== TEST 13: EXISTING AUTHENTICATION WORKS ===")


def test_auth_register():
    r = post("/api/register", {
        "email": f"test_p7auth_{TEST_SUFFIX}@test.com",
        "password": "test123",
        "name": "Phase7 Auth Test",
        "role": "student",
    })
    return r.status_code == 201 and r.get_json()["success"]


test("Registration works", test_auth_register)


def test_auth_login():
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    return r.status_code == 200 and r.get_json()["success"]


test("Login works", test_auth_login)


def test_auth_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Profile endpoint works", test_auth_profile)


def test_auth_unauthorized():
    r = get("/api/profile")
    return r.status_code == 401


test("Unauthorized access blocked", test_auth_unauthorized)


# ==================== TEST 14: PHASE 3 REGRESSION ====================
print("\n=== TEST 14: PHASE 3 REGRESSION ===")


def test_p3_health():
    r = get("/api/health")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["status"] == "healthy"


test("Health check", test_p3_health)


def test_p3_register():
    r = post("/api/register", {
        "email": f"test_p7reg_{TEST_SUFFIX}@test.com",
        "password": "test123",
        "name": "Phase7 Regression",
        "role": "student",
    })
    return r.status_code == 201 and r.get_json()["success"]


test("Registration", test_p3_register)


def test_p3_login():
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    return r.status_code == 200 and r.get_json()["success"]


test("Login", test_p3_login)


def test_p3_chat_mock():
    r = post("/api/chat", {"message": "What is admission process?", "mode": "mock"})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d.get("data", {}).get("answer")


test("Mock chat", test_p3_chat_mock)


def test_p3_faqs():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]


test("FAQs endpoint", test_p3_faqs)


def test_p3_knowledge():
    r = get("/api/knowledge")
    return r.status_code == 200 and r.get_json()["success"]


test("Knowledge endpoint", test_p3_knowledge)


def test_p3_courses():
    r = get("/api/courses")
    return r.status_code == 200 and r.get_json()["success"]


test("Courses endpoint", test_p3_courses)


def test_p3_contacts():
    r = get("/api/contacts")
    return r.status_code == 200 and r.get_json()["success"]


test("Contacts endpoint", test_p3_contacts)


# ==================== TEST 15: PHASE 4 REGRESSION ====================
print("\n=== TEST 15: PHASE 4 REGRESSION ===")


def test_p4_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Profile", test_p4_profile)


def test_p4_admin_users():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin users", test_p4_admin_users)


def test_p4_student_blocked_admin():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from admin", test_p4_student_blocked_admin)


def test_p4_faculty_blocked_admin():
    r = get("/api/admin/users", headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from admin", test_p4_faculty_blocked_admin)


def test_p4_conversations():
    r = post("/api/conversations", {"title": "Regression Test"}, headers={"X-Session-Id": student_session})
    return r.status_code == 201 and r.get_json()["success"]


test("Create conversation", test_p4_conversations)


def test_p4_history():
    r = get("/api/history", headers={"X-Session-Id": student_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Chat history", test_p4_history)


# ==================== TEST 16: PHASE 5 REGRESSION ====================
print("\n=== TEST 16: PHASE 5 REGRESSION ===")


def test_p5_kb_list():
    r = get("/api/knowledge")
    return r.status_code == 200 and r.get_json()["success"]


test("KB list", test_p5_kb_list)


def test_p5_faq_list():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]


test("FAQ list", test_p5_faq_list)


def test_p5_kb_search():
    r = get("/api/knowledge/search?q=admission")
    return r.status_code == 200 and r.get_json()["success"]


test("KB search", test_p5_kb_search)


def test_p5_faq_search():
    r = get("/api/faqs/search?q=fee")
    return r.status_code == 200 and r.get_json()["success"]


test("FAQ search", test_p5_faq_search)


def test_p5_kb_admin_create():
    r = post("/api/knowledge", {
        "question": f"Regression KB {TEST_SUFFIX}",
        "answer": f"Regression answer {TEST_SUFFIX}",
        "category": "General",
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 201 and r.get_json()["success"]


test("Admin creates KB entry", test_p5_kb_admin_create)


def test_p5_student_blocked_kb_create():
    r = post("/api/knowledge", {"question": "Hacked?", "answer": "Hacked"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from KB create", test_p5_student_blocked_kb_create)


# ==================== TEST 17: PHASE 6 REGRESSION ====================
print("\n=== TEST 17: PHASE 6 REGRESSION ===")


def test_p6_mock_mode():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"


test("Mock mode works", test_p6_mock_mode)


def test_p6_mode_isolation():
    """Mock should never return a Live AI response."""
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return resp.get("mode") == "mock" and "AI (" not in resp.get("source", "")


test("Mode isolation maintained", test_p6_mode_isolation)


def test_p6_invalid_mode_defaults_mock():
    r = post("/api/chat", {"message": "Hello", "mode": "invalid"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"


test("Invalid mode defaults to mock", test_p6_invalid_mode_defaults_mock)


def test_p6_kb_data_available():
    r = get("/api/knowledge")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d.get("data", [])) >= 5


test("KB data available", test_p6_kb_data_available)


def test_p6_faqs_data_available():
    r = get("/api/faqs")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d.get("data", [])) >= 5


test("FAQs data available", test_p6_faqs_data_available)


# ==================== CLEANUP ====================
print("\n=== CLEANUP ===")


def test_cleanup_restore_config():
    """Restore AI config to disabled state."""
    r = put("/api/settings/ai", {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": "",
        "enabled": False,
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 200


test("Restore AI config to disabled state", test_cleanup_restore_config)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 7 TEST RESULTS")
print("=" * 55)
print(f"  Total:  {PASSED + FAILED}")
print(f"  Passed: {PASSED}")
print(f"  Failed: {FAILED}")
print("=" * 55)

if FAILED > 0:
    print("\nSome tests failed. Review output above.")
    sys.exit(1)
else:
    print("\nAll tests passed!")
    sys.exit(0)
