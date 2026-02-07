/*
═══════════════════════════════════════════════════════
  I PWNED YOU - OSINT THREAT DETECTION PLATFORM
  Main JavaScript File
  Version: 1.0 - Production Ready
═══════════════════════════════════════════════════════
*/

// Global utility functions

/**
 * Format bytes to human-readable format
 */
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Format timestamp
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

/**
 * Show alert message
 */
function showAlert(type, message, containerId) {
    const alert = document.getElementById(containerId);
    if (alert) {
        alert.className = `alert alert-${type} show`;
        alert.textContent = message;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.classList.remove('show');
        }, 5000);
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Copied to clipboard');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            console.log('Copied to clipboard (fallback)');
        } catch (err) {
            console.error('Fallback copy failed:', err);
        }
        document.body.removeChild(textArea);
    }
}

/**
 * Validate IP address format
 */
function isValidIP(ip) {
    const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipv4Regex.test(ip);
}

/**
 * Validate domain format
 */
function isValidDomain(domain) {
    const domainRegex = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$/i;
    return domainRegex.test(domain);
}

/**
 * Show loading state
 */
function showLoading(show = true) {
    const loading = document.getElementById('loading');
    if (loading) {
        if (show) {
            loading.classList.add('show');
        } else {
            loading.classList.remove('show');
        }
    }
}

/**
 * Create result item HTML
 */
function createResultItem(label, value, isLink = false) {
    const item = document.createElement('div');
    item.className = 'result-item';
    
    const labelDiv = document.createElement('div');
    labelDiv.className = 'result-label';
    labelDiv.textContent = label + ':';
    
    const valueDiv = document.createElement('div');
    valueDiv.className = 'result-value';
    
    if (isLink && value && value.startsWith('http')) {
        const link = document.createElement('a');
        link.href = value;
        link.target = '_blank';
        link.textContent = value;
        valueDiv.appendChild(link);
    } else {
        valueDiv.textContent = value || 'N/A';
    }
    
    item.appendChild(labelDiv);
    item.appendChild(valueDiv);
    
    return item;
}

/**
 * Initialize tooltips (if needed in future)
 */
function initTooltips() {
    // Placeholder for tooltip initialization
    console.log('Tooltips initialized');
}

/**
 * Handle API errors gracefully
 */
function handleAPIError(error, userMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    if (error.message) {
        return `${userMessage}: ${error.message}`;
    }
    
    return userMessage;
}

/**
 * Debounce function for search/input optimization
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('I Pwned You - OSINT Platform Loaded');
    initTooltips();
    
    // Add active class to current page in sidebar
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu a');
    
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Session timeout warning (optional enhancement)
let sessionTimeout;
function resetSessionTimeout() {
    clearTimeout(sessionTimeout);
    // 25 minutes warning (5 minutes before 30-minute timeout)
    sessionTimeout = setTimeout(() => {
        console.warn('Session expiring soon');
    }, 25 * 60 * 1000);
}

// Reset timeout on user activity
document.addEventListener('mousemove', debounce(resetSessionTimeout, 1000));
document.addEventListener('keypress', debounce(resetSessionTimeout, 1000));
resetSessionTimeout();


/* ═════════════ CYBER CURSOR LOGIC ═════════════ */

const cyberCursor = document.getElementById("cyber-cursor");

document.addEventListener("mousemove", (e) => {
    if (!cyberCursor) return;
    cyberCursor.style.left = e.clientX + "px";
    cyberCursor.style.top = e.clientY + "px";
});

/* Hover effect */
document.querySelectorAll(
    "button, .btn, .card, .sidebar-menu a, .social-link"
).forEach(el => {
    el.addEventListener("mouseenter", () => {
        cyberCursor.classList.add("cursor-hover");
    });
    el.addEventListener("mouseleave", () => {
        cyberCursor.classList.remove("cursor-hover");
    });
});
/* Cursor scan mode */
function startScanCursor() {
    cyberCursor.classList.add("cursor-scan");
}

function stopScanCursor() {
    cyberCursor.classList.remove("cursor-scan");
}
/* Threat detected cursor */
function threatDetectedCursor() {
    cyberCursor.classList.add("cursor-threat");

    setTimeout(() => {
        cyberCursor.classList.remove("cursor-threat");
    }, 3000);
}
