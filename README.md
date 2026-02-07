# I Pwned You - OSINT Threat Detection Platform

![Version](https://img.shields.io/badge/version-1.0-red)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-2.3.0-green)
![License](https://img.shields.io/badge/license-Educational-orange)

## 🎯 Project Overview

**I Pwned You** is a professional OSINT (Open Source Intelligence) Threat Detection Platform designed for cyber security education, SOC training, and real-world learning. The platform provides automated reconnaissance capabilities while emphasizing human analyst validation and professional OSINT methodologies.

---

## ✨ Core Features

### 🌐 Domain OSINT Scan
- DNS record enumeration (A, AAAA, MX, NS, TXT, CNAME)
- WHOIS information retrieval
- IP address resolution
- Domain status monitoring
- Privacy-protected data handling

### 📡 IP Intelligence Scan
- Geolocation (Country, Region, City)
- ISP and Organization identification
- ASN (Autonomous System Number) lookup
- Reverse DNS resolution
- VPN/Proxy detection warnings

### 🖼️ Image Intelligence Analysis
- **EXIF Metadata Extraction** (with real-world disclaimers)
- **OCR Text Extraction** (Tesseract - offline, informational only)
- **GPS Coordinate Extraction** (with spoofing warnings)
- **Reverse Geocoding** (OpenStreetMap)
- **Reverse Image Search Links** (Google, Yandex, Bing, TinEye)
- Professional OSINT disclaimers throughout
- Human analyst validation emphasis

### 📊 Report Generation
- Automated text-based reports
- SOC-appropriate formatting
- Timestamp and metadata inclusion
- Download functionality
- Professional limitations documentation

### 🔐 Authentication System
- Secure session management
- Hardcoded credentials for training environment
- Protected routes
- Automatic logout on timeout

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ with Flask 2.3.0 |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Styling** | Custom CSS (Dark Cyber Theme) |
| **OSINT Tools** | python-whois, dnspython, requests |
| **Image Processing** | Pillow, pytesseract, exifread |
| **Geolocation** | geopy (OpenStreetMap Nominatim) |
| **APIs** | ip-api.com (free tier), OpenStreetMap |

---

## 📁 Project Structure
```
I-Pwned-You/
│
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── test_authentication.py          # Automated testing script
├── README.md                       # Project documentation
├── SETUP_WINDOWS.md               # Windows setup guide
├── TESTING_GUIDE.md               # Testing procedures
│
├── static/
│   ├── css/
│   │   └── style.css              # Dark cyber-threat theme
│   ├── js/
│   │   └── main.js                # Frontend utilities
│   └── images/
│       └── logo.png               # Project logo
│
├── templates/
│   ├── login.html                 # Authentication page
│   ├── dashboard.html             # Main dashboard
│   ├── domain_scan.html           # Domain OSINT page
│   ├── ip_scan.html               # IP intelligence page
│   ├── image_intel.html           # Image analysis page
│   ├── reports.html               # Reports listing
│   └── creator.html               # Developer profile
│
├── modules/
│   ├── __init__.py                # Module initialization
│   ├── auth.py                    # Authentication logic
│   ├── domain_osint.py            # Domain scanning
│   ├── ip_osint.py                # IP scanning
│   └── image_intel.py             # Image intelligence
│
├── reports/                        # Generated reports (auto-created)
└── uploads/                        # Uploaded images (auto-created)
```

---

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8 or higher
- Tesseract OCR (for image text extraction)

### Installation

1. **Clone or download the project**
```bash
cd I-Pwned-You
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Tesseract OCR** (Optional but recommended)
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location: `C:\Program Files\Tesseract-OCR\`

5. **Run the application**
```bash
python app.py
```

6. **Access the platform**
- Open browser: `http://127.0.0.1:5000`
- Login with default credentials:
  - **Username:** `admin`
  - **Password:** `admin123`

---

## 📖 Usage Guide

### Domain Scan
1. Navigate to **Domain Scan** from sidebar
2. Enter target domain (e.g., `example.com`)
3. Click **START SCAN**
4. Review results including DNS, WHOIS, and IP data
5. Download report if needed

### IP Scan
1. Navigate to **IP Scan** from sidebar
2. Enter target IP address (e.g., `8.8.8.8`)
3. Click **START SCAN**
4. Review geolocation, ISP, and network information
5. Download report if needed

### Image Intelligence
1. Navigate to **Image Intelligence** from sidebar
2. Upload image (drag-and-drop or click to select)
3. Click **ANALYZE IMAGE**
4. Review EXIF, OCR, GPS, and reverse search links
5. **IMPORTANT:** Manually verify all findings
6. Download full report

### Reports
1. Navigate to **Reports** from sidebar
2. View all generated reports
3. Click **DOWNLOAD** to save report locally
4. Reports are stored in `reports/` folder

---

## ⚠️ OSINT Disclaimers & Limitations

### Critical Reminders for Analysts

**This tool provides INFORMATIONAL DATA ONLY.**  
**Human validation is REQUIRED for all findings.**

#### EXIF Metadata
- ⚠️ Can be stripped by social media or editing software
- ⚠️ Can be edited or completely fabricated
- ⚠️ Missing EXIF is NOT suspicious
- ⚠️ Camera information may be spoofed

#### OCR Text Extraction
- ⚠️ Accuracy is NOT guaranteed
- ⚠️ Results are informational only
- ⚠️ Low-quality images produce unreliable results
- ⚠️ Manual verification required

#### GPS Coordinates
- ⚠️ Can be edited or spoofed
- ⚠️ Location accuracy varies (city-level typical)
- ⚠️ Street-level accuracy NOT guaranteed
- ⚠️ Verify with independent sources

#### Reverse Image Search
- ⚠️ Manual upload required (no automation)
- ⚠️ Similar images DO NOT confirm origin
- ⚠️ Platform identification requires additional OSINT
- ⚠️ Results may show edited/cropped versions

#### IP Geolocation
- ⚠️ Accuracy varies by region
- ⚠️ VPN/Proxy may show incorrect location
- ⚠️ ISP/ASN data may be outdated
- ⚠️ Free API has rate limits

#### Domain/WHOIS Data
- ⚠️ Privacy protection may hide information
- ⚠️ WHOIS data can be limited or redacted
- ⚠️ DNS records change frequently
- ⚠️ Registration data may be proxied

---

## 🔐 Default Credentials

**⚠️ IMPORTANT: Change in production environments**

- **Username:** `admin`
- **Password:** `admin123`

These hardcoded credentials are for training/educational use only.

---

## 🧪 Testing

### Manual Testing
See `TESTING_GUIDE.md` for detailed procedures.

### Automated Testing
```bash
# Ensure server is running
python app.py

# In another terminal
python test_authentication.py
```

Expected: All 5 tests should pass.

---

## 📊 Performance

- **Login:** < 200ms
- **Dashboard Load:** < 300ms
- **Domain Scan:** 2-5 seconds
- **IP Scan:** 1-3 seconds
- **Image Analysis:** 3-10 seconds (depends on image size)

---

## 🐛 Known Limitations

1. **Tesseract OCR:** Must be installed separately (Windows)
2. **Rate Limits:** Free APIs have request limitations
3. **Geolocation:** City-level accuracy only
4. **WHOIS:** Privacy protection limits data availability
5. **Image Upload:** 16MB max file size
6. **Reverse Search:** Manual upload required (no automation)

---

## 🔮 Future Enhancements

- [ ] Advanced DNS enumeration (subdomains)
- [ ] Integration with VirusTotal API
- [ ] Shodan API integration
- [ ] Additional OCR engines (Google Vision API option)
- [ ] Certificate transparency log checks
- [ ] Email OSINT capabilities
- [ ] Social media username search
- [ ] Dark web monitoring indicators
- [ ] Export to PDF/JSON formats
- [ ] Multi-user support with roles
- [ ] API key management interface
- [ ] Scan history and analytics

---

## 🎓 Educational Purpose

This platform is designed for:
- ✅ Cyber security education
- ✅ SOC analyst training
- ✅ OSINT methodology learning
- ✅ Penetration testing practice (authorized targets only)
- ✅ Red team/Blue team exercises
- ✅ Security awareness training

**⚠️ Use responsibly and only on authorized targets.**

---

## 📚 Resources

### OSINT Learning
- [OSINT Framework](https://osintframework.com/)
- [Bellingcat Online Investigation Toolkit](https://www.bellingcat.com/)
- [IntelTechniques](https://inteltechniques.com/)

### Tools Used
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [ip-api.com](https://ip-api.com/)
- [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/)

### Python Libraries
- [Flask Documentation](https://flask.palletsprojects.com/)
- [python-whois](https://pypi.org/project/python-whois/)
- [dnspython](https://www.dnspython.org/)

---

## 👤 Developer

**[Your Name Here]**  
Cyber Security Engineer | Full-Stack Developer

- 🐙 GitHub: [github.com/yourusername](https://github.com/yourusername)
- 💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- 📧 Email: your.email@example.com

---

## 📄 License

This project is for **educational purposes only**.  
Not for commercial use without permission.

---

## 🙏 Acknowledgments

- OSINT community for methodologies and best practices
- Flask framework developers
- Tesseract OCR contributors
- Free API providers (ip-api.com, OpenStreetMap)
- Cyber security education community

---

## 📞 Support

For issues, questions, or contributions:
1. Check `TESTING_GUIDE.md` for common issues
2. Review `SETUP_WINDOWS.md` for installation problems
3. Create an issue on GitHub (if applicable)
4. Contact developer via email

---

**Version:** 1.0  
**Last Updated:** January 2025  
**Status:** Production Ready ✅

---

Made with ❤️ for the cyber security community