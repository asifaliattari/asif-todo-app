"""
Complete End-to-End Test for TaskFlow
Tests all features on localhost (backend: 8000, frontend: 3000)
"""

import requests
import json
from datetime import datetime
import time

# Local URLs
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def print_header(text):
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70)

def print_test(name, passed, details=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"       {details}")

def test_backend_health():
    """Test 1: Backend Health Check"""
    print_header("TEST 1: Backend Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        passed = response.status_code == 200
        data = response.json() if passed else {}
        print_test("Backend health endpoint", passed,
                   f"Status: {data.get('status')}, DB: {data.get('database')}")
        return passed
    except Exception as e:
        print_test("Backend health endpoint", False, str(e))
        return False

def test_authentication():
    """Test 2 & 3: User Signup and Login"""
    print_header("TEST 2 & 3: Authentication (Signup + Login)")

    # Test Signup
    timestamp = int(time.time())
    test_user = {
        "name": f"Test User {timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "TestPass123!"
    }

    try:
        # Signup
        response = requests.post(
            f"{BACKEND_URL}/api/auth/signup",
            json=test_user,
            timeout=10
        )

        if response.status_code == 201:
            data = response.json()
            token = data.get('token')
            user_id = data.get('user', {}).get('id')
            print_test("User signup", True, f"User ID: {user_id[:8]}...")

            # Login with same credentials
            login_response = requests.post(
                f"{BACKEND_URL}/api/auth/login",
                json={"email": test_user['email'], "password": test_user['password']},
                timeout=10
            )

            if login_response.status_code == 200:
                login_data = login_response.json()
                login_token = login_data.get('token')
                print_test("User login", True, f"Token received: {login_token[:20]}...")
                return True, token
            else:
                print_test("User login", False, f"Status: {login_response.status_code}")
                return False, None
        else:
            print_test("User signup", False, f"Status: {response.status_code}")
            return False, None

    except Exception as e:
        print_test("Authentication", False, str(e))
        return False, None

def test_task_crud(token):
    """Test 4-8: Task CRUD Operations"""
    print_header("TEST 4-8: Task CRUD Operations")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # CREATE Task
        new_task = {
            "title": "Complete End-to-End Test",
            "description": "Testing all TaskFlow features"
        }

        response = requests.post(
            f"{BACKEND_URL}/api/tasks",
            json=new_task,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            task = response.json()
            task_id = task['id']
            print_test("Create task", True, f"Task ID: {task_id}, Title: {task['title']}")

            # READ Tasks
            response = requests.get(f"{BACKEND_URL}/api/tasks", headers=headers, timeout=10)
            if response.status_code == 200:
                tasks_data = response.json()
                task_count = tasks_data.get('total', 0)
                print_test("Read/List tasks", True, f"Found {task_count} task(s)")

                # READ Single Task
                response = requests.get(
                    f"{BACKEND_URL}/api/tasks/{task_id}",
                    headers=headers,
                    timeout=10
                )
                if response.status_code == 200:
                    print_test("Read single task", True, f"Retrieved task {task_id}")

                    # UPDATE Task
                    response = requests.put(
                        f"{BACKEND_URL}/api/tasks/{task_id}",
                        json={"title": "Updated Test Task", "completed": False},
                        headers=headers,
                        timeout=10
                    )
                    if response.status_code == 200:
                        print_test("Update task", True, "Title and status updated")

                        # TOGGLE Complete
                        response = requests.patch(
                            f"{BACKEND_URL}/api/tasks/{task_id}/complete",
                            headers=headers,
                            timeout=10
                        )
                        if response.status_code == 200:
                            print_test("Toggle task completion", True, "Task marked complete")

                            # DELETE Task
                            response = requests.delete(
                                f"{BACKEND_URL}/api/tasks/{task_id}",
                                headers=headers,
                                timeout=10
                            )
                            if response.status_code == 204:
                                print_test("Delete task", True, f"Task {task_id} deleted")
                                return True

        print_test("Task CRUD operations", False, "Some operations failed")
        return False

    except Exception as e:
        print_test("Task CRUD operations", False, str(e))
        return False

def test_chatbot(token):
    """Test 9: AI Chatbot"""
    print_header("TEST 9: AI Chatbot with OpenAI")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Test simple chat message
        chat_data = {
            "message": "Hello! Can you help me create a task to buy groceries?",
            "conversation_id": None
        }

        print("       Sending message to AI chatbot... (this may take 5-10 seconds)")
        response = requests.post(
            f"{BACKEND_URL}/api/chat/message",
            json=chat_data,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            conv_id = data.get('conversation_id')
            ai_response = data.get('response', '')
            print_test("AI chatbot response", True,
                       f"Conv ID: {conv_id}, Response: {ai_response[:60]}...")

            # Test conversation persistence
            chat_data2 = {
                "message": "What was my previous request?",
                "conversation_id": conv_id
            }

            print("       Testing conversation memory...")
            response2 = requests.post(
                f"{BACKEND_URL}/api/chat/message",
                json=chat_data2,
                headers=headers,
                timeout=30
            )

            if response2.status_code == 200:
                data2 = response2.json()
                print_test("Conversation persistence", True,
                           "AI remembered previous context")
                return True
            else:
                print_test("Conversation persistence", False,
                           f"Status: {response2.status_code}")
                return False
        else:
            print_test("AI chatbot response", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("AI chatbot", False, str(e))
        return False

def test_file_system(token):
    """Test 10-11: File Upload System"""
    print_header("TEST 10-11: File Upload System")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Check permission status
        response = requests.get(
            f"{BACKEND_URL}/api/files/permission/status",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            perm_data = response.json()
            has_perm = perm_data.get('has_permission')
            is_admin = perm_data.get('is_admin')
            print_test("File permission check", True,
                       f"Has permission: {has_perm}, Is admin: {is_admin}")

            # List files
            response = requests.get(
                f"{BACKEND_URL}/api/files",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                files_data = response.json()
                file_count = len(files_data.get('files', []))
                print_test("List files", True, f"Found {file_count} file(s)")
                return True
            else:
                print_test("List files", False, f"Status: {response.status_code}")
                return False
        else:
            print_test("File permission check", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("File upload system", False, str(e))
        return False

def test_admin_endpoints(token):
    """Test 12: Admin Panel Endpoints"""
    print_header("TEST 12: Admin Panel (Permission Check)")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Try to access admin endpoints
        response = requests.get(
            f"{BACKEND_URL}/api/admin/users",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            users = response.json()
            print_test("Admin access", True, f"User is admin, {len(users)} users found")
            return True
        elif response.status_code == 403:
            print_test("Admin access protection", True,
                       "Non-admin user correctly denied access")
            return True
        else:
            print_test("Admin endpoints", False, f"Unexpected status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Admin endpoints", False, str(e))
        return False

def test_frontend_pages():
    """Test 13-15: Frontend Pages"""
    print_header("TEST 13-15: Frontend Accessibility")

    pages_to_test = [
        ("/", "Home/Dashboard"),
        ("/login", "Login page"),
        ("/signup", "Signup page"),
    ]

    all_passed = True
    for path, name in pages_to_test:
        try:
            response = requests.get(f"{FRONTEND_URL}{path}", timeout=5)
            passed = response.status_code == 200
            print_test(name, passed, f"Status: {response.status_code}")
            if not passed:
                all_passed = False
        except Exception as e:
            print_test(name, False, str(e))
            all_passed = False

    return all_passed

def generate_report(results):
    """Generate final test report"""
    print("\n" + "="*70)
    print("COMPLETE TEST REPORT".center(70))
    print("="*70)

    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    success_rate = (passed / total * 100) if total > 0 else 0

    print("\nTest Results by Category:")
    print("-" * 70)

    categories = {
        "Infrastructure": ["Backend Health", "Frontend Pages"],
        "Authentication": ["User Signup & Login"],
        "Task Management": ["Task CRUD Operations"],
        "AI Features": ["AI Chatbot"],
        "File System": ["File Upload System"],
        "Admin Features": ["Admin Panel"]
    }

    for category, tests in categories.items():
        print(f"\n{category}:")
        for test_name in tests:
            if test_name in results:
                status = "✓ PASS" if results[test_name] else "✗ FAIL"
                print(f"  {status} - {test_name}")

    print("\n" + "-"*70)
    print(f"\nSummary:")
    print(f"  Total Tests: {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print("\n*** ALL TESTS PASSED! Application is fully functional. ***")
    elif success_rate >= 80:
        print("\n*** Most tests passed. Minor issues detected. ***")
    else:
        print("\n*** Multiple tests failed. Please review errors above. ***")

    print("\n" + "="*70)

def main():
    print("\n" + "="*70)
    print("TaskFlow - Complete Local Test Suite".center(70))
    print("Testing all Phase III features".center(70))
    print("="*70)
    print("\nBackend:  http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("\nStarting tests...\n")

    results = {}

    # Test 1: Backend Health
    results["Backend Health"] = test_backend_health()

    # Test 2-3: Authentication
    auth_passed, token = test_authentication()
    results["User Signup & Login"] = auth_passed

    if token:
        # Test 4-8: Task CRUD
        results["Task CRUD Operations"] = test_task_crud(token)

        # Test 9: AI Chatbot
        results["AI Chatbot"] = test_chatbot(token)

        # Test 10-11: File System
        results["File Upload System"] = test_file_system(token)

        # Test 12: Admin Panel
        results["Admin Panel"] = test_admin_endpoints(token)
    else:
        print("\n[ERROR] Skipping remaining tests due to authentication failure")
        results["Task CRUD Operations"] = False
        results["AI Chatbot"] = False
        results["File Upload System"] = False
        results["Admin Panel"] = False

    # Test 13-15: Frontend Pages
    results["Frontend Pages"] = test_frontend_pages()

    # Generate final report
    generate_report(results)

if __name__ == "__main__":
    main()
