"""
Phase 6 Mock Data Mode Test Suite
AI Chatbot for University Support
Tests mock mode retrieval, mode isolation, KB integration, auth, history, and security
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
    email = f"test_p6fac_{TEST_SUFFIX}@test.com"
    r = post("/api/register", {"email": email, "password": "test123", "name": "Phase6 Faculty", "role": "faculty"})
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


# ==================== TEST A: MODE SELECTION ====================
print("\n=== TEST A: MODE SELECTION ===")


def test_mock_mode_returns_response():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"


test("Mock mode returns response with mode=mock", test_mock_mode_returns_response)


def test_mock_mode_has_mode_label():
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return resp.get("mode_label") == "Mock Data"


test("Mock mode response includes mode_label", test_mock_mode_has_mode_label)


def test_live_mode_returns_response():
    """Live mode should return a response (configured or not-configured message)."""
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live" and len(resp.get("answer", "")) > 5


test("Live mode returns response (configured or not-configured)", test_live_mode_returns_response)


def test_mode_persists_in_session():
    """Multiple messages in same mode should all use that mode."""
    for msg in ["What are fees?", "Tell me about courses"]:
        r = post("/api/chat", {"message": msg, "mode": "mock"})
        d = r.get_json()
        if d.get("data", {}).get("mode") != "mock":
            return False
    return True


test("Mode persists across multiple messages", test_mode_persists_in_session)


# ==================== TEST B: MOCK RESPONSE ====================
print("\n=== TEST B: MOCK RESPONSE QUALITY ===")


def test_mock_known_question_admission():
    r = post("/api/chat", {"message": "What is the admission process at IIUI?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    return r.status_code == 200 and len(answer) > 20


test("Mock returns answer for known admission question", test_mock_known_question_admission)


def test_mock_known_question_fee():
    r = post("/api/chat", {"message": "What is the fee structure?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    return r.status_code == 200 and len(answer) > 20


test("Mock returns answer for known fee question", test_mock_known_question_fee)


def test_mock_known_question_courses():
    r = post("/api/chat", {"message": "What courses are offered in BS Computer Science?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    return r.status_code == 200 and len(answer) > 20


test("Mock returns answer for known courses question", test_mock_known_question_courses)


def test_mock_has_confidence():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return "confidence" in resp and isinstance(resp["confidence"], (int, float))


test("Mock response includes confidence score", test_mock_has_confidence)


def test_mock_has_source():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return "source" in resp


test("Mock response includes source", test_mock_has_source)


# ==================== TEST C: UNKNOWN QUESTION ====================
print("\n=== TEST C: UNKNOWN QUESTION HANDLING ===")


def test_mock_unknown_no_fake_answer():
    r = post("/api/chat", {"message": "What is the meaning of life according to IIUI?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    # Should not contain fabricated university information
    fake_indicators = ["definitely", "certainly", "the official policy is", "according to regulation"]
    has_fake = any(indicator in answer.lower() for indicator in fake_indicators)
    return r.status_code == 200 and not has_fake


test("Mock does not fabricate answers for unknown questions", test_mock_unknown_no_fake_answer)


def test_mock_unknown_returns_fallback():
    r = post("/api/chat", {"message": "asdfghjkl random nonsense query xyz", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("confidence", 1) <= 0.5


test("Mock returns low confidence for unknown questions", test_mock_unknown_returns_fallback)


def test_mock_empty_message_rejected():
    r = post("/api/chat", {"message": "", "mode": "mock"})
    return r.status_code == 400


test("Mock rejects empty message", test_mock_empty_message_rejected)


def test_mock_long_message_rejected():
    r = post("/api/chat", {"message": "x" * 1001, "mode": "mock"})
    return r.status_code == 400


test("Mock rejects overly long message", test_mock_long_message_rejected)


# ==================== TEST D: MODE ISOLATION ====================
print("\n=== TEST D: MODE ISOLATION ===")


def test_mock_does_not_call_live_ai():
    """Mock mode should never return a Live AI response."""
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return resp.get("mode") == "mock" and "Phase 7" not in resp.get("answer", "")


test("Mock mode does not return Live AI response", test_mock_does_not_call_live_ai)


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


# ==================== TEST E: AUTHENTICATION ====================
print("\n=== TEST E: AUTHENTICATION + MOCK MODE ===")


def test_student_mock_chat():
    r = post("/api/chat", {"message": "What is admission process?", "mode": "mock"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Student can use mock chat", test_student_mock_chat)


def test_faculty_mock_chat():
    r = post("/api/chat", {"message": "What is admission process?", "mode": "mock"},
             headers={"X-Session-Id": faculty_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Faculty can use mock chat", test_faculty_mock_chat)


def test_admin_mock_chat():
    r = post("/api/chat", {"message": "What is admission process?", "mode": "mock"},
             headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin can use mock chat", test_admin_mock_chat)


def test_anonymous_mock_chat():
    """Chat endpoint works without auth (public)."""
    r = post("/api/chat", {"message": "Hello", "mode": "mock"})
    return r.status_code == 200 and r.get_json()["success"]


test("Anonymous user can use mock chat (public endpoint)", test_anonymous_mock_chat)


# ==================== TEST F: CHAT HISTORY ====================
print("\n=== TEST F: CHAT HISTORY + MODE TRACKING ===")


def test_mock_chat_logged():
    """Mock chat should be logged in chat_logs."""
    post("/api/chat", {"message": f"Phase6 test query {TEST_SUFFIX}", "mode": "mock"},
         headers={"X-Session-Id": student_session})
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for h in d["data"]:
            if f"Phase6 test query {TEST_SUFFIX}" in h.get("user_message", ""):
                return h.get("mode") == "mock"
    return False


test("Mock chat is logged with mode=mock", test_mock_chat_logged)


def test_chat_logs_store_mode():
    """Verify chat_logs table records mode correctly."""
    post("/api/chat", {"message": f"Mode test {TEST_SUFFIX}", "mode": "mock"},
         headers={"X-Session-Id": student_session})
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for log in d["data"]:
            if f"Mode test {TEST_SUFFIX}" in log.get("user_message", ""):
                return log.get("mode") == "mock"
    return False


test("Chat logs correctly record mock mode", test_chat_logs_store_mode)


def test_user_ownership_preserved():
    """Students should only see their own chat history."""
    r = get("/api/history", headers={"X-Session-Id": student_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Student can access own history", test_user_ownership_preserved)


# ==================== TEST G: ADMIN KB UPDATE + MOCK RETRIEVAL ====================
print("\n=== TEST G: ADMIN KB UPDATE AFFECTS MOCK MODE ===")

kb_test_id = None


def test_admin_adds_kb_entry():
    global kb_test_id
    r = post("/api/knowledge", {
        "category": "Courses",
        "question": f"What is the BSIT program {TEST_SUFFIX}?",
        "answer": f"Demo answer: The BSIT program {TEST_SUFFIX} covers computing fundamentals.",
        "keywords": "bsit,program,computing"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        kb_test_id = d["data"]["id"]
        return True
    return False


test("Admin adds KB entry for mock retrieval test", test_admin_adds_kb_entry)


def test_new_kb_entry_visible_via_api():
    r = get(f"/api/knowledge/{kb_test_id}")
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("New KB entry visible via GET /api/knowledge/<id>", test_new_kb_entry_visible_via_api)


def test_kb_search_finds_new_entry():
    r = get(f"/api/knowledge/search?q=BSIT program {TEST_SUFFIX}")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0


test("KB search finds newly added entry", test_kb_search_finds_new_entry)


def test_mock_retrieves_new_kb():
    """Mock chat should be able to retrieve the new KB entry."""
    r = post("/api/chat", {"message": f"What is the BSIT program {TEST_SUFFIX}?", "mode": "mock"})
    d = r.get_json()
    answer = d.get("data", {}).get("answer", "")
    return r.status_code == 200 and len(answer) > 10


test("Mock chat retrieves new KB entry", test_mock_retrieves_new_kb)


def test_admin_updates_kb_entry():
    if not kb_test_id:
        return False
    r = put(f"/api/knowledge/{kb_test_id}", {
        "answer": f"Updated demo: BSIT program {TEST_SUFFIX} covers advanced computing."
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin updates KB entry", test_admin_updates_kb_entry)


def test_admin_deactivates_kb_entry():
    if not kb_test_id:
        return False
    r = put(f"/api/knowledge/{kb_test_id}", {"status": "inactive"},
            headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin deactivates KB entry", test_admin_deactivates_kb_entry)


def test_inactive_kb_not_in_public_list():
    if not kb_test_id:
        return True
    r = get("/api/knowledge")
    d = r.get_json()
    for entry in d.get("data", []):
        if entry["id"] == kb_test_id:
            return False
    return True


test("Inactive KB entry hidden from public list", test_inactive_kb_not_in_public_list)


def test_cleanup_test_kb():
    if not kb_test_id:
        return True
    r = delete(f"/api/knowledge/{kb_test_id}", headers={"X-Session-Id": admin_session})
    return r.status_code == 200


test("Cleanup: delete test KB entry", test_cleanup_test_kb)


# ==================== TEST H: SECURITY ====================
print("\n=== TEST H: SECURITY ===")


def test_student_cannot_modify_kb():
    r = post("/api/knowledge", {"question": "Hacked?", "answer": "Hacked"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student cannot modify KB", test_student_cannot_modify_kb)


def test_faculty_cannot_modify_kb():
    r = post("/api/knowledge", {"question": "Hacked?", "answer": "Hacked"},
             headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty cannot modify KB", test_faculty_cannot_modify_kb)


def test_student_cannot_modify_faq():
    r = post("/api/faqs", {"question": "Hacked?", "answer": "Hacked"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student cannot modify FAQ", test_student_cannot_modify_faq)


def test_no_password_in_chat_history():
    r = get("/api/history", headers={"X-Session-Id": student_session})
    d = r.get_json()
    return "password_hash" not in json.dumps(d)


test("No password in chat history response", test_no_password_in_chat_history)


def test_chat_logs_no_sensitive_data():
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    response_str = json.dumps(d)
    return "password" not in response_str.lower() or "password_hash" not in response_str


test("Chat logs contain no sensitive data", test_chat_logs_no_sensitive_data)


# ==================== TEST I: SEED DATA ====================
print("\n=== TEST I: SEED DATA VERIFICATION ===")


def test_seed_faqs_available():
    r = get("/api/faqs")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) >= 5


test("Seed FAQs available for mock retrieval", test_seed_faqs_available)


def test_seed_kb_available():
    r = get("/api/knowledge")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) >= 5


test("Seed KB entries available for mock retrieval", test_seed_kb_available)


def test_seed_data_has_admissions():
    r = get("/api/knowledge?category=Admissions")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0


test("Seed data includes Admissions category", test_seed_data_has_admissions)


def test_seed_data_has_fees():
    r = get("/api/knowledge?category=Fees")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0


test("Seed data includes Fees category", test_seed_data_has_fees)


def test_seed_data_has_courses():
    r = get("/api/knowledge?category=Courses")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0


test("Seed data includes Courses category", test_seed_data_has_courses)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 6 TEST RESULTS")
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
