"""
Authentication & Dashboard Testing Script
Tests login functionality and session management
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"


def test_login_valid():
    """Test login with valid credentials"""
    print("\n🔍 TEST 1: Valid Login Credentials")
    print("=" * 50)
    
    url = f"{BASE_URL}/login"
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('success'):
            print("✅ PASSED: Login successful")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print("❌ FAILED: Login failed")
            print(f"   Message: {data.get('message')}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_login_invalid():
    """Test login with invalid credentials"""
    print("\n🔍 TEST 2: Invalid Login Credentials")
    print("=" * 50)
    
    url = f"{BASE_URL}/login"
    payload = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if not data.get('success'):
            print("✅ PASSED: Invalid credentials rejected")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print("❌ FAILED: Invalid credentials accepted")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_dashboard_redirect():
    """Test dashboard redirect without login"""
    print("\n🔍 TEST 3: Dashboard Redirect (No Login)")
    print("=" * 50)
    
    url = f"{BASE_URL}/dashboard"
    
    try:
        response = requests.get(url, allow_redirects=False)
        
        if response.status_code in [301, 302, 303, 307, 308]:
            print("✅ PASSED: Dashboard redirects to login")
            print(f"   Redirect to: {response.headers.get('Location')}")
            return True
        else:
            print("❌ FAILED: Dashboard accessible without login")
            print(f"   Status Code: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_session_management():
    """Test session creation and persistence"""
    print("\n🔍 TEST 4: Session Management")
    print("=" * 50)
    
    session = requests.Session()
    
    # Login
    login_url = f"{BASE_URL}/login"
    login_payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    try:
        # Perform login
        login_response = session.post(login_url, json=login_payload)
        login_data = login_response.json()
        
        if not login_data.get('success'):
            print("❌ FAILED: Could not login")
            return False
        
        print("✓ Login successful")
        
        # Try accessing dashboard
        dashboard_url = f"{BASE_URL}/dashboard"
        dashboard_response = session.get(dashboard_url)
        
        if dashboard_response.status_code == 200:
            print("✅ PASSED: Dashboard accessible with session")
            print(f"   Status Code: {dashboard_response.status_code}")
            return True
        else:
            print("❌ FAILED: Dashboard not accessible with session")
            print(f"   Status Code: {dashboard_response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_health_check():
    """Test health check endpoint"""
    print("\n🔍 TEST 5: Health Check Endpoint")
    print("=" * 50)
    
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 'healthy':
            print("✅ PASSED: Server is healthy")
            print(f"   Version: {data.get('version')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            return True
        else:
            print("❌ FAILED: Health check failed")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def run_all_tests():
    """Run all authentication tests"""
    print("\n" + "=" * 50)
    print("  AUTHENTICATION & DASHBOARD TEST SUITE")
    print("=" * 50)
    print(f"Target Server: {BASE_URL}")
    print(f"Test User: {TEST_USERNAME}")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Valid Login", test_login_valid()))
    results.append(("Invalid Login", test_login_invalid()))
    results.append(("Dashboard Redirect", test_dashboard_redirect()))
    results.append(("Session Management", test_session_management()))
    
    # Summary
    print("\n" + "=" * 50)
    print("  TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - Review output above")
    
    print("=" * 50)
    
    return passed == total


if __name__ == "__main__":
    print("\n🔐 Starting Authentication Tests...")
    print("⚠️  Make sure the Flask server is running!")
    print("   Run: python app.py")
    print("")
    
    input("Press ENTER to start tests...")
    
    success = run_all_tests()
    
    print("\n✓ Testing complete")
    exit(0 if success else 1)