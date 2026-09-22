#!/usr/bin/env python
"""Startup script for Phase 8 - starts Flask backend in background."""
import subprocess
import time
import sys
import os
import tempfile

print("=" * 60)
print("IIUI Smart Chatbot - Phase 8 Startup")
print("=" * 60)

# Start Flask backend
print("\n[1/3] Starting Flask backend on port 5000...")
flask_proc = subprocess.Popen(
    [sys.executable, "flask_server.py"],
    stdout=open(os.path.join(tempfile.gettempdir(), "flask_out.log"), "w"),
    stderr=subprocess.STDOUT,
    cwd=os.getcwd(),
)
print(f"  Flask PID: {flask_proc.pid}")

# Wait for Flask to be ready
print("  Waiting for model loading and server startup...")
for i in range(90):
    time.sleep(1)
    if flask_proc.poll() is not None:
        print(f"  ERROR: Flask server exited with code {flask_proc.returncode}")
        with open(os.path.join(tempfile.gettempdir(), "flask_out.log")) as f:
            print(f.read()[-500:])
        sys.exit(1)
    try:
        import urllib.request
        req = urllib.request.urlopen("http://localhost:5000/api/health", timeout=2)
        data = req.read().decode()
        print(f"  Flask backend HEALTHY: {data}")
        break
    except Exception:
        if i % 10 == 9:
            print(f"  Still loading... ({i+1}s)")
        continue
else:
    print("  WARNING: Flask did not become healthy in 90s, checking anyway...")
    try:
        import urllib.request
        req = urllib.request.urlopen("http://localhost:5000/api/health", timeout=2)
        print(f"  Flask backend HEALTHY: {req.read().decode()}")
    except Exception as e:
        print(f"  ERROR: Flask not responding: {e}")
        sys.exit(1)

# Test key endpoints
print("\n[2/3] Testing key endpoints...")
import json
import urllib.request

tests = [
    ("Health", "http://localhost:5000/api/health"),
    ("FAQs", "http://localhost:5000/api/faqs"),
    ("Knowledge", "http://localhost:5000/api/knowledge"),
    ("Chat Modes", "http://localhost:5000/api/chat/modes"),
    ("AI Status", "http://localhost:5000/api/settings/ai/status"),
]

for name, url in tests:
    try:
        req = urllib.request.urlopen(url, timeout=5)
        data = json.loads(req.read().decode())
        status = "OK" if data.get("success") else "FAIL"
        print(f"  {name}: {status}")
    except Exception as e:
        print(f"  {name}: ERROR - {e}")

# Test chat
print("\n[3/3] Testing chat endpoints...")
try:
    chat_data = json.dumps({"message": "What is the admission process?", "mode": "mock"}).encode()
    req = urllib.request.Request(
        "http://localhost:5000/api/chat",
        data=chat_data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print(f"  Mock Chat: {'OK' if result.get('success') else 'FAIL'}")
    print(f"    Mode: {result.get('data', {}).get('mode', 'N/A')}")
    print(f"    Answer: {result.get('data', {}).get('answer', 'N/A')[:80]}...")
except Exception as e:
    print(f"  Mock Chat: ERROR - {e}")

try:
    chat_data = json.dumps({"message": "Hello", "mode": "live"}).encode()
    req = urllib.request.Request(
        "http://localhost:5000/api/chat",
        data=chat_data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=10)
    result = json.loads(resp.read().decode())
    print(f"  Live Chat: {'OK' if result.get('success') else 'FAIL'}")
    print(f"    Mode: {result.get('data', {}).get('mode', 'N/A')}")
except Exception as e:
    print(f"  Live Chat: ERROR - {e}")

print("\n" + "=" * 60)
print("APPLICATION STARTUP COMPLETE")
print("=" * 60)
print(f"\nFlask backend running on: http://localhost:5000")
print(f"Flask PID: {flask_proc.pid}")
print(f"\nTo start Streamlit frontend, run:")
print(f"  streamlit run app.py")
print(f"\nTo stop Flask backend:")
print(f"  kill {flask_proc.pid}")
