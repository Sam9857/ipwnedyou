# I Pwned You - Windows Setup Guide

Complete installation and configuration guide for Windows 10/11

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites Installation](#prerequisites-installation)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Testing Installation](#testing-installation)
6. [Common Issues & Solutions](#common-issues--solutions)
7. [Configuration Options](#configuration-options)
8. [Security Considerations](#security-considerations)

---

## 💻 System Requirements

### Minimum Requirements
- **OS:** Windows 10 (64-bit) or Windows 11
- **RAM:** 4 GB minimum (8 GB recommended)
- **Storage:** 500 MB free space
- **Internet:** Required for API calls and package installation

### Software Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Edge, or Firefox)
- Text editor (VS Code recommended)

---

## 🔧 Prerequisites Installation

### Step 1: Install Python

#### Download Python
1. Go to https://www.python.org/downloads/
2. Download **Python 3.8+** (latest stable version recommended)
3. Run the installer

#### Installation Settings (IMPORTANT!)
✅ **CHECK** "Add Python to PATH"  
✅ **CHECK** "Install pip"  
✅ Click "Install Now"

#### Verify Installation
Open Command Prompt (cmd) and run:
```bash
python --version
```
Expected output: `Python 3.x.x`
```bash
pip --version
```
Expected output: `pip 23.x.x from ...`

---

### Step 2: Install Tesseract OCR (Optional but Recommended)

Tesseract is required for OCR text extraction from images.

#### Download Tesseract
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download: **tesseract-ocr-w64-setup-5.3.x.exe** (latest version)
3. Run installer

#### Installation Path (CRITICAL!)
Install to default location:
```
C:\Program Files\Tesseract-OCR\
```

⚠️ **If you install elsewhere, update `config.py`:**
```python
TESSERACT_PATH = r'C:\Your\Custom\Path\tesseract.exe'
```

#### Verify Installation
```bash
tesseract --version
```
Expected output: `tesseract 5.x.x`

If command not found, add to PATH:
1. Right-click "This PC" → Properties
2. Advanced system settings → Environment Variables
3. Edit "Path" under System variables
4. Add: `C:\Program Files\Tesseract-OCR`
5. Click OK and restart Command Prompt

---

### Step 3: Install Git (Optional)

For version control and updates.

1. Download from: https://git-scm.com/download/win
2. Run installer with default settings
3. Verify: `git --version`

---

## 📦 Project Setup

### Step 1: Download Project

#### Option A: Direct Download
1. Download ZIP file
2. Extract to desired location (e.g., `C:\Projects\I-Pwned-You`)

#### Option B: Git Clone
```bash
git clone <repository-url>
cd I-Pwned-You
```

---

### Step 2: Create Virtual Environment

Open Command Prompt in project directory:
```bash
# Navigate to project folder
cd C:\Path\To\I-Pwned-You

# Create virtual environment
python -m venv venv
```

This creates a `venv` folder containing isolated Python environment.

---

### Step 3: Activate Virtual Environment
```bash
# Activate (Command Prompt)
venv\Scripts\activate

# If using PowerShell:
venv\Scripts\Activate.ps1
```

✅ You should see `(venv)` prefix in command prompt

**PowerShell Execution Policy Error?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Step 4: Install Python Dependencies

With virtual environment activated:
```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.0
- Werkzeug 2.3.0
- requests 2.31.0
- python-whois 0.8.0
- dnspython 2.3.0
- Pillow 10.0.0
- pytesseract 0.3.10
- exifread 3.0.0
- geopy 2.3.0

**Installation Time:** 2-5 minutes depending on internet speed

#### Verify Installation
```bash
pip list
```
Check that all packages are listed.

---

## 🚀 Running the Application

### Step 1: Start Flask Server

With virtual environment activated:
```bash
python app.py
```

#### Expected Output:
```
═══════════════════════════════════════════════════════
    I PWNED YOU - OSINT THREAT DETECTION PLATFORM
═══════════════════════════════════════════════════════
✓ Server starting on http://127.0.0.1:5000
✓ Server starting on http://localhost:5000

🔐 DEFAULT CREDENTIALS:
   Username: admin
   Password: admin123

📁 DIRECTORIES:
   Uploads: C:\...\uploads
   Reports: C:\...\reports

⚙️  CONFIGURATION:
   Max Upload Size: 16MB
   Session Timeout: 30 minutes
   Debug Mode: True
═══════════════════════════════════════════════════════

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

---

### Step 2: Access Application

1. Open web browser
2. Navigate to: **http://127.0.0.1:5000**
3. Login page should appear

---

### Step 3: Login

Use default credentials:
- **Username:** `admin`
- **Password:** `admin123`

✅ You should be redirected to Dashboard

---

## 🧪 Testing Installation

### Quick Functionality Test

#### 1. Test Domain Scan
1. Click **Domain Scan** in sidebar
2. Enter: `example.com`
3. Click **START SCAN**
4. ✅ Results should appear within 5 seconds
5. ✅ Download report button should work

#### 2. Test IP Scan
1. Click **IP Scan** in sidebar
2. Enter: `8.8.8.8`
3. Click **START SCAN**
4. ✅ Geolocation results should appear
5. ✅ Download report button should work

#### 3. Test Image Intelligence
1. Click **Image Intelligence** in sidebar
2. Upload any image (JPG/PNG)
3. Click **ANALYZE IMAGE**
4. ✅ Results should appear (EXIF, OCR, etc.)
5. ✅ Download report button should work

**Note:** OCR will only work if Tesseract is installed

#### 4. Test Reports Page
1. Click **Reports** in sidebar
2. ✅ Generated reports should be listed
3. ✅ Download buttons should work

---

### Automated Testing

Run test suite:
```bash
# Ensure server is running in another terminal
python app.py

# In new terminal with venv activated
python test_authentication.py
```

Expected: **5/5 tests passed**

---

## 🐛 Common Issues & Solutions

### Issue 1: "Python is not recognized"

**Cause:** Python not in PATH

**Solution:**
1. Reinstall Python
2. ✅ CHECK "Add Python to PATH" during installation
3. Or manually add to PATH:
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\`

---

### Issue 2: "pip is not recognized"

**Cause:** pip not installed or not in PATH

**Solution:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

### Issue 3: Virtual Environment Won't Activate

**PowerShell Error:**
```
cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Issue 4: "Port 5000 already in use"

**Cause:** Another application using port 5000

**Solution 1:** Stop other application using port 5000

**Solution 2:** Change port in `app.py`:
```python
app.run(debug=DEBUG, host='0.0.0.0', port=5001)  # Use port 5001
```

Then access: http://127.0.0.1:5001

---

### Issue 5: Tesseract Not Found

**Error:** `TesseractNotFoundError`

**Solution:**
1. Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR\`
3. Or update path in `config.py`

**Temporary Workaround:**
Image analysis will still work, but OCR will be disabled.

---

### Issue 6: "ModuleNotFoundError"

**Cause:** Dependency not installed

**Solution:**
```bash
# Ensure venv is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue 7: Login Not Working

**Symptoms:**
- Button doesn't respond
- Error message appears

**Solutions:**

1. **Check browser console** (F12)
   - Look for JavaScript errors

2. **Verify Flask server is running**
   - Check terminal for errors

3. **Clear browser cache**
   - Ctrl + Shift + Delete
   - Clear cached images and files

4. **Try different browser**
   - Chrome, Edge, or Firefox

5. **Check credentials**
   - Username: `admin`
   - Password: `admin123`
   - Case-sensitive!

---

### Issue 8: Blank/White Screen

**Cause:** CSS not loading or JavaScript error

**Solution:**

1. **Check Flask console** for errors

2. **Verify file structure:**
```
static/
  css/
    style.css
  js/
    main.js
```

3. **Hard refresh browser:**
   - Ctrl + Shift + R

4. **Check file permissions**
   - Ensure files are readable

---

### Issue 9: API Rate Limits

**Error:** "Rate limit exceeded" or "Too many requests"

**Cause:** Free API limits reached (ip-api.com)

**Solution:**
- Wait 1 minute and retry
- ip-api.com limit: 45 requests/minute
- OpenStreetMap: 1 request/second

---

### Issue 10: Image Upload Fails

**Error:** "File too large" or "Invalid file type"

**Solutions:**

1. **File size limit:** 16MB maximum
   - Compress image before upload

2. **Allowed formats:** PNG, JPG, JPEG, GIF, BMP
   - Convert to supported format

3. **Check uploads folder exists:**
```bash
# Should be created automatically
# If not, create manually:
mkdir uploads
```

---

## ⚙️ Configuration Options

### Changing Port

Edit `app.py` (bottom of file):
```python
app.run(debug=DEBUG, host='0.0.0.0', port=8080)  # Change to 8080
```

---

### Changing Credentials

Edit `config.py`:
```python
ADMIN_USERNAME = 'yourusername'
ADMIN_PASSWORD = 'yourpassword123'
```

⚠️ **For production, use proper authentication system**

---

### Adjusting Upload Limits

Edit `config.py`:
```python
MAX_FILE_SIZE = 32 * 1024 * 1024  # 32MB instead of 16MB
```

---

### Session Timeout

Edit `config.py`:
```python
PERMANENT_SESSION_LIFETIME = 3600  # 60 minutes instead of 30
```

---

### Tesseract Path

Edit `config.py`:
```python
TESSERACT_PATH = r'C:\Custom\Path\tesseract.exe'
```

---

## 🔐 Security Considerations

### For Training Environment (Current Setup)

✅ Hardcoded credentials acceptable  
✅ Debug mode enabled for learning  
✅ Running on localhost only  

### For Production Environment (NOT RECOMMENDED AS-IS)

⚠️ **DO NOT deploy this setup to production**

Required changes:
- [ ] Implement proper user authentication
- [ ] Use environment variables for secrets
- [ ] Disable debug mode
- [ ] Add HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Enable logging
- [ ] Add CSRF tokens
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Set up firewall rules

---

## 📊 Performance Optimization

### Recommended Settings

**For faster performance:**

1. **Use SSD storage** for reports/uploads folders

2. **Close unnecessary applications** while running

3. **Allocate more RAM:**
   - Close browser tabs
   - Stop background processes

4. **Use latest Python version**
   - Python 3.11+ has performance improvements

---

## 🔄 Updating the Application

### Getting Updates

#### If using Git:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

#### Manual update:
1. Download new version
2. Extract files
3. Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

---

## 🗑️ Uninstallation

### Complete Removal

1. **Deactivate virtual environment:**
```bash
deactivate
```

2. **Delete project folder:**
```bash
rmdir /s /q C:\Path\To\I-Pwned-You
```

3. **Optional: Uninstall Tesseract**
   - Control Panel → Programs → Uninstall Tesseract

4. **Optional: Remove Python**
   - Only if not used for other projects

---

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Official Docs](https://docs.python.org/3/)
- [Tesseract OCR Guide](https://tesseract-ocr.github.io/)

### Troubleshooting
- Check `TESTING_GUIDE.md` for test procedures
- Review `README.md` for feature descriptions
- Check Flask console output for errors

### Getting Help
1. Review this guide thoroughly
2. Check common issues section
3. Enable debug mode for detailed errors
4. Check browser console (F12)
5. Review Flask terminal output

---

## ✅ Installation Checklist

Use this checklist to verify complete setup:

**Prerequisites:**
- [ ] Python 3.8+ installed and in PATH
- [ ] pip working correctly
- [ ] Tesseract OCR installed (optional)
- [ ] Project files extracted

**Setup:**
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No installation errors

**Testing:**
- [ ] Flask server starts without errors
- [ ] Can access http://127.0.0.1:5000
- [ ] Login page loads correctly
- [ ] Can login with admin/admin123
- [ ] Dashboard loads
- [ ] Domain scan works
- [ ] IP scan works
- [ ] Image upload works
- [ ] Reports page shows generated reports
- [ ] Download reports works
- [ ] All automated tests pass

---

## 🎓 Learning Resources

### Windows Command Line Basics
```bash
cd                  # Change directory
dir                 # List files
mkdir dirname       # Create directory
del filename        # Delete file
cls                 # Clear screen
```

### Python Virtual Environment Commands
```bash
python -m venv venv         # Create venv
venv\Scripts\activate       # Activate (CMD)
deactivate                  # Deactivate
pip list                    # List installed packages
pip freeze                  # Show installed versions
```

### Flask Development
```bash
python app.py               # Run server
Ctrl + C                    # Stop server
```

---

## 📞 Support & Feedback

For issues not covered in this guide:

1. **Review Documentation:**
   - README.md
   - TESTING_GUIDE.md
   - CHANGELOG.md

2. **Check Common Issues** section above

3. **Enable Debug Output:**
   - Check Flask console
   - Check browser console (F12)

4. **Contact Developer:**
   - See creator.html for contact information

---

**Installation Guide Version:** 1.0  
**Last Updated:** January 2025  
**Platform:** Windows 10/11  
**Status:** Production Ready ✅

---

Made with ❤️ for Windows users learning cyber security