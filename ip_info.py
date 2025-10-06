from flask import Flask, render_template
import requests

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
    """Retrieve IP information (location, ISP, ASN, etc.) using ipapi.co."""
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5) #REST API for IP information using ipapi.co
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException:
        return None

@app.route("/")
def index():
    """Main route to show both IPv4 and IPv6 addresses in one table."""
    ipv4 = get_ip_address("ipv4")
    ipv6 = get_ip_address("ipv6")

    # Uses IPv4 info for geolocation, fallback to IPv6
    info_data = get_ip_info(ipv4) if ipv4 else get_ip_info(ipv6)

    return render_template("index.html", ipv4=ipv4, ipv6=ipv6, data=info_data)

if __name__ == "__main__":
    app.run(debug=True)
