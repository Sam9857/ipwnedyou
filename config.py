"""
Configuration File for I Pwned You - OSINT Platform
Windows-compatible configuration
"""

import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for Flask sessions
SECRET_KEY = 'cyber-sec-osint-platform-2025'

# Hardcoded Admin Credentials (LOCKED - DO NOT CHANGE)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
REPORTS_FOLDER = os.path.join(BASE_DIR, 'reports')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

# API Settings (Free tier / Basic functionality)
# Note: Using free services for basic OSINT functionality
IP_GEOLOCATION_API = 'http://ip-api.com/json/'  # Free, no key required
NOMINATIM_API = 'https://nominatim.openstreetmap.org/reverse'

# Tesseract OCR Path (Windows default installation)
# Users must install Tesseract separately
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Session timeout (30 minutes)
PERMANENT_SESSION_LIFETIME = 1800

# Debug mode (disable in production)
DEBUG = True