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

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")

def test_frontend_accessible():
    """Test if frontend is accessible"""
    print_header("Testing Frontend Accessibility")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print_success(f"Frontend accessible at {FRONTEND_URL}")
            print_info(f"Response time: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print_error(f"Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Frontend not accessible: {e}")
        return False

def test_backend_health():
    """Test backend API health"""
    print_header("Testing Backend API Health")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend API healthy")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Database: {data.get('database')}")
            return True
        else:
            print_error(f"Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Backend not accessible: {e}")
        return False

def test_auth_endpoints():
    """Test authentication system"""
    print_header("Testing Authentication System")

    # Test signup endpoint exists
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
            print_success("User signup successful")
            print_info(f"User ID: {data.get('user', {}).get('id')}")
            token = data.get('token')

            # Test authenticated request
            headers = {"Authorization": f"Bearer {token}"}
            tasks_response = requests.get(
                f"{BACKEND_URL}/api/tasks",
                headers=headers,
                timeout=10
            )

            if tasks_response.status_code == 200:
                print_success("JWT authentication working")
                return True, token
            else:
                print_error("JWT authentication failed")
                return False, None
        else:
            print_error(f"Signup failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False, None

    except Exception as e:
        print_error(f"Auth test failed: {e}")
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
            print_success(f"Created task ID: {task_id}")

            # READ
            response = requests.get(
                f"{BACKEND_URL}/api/tasks",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                print_success("Read tasks successful")

                # UPDATE
                response = requests.put(
                    f"{BACKEND_URL}/api/tasks/{task_id}",
                    json={"completed": True},
                    headers=headers,
                    timeout=10
                )
                if response.status_code == 200:
                    print_success("Updated task successful")

                    # DELETE
                    response = requests.delete(
                        f"{BACKEND_URL}/api/tasks/{task_id}",
                        headers=headers,
                        timeout=10
                    )
                    if response.status_code == 204:
                        print_success("Deleted task successful")
                        return True

        print_error("Task CRUD test incomplete")
        return False

    except Exception as e:
        print_error(f"Task CRUD test failed: {e}")
        return False

def test_chat_endpoint(token):
    """Test AI chatbot endpoint"""
    print_header("Testing AI Chatbot Endpoint")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Test chat message
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
            print_success("Chat endpoint working")
            print_info(f"Conversation ID: {data.get('conversation_id')}")
            print_info(f"Response preview: {data.get('response', '')[:100]}...")
            return True
        else:
            print_error(f"Chat endpoint failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Chat test failed: {e}")
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
            print_success("File permission endpoint working")
            print_info(f"Has permission: {perm_data.get('has_permission')}")
            print_info(f"Is admin: {perm_data.get('is_admin')}")

            # List files
            response = requests.get(
                f"{BACKEND_URL}/api/files",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                files_data = response.json()
                print_success(f"File listing working ({len(files_data.get('files', []))} files)")
                return True

        print_error("File endpoints test incomplete")
        return False

    except Exception as e:
        print_error(f"File test failed: {e}")
        return False

def test_admin_endpoints(token):
    """Test admin panel endpoints"""
    print_header("Testing Admin Panel Endpoints")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Try to access admin endpoints (will fail if not admin, which is expected)
        response = requests.get(
            f"{BACKEND_URL}/api/admin/users",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print_success("Admin endpoints accessible (user is admin)")
            return True
        elif response.status_code == 403:
            print_info("Admin endpoints protected (user not admin) - This is correct!")
            return True
        else:
            print_error(f"Admin endpoints returned unexpected status: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Admin test failed: {e}")
        return False

def generate_final_report(results):
    """Generate final test report"""
    print_header("FINAL TEST REPORT")

    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"\n{Colors.BOLD}Test Results:{Colors.END}")
    for test_name, passed in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if passed else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name}: {status}")

    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {Colors.GREEN}{passed_tests}{Colors.END}")
    print(f"  Failed: {Colors.RED}{failed_tests}{Colors.END}")
    print(f"  Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.END}")

    if success_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! Production deployment is fully functional.{Colors.END}")
    elif success_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Most tests passed. Minor issues detected.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Multiple tests failed. Production needs attention.{Colors.END}")

    print(f"\n{Colors.BOLD}Deployment URLs:{Colors.END}")
    print(f"  Frontend: {FRONTEND_URL}")
    print(f"  Backend:  {BACKEND_URL}")
    print(f"\n{Colors.BOLD}Phase III Features:{Colors.END}")
    print(f"  ✓ AI-Powered Chatbot (OpenAI GPT-4o-mini)")
    print(f"  ✓ Conversation Persistence (Database)")
    print(f"  ✓ Natural Language Task Management")
    print(f"  ✓ File Upload System")
    print(f"  ✓ Admin Permission Management")
    print(f"  ✓ JWT Authentication")
    print(f"  ✓ Multi-user Support")

    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}\n")

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        TaskFlow Phase III - Final Production Test         ║")
    print("║                 GIAIC Hackathon II 2026                    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")

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
        print_error("Skipping authenticated tests due to auth failure")
        results["Task CRUD"] = False
        results["AI Chatbot"] = False
        results["File System"] = False
        results["Admin Panel"] = False

    # Generate report
    generate_final_report(results)

if __name__ == "__main__":
    main()
