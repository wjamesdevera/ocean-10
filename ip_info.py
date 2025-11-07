from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_ip_address(version="ipv4"):
    """Retrieve public IPv4 or IPv6 address using ipify."""
    try:
        if version == "ipv6":
            res = requests.get("https://api6.ipify.org?format=json", timeout=5) #REST API for IPv6
        else:
            res = requests.get("https://api.ipify.org?format=json", timeout=5) #REST API for IPv4
        res.raise_for_status()
        return res.json().get("ip")
    except requests.exceptions.RequestException:
        return None
    
# This function retrieves the user's public IP address using the ipify API
def get_ip_info(ip):
    """Retrieve IP information (location, ISP, ASN, etc.) using ipapi.co with fallback."""
    if not ip:
        return None
    
    # Try ipapi.co first
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        res.raise_for_status()
        data = res.json()
        
        # Check if API returned an error (rate limit, invalid IP, etc.)
        if "error" in data:
            error_reason = data.get("reason", "Unknown error")
            print(f"ipapi.co error for {ip}: {error_reason}")
            # If rate limited, try fallback API
            if "rate" in error_reason.lower() or "limit" in error_reason.lower():
                return get_ip_info_fallback(ip)
            return None
        
        # Check if we have valid data
        if "ip" in data:
            return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP info from ipapi.co for {ip}: {e}")
    
    # Fallback to alternative API
    return get_ip_info_fallback(ip)

def get_ip_info_fallback(ip):
    """Fallback API using ip-api.com (free, no key required)."""
    try:
        # ip-api.com returns data in different format, need to map fields
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        res.raise_for_status()
        data = res.json()
        
        # Check if query was successful
        if data.get("status") == "success":
            # Map ip-api.com fields to match ipapi.co format
            mapped_data = {
                "ip": data.get("query", ip),
                "city": data.get("city"),
                "region": data.get("regionName"),
                "country": data.get("countryCode"),
                "country_name": data.get("country"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone"),
                "org": data.get("isp"),
                "asn": data.get("as", "").split()[0] if data.get("as") else None,
                "postal": data.get("zip"),
            }
            print(f"Using fallback API (ip-api.com) for {ip}")
            return mapped_data
        else:
            print(f"Fallback API error for {ip}: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP info from fallback API for {ip}: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route to show both IPv4 and IPv6 addresses, or lookup a specific IP."""
    # Get timestamp for when data was fetched
    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if user submitted an IP address to lookup
    # Only get from form if it's a POST request (to avoid conflicts with "My IP" button)
    lookup_ip = None
    if request.method == "POST":
        lookup_ip = request.form.get("ip_address", "").strip()
        if not lookup_ip:  # Empty string or whitespace only
            lookup_ip = None
    
    if lookup_ip:
        # User wants to lookup a specific IP
        lookup_ipv4 = lookup_ip if ":" not in lookup_ip else None
        lookup_ipv6 = lookup_ip if ":" in lookup_ip else None
        info_data = get_ip_info(lookup_ip)
        # For lookup mode, show the looked-up IP
        ipv4 = lookup_ipv4
        ipv6 = lookup_ipv6
    else:
        # Auto-detect user's IP addresses (My IP mode)
        ipv4 = get_ip_address("ipv4")
        ipv6 = get_ip_address("ipv6")
        
        # Try to get geolocation info - prefer IPv4, fallback to IPv6
        info_data = None
        if ipv4:
            info_data = get_ip_info(ipv4)
        if not info_data and ipv6:
            info_data = get_ip_info(ipv6)

    # Determine if lookup failed and provide error context
    lookup_failed = lookup_ip and not info_data
    auto_detect_failed = not lookup_ip and not info_data
    
    return render_template("index.html", 
                         ipv4=ipv4, 
                         ipv6=ipv6, 
                         data=info_data, 
                         fetch_time=fetch_time, 
                         lookup_ip=lookup_ip or "", 
                         lookup_failed=lookup_failed,
                         auto_detect_failed=auto_detect_failed)

if __name__ == "__main__":
    app.run(debug=True)
