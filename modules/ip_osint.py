"""
IP OSINT Module
Performs IP address reconnaissance using free geolocation APIs
"""

import requests
import socket
from datetime import datetime


def scan_ip(ip_address):
    """
    Perform OSINT scan on an IP address
    Uses free IP geolocation API (ip-api.com)
    
    Args:
        ip_address (str): Target IP address
    
    Returns:
        dict: IP intelligence data
    """
    
    result = {
        'ip': ip_address,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'geolocation': {},
        'reverse_dns': None,
        'status': 'Unknown',
        'errors': [],
        'limitations': []
    }
    
    try:
        # 1. Validate IP format
        try:
            socket.inet_aton(ip_address)
        except socket.error:
            result['errors'].append('Invalid IP address format')
            result['status'] = 'Invalid'
            return result
        
        # 2. Geolocation lookup using ip-api.com (free, no key required)
        try:
            api_url = f'http://ip-api.com/json/{ip_address}'
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    result['geolocation'] = {
                        'country': data.get('country', 'N/A'),
                        'country_code': data.get('countryCode', 'N/A'),
                        'region': data.get('regionName', 'N/A'),
                        'region_code': data.get('region', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'zip_code': data.get('zip', 'N/A'),
                        'latitude': data.get('lat', 'N/A'),
                        'longitude': data.get('lon', 'N/A'),
                        'timezone': data.get('timezone', 'N/A'),
                        'isp': data.get('isp', 'N/A'),
                        'organization': data.get('org', 'N/A'),
                        'asn': data.get('as', 'N/A')
                    }
                    result['status'] = 'Active'
                else:
                    result['errors'].append(f"Geolocation failed: {data.get('message', 'Unknown error')}")
                    result['status'] = 'Lookup Failed'
            else:
                result['errors'].append(f'API request failed: HTTP {response.status_code}')
                result['status'] = 'API Error'
        
        except requests.exceptions.Timeout:
            result['errors'].append('API request timed out')
            result['status'] = 'Timeout'
        except requests.exceptions.RequestException as e:
            result['errors'].append(f'API request error: {str(e)}')
            result['status'] = 'Error'
        
        # 3. Reverse DNS lookup
        try:
            hostname = socket.gethostbyaddr(ip_address)
            result['reverse_dns'] = hostname[0]
        except socket.herror:
            result['reverse_dns'] = 'No PTR record'
        except Exception as e:
            result['reverse_dns'] = f'Lookup failed: {str(e)}'
        
        # Add limitations
        result['limitations'].append('Geolocation accuracy varies (city-level typical)')
        result['limitations'].append('ISP/ASN data may be outdated')
        result['limitations'].append('VPN/Proxy usage may show incorrect location')
        result['limitations'].append('Free API has rate limits (45 requests/minute)')
        
    except Exception as e:
        result['errors'].append(f'Scan error: {str(e)}')
        result['status'] = 'Error'
    
    return result


def format_ip_report(scan_result):
    """
    Format IP scan results into a readable report
    
    Args:
        scan_result (dict): Result from scan_ip()
    
    Returns:
        str: Formatted text report
    """
    
    report = f"""
═══════════════════════════════════════════════════════
           IP OSINT SCAN REPORT
═══════════════════════════════════════════════════════

Target IP: {scan_result['ip']}
Scan Time: {scan_result['timestamp']}
Status: {scan_result['status']}

─────────────────────────────────────────────────────
GEOLOCATION INFORMATION
─────────────────────────────────────────────────────
"""
    
    if scan_result['geolocation']:
        for key, value in scan_result['geolocation'].items():
            report += f"{key.replace('_', ' ').title()}: {value}\n"
    else:
        report += "No geolocation data available\n"
    
    report += f"""
─────────────────────────────────────────────────────
REVERSE DNS
─────────────────────────────────────────────────────
Hostname: {scan_result['reverse_dns'] or 'Not available'}
"""
    
    if scan_result['limitations']:
        report += f"""
─────────────────────────────────────────────────────
LIMITATIONS
─────────────────────────────────────────────────────
"""
        for limitation in scan_result['limitations']:
            report += f"⚠ {limitation}\n"
    
    if scan_result['errors']:
        report += f"""
─────────────────────────────────────────────────────
ERRORS
─────────────────────────────────────────────────────
"""
        for error in scan_result['errors']:
            report += f"❌ {error}\n"
    
    report += """
═══════════════════════════════════════════════════════
        Generated by I Pwned You OSINT Platform
═══════════════════════════════════════════════════════
"""
    
    return report