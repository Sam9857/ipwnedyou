"""
Image Intelligence Module - REAL-WORLD OSINT CONSTRAINTS
Follows professional OSINT standards with human analyst validation
Version: 1.0 - Production Ready

IMPORTANT DISCLAIMERS:
- EXIF metadata may be missing, stripped, or falsified
- OCR accuracy is not guaranteed and is informational only
- Reverse image search requires manual verification
- Geolocation is approximate and may be inaccurate
- Human analyst validation is the final authority

Tools Used:
- ExifRead: EXIF metadata extraction
- Tesseract OCR: Offline text extraction (English only)
- OpenStreetMap Nominatim: Reverse geocoding (free tier)
- Manual reverse search links: Google, Yandex, Bing, TinEye
"""

import os
import exifread
from PIL import Image
import pytesseract
from datetime import datetime
import hashlib
from geopy.geocoders import Nominatim
import time


# ═══════════════════════════════════════════════════════
# EXIF METADATA EXTRACTION
# ═══════════════════════════════════════════════════════

def extract_exif_metadata(image_path):
    """
    Extract EXIF metadata from image using ExifRead
    
    OSINT CONSTRAINTS:
    - EXIF may be missing due to social media processing
    - EXIF can be edited or completely fabricated
    - Missing EXIF is NOT suspicious or unusual
    - Camera/device info may be spoofed
    
    Args:
        image_path (str): Path to uploaded image file
    
    Returns:
        dict: EXIF data with professional disclaimers
    """
    
    exif_data = {
        'available': False,
        'gps_coordinates': None,
        'camera_info': {},
        'timestamp': None,
        'software': None,
        'raw_tags': {},
        'disclaimer': None
    }
    
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        
        if not tags:
            exif_data['disclaimer'] = (
                "⚠ NO EXIF METADATA FOUND - This is common and expected. "
                "Reasons: Social media stripping, screenshot, edited image, or camera settings. "
                "Missing EXIF is NOT suspicious."
            )
            return exif_data
        
        exif_data['available'] = True
        
        # Extract GPS coordinates (if available)
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
        
        if all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
            # Convert GPS to decimal degrees
            lat = _convert_gps_to_decimal(gps_latitude.values, str(gps_latitude_ref))
            lon = _convert_gps_to_decimal(gps_longitude.values, str(gps_longitude_ref))
            
            exif_data['gps_coordinates'] = {
                'latitude': lat,
                'longitude': lon,
                'disclaimer': "⚠ GPS coordinates can be edited or spoofed. Verify independently."
            }
        
        # Extract camera/device information
        exif_data['camera_info'] = {
            'make': str(tags.get('Image Make', 'N/A')),
            'model': str(tags.get('Image Model', 'N/A')),
            'lens': str(tags.get('EXIF LensModel', 'N/A')),
            'disclaimer': "⚠ Camera information can be modified or faked."
        }
        
        # Extract timestamp
        datetime_original = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
        if datetime_original:
            exif_data['timestamp'] = str(datetime_original)
            exif_data['timestamp_disclaimer'] = "⚠ Timestamps can be altered. Verify with other sources."
        
        # Extract software/editing info
        software = tags.get('Image Software')
        if software:
            exif_data['software'] = str(software)
        
        # Store select raw tags for advanced users
        important_tags = [
            'Image Make', 'Image Model', 'EXIF DateTimeOriginal',
            'GPS GPSLatitude', 'GPS GPSLongitude', 'Image Software',
            'EXIF LensModel', 'Image Orientation'
        ]
        
        for tag in important_tags:
            if tag in tags:
                exif_data['raw_tags'][tag] = str(tags[tag])
        
        exif_data['disclaimer'] = (
            "⚠ EXIF DATA FOUND - Remember: EXIF can be edited, deleted, or fabricated. "
            "Use as informational guidance only. Verify all findings independently."
        )
        
    except Exception as e:
        exif_data['disclaimer'] = f"⚠ EXIF extraction error: {str(e)}. File may be corrupted or unsupported format."
    
    return exif_data


def _convert_gps_to_decimal(coords, ref):
    """
    Convert GPS coordinates from degrees/minutes/seconds to decimal
    
    Args:
        coords: GPS coordinate values
        ref: Reference (N/S/E/W)
    
    Returns:
        float: Decimal coordinate
    """
    try:
        degrees = float(coords[0].num) / float(coords[0].den)
        minutes = float(coords[1].num) / float(coords[1].den) / 60.0
        seconds = float(coords[2].num) / float(coords[2].den) / 3600.0
        
        decimal = degrees + minutes + seconds
        
        if ref in ['S', 'W']:
            decimal = -decimal
        
        return round(decimal, 6)
    except:
        return 0.0


# ═══════════════════════════════════════════════════════
# OCR TEXT EXTRACTION
# ═══════════════════════════════════════════════════════

def extract_text_ocr(image_path, tesseract_path=None):
    """
    Extract text from image using Tesseract OCR (offline)
    
    OSINT CONSTRAINTS:
    - Accuracy is NOT guaranteed
    - Results are informational only
    - English language only by default
    - Low-quality images may produce poor results
    - Manual verification required
    
    Args:
        image_path (str): Path to image file
        tesseract_path (str): Path to Tesseract executable (Windows)
    
    Returns:
        dict: OCR results with disclaimers
    """
    
    ocr_result = {
        'text_found': False,
        'extracted_text': None,
        'confidence': 'Unknown',
        'disclaimer': None,
        'method': 'Tesseract OCR (Offline)'
    }
    
    try:
        # Set Tesseract path if provided (Windows compatibility)
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Open and process image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Perform OCR
        extracted_text = pytesseract.image_to_string(img, lang='eng')
        
        # Clean and process text
        extracted_text = extracted_text.strip()
        
        if extracted_text:
            ocr_result['text_found'] = True
            ocr_result['extracted_text'] = extracted_text
            ocr_result['disclaimer'] = (
                "⚠ OCR ACCURACY NOT GUARANTEED - Text extraction is informational only. "
                "Results may contain errors, misreads, or artifacts. "
                "Verify all extracted text manually. "
                "Low-quality images produce unreliable results."
            )
        else:
            ocr_result['disclaimer'] = (
                "⚠ NO TEXT DETECTED - Image may not contain readable text, "
                "or text quality is too poor for OCR. This is common and not suspicious."
            )
        
    except Exception as e:
        ocr_result['disclaimer'] = (
            f"⚠ OCR FAILED: {str(e)}. "
            "Possible reasons: Tesseract not installed, unsupported image format, or corrupted file. "
            "Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki"
        )
    
    return ocr_result


# ═══════════════════════════════════════════════════════
# REVERSE GEOCODING (GPS TO LOCATION)
# ═══════════════════════════════════════════════════════

def reverse_geocode_location(latitude, longitude):
    """
    Convert GPS coordinates to approximate location using OpenStreetMap
    
    OSINT CONSTRAINTS:
    - Location is approximate only
    - Accuracy varies by region (city-level typical)
    - Free tier has rate limits
    - GPS coordinates may be spoofed
    
    Args:
        latitude (float): GPS latitude
        longitude (float): GPS longitude
    
    Returns:
        dict: Location information with disclaimers
    """
    
    location_data = {
        'city': None,
        'state': None,
        'country': None,
        'full_address': None,
        'map_link': None,
        'disclaimer': None
    }
    
    try:
        # Initialize Nominatim geocoder (free, no API key)
        geolocator = Nominatim(user_agent="ipwnedyou_osint_v1")
        
        # Add delay to respect rate limits
        time.sleep(1)
        
        # Reverse geocode
        location = geolocator.reverse(f"{latitude}, {longitude}", language='en', timeout=10)
        
        if location and location.raw:
            address = location.raw.get('address', {})
            
            location_data['city'] = address.get('city') or address.get('town') or address.get('village') or 'N/A'
            location_data['state'] = address.get('state') or address.get('region') or 'N/A'
            location_data['country'] = address.get('country') or 'N/A'
            location_data['full_address'] = location.address if location.address else 'Not Available'
            
            # Generate map links
            location_data['map_link'] = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"
            location_data['google_maps_link'] = f"https://www.google.com/maps?q={latitude},{longitude}"
            
            location_data['disclaimer'] = (
                "⚠ APPROXIMATE LOCATION - Geolocation accuracy varies. "
                "GPS coordinates may be edited or spoofed. "
                "Street-level accuracy is NOT guaranteed. "
                "Verify location through multiple sources."
            )
        else:
            location_data['disclaimer'] = "⚠ GEOCODING FAILED - Coordinates may be in remote area or invalid."
        
    except Exception as e:
        location_data['disclaimer'] = (
            f"⚠ GEOCODING ERROR: {str(e)}. "
            "Possible rate limit or network issue. Wait 60 seconds and retry."
        )
    
    return location_data


# ═══════════════════════════════════════════════════════
# REVERSE IMAGE SEARCH LINKS (MANUAL VERIFICATION ONLY)
# ═══════════════════════════════════════════════════════

def generate_reverse_search_links(image_path):
    """
    Generate manual reverse image search links
    
    OSINT CONSTRAINTS:
    - NO AUTOMATED UPLOADS - Links only
    - Manual verification REQUIRED by analyst
    - Similar images DO NOT confirm origin
    - Platform identification is IMPOSSIBLE from metadata alone
    - Results may show edited/cropped versions
    
    Args:
        image_path (str): Path to local image file
    
    Returns:
        dict: Search engine links with instructions
    """
    
    # Calculate file hash for reference
    file_hash = _calculate_file_hash(image_path)
    
    search_links = {
        'instructions': (
            "⚠ MANUAL VERIFICATION REQUIRED\n"
            "Upload the image to each search engine manually.\n"
            "Similar images DO NOT confirm original source.\n"
            "Edited/cropped versions may appear.\n"
            "Cross-reference results from multiple engines."
        ),
        'search_engines': {
            'Google Lens': 'https://lens.google.com/',
            'Google Images': 'https://images.google.com/',
            'Yandex Images': 'https://yandex.com/images/',
            'Bing Visual Search': 'https://www.bing.com/visualsearch',
            'TinEye': 'https://tineye.com/'
        },
        'file_hash_sha256': file_hash,
        'disclaimer': (
            "⚠ REVERSE SEARCH LIMITATIONS:\n"
            "• This tool does NOT upload images automatically\n"
            "• Analyst must manually upload to each search engine\n"
            "• Similar ≠ Original source\n"
            "• Platform identification requires additional OSINT\n"
            "• Results may include unrelated but visually similar images"
        )
    }
    
    return search_links


def _calculate_file_hash(file_path):
    """Calculate SHA256 hash of file for reference"""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return "Hash calculation failed"


# ═══════════════════════════════════════════════════════
# MAIN IMAGE ANALYSIS FUNCTION
# ═══════════════════════════════════════════════════════

def analyze_image(image_path, tesseract_path=None):
    """
    Complete image intelligence analysis following OSINT best practices
    
    This function integrates all image analysis components with
    professional disclaimers and human-in-the-loop validation emphasis.
    
    Args:
        image_path (str): Path to uploaded image
        tesseract_path (str): Path to Tesseract executable (optional)
    
    Returns:
        dict: Complete analysis results with all disclaimers
    """
    
    analysis_result = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'filename': os.path.basename(image_path),
        'file_size': os.path.getsize(image_path),
        'image_dimensions': None,
        'exif_data': {},
        'ocr_results': {},
        'location_data': {},
        'reverse_search': {},
        'status': 'Analysis Complete',
        'overall_disclaimer': None,
        'analyst_notes': []
    }
    
    try:
        # Get image dimensions
        with Image.open(image_path) as img:
            analysis_result['image_dimensions'] = f"{img.width} x {img.height} pixels"
        
        # 1. EXIF Metadata Extraction
        analysis_result['exif_data'] = extract_exif_metadata(image_path)
        
        # 2. OCR Text Extraction
        analysis_result['ocr_results'] = extract_text_ocr(image_path, tesseract_path)
        
        # 3. Reverse Geocoding (if GPS available)
        if analysis_result['exif_data'].get('gps_coordinates'):
            coords = analysis_result['exif_data']['gps_coordinates']
            analysis_result['location_data'] = reverse_geocode_location(
                coords['latitude'],
                coords['longitude']
            )
        else:
            analysis_result['location_data'] = {
                'disclaimer': '⚠ NO GPS DATA - Location cannot be determined from image metadata alone.'
            }
        
        # 4. Generate Reverse Search Links
        analysis_result['reverse_search'] = generate_reverse_search_links(image_path)
        
        # 5. Overall Professional Disclaimer
        analysis_result['overall_disclaimer'] = (
            "═══════════════════════════════════════════════════════\n"
            "                 OSINT ANALYST GUIDANCE                \n"
            "═══════════════════════════════════════════════════════\n\n"
            "⚠ HUMAN VALIDATION REQUIRED ⚠\n\n"
            "This automated analysis provides INFORMATIONAL DATA ONLY.\n"
            "The human analyst is the FINAL AUTHORITY on all findings.\n\n"
            "CRITICAL REMINDERS:\n"
            "• EXIF can be stripped, edited, or fabricated\n"
            "• OCR accuracy is not guaranteed\n"
            "• GPS coordinates may be spoofed\n"
            "• Reverse search requires manual verification\n"
            "• Similar images ≠ confirmed source\n"
            "• Cross-reference ALL findings with independent sources\n\n"
            "DO NOT make conclusions based solely on this analysis.\n"
            "Always corroborate findings through multiple OSINT methods.\n"
            "═══════════════════════════════════════════════════════"
        )
        
        # 6. Generate analyst action items
        analysis_result['analyst_notes'] = [
            "✓ Review EXIF data for inconsistencies",
            "✓ Manually verify OCR-extracted text",
            "✓ Upload image to reverse search engines manually",
            "✓ Cross-reference location data with other intelligence",
            "✓ Check for signs of editing or manipulation",
            "✓ Document findings in formal intelligence report"
        ]
        
    except Exception as e:
        analysis_result['status'] = f'Analysis Error: {str(e)}'
        analysis_result['overall_disclaimer'] = f"⚠ CRITICAL ERROR: {str(e)}"
    
    return analysis_result


# ═══════════════════════════════════════════════════════
# REPORT FORMATTING
# ═══════════════════════════════════════════════════════

def format_image_intel_report(analysis_result):
    """
    Format image intelligence results into professional OSINT report
    
    Args:
        analysis_result (dict): Result from analyze_image()
    
    Returns:
        str: Formatted text report following SOC standards
    """
    
    report = f"""
═══════════════════════════════════════════════════════
      IMAGE INTELLIGENCE ANALYSIS REPORT
═══════════════════════════════════════════════════════

Analysis Timestamp: {analysis_result['timestamp']}
Filename: {analysis_result['filename']}
File Size: {analysis_result['file_size']} bytes
Image Dimensions: {analysis_result['image_dimensions']}
Status: {analysis_result['status']}

─────────────────────────────────────────────────────
EXIF METADATA ANALYSIS
─────────────────────────────────────────────────────
"""
    
    exif = analysis_result['exif_data']
    report += f"EXIF Available: {'Yes' if exif.get('available') else 'No'}\n"
    
    if exif.get('available'):
        # GPS Data
        if exif.get('gps_coordinates'):
            gps = exif['gps_coordinates']
            report += f"\n📍 GPS COORDINATES FOUND:\n"
            report += f"  Latitude: {gps['latitude']}\n"
            report += f"  Longitude: {gps['longitude']}\n"
            report += f"  {gps['disclaimer']}\n"
        
        # Camera Info
        if exif.get('camera_info'):
            cam = exif['camera_info']
            report += f"\n📷 CAMERA INFORMATION:\n"
            report += f"  Make: {cam.get('make', 'N/A')}\n"
            report += f"  Model: {cam.get('model', 'N/A')}\n"
            report += f"  Lens: {cam.get('lens', 'N/A')}\n"
            report += f"  {cam.get('disclaimer', '')}\n"
        
        # Timestamp
        if exif.get('timestamp'):
            report += f"\n🕐 TIMESTAMP:\n"
            report += f"  Original: {exif['timestamp']}\n"
            if exif.get('timestamp_disclaimer'):
                report += f"  {exif['timestamp_disclaimer']}\n"
        
        # Software
        if exif.get('software'):
            report += f"\n💾 SOFTWARE:\n"
            report += f"  {exif['software']}\n"
    
    report += f"\n{exif.get('disclaimer', '')}\n"
    
    # OCR Results
    report += f"""
─────────────────────────────────────────────────────
OCR TEXT EXTRACTION
─────────────────────────────────────────────────────
"""
    
    ocr = analysis_result['ocr_results']
    report += f"Method: {ocr.get('method', 'Unknown')}\n"
    report += f"Text Found: {'Yes' if ocr.get('text_found') else 'No'}\n"
    
    if ocr.get('text_found'):
        report += f"\n📝 EXTRACTED TEXT:\n"
        report += f"{'-' * 50}\n"
        report += f"{ocr['extracted_text']}\n"
        report += f"{'-' * 50}\n"
    
    report += f"\n{ocr.get('disclaimer', '')}\n"
    
    # Location Data
    report += f"""
─────────────────────────────────────────────────────
GEOLOCATION ANALYSIS
─────────────────────────────────────────────────────
"""
    
    loc = analysis_result['location_data']
    if loc.get('city'):
        report += f"City: {loc.get('city', 'N/A')}\n"
        report += f"State/Region: {loc.get('state', 'N/A')}\n"
        report += f"Country: {loc.get('country', 'N/A')}\n"
        report += f"Full Address: {loc.get('full_address', 'N/A')}\n"
        report += f"\n🗺️ MAP LINKS:\n"
        report += f"  OpenStreetMap: {loc.get('map_link', 'N/A')}\n"
        report += f"  Google Maps: {loc.get('google_maps_link', 'N/A')}\n"
    
    report += f"\n{loc.get('disclaimer', '')}\n"
    
    # Reverse Search
    report += f"""
─────────────────────────────────────────────────────
REVERSE IMAGE SEARCH (MANUAL VERIFICATION)
─────────────────────────────────────────────────────
"""
    
    rev_search = analysis_result['reverse_search']
    report += f"{rev_search.get('instructions', '')}\n\n"
    report += f"🔍 SEARCH ENGINES:\n"
    
    for engine, link in rev_search.get('search_engines', {}).items():
        report += f"  • {engine}: {link}\n"
    
    report += f"\nFile Hash (SHA-256): {rev_search.get('file_hash_sha256', 'N/A')}\n"
    report += f"\n{rev_search.get('disclaimer', '')}\n"
    
    # Analyst Notes
    report += f"""
─────────────────────────────────────────────────────
ANALYST ACTION ITEMS
─────────────────────────────────────────────────────
"""
    
    for note in analysis_result.get('analyst_notes', []):
        report += f"{note}\n"
    
    # Overall Disclaimer
    report += f"\n{analysis_result.get('overall_disclaimer', '')}\n"
    
    report += """
═══════════════════════════════════════════════════════
     Generated by I Pwned You OSINT Platform
          Professional Image Intelligence Tool
═══════════════════════════════════════════════════════
"""
    
    return report