"""
Phase 12 + 13 Test Suite: Admin Dashboard + Student Academic Assistance
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


# ==================== PHASE 12: ADMIN DASHBOARD ====================
print("\n=== PHASE 12: ADMIN DASHBOARD ===")


def test_admin_monitoring():
    r = get("/api/admin/monitoring", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and "total_users" in d.get("data", {})

test("Admin monitoring endpoint", test_admin_monitoring)


def test_admin_analytics():
    r = get("/api/admin/analytics", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("Admin analytics endpoint", test_admin_analytics)


def test_admin_chat_logs():
    r = get("/api/admin/chat-logs", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("Admin chat logs endpoint", test_admin_chat_logs)


def test_admin_users():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and isinstance(d.get("data"), list)

test("Admin users list", test_admin_users)


# ==================== KNOWLEDGE BASE CRUD ====================
print("\n=== KNOWLEDGE BASE CRUD ===")


def test_kb_create():
    r = post("/api/knowledge", {
        "category": "Courses",
        "question": f"Test KB entry {TEST_SUFFIX}",
        "answer": f"Test answer for KB {TEST_SUFFIX}",
        "keywords": "test, kb"
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 201 and r.get_json()["success"]

test("KB: Create entry", test_kb_create)


def test_kb_list():
    r = get("/api/knowledge", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("KB: List entries", test_kb_list)


def test_kb_search():
    r = get(f"/api/knowledge/search?q=test {TEST_SUFFIX}")
    return r.status_code == 200 and r.get_json()["success"]

test("KB: Search entries", test_kb_search)


def test_kb_update():
    # Get the latest entry
    r = get("/api/knowledge")
    entries = r.get_json().get("data", [])
    for e in entries:
        if f"Test KB entry {TEST_SUFFIX}" in e.get("question", ""):
            r2 = put(f"/api/knowledge/{e['id']}", {"answer": "Updated test answer"},
                     headers={"X-Session-Id": admin_session})
            return r2.status_code == 200
    return False

test("KB: Update entry", test_kb_update)


def test_kb_student_blocked():
    r = post("/api/knowledge", {"question": "X", "answer": "Y"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("KB: Student blocked from create", test_kb_student_blocked)


def test_kb_faculty_blocked():
    r = post("/api/knowledge", {"question": "X", "answer": "Y"})
    return r.status_code == 401

test("KB: Unauth blocked from create", test_kb_faculty_blocked)


# ==================== FAQ CRUD ====================
print("\n=== FAQ CRUD ===")


def test_faq_create():
    r = post("/api/faqs", {
        "question": f"Test FAQ {TEST_SUFFIX}",
        "answer": f"Test FAQ answer {TEST_SUFFIX}",
        "category": "General",
        "tags": "test"
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 201 and r.get_json()["success"]

test("FAQ: Create entry", test_faq_create)


def test_faq_list():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]

test("FAQ: List entries", test_faq_list)


def test_faq_search():
    r = get(f"/api/faqs/search?q=Test FAQ {TEST_SUFFIX}")
    return r.status_code == 200

test("FAQ: Search entries", test_faq_search)


def test_faq_student_blocked():
    r = post("/api/faqs", {"question": "X", "answer": "Y"},
             headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("FAQ: Student blocked", test_faq_student_blocked)


# ==================== USER MANAGEMENT ====================
print("\n=== USER MANAGEMENT ===")


def test_user_list():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0

test("Users: List all users", test_user_list)


def test_user_no_password():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    for u in d.get("data", []):
        if "password_hash" in u:
            return False
    return True

test("Users: No password exposed", test_user_no_password)


def test_student_blocked_users():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("Users: Student blocked", test_student_blocked_users)


# ==================== AI CONFIGURATION ====================
print("\n=== AI CONFIGURATION ===")


def test_ai_config_get():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]

test("AI: Get config", test_ai_config_get)


def test_ai_providers():
    r = get("/api/settings/ai/providers", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d.get("data", [])) > 0

test("AI: List providers", test_ai_providers)


def test_ai_status():
    r = get("/api/settings/ai/status")
    return r.status_code == 200 and r.get_json()["success"]

test("AI: Status endpoint", test_ai_status)


def test_ai_student_blocked():
    r = get("/api/settings/ai", headers={"X-Session-Id": student_session})
    return r.status_code == 403

test("AI: Student blocked", test_ai_student_blocked)


# ==================== PHASE 13: ACADEMIC ASSISTANCE ====================
print("\n=== PHASE 13: ACADEMIC ASSISTANCE ===")


def test_courses_list():
    r = get("/api/courses")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and isinstance(d.get("data"), list)

test("Courses: List all courses", test_courses_list)


def test_courses_by_semester():
    r = get("/api/courses?semester=1")
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("Courses: Filter by semester", test_courses_by_semester)


def test_courses_by_department():
    r = get("/api/courses?department=Computer")
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("Courses: Filter by department", test_courses_by_department)


def test_reminders_list():
    r = get("/api/reminders", headers={"X-Session-Id": student_session})
    return r.status_code == 200 and r.get_json()["success"]

test("Reminders: List reminders", test_reminders_list)


def test_reminders_create():
    r = post("/api/reminders", {
        "title": f"Test Reminder {TEST_SUFFIX}",
        "type": "exam",
        "description": "Test exam reminder",
        "reminder_date": "2026-12-15"
    }, headers={"X-Session-Id": student_session})
    return r.status_code == 201 and r.get_json()["success"]

test("Reminders: Create reminder", test_reminders_create)


def test_exam_knowledge():
    r = get("/api/knowledge?category=Examinations")
    d = r.get_json()
    return r.status_code == 200 and d["success"]

test("Academic: Exam knowledge available", test_exam_knowledge)


# ==================== CHAT WORKS WITH ALL PHASES ====================
print("\n=== CHAT INTEGRATION ===")


def test_chat_mock():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    return r.status_code == 200 and r.get_json()["success"]

test("Chat: Mock mode works", test_chat_mock)


def test_chat_live():
    r = post("/api/chat", {"message": "Hello", "mode": "live"})
    return r.status_code == 200 and r.get_json()["success"]

test("Chat: Live mode works", test_chat_live)


def test_chat_modes():
    r = get("/api/chat/modes")
    d = r.get_json()
    return r.status_code == 200 and "mock" in d.get("data", {})

test("Chat: Modes endpoint", test_chat_modes)


# ==================== HEALTH ====================
print("\n=== HEALTH ===")


def test_health():
    r = get("/api/health")
    return r.status_code == 200 and r.get_json()["success"]

test("Health check", test_health)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 12/13 TEST RESULTS")
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
