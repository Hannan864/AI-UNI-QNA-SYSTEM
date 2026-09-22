"""
Phase 8 Mock/Live Mode Router Test Suite
AI Chatbot for University Support
Tests mode routing, isolation, authentication, error handling, and regressions
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
    email = f"test_p8fac_{TEST_SUFFIX}@test.com"
    r = post("/api/register", {"email": email, "password": "test123", "name": "Phase8 Faculty", "role": "faculty"})
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


# ==================== TEST 1: MODE ROUTING ====================
print("\n=== TEST 1: MODE ROUTING ===")


def test_mock_mode_routes_to_mock():
    """Mock mode should use knowledge base, not AI provider."""
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"


test("Mock mode routes to Mock Service", test_mock_mode_routes_to_mock)


def test_mock_mode_has_correct_label():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return resp.get("mode_label") == "Mock Data"


test("Mock mode has correct mode_label", test_mock_mode_has_correct_label)


def test_live_mode_routes_to_live():
    """Live mode should use AI provider (or return not-configured message)."""
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live"


test("Live mode routes to Live AI Service", test_live_mode_routes_to_live)


def test_live_mode_has_correct_label():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return resp.get("mode_label") == "Live AI"


test("Live mode has correct mode_label", test_live_mode_has_correct_label)


def test_invalid_mode_defaults_to_mock():
    r = post("/api/chat", {"message": "Hello", "mode": "invalid"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"


test("Invalid mode defaults to mock", test_invalid_mode_defaults_to_mock)


def test_default_mode_is_mock():
    r = post("/api/chat", {"message": "Hello"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"


test("Default mode is mock", test_default_mode_is_mock)


def test_empty_mode_defaults_to_mock():
    r = post("/api/chat", {"message": "Hello", "mode": ""})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"


test("Empty mode defaults to mock", test_empty_mode_defaults_to_mock)


# ==================== TEST 2: MODE ROUTER ENDPOINT ====================
print("\n=== TEST 2: MODE ROUTER ENDPOINT ===")


def test_chat_modes_endpoint():
    r = get("/api/chat/modes")
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        modes = d["data"]
        return "mock" in modes and "live" in modes
    return False


test("Chat modes endpoint returns mock and live", test_chat_modes_endpoint)


def test_chat_modes_mock_always_available():
    r = get("/api/chat/modes")
    d = r.get_json()
    return d["data"]["mock"]["available"] is True


test("Mock mode always available", test_chat_modes_mock_always_available)


# ==================== TEST 3: MOCK MODE QUALITY ====================
print("\n=== TEST 3: MOCK MODE QUALITY ===")


def test_mock_known_question():
    r = post("/api/chat", {"message": "What is the admission process at IIUI?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    return r.status_code == 200 and len(answer) > 20


test("Mock returns answer for known question", test_mock_known_question)


def test_mock_has_confidence():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return "confidence" in resp and isinstance(resp["confidence"], (int, float))


test("Mock response includes confidence", test_mock_has_confidence)


def test_mock_has_source():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return "source" in resp


test("Mock response includes source", test_mock_has_source)


def test_mock_unknown_no_fake():
    r = post("/api/chat", {"message": "What is the meaning of life according to IIUI?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    fake_indicators = ["definitely", "certainly", "the official policy is"]
    has_fake = any(ind in answer.lower() for ind in fake_indicators)
    return r.status_code == 200 and not has_fake


test("Mock does not fabricate answers", test_mock_unknown_no_fake)


def test_mock_empty_rejected():
    r = post("/api/chat", {"message": "", "mode": "mock"})
    return r.status_code == 400


test("Mock rejects empty message", test_mock_empty_rejected)


def test_mock_long_rejected():
    r = post("/api/chat", {"message": "x" * 1001, "mode": "mock"})
    return r.status_code == 400


test("Mock rejects long message", test_mock_long_rejected)


# ==================== TEST 4: LIVE MODE BEHAVIOR ====================
print("\n=== TEST 4: LIVE MODE BEHAVIOR ===")


def test_live_unconfigured_returns_message():
    """When AI is not configured, live mode should return a helpful message."""
    # Disable AI
    put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live"


test("Live mode returns response when not configured", test_live_unconfigured_returns_message)


def test_live_no_crash_unconfigured():
    """Live mode should never crash when not configured."""
    r = post("/api/chat", {"message": "What is admission process?", "mode": "live"})
    return r.status_code == 200 and r.get_json()["success"]


test("Live mode does not crash when unconfigured", test_live_no_crash_unconfigured)


# ==================== TEST 5: MODE ISOLATION ====================
print("\n=== TEST 5: MODE ISOLATION ===")


def test_mock_never_calls_ai():
    """Mock mode should never return an AI-sourced response."""
    # Enable AI to ensure mock still doesn't use it
    put("/api/settings/ai", {"enabled": True}, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    # Source should NOT contain "AI (" which indicates live AI provider
    return resp.get("mode") == "mock" and "AI (" not in resp.get("source", "")


test("Mock mode never calls AI provider", test_mock_never_calls_ai)


def test_live_never_falls_back_to_mock():
    """Live mode errors should NOT silently become mock responses."""
    # Disable AI to trigger error
    put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    # Should still report mode=live even on error
    return resp.get("mode") == "live" and resp.get("mode_label") == "Live AI"


test("Live mode never silently falls back to mock", test_live_never_falls_back_to_mock)


def test_mock_and_live_give_different_responses():
    """Mock and Live should use different services."""
    # Get mock response
    r_mock = post("/api/chat", {"message": "What is IIUI?", "mode": "mock"})
    mock_resp = r_mock.get_json().get("data", {})

    # Get live response (will be error/unconfigured)
    r_live = post("/api/chat", {"message": "What is IIUI?", "mode": "live"})
    live_resp = r_live.get_json().get("data", {})

    # Modes should be different
    return mock_resp.get("mode") == "mock" and live_resp.get("mode") == "live"


test("Mock and Live use different services", test_mock_and_live_give_different_responses)


# Reset AI config
put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})


# ==================== TEST 6: CHAT HISTORY MODE ====================
print("\n=== TEST 6: CHAT HISTORY MODE ===")


def test_mock_chat_stores_mode():
    msg = f"Phase8 mode check mock {TEST_SUFFIX}"
    post("/api/chat", {"message": msg, "mode": "mock", "session_id": student_session})

    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for log in d["data"]:
            if msg in log.get("user_message", ""):
                return log.get("mode") == "mock"
    return False


test("Mock chat stored with mode=mock", test_mock_chat_stores_mode)


def test_live_chat_stores_mode():
    msg = f"Phase8 mode check live {TEST_SUFFIX}"
    post("/api/chat", {"message": msg, "mode": "live", "session_id": student_session})

    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for log in d["data"]:
            if msg in log.get("user_message", ""):
                return log.get("mode") == "live"
    return False


test("Live chat stored with mode=live", test_live_chat_stores_mode)


def test_mode_not_mixed_in_history():
    """Each chat log entry should have exactly one mode."""
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for log in d["data"][:20]:
            mode = log.get("mode", "")
            if mode not in ("mock", "live"):
                return False
        return True
    return True


test("No mixed modes in chat history", test_mode_not_mixed_in_history)


# ==================== TEST 7: AUTHENTICATION ====================
print("\n=== TEST 7: AUTHENTICATION ===")


def test_student_can_chat_mock():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Student can use mock chat", test_student_can_chat_mock)


def test_faculty_can_chat_mock():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"},
             headers={"X-Session-Id": faculty_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Faculty can use mock chat", test_faculty_can_chat_mock)


def test_admin_can_chat_mock():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"},
             headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin can use mock chat", test_admin_can_chat_mock)


def test_anonymous_can_chat():
    """Chat endpoint works without auth (public)."""
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    return r.status_code == 200 and r.get_json()["success"]


test("Anonymous user can use chat (public endpoint)", test_anonymous_can_chat)


def test_expired_session_rejected():
    r = post("/api/chat", {"message": "Hello", "mode": "mock", "session_id": "invalid_session_id"})
    return r.status_code == 401


test("Expired/invalid session rejected", test_expired_session_rejected)


# ==================== TEST 8: AUTHORIZATION ====================
print("\n=== TEST 8: AUTHORIZATION ===")


def test_student_blocked_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from AI config", test_student_blocked_ai_config)


def test_faculty_blocked_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from AI config", test_faculty_blocked_ai_config)


def test_admin_can_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin can access AI config", test_admin_can_ai_config)


def test_student_blocked_admin_users():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from admin users", test_student_blocked_admin_users)


def test_faculty_blocked_admin_users():
    r = get("/api/admin/users", headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from admin users", test_faculty_blocked_admin_users)


# ==================== TEST 9: ERROR HANDLING ====================
print("\n=== TEST 9: ERROR HANDLING ===")


def test_empty_message_rejected():
    r = post("/api/chat", {"message": ""})
    return r.status_code == 400


test("Empty message rejected", test_empty_message_rejected)


def test_long_message_rejected():
    r = post("/api/chat", {"message": "x" * 1001})
    return r.status_code == 400


test("Long message rejected", test_long_message_rejected)


def test_no_body_rejected():
    r = client.post("/api/chat", content_type="application/json")
    return r.status_code == 400


test("No body rejected", test_no_body_rejected)


def test_invalid_api_key_safe():
    """Invalid API key should not crash the server."""
    put("/api/settings/ai", {
        "provider": "openai", "model": "gpt-3.5-turbo",
        "api_key": "sk-invalid-test-key", "enabled": True,
    }, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    # Should return gracefully, not crash
    return r.status_code == 200 and resp.get("mode") == "live"


test("Invalid API key handled safely", test_invalid_api_key_safe)


def test_provider_unavailable_safe():
    """Unavailable provider should not crash the server."""
    put("/api/settings/ai", {
        "provider": "custom", "model": "test",
        "api_key": "test", "base_url": "http://localhost:19999/v1",
        "enabled": True,
    }, headers={"X-Session-Id": admin_session})

    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Provider unavailable handled safely", test_provider_unavailable_safe)


# Reset
put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})


def test_no_api_key_exposed():
    """API key should never appear in any response."""
    put("/api/settings/ai", {
        "provider": "openai", "model": "gpt-3.5-turbo",
        "api_key": f"sk-secret-{TEST_SUFFIX}", "enabled": False,
    }, headers={"X-Session-Id": admin_session})

    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return f"sk-secret-{TEST_SUFFIX}" not in json.dumps(d)


test("API key not exposed in config response", test_no_api_key_exposed)


# ==================== TEST 10: SECURITY ====================
print("\n=== TEST 10: SECURITY ===")


def test_no_password_in_responses():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return "password_hash" not in json.dumps(d.get("data", {}))


test("No password in profile response", test_no_password_in_responses)


def test_no_password_in_chat_logs():
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    response_str = json.dumps(d)
    return "password_hash" not in response_str


test("No password in chat logs", test_no_password_in_chat_logs)


def test_unauthorized_api_blocked():
    r = get("/api/profile")
    return r.status_code == 401


test("Unauthorized API call blocked", test_unauthorized_api_blocked)


# ==================== TEST 11: PHASE 3 REGRESSION ====================
print("\n=== TEST 11: PHASE 3 REGRESSION ===")


def test_p3_health():
    r = get("/api/health")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["status"] == "healthy"


test("Health check", test_p3_health)


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


# ==================== TEST 12: PHASE 4 REGRESSION ====================
print("\n=== TEST 12: PHASE 4 REGRESSION ===")


def test_p4_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Profile", test_p4_profile)


def test_p4_admin_users():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin users", test_p4_admin_users)


def test_p4_student_blocked():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from admin", test_p4_student_blocked)


# ==================== TEST 13: PHASE 5 REGRESSION ====================
print("\n=== TEST 13: PHASE 5 REGRESSION ===")


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


# ==================== TEST 14: PHASE 6 REGRESSION ====================
print("\n=== TEST 14: PHASE 6 REGRESSION ===")


def test_p6_mock_mode():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"


test("Mock mode works", test_p6_mock_mode)


def test_p6_mode_isolation():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return resp.get("mode") == "mock" and "AI (" not in resp.get("source", "")


test("Mode isolation maintained", test_p6_mode_isolation)


def test_p6_kb_data():
    r = get("/api/knowledge")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d.get("data", [])) >= 5


test("KB data available", test_p6_kb_data)


# ==================== TEST 15: PHASE 7 REGRESSION ====================
print("\n=== TEST 15: PHASE 7 REGRESSION ===")


def test_p7_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("AI config endpoint", test_p7_ai_config)


def test_p7_providers():
    r = get("/api/settings/ai/providers", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        ids = [p["id"] for p in d["data"]]
        return "openai" in ids and "anthropic" in ids
    return False


test("Providers list", test_p7_providers)


def test_p7_ai_status():
    r = get("/api/settings/ai/status")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "status" in d["data"]


test("AI status endpoint", test_p7_ai_status)


def test_p7_live_mode():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live"


test("Live mode works", test_p7_live_mode)


def test_p7_live_no_crash():
    """Live mode should never crash."""
    r = post("/api/chat", {"message": "What is admission?", "mode": "live"})
    return r.status_code == 200 and r.get_json()["success"]


test("Live mode does not crash", test_p7_live_no_crash)


# ==================== CLEANUP ====================
print("\n=== CLEANUP ===")


def test_cleanup():
    put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})
    return True


test("Cleanup: disable AI", test_cleanup)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 8 TEST RESULTS")
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
