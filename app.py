"""
I Pwned You - OSINT Threat Detection Platform
Main Flask Application - COMPLETE VERSION
Windows-compatible backend with all features integrated
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import os
from datetime import datetime
from functools import wraps
from config import *
from modules import (
    validate_login, 
    scan_domain, 
    format_domain_report,
    scan_ip, 
    format_ip_report,
    analyze_image, 
    format_image_intel_report
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)


# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def login_required(f):
    """
    Decorator to require login for protected routes
    Ensures user is authenticated before accessing pages
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """
    Check if uploaded file has allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ═══════════════════════════════════════════════════════
# AUTHENTICATION ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/')
def index():
    """
    Root route - redirect based on authentication status
    """
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page and authentication handler
    Supports both GET (display form) and POST (authenticate)
    """
    # If already logged in, redirect to dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            # Validate credentials using auth module
            auth_result = validate_login(username, password)
            
            if auth_result['success']:
                # Set session variables
                session['logged_in'] = True
                session['username'] = auth_result['username']
                session.permanent = True
                
                return jsonify({
                    'success': True,
                    'message': 'Authentication successful'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': auth_result['message']
                })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Authentication error: {str(e)}'
            })
    
    # GET request - display login page
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Logout handler - clears session and redirects to login
    """
    session.clear()
    return redirect(url_for('login'))


# ═══════════════════════════════════════════════════════
# DASHBOARD ROUTES (PROTECTED)
# ═══════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Main dashboard page
    """
    return render_template('dashboard.html', username=session.get('username'))


@app.route('/domain-scan')
@login_required
def domain_scan_page():
    """
    Domain OSINT scan page
    """
    return render_template('domain_scan.html', username=session.get('username'))


@app.route('/ip-scan')
@login_required
def ip_scan_page():
    """
    IP OSINT scan page
    """
    return render_template('ip_scan.html', username=session.get('username'))


@app.route('/image-intel')
@login_required
def image_intel_page():
    """
    Image Intelligence page
    """
    return render_template('image_intel.html', username=session.get('username'))


@app.route('/reports')
@login_required
def reports_page():
    """
    Reports page - lists all generated reports
    """
    reports = []
    
    try:
        if os.path.exists(REPORTS_FOLDER):
            # Get all .txt files in reports folder
            all_files = os.listdir(REPORTS_FOLDER)
            reports = [f for f in all_files if f.endswith('.txt')]
            # Sort by modification time (most recent first)
            reports.sort(key=lambda x: os.path.getmtime(os.path.join(REPORTS_FOLDER, x)), reverse=True)
    except Exception as e:
        print(f"Error loading reports: {str(e)}")
    
    return render_template('reports.html', username=session.get('username'), reports=reports)


@app.route('/creator')
@login_required
def creator_page():
    """
    Creator profile page
    """
    return render_template('creator.html', username=session.get('username'))


# ═══════════════════════════════════════════════════════
# API ENDPOINTS - OSINT SCANNING
# ═══════════════════════════════════════════════════════

@app.route('/api/scan/domain', methods=['POST'])
@login_required
def api_scan_domain():
    """
    API endpoint for domain scanning
    Accepts JSON with 'domain' field
    Returns scan results and generates report
    """
    try:
        data = request.get_json()
        domain = data.get('domain', '').strip()
        
        if not domain:
            return jsonify({
                'success': False,
                'message': 'Domain is required'
            })
        
        # Remove protocol if present
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.replace('www.', '')
        domain = domain.split('/')[0]  # Remove path if present
        
        # Perform domain scan
        scan_result = scan_domain(domain)
        
        # Generate report file
        report_content = format_domain_report(scan_result)
        report_filename = f"domain_{domain.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Add report filename to result
        scan_result['report_file'] = report_filename
        scan_result['success'] = True
        
        return jsonify(scan_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Scan error: {str(e)}'
        })


@app.route('/api/scan/ip', methods=['POST'])
@login_required
def api_scan_ip():
    """
    API endpoint for IP scanning
    Accepts JSON with 'ip' field
    Returns scan results and generates report
    """
    try:
        data = request.get_json()
        ip_address = data.get('ip', '').strip()
        
        if not ip_address:
            return jsonify({
                'success': False,
                'message': 'IP address is required'
            })
        
        # Perform IP scan
        scan_result = scan_ip(ip_address)
        
        # Generate report file
        report_content = format_ip_report(scan_result)
        report_filename = f"ip_{ip_address.replace('.', '-')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Add report filename to result
        scan_result['report_file'] = report_filename
        scan_result['success'] = True
        
        return jsonify(scan_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Scan error: {str(e)}'
        })


@app.route('/api/scan/image', methods=['POST'])
@login_required
def api_scan_image():
    """
    API endpoint for image intelligence analysis
    Accepts multipart/form-data with 'image' file
    Returns analysis results and generates report
    """
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file uploaded'
            })
        
        file = request.files['image']
        
        # Validate file
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            })
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            })
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"img_{timestamp}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Save uploaded file
        file.save(filepath)
        
        # Perform image intelligence analysis
        analysis_result = analyze_image(filepath, TESSERACT_PATH)
        
        # Generate report
        report_content = format_image_intel_report(analysis_result)
        report_filename = f"image_intel_{timestamp}.txt"
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Add report filename to result
        analysis_result['report_file'] = report_filename
        analysis_result['success'] = True
        analysis_result['uploaded_filename'] = safe_filename
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Image analysis error: {str(e)}',
            'hint': 'Ensure Tesseract OCR is installed: https://github.com/UB-Mannheim/tesseract/wiki'
        })


# ═══════════════════════════════════════════════════════
# UTILITY ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/download-report/<filename>')
@login_required
def download_report(filename):
    """
    Download generated report
    Validates filename to prevent directory traversal attacks
    """
    try:
        # Security: Only allow alphanumeric, dash, underscore, and .txt
        if not filename.endswith('.txt'):
            return "Invalid file type", 400
        
        # Remove any path components
        filename = os.path.basename(filename)
        
        report_path = os.path.join(REPORTS_FOLDER, filename)
        
        if os.path.exists(report_path) and os.path.isfile(report_path):
            return send_file(report_path, as_attachment=True, download_name=filename)
        else:
            return "Report not found", 404
    
    except Exception as e:
        return f"Error downloading report: {str(e)}", 500


@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring
    """
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


# ═══════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    if session.get('logged_in'):
        return render_template('dashboard.html', 
                             username=session.get('username'),
                             error="Page not found"), 404
    return redirect(url_for('login'))


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error. Please try again.'
    }), 500


@app.errorhandler(413)
def request_entity_too_large(e):
    """Handle file upload size exceeded"""
    return jsonify({
        'success': False,
        'message': f'File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB'
    }), 413


# ═══════════════════════════════════════════════════════
# APPLICATION STARTUP
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    print("═══════════════════════════════════════════════════════")
    print("    I PWNED YOU - OSINT THREAT DETECTION PLATFORM")
    print("═══════════════════════════════════════════════════════")
    print(f"✓ Server starting on http://127.0.0.1:5000")
    print(f"✓ Server starting on http://localhost:5000")
    print(f"")
    print(f"🔐 DEFAULT CREDENTIALS:")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print(f"")
    print(f"📁 DIRECTORIES:")
    print(f"   Uploads: {UPLOAD_FOLDER}")
    print(f"   Reports: {REPORTS_FOLDER}")
    print(f"")
    print(f"⚙️  CONFIGURATION:")
    print(f"   Max Upload Size: {MAX_FILE_SIZE // (1024*1024)}MB")
    print(f"   Session Timeout: {PERMANENT_SESSION_LIFETIME // 60} minutes")
    print(f"   Debug Mode: {DEBUG}")
    print("═══════════════════════════════════════════════════════")
    print("")
    
    # Run Flask application
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)