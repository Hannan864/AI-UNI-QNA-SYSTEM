"""
Phase 14-18 Comprehensive Test Suite
Analytics + Chat History + Settings + Voice + Integration + Testing
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
print("\n=== SETUP ===")

admin_session = None
student_session = None


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


# ==================== PHASE 14: ANALYTICS ====================
print("\n=== PHASE 14: ANALYTICS ===")


def test_analytics_endpoint():
    r = get("/api/admin/analytics", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "chat_stats" in d.get("data", {})

test("Analytics endpoint returns data", test_analytics_endpoint)


def test_monitoring_endpoint():
    r = get("/api/admin/monitoring", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "total_users" in d.get("data", {})

test("Monitoring endpoint returns data", test_monitoring_endpoint)


def test_analytics_has_chat_stats():
    r = get("/api/admin/analytics", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    stats = d.get("data", {}).get("chat_stats", {})
    return "total_chats" in stats and "mock_chats" in stats and "live_chats" in stats

test("Analytics has chat statistics", test_analytics_has_chat_stats)


def test_analytics_has_frequent_queries():
    r = get("/api/admin/analytics", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return "frequent_queries" in d.get("data", {})

test("Analytics has frequent queries", test_analytics_has_frequent_queries)


def test_analytics_student_blocked():
    r = get("/api/admin/analytics", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Analytics blocked for students", test_analytics_student_blocked)


def test_monitoring_student_blocked():
    r = get("/api/admin/monitoring", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Monitoring blocked for students", test_monitoring_student_blocked)


# ==================== PHASE 15: CHAT HISTORY ====================
print("\n=== PHASE 15: CHAT HISTORY ===")


def test_history_requires_auth():
    r = get("/api/history")
    return r.status_code == 401

test("History requires authentication", test_history_requires_auth)


def test_history_returns_data():
    r = get("/api/history", headers={"X-Session-Id": student_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("History returns data for authenticated user", test_history_returns_data)


def test_history_no_password():
    r = get("/api/history", headers={"X-Session-Id": student_session})
    d = r.get_json()
    return "password_hash" not in json.dumps(d)

test("History does not expose passwords", test_history_no_password)


def test_conversation_create():
    r = post("/api/conversations", {"title": f"Test Conv {TEST_SUFFIX}", "mode": "mock"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 201 and r.get_json()["success"]

test("Create conversation", test_conversation_create)


def test_conversation_list():
    r = get("/api/conversations", headers={"X-Session-Id": student_session})
    return r.status_code == 200 and r.get_json()["success"]

test("List conversations", test_conversation_list)


def test_chat_logs_admin():
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and isinstance(d.get("data"), list)

test("Admin can view chat logs", test_chat_logs_admin)


def test_chat_logs_student_blocked():
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student blocked from chat logs", test_chat_logs_student_blocked)


# ==================== PHASE 16: SETTINGS ====================
print("\n=== PHASE 16: SETTINGS ===")


def test_ai_config_get():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("Admin can get AI config", test_ai_config_get)


def test_ai_providers_list():
    r = get("/api/settings/ai/providers", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d.get("data", [])) >= 2

test("Providers list has multiple providers", test_ai_providers_list)


def test_ai_status():
    r = get("/api/settings/ai/status")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "status" in d.get("data", {})

test("AI status endpoint works", test_ai_status)


def test_ai_config_save():
    r = put("/api/settings/ai", {
        "provider": "openai", "model": "gpt-3.5-turbo",
        "api_key": f"sk-test-{TEST_SUFFIX}", "enabled": False
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("Admin can save AI config", test_ai_config_save)


def test_api_key_masked():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    cfg = d.get("data", {})
    return f"sk-test-{TEST_SUFFIX}" not in json.dumps(cfg)

test("API key is masked in response", test_api_key_masked)


def test_ai_student_blocked():
    r = get("/api/settings/ai", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student blocked from AI config", test_ai_student_blocked)


def test_temp_validation():
    r = put("/api/settings/ai", {"temperature": 3.0}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400

test("Invalid temperature rejected", test_temp_validation)


def test_max_tokens_validation():
    r = put("/api/settings/ai", {"max_tokens": 0}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400

test("Invalid max tokens rejected", test_max_tokens_validation)


# Reset AI config
put("/api/settings/ai", {"enabled": False}, headers={"X-Session-Id": admin_session})


# ==================== PHASE 16: VOICE ====================
print("\n=== PHASE 16: VOICE ===")


def test_voice_transcribe_requires_file():
    r = client.post("/api/voice/transcribe")
    return r.status_code == 400

test("Voice transcribe requires audio file", test_voice_transcribe_requires_file)


def test_voice_endpoint_exists():
    r = client.options("/api/voice/transcribe")
    return r.status_code in (200, 405)

test("Voice transcribe endpoint exists", test_voice_endpoint_exists)


# ==================== PHASE 17: INTEGRATION ====================
print("\n=== PHASE 17: INTEGRATION ===")


def test_full_flow_mock():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock" and len(resp.get("answer", "")) > 10

test("Full flow: Mock mode chat works", test_full_flow_mock)


def test_full_flow_live():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live"

test("Full flow: Live mode chat works", test_full_flow_live)


def test_mode_switching():
    r1 = post("/api/chat", {"message": "What is admission?", "mode": "mock"})
    r2 = post("/api/chat", {"message": "What is admission?", "mode": "live"})
    m1 = r1.get_json().get("data", {}).get("mode")
    m2 = r2.get_json().get("data", {}).get("mode")
    return m1 == "mock" and m2 == "live"

test("Mode switching works correctly", test_mode_switching)


def test_invalid_mode_fallback():
    r = post("/api/chat", {"message": "Hello", "mode": "invalid"})
    return r.get_json().get("data", {}).get("mode") == "mock"

test("Invalid mode falls back to mock", test_invalid_mode_fallback)


def test_chat_modes_endpoint():
    r = get("/api/chat/modes")
    d = r.get_json()
    return r.status_code == 200 and "mock" in d.get("data", {}) and "live" in d.get("data", {})

test("Chat modes endpoint shows both modes", test_chat_modes_endpoint)


def test_health_check():
    r = get("/api/health")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["status"] == "healthy"

test("Health check", test_health_check)


# ==================== KNOWLEDGE BASE ====================
print("\n=== KNOWLEDGE BASE ===")


def test_kb_list():
    r = get("/api/knowledge")
    return r.status_code == 200 and r.get_json()["success"]

test("KB list works", test_kb_list)


def test_kb_search():
    r = get("/api/knowledge/search?q=admission")
    return r.status_code == 200 and r.get_json()["success"]

test("KB search works", test_kb_search)


def test_faq_list():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]

test("FAQ list works", test_faq_list)


def test_courses_list():
    r = get("/api/courses")
    return r.status_code == 200 and r.get_json()["success"]

test("Courses list works", test_courses_list)


# ==================== NLP ====================
print("\n=== NLP ===")


def test_nlp_admissions():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What is the admission process?")
    return result["intent"] == "admissions" and result["confidence"] > 0.3

test("NLP detects admissions intent", test_nlp_admissions)


def test_nlp_fees():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What is the fee structure?")
    return result["intent"] == "fees" and result["confidence"] > 0.3

test("NLP detects fees intent", test_nlp_fees)


def test_nlp_unknown():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("Tell me a joke")
    return result["intent"] == "unknown"

test("NLP detects unknown intent", test_nlp_unknown)


# ==================== ML ====================
print("\n=== ML ===")


def test_ml_trained():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    return ml.is_trained

test("ML model is trained", test_ml_trained)


def test_ml_predict():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What is the admission process?")
    return result["intent"] == "admissions" and result["confidence"] > 0.2

test("ML predicts admissions correctly", test_ml_predict)


def test_ml_status():
    r = get("/api/ml/status")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"].get("is_trained")

test("ML status endpoint works", test_ml_status)


# ==================== SECURITY ====================
print("\n=== SECURITY ===")


def test_no_password_in_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return "password_hash" not in json.dumps(d.get("data", {}))

test("No password in profile response", test_no_password_in_profile)


def test_no_password_in_users():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    for u in d.get("data", []):
        if "password_hash" in u:
            return False
    return True

test("No password in users list", test_no_password_in_users)


def test_unauthorized_blocked():
    r = get("/api/profile")
    return r.status_code == 401

test("Unauthorized access blocked", test_unauthorized_blocked)


def test_student_cannot_admin():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student cannot access admin endpoints", test_student_cannot_admin)


# ==================== ERROR HANDLING ====================
print("\n=== ERROR HANDLING ===")


def test_empty_message():
    r = post("/api/chat", {"message": ""})
    return r.status_code == 400

test("Empty message rejected", test_empty_message)


def test_long_message():
    r = post("/api/chat", {"message": "x" * 1001})
    return r.status_code == 400

test("Long message rejected", test_long_message)


def test_invalid_json():
    r = client.post("/api/chat", content_type="application/json")
    return r.status_code == 400

test("Invalid JSON rejected", test_invalid_json)


def test_mock_no_crash():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    return r.status_code == 200 and r.get_json()["success"]

test("Mock mode does not crash", test_mock_no_crash)


def test_live_no_crash():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    return r.status_code == 200 and r.get_json()["success"]

test("Live mode does not crash", test_live_no_crash)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 14-18 TEST RESULTS")
print("=" * 55)
print(f"  Total:  {PASSED + FAILED}")
print(f"  Passed: {PASSED}")
print(f"  Failed: {FAILED}")
print("=" * 55)

if FAILED > 0:
    print("\nSome tests failed.")
    sys.exit(1)
else:
    print("\nAll tests passed!")
    sys.exit(0)
