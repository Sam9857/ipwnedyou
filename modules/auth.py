"""
Authentication Module
Handles login validation with hardcoded credentials
"""

from config import ADMIN_USERNAME, ADMIN_PASSWORD


def validate_login(username, password):
    """
    Validate login credentials against hardcoded admin account
    
    Args:
        username (str): Provided username
        password (str): Provided password
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'username': str (if successful)
        }
    """
    
    # Trim whitespace
    username = username.strip()
    password = password.strip()
    
    # Validate against hardcoded credentials
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {
            'success': True,
            'message': 'Authentication successful',
            'username': username
        }
    
    # Failed authentication
    return {
        'success': False,
        'message': 'Invalid credentials. Default is admin/admin123',
        'username': None
    }


def check_session(session):
    """
    Check if user session is valid
    
    Args:
        session: Flask session object
    
    Returns:
        bool: True if logged in, False otherwise
    """
    return session.get('logged_in', False) and session.get('username') == ADMIN_USERNAME