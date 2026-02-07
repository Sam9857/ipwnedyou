# Testing Guide - I Pwned You OSINT Platform

## Pre-Testing Checklist

Before running tests, ensure:

1. ✅ Python 3.8+ is installed
2. ✅ All dependencies are installed (`pip install -r requirements.txt`)
3. ✅ Flask server is running (`python app.py`)
4. ✅ Server is accessible at `http://127.0.0.1:5000`

---

## Manual Testing Procedures

### 1. Authentication Testing

#### Test 1.1: Valid Login
**Steps:**
1. Navigate to `http://127.0.0.1:5000`
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click "LOGIN"

**Expected Result:**
- ✅ Login successful message
- ✅ Redirect to dashboard
- ✅ Username displayed in sidebar
- ✅ All menu items visible

#### Test 1.2: Invalid Login
**Steps:**
1. Navigate to `http://127.0.0.1:5000/login`
2. Enter wrong credentials
3. Click "LOGIN"

**Expected Result:**
- ✅ Error message displayed
- ✅ "Invalid credentials. Default is admin/admin123"
- ✅ Remains on login page
- ✅ Form fields cleared

#### Test 1.3: Direct Dashboard Access (Not Logged In)
**Steps:**
1. Open incognito/private window
2. Navigate directly to `http://127.0.0.1:5000/dashboard`

**Expected Result:**
- ✅ Automatic redirect to login page
- ✅ No dashboard content visible

---

### 2. Dashboard Testing

#### Test 2.1: Dashboard Loads
**Steps:**
1. Login with valid credentials
2. Observe dashboard page

**Expected Result:**
- ✅ Dashboard title visible
- ✅ Three quick-start cards displayed
- ✅ Platform information card visible
- ✅ Getting started section visible
- ✅ Dark theme applied
- ✅ Crosshair cursor active

#### Test 2.2: Navigation
**Steps:**
1. From dashboard, click each sidebar menu item
2. Verify each page loads

**Expected Result:**
- ✅ Domain Scan page loads
- ✅ IP Scan page loads
- ✅ Image Intelligence page loads
- ✅ Reports page loads
- ✅ Creator page loads
- ✅ Active menu item highlighted in red

#### Test 2.3: Logout
**Steps:**
1. Click "LOGOUT" button in sidebar
2. Observe result

**Expected Result:**
- ✅ Redirect to login page
- ✅ Session cleared
- ✅ Cannot access protected pages

---

### 3. Session Persistence Testing

#### Test 3.1: Session Maintains After Navigation
**Steps:**
1. Login successfully
2. Navigate through multiple pages
3. Check if session persists

**Expected Result:**
- ✅ Username remains in sidebar
- ✅ No logout or redirect
- ✅ All pages accessible

#### Test 3.2: Multiple Tab Handling
**Steps:**
1. Login in one tab
2. Open new tab
3. Navigate to `http://127.0.0.1:5000/dashboard`

**Expected Result:**
- ✅ Dashboard loads immediately (session shared)
- ✅ No login required

---

## Automated Testing

### Running Test Script
```bash
# Ensure server is running first
python app.py

# In another terminal, run tests
python test_authentication.py
```

### Expected Output
```
═══════════════════════════════════════════════════════
  AUTHENTICATION & DASHBOARD TEST SUITE
═══════════════════════════════════════════════════════

🔍 TEST 1: Valid Login Credentials
✅ PASSED: Login successful

🔍 TEST 2: Invalid Login Credentials
✅ PASSED: Invalid credentials rejected

🔍 TEST 3: Dashboard Redirect (No Login)
✅ PASSED: Dashboard redirects to login

🔍 TEST 4: Session Management
✅ PASSED: Dashboard accessible with session

🔍 TEST 5: Health Check Endpoint
✅ PASSED: Server is healthy

═══════════════════════════════════════════════════════
  TEST SUMMARY
═══════════════════════════════════════════════════════
✅ PASSED: Health Check
✅ PASSED: Valid Login
✅ PASSED: Invalid Login
✅ PASSED: Dashboard Redirect
✅ PASSED: Session Management
═══════════════════════════════════════════════════════
Results: 5/5 tests passed
🎉 ALL TESTS PASSED!
```

---

## Common Issues & Solutions

### Issue 1: Login button not responding
**Solution:**
- Check browser console for JavaScript errors
- Verify Flask server is running
- Clear browser cache and cookies

### Issue 2: "Connection refused" error
**Solution:**
- Ensure Flask server is running: `python app.py`
- Check if port 5000 is available
- Verify no firewall blocking

### Issue 3: Session expires immediately
**Solution:**
- Check `config.py` - `SECRET_KEY` must be set
- Verify `PERMANENT_SESSION_LIFETIME` setting
- Check browser cookie settings

### Issue 4: Dashboard shows blank page
**Solution:**
- Check Flask console for errors
- Verify all template files exist
- Check `static/css/style.css` is loading

---

## Browser Compatibility

Tested and verified on:
- ✅ Google Chrome (Latest)
- ✅ Microsoft Edge (Latest)
- ✅ Firefox (Latest)
- ⚠️ Safari (May require testing)

---

## Security Validation

### ✅ Security Checks Passed:
1. Session-based authentication implemented
2. Login required decorator on all protected routes
3. CSRF protection via Flask session
4. File upload validation
5. Path traversal prevention in downloads
6. Error handlers prevent information leakage

---

## Performance Benchmarks

Expected response times:
- Login: < 200ms
- Dashboard load: < 300ms
- Page navigation: < 200ms
- Domain scan: 2-5 seconds
- IP scan: 1-3 seconds
- Image analysis: 3-10 seconds (depends on image size)

---

## Next Steps After Phase 5

Once all tests pass:
1. ✅ Proceed to Phase 6 (Reports & Creator Page)
2. ✅ Generate test reports
3. ✅ Verify download functionality
4. ✅ Complete Windows setup documentation

---

**Testing Completed By:** [Your Name]  
**Date:** [Current Date]  
**Status:** ✅ All tests must pass before proceeding