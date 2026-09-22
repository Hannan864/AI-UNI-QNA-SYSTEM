"""
Phase 5 Knowledge Base & FAQ Management Test Suite
AI Chatbot for University Support
Tests all KB/FAQ CRUD, search, authorization, validation, and security
"""
import sys
import json
import time

sys.path.insert(0, '.')

from flask_server import app

client = app.test_client()
PASSED = 0
FAILED = 0
TEST_SUFFIX = str(int(time.time()))[-4:]  # unique suffix for this run


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


# ==================== SETUP: Login all roles ====================
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
    email = f"test_fac_{TEST_SUFFIX}@test.com"
    r = post("/api/register", {"email": email, "password": "test123", "name": "Phase5 Faculty", "role": "faculty"})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        faculty_session = d["data"]["session_id"]
        return True
    # Try login
    r2 = post("/api/login", {"email": email, "password": "test123"})
    d2 = r2.get_json()
    if r2.status_code == 200 and d2["success"]:
        faculty_session = d2["data"]["session_id"]
        return True
    return False


test("Setup faculty session", test_register_faculty)


# ==================== 1. KNOWLEDGE BASE - CREATE ====================
print("\n=== 1. KNOWLEDGE BASE - CREATE ===")

kb_id_1 = None


def test_kb_create_admin():
    global kb_id_1
    r = post("/api/knowledge", {
        "category": "Admissions",
        "question": f"Test question {TEST_SUFFIX} - What documents are needed for admission?",
        "answer": f"Test answer {TEST_SUFFIX}: Matric certificate, Intermediate certificate, CNIC, photos.",
        "keywords": "admission,documents,test"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        kb_id_1 = d["data"]["id"]
        return True
    print(f"    (status={r.status_code}, msg={d.get('message','')})")
    return False


test("Admin creates KB entry", test_kb_create_admin)


def test_kb_create_minimal():
    r = post("/api/knowledge", {
        "question": f"Test minimal {TEST_SUFFIX} - What are library hours?",
        "answer": f"Test {TEST_SUFFIX}: Library is open Mon-Sat, 8AM-8PM."
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 201 and d["success"]


test("Admin creates KB entry (minimal fields)", test_kb_create_minimal)


def test_kb_create_duplicate():
    r = post("/api/knowledge", {
        "category": "Admissions",
        "question": f"Test question {TEST_SUFFIX} - What documents are needed for admission?",
        "answer": "Duplicate answer"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 409 and not d["success"]


test("Admin KB create duplicate rejected (409)", test_kb_create_duplicate)


def test_kb_create_missing_question():
    r = post("/api/knowledge", {"answer": "Some answer"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("KB create missing question rejected", test_kb_create_missing_question)


def test_kb_create_missing_answer():
    r = post("/api/knowledge", {"question": "Some question?"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("KB create missing answer rejected", test_kb_create_missing_answer)


def test_kb_create_empty_body():
    r = post("/api/knowledge", {}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("KB create empty body rejected", test_kb_create_empty_body)


# ==================== 2. KNOWLEDGE BASE - READ ====================
print("\n=== 2. KNOWLEDGE BASE - READ ===")


def test_kb_list():
    r = get("/api/knowledge")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0


test("List KB entries (public)", test_kb_list)


def test_kb_list_filters_active_only():
    r = get("/api/knowledge")
    d = r.get_json()
    if not d.get("data"):
        return True
    for entry in d["data"]:
        if entry.get("status") != "active":
            return False
    return True


test("KB list returns only active for non-admin", test_kb_list_filters_active_only)


def test_kb_get_by_id():
    if not kb_id_1:
        return False
    r = get(f"/api/knowledge/{kb_id_1}")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["id"] == kb_id_1


test("Get KB entry by ID", test_kb_get_by_id)


def test_kb_list_by_category():
    r = get("/api/knowledge?category=Admissions")
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("List KB entries filtered by category", test_kb_list_by_category)


def test_kb_list_admin_sees_all():
    r = get("/api/knowledge", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Admin can list all KB entries", test_kb_list_admin_sees_all)


# ==================== 3. KNOWLEDGE BASE - SEARCH ====================
print("\n=== 3. KNOWLEDGE BASE - SEARCH ===")


def test_kb_search():
    r = get("/api/knowledge/search?q=admission")
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("KB search by keyword", test_kb_search)


def test_kb_search_no_results():
    r = get("/api/knowledge/search?q=xyznonexistent")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) == 0


test("KB search no results", test_kb_search_no_results)


def test_kb_search_empty_query():
    r = get("/api/knowledge/search")
    return r.status_code == 400


test("KB search empty query rejected", test_kb_search_empty_query)


def test_kb_search_injection():
    r = get("/api/knowledge/search?q='; DROP TABLE knowledge_base; --")
    d = r.get_json()
    return r.status_code in (200, 400)


test("KB search SQL injection attempt safe", test_kb_search_injection)


# ==================== 4. KNOWLEDGE BASE - UPDATE ====================
print("\n=== 4. KNOWLEDGE BASE - UPDATE ===")


def test_kb_update_admin():
    if not kb_id_1:
        return False
    r = put(f"/api/knowledge/{kb_id_1}", {
        "answer": f"Updated {TEST_SUFFIX}: Matric, Intermediate, CNIC, photos, domicile.",
        "keywords": "admission,documents,updated"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Admin updates KB entry", test_kb_update_admin)


def test_kb_update_status():
    if not kb_id_1:
        return False
    r = put(f"/api/knowledge/{kb_id_1}", {"status": "inactive"}, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("Admin updates KB status to inactive", test_kb_update_status)


def test_kb_inactive_hidden_from_public():
    if not kb_id_1:
        return True
    r = get("/api/knowledge")
    d = r.get_json()
    if d.get("data"):
        for entry in d["data"]:
            if entry["id"] == kb_id_1:
                return False
    return True


test("Inactive KB entry hidden from public", test_kb_inactive_hidden_from_public)


def test_kb_reactivate():
    if not kb_id_1:
        return False
    r = put(f"/api/knowledge/{kb_id_1}", {"status": "active"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin reactivates KB entry", test_kb_reactivate)


def test_kb_update_not_found():
    r = put("/api/knowledge/99999", {"answer": "Updated"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 404


test("KB update non-existent entry (404)", test_kb_update_not_found)


def test_kb_update_empty_fields():
    if not kb_id_1:
        return True
    r = put(f"/api/knowledge/{kb_id_1}", {}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("KB update with no fields rejected", test_kb_update_empty_fields)


# ==================== 5. KNOWLEDGE BASE - DELETE ====================
print("\n=== 5. KNOWLEDGE BASE - DELETE ===")

kb_id_to_delete = None


def test_kb_create_for_delete():
    global kb_id_to_delete
    r = post("/api/knowledge", {
        "question": f"Delete me {TEST_SUFFIX}",
        "answer": f"Delete this {TEST_SUFFIX}",
        "category": "General"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        kb_id_to_delete = d["data"]["id"]
        return True
    print(f"    (status={r.status_code}, msg={d.get('message','')})")
    return False


test("Create KB entry for deletion", test_kb_create_for_delete)


def test_kb_delete_admin():
    if not kb_id_to_delete:
        return False
    r = delete(f"/api/knowledge/{kb_id_to_delete}", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin deletes KB entry", test_kb_delete_admin)


def test_kb_delete_not_found():
    if not kb_id_to_delete:
        return True
    r = delete(f"/api/knowledge/{kb_id_to_delete}", headers={"X-Session-Id": admin_session})
    return r.status_code == 404


test("KB delete already-deleted entry (404)", test_kb_delete_not_found)


# ==================== 6. FAQ - CREATE ====================
print("\n=== 6. FAQ - CREATE ===")

faq_id_1 = None


def test_faq_create_admin():
    global faq_id_1
    r = post("/api/faqs", {
        "question": f"Test FAQ {TEST_SUFFIX} - How do I apply for financial aid?",
        "answer": f"Test {TEST_SUFFIX}: Submit application to financial aid office.",
        "category": "Scholarships",
        "tags": "financial aid,test"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        faq_id_1 = d["data"]["id"]
        return True
    print(f"    (status={r.status_code}, msg={d.get('message','')})")
    return False


test("Admin creates FAQ", test_faq_create_admin)


def test_faq_create_duplicate():
    r = post("/api/faqs", {
        "question": f"Test FAQ {TEST_SUFFIX} - How do I apply for financial aid?",
        "answer": "Duplicate",
        "category": "Scholarships"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return r.status_code == 409 and not d["success"]


test("FAQ create duplicate rejected (409)", test_faq_create_duplicate)


def test_faq_create_missing_question():
    r = post("/api/faqs", {"answer": "Answer"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("FAQ create missing question rejected", test_faq_create_missing_question)


def test_faq_create_missing_answer():
    r = post("/api/faqs", {"question": "Question?"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("FAQ create missing answer rejected", test_faq_create_missing_answer)


# ==================== 7. FAQ - READ ====================
print("\n=== 7. FAQ - READ ===")


def test_faq_list():
    r = get("/api/faqs")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) > 0


test("List FAQs (public)", test_faq_list)


def test_faq_get_by_id():
    if not faq_id_1:
        return False
    r = get(f"/api/faqs/{faq_id_1}")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["id"] == faq_id_1


test("Get FAQ by ID", test_faq_get_by_id)


def test_faq_get_not_found():
    r = get("/api/faqs/99999")
    return r.status_code == 404


test("Get FAQ not found (404)", test_faq_get_not_found)


# ==================== 8. FAQ - SEARCH ====================
print("\n=== 8. FAQ - SEARCH ===")


def test_faq_search():
    r = get("/api/faqs/search?q=financial")
    d = r.get_json()
    return r.status_code == 200 and d["success"]


test("FAQ search by keyword", test_faq_search)


def test_faq_search_no_results():
    r = get("/api/faqs/search?q=xyznonexistent")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) == 0


test("FAQ search no results", test_faq_search_no_results)


def test_faq_search_empty():
    r = get("/api/faqs/search")
    return r.status_code == 400


test("FAQ search empty query rejected", test_faq_search_empty)


# ==================== 9. FAQ - UPDATE ====================
print("\n=== 9. FAQ - UPDATE ===")


def test_faq_update_admin():
    if not faq_id_1:
        return False
    r = put(f"/api/faqs/{faq_id_1}", {
        "answer": f"Updated {TEST_SUFFIX}: Submit to financial aid office with income certificate.",
        "status": "draft"
    }, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin updates FAQ", test_faq_update_admin)


def test_faq_update_status():
    if not faq_id_1:
        return False
    r = put(f"/api/faqs/{faq_id_1}", {"status": "archived"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin updates FAQ status", test_faq_update_status)


def test_faq_update_not_found():
    r = put("/api/faqs/99999", {"answer": "Updated"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 404


test("FAQ update not found (404)", test_faq_update_not_found)


def test_faq_update_empty():
    if not faq_id_1:
        return True
    r = put(f"/api/faqs/{faq_id_1}", {}, headers={"X-Session-Id": admin_session})
    return r.status_code == 400


test("FAQ update empty fields rejected", test_faq_update_empty)


# ==================== 10. FAQ - DELETE ====================
print("\n=== 10. FAQ - DELETE ===")

faq_id_to_delete = None


def test_faq_create_for_delete():
    global faq_id_to_delete
    r = post("/api/faqs", {
        "question": f"Delete me FAQ {TEST_SUFFIX}",
        "answer": f"Delete this FAQ {TEST_SUFFIX}",
        "category": "General"
    }, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        faq_id_to_delete = d["data"]["id"]
        return True
    print(f"    (status={r.status_code}, msg={d.get('message','')})")
    return False


test("Create FAQ for deletion", test_faq_create_for_delete)


def test_faq_delete_admin():
    if not faq_id_to_delete:
        return False
    r = delete(f"/api/faqs/{faq_id_to_delete}", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]


test("Admin deletes FAQ", test_faq_delete_admin)


def test_faq_delete_not_found():
    if not faq_id_to_delete:
        return True
    r = delete(f"/api/faqs/{faq_id_to_delete}", headers={"X-Session-Id": admin_session})
    return r.status_code == 404


test("FAQ delete already-deleted (404)", test_faq_delete_not_found)


# ==================== 11. AUTHORIZATION ====================
print("\n=== 11. AUTHORIZATION ===")


def test_student_blocked_kb_create():
    r = post("/api/knowledge", {"question": "Auth test?", "answer": "Auth test"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from KB create", test_student_blocked_kb_create)


def test_student_blocked_kb_update():
    if not kb_id_1:
        return True  # skip if no test entry
    r = put(f"/api/knowledge/{kb_id_1}", {"answer": "Hacked"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from KB update", test_student_blocked_kb_update)


def test_student_blocked_kb_delete():
    if not kb_id_1:
        return True  # skip if no test entry
    r = delete(f"/api/knowledge/{kb_id_1}", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from KB delete", test_student_blocked_kb_delete)


def test_student_blocked_faq_create():
    r = post("/api/faqs", {"question": "Auth test?", "answer": "Auth test"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from FAQ create", test_student_blocked_faq_create)


def test_student_blocked_faq_update():
    if not faq_id_1:
        return True
    r = put(f"/api/faqs/{faq_id_1}", {"answer": "Hacked"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from FAQ update", test_student_blocked_faq_update)


def test_student_blocked_faq_delete():
    if not faq_id_1:
        return True
    r = delete(f"/api/faqs/{faq_id_1}", headers={"X-Session-Id": student_session})
    return r.status_code == 403


test("Student blocked from FAQ delete", test_student_blocked_faq_delete)


def test_faculty_blocked_kb_create():
    r = post("/api/knowledge", {"question": "Auth test?", "answer": "Auth test"}, headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from KB create", test_faculty_blocked_kb_create)


def test_faculty_blocked_faq_create():
    r = post("/api/faqs", {"question": "Auth test?", "answer": "Auth test"}, headers={"X-Session-Id": faculty_session})
    return r.status_code == 403


test("Faculty blocked from FAQ create", test_faculty_blocked_faq_create)


def test_student_can_read_kb():
    r = get("/api/knowledge")
    return r.status_code == 200 and r.get_json()["success"]


test("Student can read KB entries", test_student_can_read_kb)


def test_student_can_read_faqs():
    r = get("/api/faqs")
    return r.status_code == 200 and r.get_json()["success"]


test("Student can read FAQs", test_student_can_read_faqs)


def test_student_can_search_kb():
    r = get("/api/knowledge/search?q=admission")
    return r.status_code == 200


test("Student can search KB", test_student_can_search_kb)


def test_unauth_blocked_kb_create():
    r = post("/api/knowledge", {"question": "Test?", "answer": "Test"})
    return r.status_code == 401


test("Unauthenticated blocked from KB create", test_unauth_blocked_kb_create)


def test_unauth_blocked_faq_create():
    r = post("/api/faqs", {"question": "Test?", "answer": "Test"})
    return r.status_code == 401


test("Unauthenticated blocked from FAQ create", test_unauth_blocked_faq_create)


# ==================== 12. SEED DATA VERIFICATION ====================
print("\n=== 12. SEED DATA VERIFICATION ===")


def test_seed_faqs_exist():
    r = get("/api/faqs")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) >= 5


test("Seed FAQ data present (>= 5)", test_seed_faqs_exist)


def test_seed_kb_exist():
    r = get("/api/knowledge")
    d = r.get_json()
    return r.status_code == 200 and d["success"] and len(d["data"]) >= 5


test("Seed KB data present (>= 5)", test_seed_kb_exist)


def test_seed_kb_has_categories():
    r = get("/api/knowledge")
    d = r.get_json()
    if not d.get("data"):
        return False
    categories = set(e.get("category") for e in d["data"])
    required = {"Admissions", "Fees", "Courses"}
    return required.issubset(categories)


test("Seed KB has required categories", test_seed_kb_has_categories)


# ==================== 13. SECURITY ====================
print("\n=== 13. SECURITY ===")


def test_no_password_in_kb_response():
    r = get("/api/knowledge")
    d = r.get_json()
    response_str = json.dumps(d)
    return "password_hash" not in response_str


test("No password in KB response", test_no_password_in_kb_response)


def test_no_password_in_faq_response():
    r = get("/api/faqs")
    d = r.get_json()
    response_str = json.dumps(d)
    return "password_hash" not in response_str


test("No password in FAQ response", test_no_password_in_faq_response)


def test_kb_search_special_chars():
    r = get("/api/knowledge/search?q=<script>alert('xss')</script>")
    return r.status_code in (200, 400)


test("KB search handles special chars safely", test_kb_search_special_chars)


def test_faq_search_special_chars():
    r = get("/api/faqs/search?q=<script>alert('xss')</script>")
    return r.status_code in (200, 400)


test("FAQ search handles special chars safely", test_faq_search_special_chars)


# ==================== 14. CHAT INTEGRATION ====================
print("\n=== 14. CHAT INTEGRATION ===")


def test_chat_with_kb_data():
    r = post("/api/chat", {"message": "What is the admission process?", "mode": "mock"})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d.get("data", {}).get("answer")


test("Mock chat returns KB-based response", test_chat_with_kb_data)


def test_chat_with_faq_data():
    r = post("/api/chat", {"message": "How do I register for courses?", "mode": "mock"})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d.get("data", {}).get("answer")


test("Mock chat returns FAQ-based response", test_chat_with_faq_data)


# ==================== RESULTS ====================
print("\n" + "=" * 55)
print(f"PHASE 5 TEST RESULTS")
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
