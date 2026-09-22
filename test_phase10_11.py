"""
Phase 10 + 11 ML Model + Response Generation Test Suite
AI Chatbot for University Support
Tests ML training, prediction, response generation, integration
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


# ==================== TEST 1: ML TRAINING ====================
print("\n=== TEST 1: ML TRAINING ===")


def test_ml_training():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    return ml.is_trained

test("ML model is trained on init", test_ml_training)


def test_ml_has_training_data():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    return ml.metadata.get('dataset_size', 0) > 50

test("Training dataset has sufficient data", test_ml_has_training_data)


def test_ml_has_intents():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    return ml.metadata.get('num_intents', 0) >= 8

test("Model covers multiple intents", test_ml_has_intents)


def test_ml_accuracy_above_threshold():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    return ml.metadata.get('accuracy', 0) > 0.5

test("Model accuracy > 50%", test_ml_accuracy_above_threshold)


def test_ml_retrain():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.retrain()
    return result is True

test("Model retrainable", test_ml_retrain)


# ==================== TEST 2: ML PREDICTION ====================
print("\n=== TEST 2: ML PREDICTION ===")


def test_ml_predict_admissions():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What is the admission process?")
    return result['intent'] == 'admissions' and result['confidence'] > 0.3

test("Predicts admissions intent", test_ml_predict_admissions)


def test_ml_predict_fees():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What is the fee structure?")
    return result['intent'] == 'fees' and result['confidence'] > 0.3

test("Predicts fees intent", test_ml_predict_fees)


def test_ml_predict_exams():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("When are final exams?")
    return result['intent'] == 'examinations' and result['confidence'] > 0.3

test("Predicts examinations intent", test_ml_predict_exams)


def test_ml_predict_courses():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What courses are offered?")
    return result['intent'] == 'courses' and result['confidence'] > 0.3

test("Predicts courses intent", test_ml_predict_courses)


def test_ml_predict_registration():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("How do I register for courses?")
    return result['intent'] == 'course_registration' and result['confidence'] > 0.3

test("Predicts course_registration intent", test_ml_predict_registration)


def test_ml_predict_unknown():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("xyzabc123 random nonsense")
    return result['intent'] == 'unknown' or result['confidence'] < 0.4

test("Low confidence for unknown input", test_ml_predict_unknown)


def test_ml_predict_empty():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("")
    return result['intent'] == 'unknown'

test("Empty input returns unknown", test_ml_predict_empty)


def test_ml_predict_policies():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What are the academic policies?")
    return result['intent'] == 'academic_policies' and result['confidence'] > 0.3

test("Predicts academic_policies intent", test_ml_predict_policies)


def test_ml_predict_services():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What services does the university offer?")
    return result['intent'] == 'university_services' and result['confidence'] > 0.3

test("Predicts university_services intent", test_ml_predict_services)


def test_ml_predict_schedules():
    from models.ml_classifier import MLClassifier
    ml = MLClassifier()
    result = ml.predict("What is the class schedule?")
    return result['intent'] == 'schedules' and result['confidence'] > 0.3

test("Predicts schedules intent", test_ml_predict_schedules)


# ==================== TEST 3: ML MODEL STATUS ====================
print("\n=== TEST 3: ML MODEL STATUS ===")


def test_ml_status_api():
    r = get("/api/ml/status")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"].get("is_trained")

test("ML status API returns trained status", test_ml_status_api)


def test_ml_status_has_metrics():
    r = get("/api/ml/status")
    d = r.get_json()
    data = d.get("data", {})
    return "accuracy" in data and "f1_score" in data

test("ML status includes evaluation metrics", test_ml_status_has_metrics)


# ==================== TEST 4: RESPONSE GENERATION ====================
print("\n=== TEST 4: RESPONSE GENERATION ===")


def test_response_generator():
    from models.response_generator import ResponseGenerator
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    rg = ResponseGenerator()
    nlp_result = nlp.process_query("What is the admission process?")
    response = rg.generate_response(nlp_result)
    return response.get("answer") and len(response["answer"]) > 10

test("Response generator produces answer", test_response_generator)


def test_response_has_intent():
    from models.response_generator import ResponseGenerator
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    rg = ResponseGenerator()
    nlp_result = nlp.process_query("What is the fee structure?")
    response = rg.generate_response(nlp_result)
    return response.get("intent") == "fees"

test("Response generator preserves intent", test_response_has_intent)


def test_response_unknown_fallback():
    from models.response_generator import ResponseGenerator
    from models.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    rg = ResponseGenerator()
    nlp_result = nlp.process_query("Tell me a joke")
    response = rg.generate_response(nlp_result)
    return response.get("answer") and response.get("intent") == "unknown"

test("Unknown queries get fallback response", test_response_unknown_fallback)


# ==================== TEST 5: CHAT INTEGRATION ====================
print("\n=== TEST 5: CHAT INTEGRATION ===")


def test_chat_with_nlp_ml():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and d["success"] and resp.get("mode") == "mock"

test("Chat works with NLP+ML integration", test_chat_with_nlp_ml)


def test_chat_admissions_response():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and len(resp.get("answer", "")) > 10

test("Admissions query gets substantive answer", test_chat_admissions_response)


def test_chat_fees_response():
    r = post("/api/chat", {"message": "What is the fee structure?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and len(resp.get("answer", "")) > 10

test("Fee query gets substantive answer", test_chat_fees_response)


def test_chat_exams_response():
    r = post("/api/chat", {"message": "When are the final exams?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"

test("Exam query works in mock mode", test_chat_exams_response)


def test_chat_courses_response():
    r = post("/api/chat", {"message": "What courses are offered?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"

test("Courses query works in mock mode", test_chat_courses_response)


def test_chat_registration_response():
    r = post("/api/chat", {"message": "How do I register for courses?", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"

test("Registration query works", test_chat_registration_response)


def test_chat_unknown_response():
    r = post("/api/chat", {"message": "Tell me a joke", "mode": "mock"})
    d = r.get_json()
    resp = d.get("data", {})
    return r.status_code == 200 and resp.get("mode") == "mock"

test("Unknown query handled gracefully", test_chat_unknown_response)


def test_chat_empty_rejected():
    r = post("/api/chat", {"message": "", "mode": "mock"})
    return r.status_code == 400

test("Empty message rejected", test_chat_empty_rejected)


def test_chat_long_rejected():
    r = post("/api/chat", {"message": "x" * 1001, "mode": "mock"})
    return r.status_code == 400

test("Long message rejected", test_chat_long_rejected)


# ==================== TEST 6: MODE ISOLATION ====================
print("\n=== TEST 6: MODE ISOLATION ===")


def test_mode_isolation_mock():
    r = post("/api/chat", {"message": "What is admission?", "mode": "mock"})
    resp = r.get_json().get("data", {})
    return resp.get("mode") == "mock"

test("Mock mode stays mock", test_mode_isolation_mock)


def test_mode_isolation_live():
    r = post("/api/chat", {"message": "What is admission?", "mode": "live"})
    resp = r.get_json().get("data", {})
    return resp.get("mode") == "live"

test("Live mode stays live", test_mode_isolation_live)


def test_invalid_mode_defaults():
    r = post("/api/chat", {"message": "Hello", "mode": "invalid"})
    resp = r.get_json().get("data", {})
    return resp.get("mode") == "mock"

test("Invalid mode defaults to mock", test_invalid_mode_defaults)


# ==================== TEST 7: AUTHORIZATION ====================
print("\n=== TEST 7: AUTHORIZATION ===")


def test_student_blocked_nlp():
    r = post("/api/nlp/process", {"message": "Hello"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student blocked from NLP endpoint", test_student_blocked_nlp)


def test_student_blocked_retrain():
    r = post("/api/ml/retrain", {}, headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student blocked from ML retrain", test_student_blocked_retrain)

def test_admin_can_nlp():
    r = post("/api/nlp/process", {"message": "What is admission?"},
             headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("Admin can use NLP endpoint", test_admin_can_nlp)

def test_admin_can_retrain():
    r = post("/api/ml/retrain", {}, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("Admin can retrain ML model", test_admin_can_retrain)


# ==================== TEST 8: CHAT HISTORY ====================
print("\n=== TEST 8: CHAT HISTORY ===")


def test_chat_stored_in_history():
    msg = f"Phase10_11 test {TEST_SUFFIX}"
    post("/api/chat", {"message": msg, "mode": "mock"},
         headers={"X-Session-Id": student_session})
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if d.get("success") and d.get("data"):
        for log in d["data"]:
            if msg in log.get("user_message", ""):
                return True
    return False

test("Chat stored in history", test_chat_stored_in_history)


# ==================== TEST 9: PHASE 3-8 REGRESSION ====================
print("\n=== TEST 9: REGRESSION SMOKE TESTS ===")


def test_reg_health():
    r = get("/api/health")
    return r.status_code == 200 and r.get_json()["success"]

test("Health check", test_reg_health)


def test_reg_faqs():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]

test("FAQs endpoint", test_reg_faqs)


def test_reg_knowledge():
    r = get("/api/knowledge")
    return r.status_code == 200 and r.get_json()["success"]

test("Knowledge endpoint", test_reg_knowledge)


def test_reg_courses():
    r = get("/api/courses")
    return r.status_code == 200 and r.get_json()["success"]

test("Courses endpoint", test_reg_courses)


def test_reg_profile():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("Profile endpoint", test_reg_profile)


def test_reg_chat_modes():
    r = get("/api/chat/modes")
    d = r.get_json()
    return r.status_code == 200 and "mock" in d.get("data", {})

test("Chat modes endpoint", test_reg_chat_modes)


def test_reg_ai_status():
    r = get("/api/settings/ai/status")
    return r.status_code == 200 and r.get_json()["success"]

test("AI status endpoint", test_reg_ai_status)


def test_reg_mock_chat():
    r = post("/api/chat", {"message": "What is admission?", "mode": "mock"})
    return r.status_code == 200 and r.get_json()["success"]

test("Mock chat regression", test_reg_mock_chat)


def test_reg_live_chat():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    return r.status_code == 200 and r.get_json()["success"]

test("Live chat regression", test_reg_live_chat)


def test_reg_student_blocked_admin():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Student blocked from admin", test_reg_student_blocked_admin)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 10/11 TEST RESULTS")
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
