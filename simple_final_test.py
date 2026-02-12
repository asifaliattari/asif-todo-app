"""
Final Comprehensive Test Suite for TaskFlow Phase III
Tests production deployment at https://asif-todo-app.vercel.app/
"""

import requests
import json
from datetime import datetime

# Production URLs
FRONTEND_URL = "https://asif-todo-app.vercel.app"
BACKEND_URL = "https://asifaliastolixgen-taskflow-api.hf.space"

def print_header(text):
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")

def test_frontend_accessible():
    """Test if frontend is accessible"""
    print_header("Testing Frontend Accessibility")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print(f"[PASS] Frontend accessible at {FRONTEND_URL}")
            print(f"       Response time: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print(f"[FAIL] Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Frontend not accessible: {e}")
        return False

def test_backend_health():
    """Test backend API health"""
    print_header("Testing Backend API Health")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Backend API healthy")
            print(f"       Status: {data.get('status')}")
            print(f"       Database: {data.get('database')}")
            return True
        else:
            print(f"[FAIL] Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Backend not accessible: {e}")
        return False

def test_auth_endpoints():
    """Test authentication system"""
    print_header("Testing Authentication System")

    try:
        test_user = {
            "name": "Test User Final",
            "email": f"finaltest_{datetime.now().timestamp()}@test.com",
            "password": "TestPass123!"
        }

        response = requests.post(
            f"{BACKEND_URL}/api/auth/signup",
            json=test_user,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] User signup successful")
            print(f"       User ID: {data.get('user', {}).get('id')}")
            token = data.get('token')

            # Test authenticated request
            headers = {"Authorization": f"Bearer {token}"}
            tasks_response = requests.get(
                f"{BACKEND_URL}/api/tasks",
                headers=headers,
                timeout=10
            )

            if tasks_response.status_code == 200:
                print(f"[PASS] JWT authentication working")
                return True, token
            else:
                print(f"[FAIL] JWT authentication failed")
                return False, None
        else:
            print(f"[FAIL] Signup failed: {response.status_code}")
            print(f"       Response: {response.text[:200]}")
            return False, None

    except Exception as e:
        print(f"[FAIL] Auth test failed: {e}")
        return False, None

def test_task_crud(token):
    """Test task CRUD operations"""
    print_header("Testing Task CRUD Operations")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # CREATE
        new_task = {
            "title": "Final Test Task",
            "description": "Testing CRUD operations"
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
            print(f"[PASS] Created task ID: {task_id}")

            # READ
            response = requests.get(
                f"{BACKEND_URL}/api/tasks",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                print(f"[PASS] Read tasks successful")

                # UPDATE
                response = requests.put(
                    f"{BACKEND_URL}/api/tasks/{task_id}",
                    json={"completed": True},
                    headers=headers,
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"[PASS] Updated task successful")

                    # DELETE
                    response = requests.delete(
                        f"{BACKEND_URL}/api/tasks/{task_id}",
                        headers=headers,
                        timeout=10
                    )
                    if response.status_code == 204:
                        print(f"[PASS] Deleted task successful")
                        return True

        print(f"[FAIL] Task CRUD test incomplete")
        return False

    except Exception as e:
        print(f"[FAIL] Task CRUD test failed: {e}")
        return False

def test_chat_endpoint(token):
    """Test AI chatbot endpoint"""
    print_header("Testing AI Chatbot Endpoint")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        chat_data = {
            "message": "Hello, can you help me create a task?",
            "conversation_id": None
        }

        response = requests.post(
            f"{BACKEND_URL}/api/chat/message",
            json=chat_data,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Chat endpoint working")
            print(f"       Conversation ID: {data.get('conversation_id')}")
            print(f"       Response preview: {data.get('response', '')[:80]}...")
            return True
        else:
            print(f"[FAIL] Chat endpoint failed: {response.status_code}")
            print(f"       Response: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"[FAIL] Chat test failed: {e}")
        return False

def test_file_endpoints(token):
    """Test file upload system"""
    print_header("Testing File Upload System")

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
            print(f"[PASS] File permission endpoint working")
            print(f"       Has permission: {perm_data.get('has_permission')}")
            print(f"       Is admin: {perm_data.get('is_admin')}")

            # List files
            response = requests.get(
                f"{BACKEND_URL}/api/files",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                files_data = response.json()
                print(f"[PASS] File listing working ({len(files_data.get('files', []))} files)")
                return True

        print(f"[FAIL] File endpoints test incomplete")
        return False

    except Exception as e:
        print(f"[FAIL] File test failed: {e}")
        return False

def test_admin_endpoints(token):
    """Test admin panel endpoints"""
    print_header("Testing Admin Panel Endpoints")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/admin/users",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print(f"[PASS] Admin endpoints accessible (user is admin)")
            return True
        elif response.status_code == 403:
            print(f"[PASS] Admin endpoints protected (user not admin) - Correct!")
            return True
        else:
            print(f"[FAIL] Admin endpoints returned unexpected status: {response.status_code}")
            return False

    except Exception as e:
        print(f"[FAIL] Admin test failed: {e}")
        return False

def generate_final_report(results):
    """Generate final test report"""
    print("\n" + "="*60)
    print("FINAL TEST REPORT".center(60))
    print("="*60 + "\n")

    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print("Test Results:")
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {test_name}: {status}")

    print(f"\nSummary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print(f"\n*** ALL TESTS PASSED! Production deployment is fully functional. ***")
    elif success_rate >= 80:
        print(f"\n*** Most tests passed. Minor issues detected. ***")
    else:
        print(f"\n*** Multiple tests failed. Production needs attention. ***")

    print(f"\nDeployment URLs:")
    print(f"  Frontend: {FRONTEND_URL}")
    print(f"  Backend:  {BACKEND_URL}")

    print(f"\nPhase III Features:")
    print(f"  - AI-Powered Chatbot (OpenAI GPT-4o-mini)")
    print(f"  - Conversation Persistence (Database)")
    print(f"  - Natural Language Task Management")
    print(f"  - File Upload System")
    print(f"  - Admin Permission Management")
    print(f"  - JWT Authentication")
    print(f"  - Multi-user Support")

    print("\n" + "="*60 + "\n")

def main():
    print("\n" + "="*60)
    print("TaskFlow Phase III - Final Production Test".center(60))
    print("GIAIC Hackathon II 2026".center(60))
    print("="*60)

    results = {}

    # Run all tests
    results["Frontend Accessible"] = test_frontend_accessible()
    results["Backend Health"] = test_backend_health()

    auth_success, token = test_auth_endpoints()
    results["Authentication"] = auth_success

    if token:
        results["Task CRUD"] = test_task_crud(token)
        results["AI Chatbot"] = test_chat_endpoint(token)
        results["File System"] = test_file_endpoints(token)
        results["Admin Panel"] = test_admin_endpoints(token)
    else:
        print("[ERROR] Skipping authenticated tests due to auth failure")
        results["Task CRUD"] = False
        results["AI Chatbot"] = False
        results["File System"] = False
        results["Admin Panel"] = False

    # Generate report
    generate_final_report(results)

if __name__ == "__main__":
    main()
