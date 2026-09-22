"""
Database Initialization - AI Chatbot for University Support
Seeds database with IIUI demo data for development/testing.
All data is clearly marked as DEMO/MOCK data.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import DatabaseManager
from auth.login import AuthManager


def initialize_iiui_data():
    db = DatabaseManager()
    auth = AuthManager()

    # === 1. ADMIN USER ===
    admin_email = 'admin@iiu.edu.pk'
    admin_pass = 'admin123'
    existing_user = db.get_user_by_email(admin_email)

    if existing_user:
        print(f"Admin '{admin_email}' exists. Resetting password...")
        conn = db._get_connection()
        cursor = conn.cursor()
        new_hash = auth.hash_password(admin_pass)
        cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (new_hash, admin_email))
        conn.commit()
        conn.close()
        print("Admin password reset.")
    else:
        print("Creating default admin...")
        auth.register_user(email=admin_email, password=admin_pass, name='Admin User', role='admin')
        print("Default admin created.")

    # === 2. DEMO STUDENT USER ===
    student_email = 'student@iiu.edu.pk'
    student_pass = 'student123'
    if not db.get_user_by_email(student_email):
        auth.register_user(email=student_email, password=student_pass, name='Demo Student', role='student')
        print("Demo student created.")

    # === 3. FAQs ===
    faqs_count = db.get_total_faqs()
    if faqs_count <= 1:
        print("Seeding FAQs...")
        faqs = [
            ("What is the admission process at IIUI?",
             "IIUI admissions require: 1) Online application submission, 2) Entry test, 3) Interview. Admission weightage: 40% Entry Test, 40% Academic Qualification, 20% Interview.",
             "admission,application,process", "Admissions"),
            ("What is the fee structure?",
             "Fee structure varies by program. For Fall 2024: B.Ed programs range from Rs. 53,300. BS CS total fee is approx Rs. 102,000.",
             "fee,cost,payment", "Fees"),
            ("How do I register for courses?",
             "Course registration is done through the IIUI student portal. Registration opens at the start of each semester.",
             "register,course,enrollment", "Courses"),
            ("When are examinations held?",
             "Mid-term exams are typically held in the middle of the semester. Final exams are held at the end.",
             "exam,examination,schedule", "Examinations"),
            ("What scholarships are available?",
             "IIUI offers merit-based scholarships, need-based financial aid, HEC scholarships, and sports quotas.",
             "scholarship,financial aid,funding", "Scholarships"),
            ("How can I contact the university?",
             "Main campus: H-9, Islamabad. Phone: +92-51-9257900. Website: www.iiu.edu.pk.",
             "contact,phone,email,address", "General"),
            ("What is the attendance policy?",
             "Students must maintain at least 75% attendance to be eligible for final examinations.",
             "attendance,policy,minimum", "Academic Policies"),
            ("How do I get my transcript?",
             "Transcripts can be requested from the examination department. Processing takes 5-7 working days.",
             "transcript,record,academic", "Student Services"),
        ]
        for q, a, tags, cat in faqs:
            db.add_faq(q, a, tags, cat)
        print(f"Seeded {len(faqs)} FAQs.")

    # === 4. KNOWLEDGE BASE ===
    kb_count = db.get_total_knowledge()
    if kb_count == 0:
        print("Seeding Knowledge Base...")
        kb_entries = [
            ("Admissions", "What documents are required for admission?",
             "Required documents: 1) Matric/O-Level certificate, 2) Intermediate/A-Level certificate, 3) CNIC/B-Form, 4) Photographs, 5) Domicile, 6) Entry test result.",
             "admission,documents,required"),
            ("Admissions", "What is the last date for admission?",
             "Admission deadlines vary by semester. Spring deadline is in January, Fall deadline is in July.",
             "admission,deadline,last date"),
            ("Fees", "What payment methods are accepted?",
             "IIUI accepts: Bank challan (HBL/ABL), online banking, and fee submission through the student portal.",
             "fee,payment,method,bank"),
            ("Courses", "What courses are offered in BS Computer Science?",
             "BS CS includes: Programming Fundamentals, Data Structures, Algorithms, Database Systems, OS, Software Engineering, AI, ML, Networks.",
             "courses,bscs,computer science"),
            ("Examinations", "What is the grading system?",
             "IIUI uses a 4.0 CGPA scale. A+=4.0, A=4.0, A-=3.7, B+=3.3, B=3.0, B-=2.7, C+=2.3, C=2.0, F=0.0.",
             "grading,cgpa,score"),
            ("Academic Policies", "What is the withdrawal policy?",
             "Students can withdraw from a course within the first 4 weeks without academic penalty.",
             "withdraw,policy,course"),
            ("Student Services", "Where is the library?",
             "The central library is in the main academic block. Open Mon-Sat, 8AM-8PM. Digital resources available 24/7.",
             "library,book,resource"),
            ("Scholarships", "How do I apply for financial aid?",
             "Financial aid applications are submitted through the financial aid office with income certificate and academic record.",
             "scholarship,financial aid,application"),
        ]
        for cat, q, a, kw in kb_entries:
            db.add_knowledge(cat, q, a, kw)
        print(f"Seeded {len(kb_entries)} Knowledge Base entries.")

    # === 5. COURSES ===
    conn = db._get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM courses")
    course_count = c.fetchone()[0]
    conn.close()

    if course_count == 0:
        print("Seeding Courses...")
        courses = [
            ("CS101", "Programming Fundamentals", 1, "Computer Science", 3),
            ("CS102", "Object Oriented Programming", 2, "Computer Science", 3),
            ("CS201", "Data Structures & Algorithms", 3, "Computer Science", 3),
            ("CS202", "Database Systems", 4, "Computer Science", 3),
            ("CS301", "Operating Systems", 5, "Computer Science", 3),
            ("CS302", "Software Engineering", 6, "Computer Science", 3),
            ("CS401", "Artificial Intelligence", 7, "Computer Science", 3),
            ("CS402", "Machine Learning", 8, "Computer Science", 3),
            ("CS403", "Computer Networks", 7, "Computer Science", 3),
            ("CS404", "Natural Language Processing", 8, "Computer Science", 3),
            ("MA101", "Calculus & Analytical Geometry", 1, "Mathematics", 3),
            ("MA201", "Linear Algebra", 3, "Mathematics", 3),
            ("EN101", "English Composition", 1, "English", 3),
            ("EN201", "Technical Writing", 3, "English", 2),
        ]
        for code, name, sem, dept, cred in courses:
            db.add_course(code, name, sem, dept, cred)
        print(f"Seeded {len(courses)} courses.")

    # === 6. ACADEMIC INFO ===
    conn = db._get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM academic_info")
    ai_count = c.fetchone()[0]
    conn.close()

    if ai_count == 0:
        print("Seeding Academic Info...")
        academic_entries = [
            ("Schedule", "Fall 2024 Semester Timeline",
             "Classes start: August 19, 2024. Mid-terms: October 7-11. Finals: December 16-27, 2024.", 1),
            ("Schedule", "Spring 2025 Semester Timeline",
             "Classes start: February 3, 2025. Mid-terms: March 24-28. Finals: June 2-13, 2025.", 2),
            ("Policies", "Academic Integrity Policy",
             "Plagiarism, cheating, and academic dishonesty are strictly prohibited.", None),
            ("Services", "Career Services",
             "Career services provide resume workshops, interview prep, and job placement assistance.", None),
        ]
        for cat, title, content, sem in academic_entries:
            db.add_academic_info(cat, title, content, sem)
        print(f"Seeded {len(academic_entries)} academic info entries.")

    # === 7. CONTACTS ===
    conn = db._get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM contacts")
    contact_count = c.fetchone()[0]
    conn.close()

    if contact_count == 0:
        print("Seeding Contacts...")
        contacts = [
            ("Admissions Office", "Admissions Desk", "admissions@iiu.edu.pk", "+92-51-9257900", "Admin Block, Room 101", "Mon-Fri 9AM-4PM"),
            ("Examination Department", "Exam Controller", "exam@iiu.edu.pk", "+92-51-9257910", "Academic Block, Room 205", "Mon-Fri 9AM-3PM"),
            ("Finance Office", "Finance Desk", "finance@iiu.edu.pk", "+92-51-9257920", "Admin Block, Room 103", "Mon-Fri 9AM-2PM"),
            ("Student Affairs", "Student Affairs", "student.affairs@iiu.edu.pk", "+92-51-9257930", "Student Center, Room 1", "Mon-Fri 8AM-5PM"),
            ("IT Help Desk", "IT Support", "ithelp@iiu.edu.pk", "+92-51-9257940", "IT Block, Room 101", "Mon-Sat 8AM-6PM"),
            ("Library", "Head Librarian", "library@iiu.edu.pk", "+92-51-9257950", "Central Library", "Mon-Sat 8AM-8PM"),
        ]
        for dept, person, email, phone, loc, hours in contacts:
            db.add_contact(dept, person, email, phone, loc, hours)
        print(f"Seeded {len(contacts)} contacts.")

    # === 8. CHAT LOG DEMO DATA ===
    conn = db._get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chat_logs")
    log_count = c.fetchone()[0]
    conn.close()

    if log_count == 0:
        print("Seeding demo chat logs...")
        demo_logs = [
            (student_email, "What is the admission process?", "IIUI admissions require online application, entry test, and interview...", 0.92, "mock", "admission_query"),
            (student_email, "Fee structure for BS CS?", "BS CS total fee is approximately Rs. 102,000 per semester.", 0.88, "mock", "fee_query"),
            (student_email, "When are exams?", "Mid-term exams are in October, finals in December.", 0.85, "mock", "exam_query"),
            (student_email, "How to register for courses?", "Course registration is done through the IIUI student portal.", 0.90, "mock", "registration_query"),
            (student_email, "Tell me about scholarships", "IIUI offers merit-based and need-based scholarships.", 0.87, "mock", "scholarship_query"),
        ]
        for email, msg, resp, conf, mode, intent in demo_logs:
            db.log_chat(email, msg, resp, conf, mode, intent)
        print(f"Seeded {len(demo_logs)} demo chat logs.")

    print("\nDatabase initialization complete!")
    print(f"\nDemo Credentials:")
    print(f"  Admin:   {admin_email} / {admin_pass}")
    print(f"  Student: {student_email} / {student_pass}")


if __name__ == '__main__':
    initialize_iiui_data()
