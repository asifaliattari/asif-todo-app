"""
Production Test - Testing live deployment
Frontend: https://asif-todo-app.vercel.app
Backend: https://asifaliastolixgen-taskflow-api.hf.space
"""

import requests
import json
import time

BACKEND_URL = "https://asifaliastolixgen-taskflow-api.hf.space"
FRONTEND_URL = "https://asif-todo-app.vercel.app"

def print_header(text):
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70)

def print_test(name, passed, details=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"       {details}")

print_header("PRODUCTION DEPLOYMENT TEST")
print(f"Frontend: {FRONTEND_URL}")
print(f"Backend:  {BACKEND_URL}")

# Test 1: Frontend Accessible
print_header("TEST 1: Frontend Accessibility")
try:
    response = requests.get(FRONTEND_URL, timeout=10)
    print_test("Frontend homepage", response.status_code == 200,
               f"Status: {response.status_code}, Time: {response.elapsed.total_seconds():.2f}s")
except Exception as e:
    print_test("Frontend homepage", False, str(e))

# Test 2: Backend Health
print_header("TEST 2: Backend API Health")
try:
    response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print_test("Backend health", True,
                   f"Status: {data.get('status')}, DB: {data.get('database')}")
    else:
        print_test("Backend health", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Backend health", False, str(e))

# Test 3: Signup
print_header("TEST 3: User Signup")
timestamp = int(time.time())
test_user = {
    "name": f"Production Test {timestamp}",
    "email": f"prodtest{timestamp}@test.com",
    "password": "ProdTest123!"
}

try:
    response = requests.post(
        f"{BACKEND_URL}/api/auth/signup",
        json=test_user,
        timeout=15
    )

    if response.status_code == 201:
        data = response.json()
        token = data.get('token')
        user_id = data.get('user', {}).get('id')
        print_test("Signup", True, f"User created: {user_id[:8]}...")
        print(f"       Token: {token[:30]}...")

        # Test 4: Login
        print_header("TEST 4: User Login")
        login_response = requests.post(
            f"{BACKEND_URL}/api/auth/login",
            json={"email": test_user['email'], "password": test_user['password']},
            timeout=15
        )

        if login_response.status_code == 200:
            print_test("Login", True, "Authentication successful")

            # Test 5: Create Task
            print_header("TEST 5: Create Task")
            headers = {"Authorization": f"Bearer {token}"}
            task_data = {
                "title": "Production Test Task",
                "description": "Testing on Vercel deployment"
            }

            task_response = requests.post(
                f"{BACKEND_URL}/api/tasks",
                json=task_data,
                headers=headers,
                timeout=15
            )

            if task_response.status_code == 200:
                task = task_response.json()
                task_id = task['id']
                print_test("Create task", True, f"Task ID: {task_id}")

                # Test 6: List Tasks
                print_header("TEST 6: List Tasks")
                list_response = requests.get(
                    f"{BACKEND_URL}/api/tasks",
                    headers=headers,
                    timeout=15
                )

                if list_response.status_code == 200:
                    tasks_data = list_response.json()
                    count = tasks_data.get('total', 0)
                    print_test("List tasks", True, f"Found {count} task(s)")

                    # Test 7: Update Task
                    print_header("TEST 7: Update Task")
                    update_response = requests.put(
                        f"{BACKEND_URL}/api/tasks/{task_id}",
                        json={"title": "Updated Production Task", "completed": True},
                        headers=headers,
                        timeout=15
                    )

                    if update_response.status_code == 200:
                        print_test("Update task", True, "Task updated successfully")

                        # Test 8: Delete Task
                        print_header("TEST 8: Delete Task")
                        delete_response = requests.delete(
                            f"{BACKEND_URL}/api/tasks/{task_id}",
                            headers=headers,
                            timeout=15
                        )

                        if delete_response.status_code == 204:
                            print_test("Delete task", True, "Task deleted")
                        else:
                            print_test("Delete task", False, f"Status: {delete_response.status_code}")
                    else:
                        print_test("Update task", False, f"Status: {update_response.status_code}")
                else:
                    print_test("List tasks", False, f"Status: {list_response.status_code}")
            else:
                print_test("Create task", False, f"Status: {task_response.status_code}")
                print(f"       Response: {task_response.text[:200]}")
        else:
            print_test("Login", False, f"Status: {login_response.status_code}")
    else:
        print_test("Signup", False, f"Status: {response.status_code}")
        print(f"       Response: {response.text[:200]}")

except Exception as e:
    print_test("Authentication tests", False, str(e))

# Test 9: AI Chatbot
print_header("TEST 9: AI Chatbot (if token available)")
try:
    if 'token' in locals():
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {
            "message": "Hello! What can you help me with?",
            "conversation_id": None
        }

        print("       Sending message to AI chatbot...")
        chat_response = requests.post(
            f"{BACKEND_URL}/api/chat/message",
            json=chat_data,
            headers=headers,
            timeout=30
        )

        if chat_response.status_code == 200:
            data = chat_response.json()
            response_text = data.get('response', '')
            print_test("AI Chatbot", True, f"Response: {response_text[:60]}...")
        else:
            print_test("AI Chatbot", False, f"Status: {chat_response.status_code}")
    else:
        print_test("AI Chatbot", False, "No auth token available")
except Exception as e:
    print_test("AI Chatbot", False, str(e))

# Test 10: File Permissions
print_header("TEST 10: File Permission System")
try:
    if 'token' in locals():
        headers = {"Authorization": f"Bearer {token}"}
        perm_response = requests.get(
            f"{BACKEND_URL}/api/files/permission/status",
            headers=headers,
            timeout=15
        )

        if perm_response.status_code == 200:
            perm_data = perm_response.json()
            print_test("File permissions", True,
                       f"Has perm: {perm_data.get('has_permission')}, Admin: {perm_data.get('is_admin')}")
        else:
            print_test("File permissions", False, f"Status: {perm_response.status_code}")
    else:
        print_test("File permissions", False, "No auth token available")
except Exception as e:
    print_test("File permissions", False, str(e))

print("\n" + "="*70)
print("PRODUCTION TEST COMPLETE".center(70))
print("="*70)
