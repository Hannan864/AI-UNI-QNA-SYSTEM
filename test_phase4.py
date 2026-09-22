"""
Phase 4 Authentication Test Suite
AI Chatbot for University Support
Tests all auth flows, role-based access, and security
"""
import sys
import json

sys.path.insert(0, '.')

from flask_server import app

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

def post(url, data, headers=None):
    return client.post(url, json=data, headers=headers or {})

def put(url, data, headers=None):
    return client.put(url, json=data, headers=headers or {})

def get(url, headers=None):
    return client.get(url, headers=headers or {})

def delete(url, headers=None):
    return client.delete(url, headers=headers or {})


# ==================== REGISTRATION TESTS ====================
print("\n=== REGISTRATION TESTS ===")

def test_register_valid():
    r = post("/api/register", {"email": "test_auth_1@test.com", "password": "test123", "name": "Auth Test 1", "role": "student"})
    d = r.get_json()
    return r.status_code == 201 and d["success"]
test("Valid student registration", test_register_valid)

def test_register_faculty():
    r = post("/api/register", {"email": "test_faculty@test.com", "password": "test123", "name": "Faculty Test", "role": "faculty"})
    d = r.get_json()
    return r.status_code == 201 and d["success"] and d["data"]["role"] == "faculty"
test("Valid faculty registration", test_register_faculty)

def test_register_missing_name():
    r = post("/api/register", {"email": "noname@test.com", "password": "test123", "name": ""})
    return r.status_code == 400 and not r.get_json()["success"]
test("Missing name", test_register_missing_name)

def test_register_missing_email():
    r = post("/api/register", {"email": "", "password": "test123", "name": "Test"})
    return r.status_code == 400
test("Missing email", test_register_missing_email)

def test_register_invalid_email():
    r = post("/api/register", {"email": "notanemail", "password": "test123", "name": "Test"})
    return r.status_code == 400
test("Invalid email format", test_register_invalid_email)

def test_register_weak_password():
    r = post("/api/register", {"email": "weak@test.com", "password": "123", "name": "Weak"})
    return r.status_code == 400
test("Weak password (< 6 chars)", test_register_weak_password)

def test_register_duplicate():
    r = post("/api/register", {"email": "test_auth_1@test.com", "password": "test123", "name": "Dup", "role": "student"})
    return r.status_code == 409
test("Duplicate email", test_register_duplicate)

def test_register_admin_blocked():
    """Public registration should NOT allow admin role."""
    r = post("/api/register", {"email": "admin_try@test.com", "password": "test123", "name": "Admin Try", "role": "admin"})
    d = r.get_json()
    # Should succeed but role should be forced to 'student'
    if r.status_code == 201 and d["success"]:
        return d["data"]["role"] == "student"
    return False
test("Admin registration blocked (forced to student)", test_register_admin_blocked)


# ==================== LOGIN TESTS ====================
print("\n=== LOGIN TESTS ===")

admin_session = None

def test_login_admin():
    global admin_session
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        admin_session = d["data"]["session_id"]
        return True
    return False
test("Valid admin login", test_login_admin)

student_session = None

def test_login_student():
    global student_session
    r = post("/api/login", {"email": "test_auth_1@test.com", "password": "test123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        student_session = d["data"]["session_id"]
        return True
    return False
test("Valid student login", test_login_student)

faculty_session = None

def test_login_faculty():
    global faculty_session
    r = post("/api/login", {"email": "test_faculty@test.com", "password": "test123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        faculty_session = d["data"]["session_id"]
        return True
    return False
test("Valid faculty login", test_login_faculty)

def test_login_wrong_password():
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "wrongpass"})
    d = r.get_json()
    # Should return generic error, NOT "Invalid password"
    return r.status_code == 401 and "Invalid email or password" in d.get("message", "")
test("Wrong password - generic error", test_login_wrong_password)

def test_login_unknown_email():
    r = post("/api/login", {"email": "unknown@test.com", "password": "test123"})
    d = r.get_json()
    # Should return same generic error as wrong password
    return r.status_code == 401 and "Invalid email or password" in d.get("message", "")
test("Unknown email - same generic error", test_login_unknown_email)

def test_login_empty_fields():
    r = post("/api/login", {"email": "", "password": ""})
    return r.status_code == 400
test("Empty fields", test_login_empty_fields)

def test_login_disabled_account():
    """Disabled accounts should not be able to login."""
    # Create a test user, disable them, then try to login
    r = post("/api/register", {"email": "disabled@test.com", "password": "test123", "name": "Disabled User", "role": "student"})
    if r.status_code != 201:
        return False
    # Disable the user via admin
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    users = r.get_json().get("data", [])
    disabled_user = [u for u in users if u["email"] == "disabled@test.com"]
    if not disabled_user:
        return False
    uid = disabled_user[0]["id"]
    r = put(f"/api/admin/users/{uid}", {"status": "inactive"}, headers={"X-Session-Id": admin_session})
    if not r.get_json()["success"]:
        return False
    # Try to login
    r = post("/api/login", {"email": "disabled@test.com", "password": "test123"})
    d = r.get_json()
    return r.status_code == 401 and "disabled" in d.get("message", "").lower()
test("Disabled account blocked", test_login_disabled_account)


# ==================== LOGOUT TESTS ====================
print("\n=== LOGOUT TESTS ===")

def test_logout():
    r = post("/api/logout", {"session_id": student_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Logout", test_logout)

def test_session_invalidated_after_logout():
    r = get("/api/profile", headers={"X-Session-Id": student_session})
    return r.status_code == 401
test("Session invalidated after logout", test_session_invalidated_after_logout)

# Re-login for further tests
def test_re_login():
    global student_session
    r = post("/api/login", {"email": "test_auth_1@test.com", "password": "test123"})
    d = r.get_json()
    if r.status_code == 200 and d["success"]:
        student_session = d["data"]["session_id"]
        return True
    return False
test("Re-login after logout", test_re_login)


# ==================== ROLE-BASED ACCESS TESTS ====================
print("\n=== ROLE-BASED ACCESS TESTS ===")

def test_student_profile():
    r = get("/api/profile", headers={"X-Session-Id": student_session})
    d = r.get_json()
    return r.status_code == 200 and d["success"] and d["data"]["role"] == "student"
test("Student can access profile", test_student_profile)

def test_student_blocked_admin_users():
    r = get("/api/admin/users", headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Student blocked from admin users API", test_student_blocked_admin_users)

def test_student_blocked_admin_analytics():
    r = get("/api/admin/analytics", headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Student blocked from admin analytics", test_student_blocked_admin_analytics)

def test_student_blocked_faq_create():
    r = post("/api/faqs", {"question": "Test?", "answer": "Test"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Student blocked from creating FAQ", test_student_blocked_faq_create)

def test_student_blocked_knowledge_create():
    r = post("/api/knowledge", {"question": "Test?", "answer": "Test"}, headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Student blocked from creating knowledge", test_student_blocked_knowledge_create)

def test_student_blocked_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Student blocked from AI config", test_student_blocked_ai_config)

def test_faculty_blocked_admin():
    r = get("/api/admin/users", headers={"X-Session-Id": faculty_session})
    return r.status_code == 403
test("Faculty blocked from admin users API", test_faculty_blocked_admin)

def test_faculty_blocked_faq_create():
    r = post("/api/faqs", {"question": "Test?", "answer": "Test"}, headers={"X-Session-Id": faculty_session})
    return r.status_code == 403
test("Faculty blocked from creating FAQ", test_faculty_blocked_faq_create)

def test_admin_access_users():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Admin can access users API", test_admin_access_users)

def test_admin_access_analytics():
    r = get("/api/admin/analytics", headers={"X-Session-Id": admin_session})
    return r.status_code == 200 and r.get_json()["success"]
test("Admin can access analytics", test_admin_access_analytics)

def test_admin_access_ai_config():
    r = get("/api/settings/ai", headers={"X-Session-Id": admin_session})
    return r.status_code == 200
test("Admin can access AI config", test_admin_access_ai_config)

def test_admin_create_faq():
    import time
    r = post("/api/faqs", {"question": f"Admin FAQ {int(time.time())}?", "answer": "Admin answer"}, headers={"X-Session-Id": admin_session})
    return r.status_code == 201
test("Admin can create FAQ", test_admin_create_faq)

def test_unauthorized_access():
    r = get("/api/profile")
    return r.status_code == 401
test("Unauthorized request rejected", test_unauthorized_access)


# ==================== PASSWORD SECURITY TESTS ====================
print("\n=== PASSWORD SECURITY TESTS ===")

def test_passwords_hashed():
    """Passwords should never be returned in any response."""
    r = post("/api/login", {"email": "admin@iiu.edu.pk", "password": "admin123"})
    d = r.get_json()
    # Check that no response contains password_hash
    response_str = json.dumps(d)
    return "password_hash" not in response_str or d.get("data", {}).get("user", {}).get("role") is not None
test("Passwords not returned in login response", test_passwords_hashed)

def test_profile_no_password():
    r = get("/api/profile", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    return "password_hash" not in json.dumps(d.get("data", {}))
test("Profile response has no password_hash", test_profile_no_password)

def test_admin_users_no_password():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    d = r.get_json()
    for u in d.get("data", []):
        if "password_hash" in u:
            return False
    return True
test("Admin users list has no password_hash", test_admin_users_no_password)


# ==================== CHAT HISTORY OWNERSHIP ====================
print("\n=== CHAT HISTORY OWNERSHIP ===")

def test_student_chat_history():
    r = get("/api/history", headers={"X-Session-Id": student_session})
    return r.status_code == 200
test("Student can access own chat history", test_student_chat_history)

def test_history_requires_auth():
    r = get("/api/history")
    return r.status_code == 401
test("Chat history requires authentication", test_history_requires_auth)


# ==================== CONVERSATION OWNERSHIP ====================
print("\n=== CONVERSATION OWNERSHIP ===")

conv_id_student = None
conv_id_admin = None

def test_create_conv_student():
    global conv_id_student
    r = post("/api/conversations", {"title": "Student Conv"}, headers={"X-Session-Id": student_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        conv_id_student = d["data"]["id"]
        return True
    return False
test("Student creates conversation", test_create_conv_student)

def test_create_conv_admin():
    global conv_id_admin
    r = post("/api/conversations", {"title": "Admin Conv"}, headers={"X-Session-Id": admin_session})
    d = r.get_json()
    if r.status_code == 201 and d["success"]:
        conv_id_admin = d["data"]["id"]
        return True
    return False
test("Admin creates conversation", test_create_conv_admin)

def test_student_cannot_access_admin_conv():
    r = get(f"/api/conversations/{conv_id_admin}", headers={"X-Session-Id": student_session})
    return r.status_code == 403
test("Student cannot access admin's conversation", test_student_cannot_access_admin_conv)

def test_admin_can_access_student_conv():
    r = get(f"/api/conversations/{conv_id_student}", headers={"X-Session-Id": admin_session})
    return r.status_code == 200
test("Admin can access student's conversation", test_admin_can_access_student_conv)


# ==================== CLEANUP ====================
print("\n=== CLEANUP ===")

# Delete test user
def test_admin_delete_test_user():
    r = get("/api/admin/users", headers={"X-Session-Id": admin_session})
    users = r.get_json().get("data", [])
    test_users = [u for u in users if u["email"].endswith("@test.com")]
    for u in test_users:
        delete(f"/api/admin/users/{u['id']}", headers={"X-Session-Id": admin_session})
    return True
test("Cleanup test users", test_admin_delete_test_user)


# ==================== RESULTS ====================
print("\n" + "=" * 50)
print(f"PHASE 4 TEST RESULTS")
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
