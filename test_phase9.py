"""
Phase 9 NLP Processing Module Test Suite
AI Chatbot for University Support
Tests NLTK preprocessing, intent detection, entity extraction, integration
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


# ==================== SETUP ====================
print("\n=== SETUP: AUTHENTICATION ===")

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


# ==================== TEST 1: NLP PREPROCESSING ====================
print("\n=== TEST 1: NLP PREPROCESSING ===")


def test_nlp_preprocessing():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.preprocess_text("What is the fee structure for BSIT?")
    return isinstance(result, str) and len(result) > 0

test("Preprocessing produces output", test_nlp_preprocessing)


def test_nlp_preprocessing_removes_stopwords():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.preprocess_text("What is the fee structure?")
    return "what" not in result.split() and "is" not in result.split() and "the" not in result.split()

test("Preprocessing removes stopwords", test_nlp_preprocessing_removes_stopwords)


def test_nlp_preprocessing_lemmatizes():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.preprocess_text("What are the fees for courses?")
    return "fee" in result or "course" in result

test("Preprocessing lemmatizes words", test_nlp_preprocessing_lemmatizes)


def test_nlp_clean_text():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.clean_text("  Hello,   World!  ")
    return result == "hello world"

test("Clean text normalizes whitespace", test_nlp_clean_text)


def test_nlp_tokenize():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    tokens = nlp.tokenize("What is the fee structure?")
    return isinstance(tokens, list) and len(tokens) > 0

test("Tokenization produces tokens", test_nlp_tokenize)


def test_nlp_empty_input():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.preprocess_text("")
    return result == ''

test("Empty input handled safely", test_nlp_empty_input)


# ==================== TEST 2: INTENT DETECTION ====================
print("\n=== TEST 2: INTENT DETECTION ===")


def test_intent_admissions():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What is the admission process?")
    return result['intent'] == 'admissions' and result['confidence'] > 0.3

test("Detects admissions intent", test_intent_admissions)


def test_intent_fees():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What is the fee structure?")
    return result['intent'] == 'fees' and result['confidence'] > 0.3

test("Detects fees intent", test_intent_fees)


def test_intent_examinations():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("When are the final exams?")
    return result['intent'] == 'examinations' and result['confidence'] > 0.3

test("Detects examinations intent", test_intent_examinations)


def test_intent_courses():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What courses are offered?")
    return result['intent'] == 'courses' and result['confidence'] > 0.3

test("Detects courses intent", test_intent_courses)


def test_intent_registration():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("How do I register for courses?")
    return result['intent'] == 'course_registration' and result['confidence'] > 0.3

test("Detects course_registration intent", test_intent_registration)


def test_intent_services():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What services does the university offer?")
    return result['intent'] == 'university_services' and result['confidence'] > 0.3

test("Detects university_services intent", test_intent_services)


def test_intent_schedules():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What is the class schedule?")
    return result['intent'] == 'schedules' and result['confidence'] > 0.3

test("Detects schedules intent", test_intent_schedules)


def test_intent_policies():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("What are the academic policies?")
    return result['intent'] == 'academic_policies' and result['confidence'] > 0.3

test("Detects academic_policies intent", test_intent_policies)


def test_intent_unknown():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("Tell me a joke")
    return result['intent'] == 'unknown'

test("Detects unknown intent", test_intent_unknown)


def test_intent_empty():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.detect_intent("")
    return result['intent'] == 'unknown' and result['confidence'] == 0.0

test("Empty input returns unknown", test_intent_empty)


# ==================== TEST 3: ENTITY EXTRACTION ====================
print("\n=== TEST 3: ENTITY EXTRACTION ===")


def test_entity_program():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    entities = nlp.extract_entities("What about the BSIT program?")
    return len(entities.get('programs', [])) > 0

test("Extracts program entity", test_entity_program)


def test_entity_semester():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    entities = nlp.extract_entities("What courses in first semester?")
    return len(entities.get('semesters', [])) > 0

test("Extracts semester entity", test_entity_semester)


def test_entity_exam_type():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    entities = nlp.extract_entities("When is the midterm exam?")
    return len(entities.get('exam_types', [])) > 0

test("Extracts exam type entity", test_entity_exam_type)


def test_entity_empty():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    entities = nlp.extract_entities("")
    return isinstance(entities, dict) and len(entities) > 0

test("Empty input returns empty entities", test_entity_empty)


# ==================== TEST 4: STRUCTURED QUERY ====================
print("\n=== TEST 4: STRUCTURED NLP RESULT ===")


def test_process_query():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.process_query("What is the fee structure for BSIT?")
    return (result.get('original_text') and
            result.get('cleaned_text') and
            isinstance(result.get('tokens'), list) and
            result.get('intent') and
            isinstance(result.get('intent_confidence'), (int, float)) and
            isinstance(result.get('entities'), dict))

test("process_query returns structured result", test_process_query)


def test_process_query_unknown():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.process_query("xyzabc123 random")
    return result.get('intent') == 'unknown'

test("process_query handles unknown queries", test_process_query_unknown)


def test_process_query_empty():
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    result = nlp.process_query("")
    return result.get('intent') == 'unknown' and result.get('intent_confidence') == 0.0

test("process_query handles empty input", test_process_query_empty)


# ==================== TEST 5: NLP INTEGRATION WITH MOCK CHAT ====================
print("\n=== TEST 5: NLP INTEGRATION WITH MOCK CHAT ===")


def test_nlp_enhanced_mock_chat():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"

test("NLP-enhanced mock chat works", test_nlp_enhanced_mock_chat)


def test_nlp_enhanced_mock_has_answer():
    r = post("/api/chat", {"message": "What is the fee structure?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and len(resp.get("answer", "")) > 10

test("NLP-enhanced mock returns answer", test_nlp_enhanced_mock_has_answer)


def test_live_mode_still_works():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "live"

test("Live mode still functional", test_live_mode_still_works)


def test_mode_isolation_with_nlp():
    r_mock = post("/api/chat", {"message": "What is admission?", "mode": "mock"})
    r_live = post("/api/chat", {"message": "What is admission?", "mode": "live"})
    mock_resp = r_mock.get_json().get("data", {})
    live_resp = r_live.get_json().get("data", {})
    return mock_resp.get("mode") == "mock" and live_resp.get("mode") == "live"

test("Mode isolation maintained with NLP", test_mode_isolation_with_nlp)


# ==================== TEST 6: NLP API ENDPOINT ====================
print("\n=== TEST 6: NLP API ENDPOINT ===")


def test_nlp_endpoint_admin():
    r = post("/api/nlp/process", {"message": "What is the admission process?"},
             headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        nlp_data = d["data"].get("nlp", {})
        return nlp_data.get("intent") == "admissions"
    return False

test("NLP endpoint works for admin", test_nlp_endpoint_admin)


def test_nlp_endpoint_student_blocked():
    r = post("/api/nlp/process", {"message": "Hello"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("NLP endpoint blocked for students", test_nlp_endpoint_student_blocked)


# ==================== TEST 7: ML STATUS ENDPOINT ====================
print("\n=== TEST 7: ML STATUS ENDPOINT ===")


def test_ml_status():
    r = get("/api/ml/status")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"].get("is_trained")

test("ML status endpoint works", test_ml_status)


# ==================== TEST 8: AUTHENTICATION REMAINS FUNCTIONAL ====================
print("\n=== TEST 8: AUTHENTICATION REMAINS FUNCTIONAL ===")


def test_auth_health():
    r = get("/api/health")
    return r.status_code == 200 and r.get_json()["success"]

test("Health check", test_auth_health)


def test_auth_register():
    r = post("/api/register", {
        "email": f"p9test_{TEST_SUFFIX}@test.com",
        "password": "test123",
        "name": "Phase9 Test",
        "role": "student"
    })
    return r.status_code == 201 and r.get_json()["success"]

test("Registration", test_auth_register)


def test_auth_login():
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    return r.status_code == 200 and r.get_json()["success"]

test("Login", test_auth_login)


def test_auth_unauthorized():
    r = get("/api/profile")
    return r.status_code == 401

test("Unauthorized blocked", test_auth_unauthorized)


# ==================== TEST 9: PHASE 3-8 REGRESSION SMOKE TESTS ====================
print("\n=== TEST 9: REGRESSION SMOKE TESTS ===")


def test_reg_faqs():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]

test("FAQs endpoint", test_reg_faqs)


def test_reg_knowledge():
    r = get("/api/knowledge")
    return r.status_code == 200 and r.get_json()["success"]

test("Knowledge endpoint", test_reg_knowledge)


def test_reg_mock_chat():
    r = post("/api/chat", {"message": "What is admission process?", "mode": "mock"})
    return r.status_code == 200 and r.get_json()["success"]

test("Mock chat", test_reg_mock_chat)


def test_reg_live_chat():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    return r.status_code == 200 and r.get_json()["success"]

test("Live chat", test_reg_live_chat)


def test_reg_chat_modes():
    r = get("/api/chat/modes")
    d = r.get_json()
    return r.status_code == 200 and "mock" in d.get("data", {})

test("Chat modes endpoint", test_reg_chat_modes)


def test_reg_ai_status():
    r = get("/api/settings/ai/status")
    return r.status_code == 200 and r.get_json()["success"]

test("AI status endpoint", test_reg_ai_status)


def test_reg_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("Profile endpoint", test_reg_profile)


def test_reg_courses():
    r = get("/api/courses")
    return r.status_code == 200 and r.get_json()["success"]

test("Courses endpoint", test_reg_courses)


def test_reg_student_blocked_admin():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student blocked from admin", test_reg_student_blocked_admin)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 9 TEST RESULTS")
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
