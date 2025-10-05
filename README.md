Your manager has received a request from the engineering department for a prototype of a new application that will provide IP addressing information to network technicians.

Search the internet for REST APIs that retrieve a user's current public IPv4 address and IPv6 address, such as ipapi.co or ipstack.com. Using the public APIs, create a Python application that displays and formats the computer’s current public IP addressing information.

Depending on the API you select, you may also obtain geolocation information, the provider (ISP), the ASN (Autonomous System Number) of the ISP, and country code.

Your manager would also like a list of other enhancements for a future revision. These are called backlog items. This backlog will be used for Project Activity 4.

**Note:** The objectives and specific tasks of your project will depend on the options provided by the IP information API you choose.

**Rubric/Deliverable:** The application that your team will work on and the reasons for your choice.


# IP Location Finder 🌍

A web application that displays your public IPv4 and IPv6 addresses along with detailed geolocation information on an interactive map.

## Features

- 🗺️ **Interactive Map**: Full-screen Leaflet.js map showing your location
- 📍 **Dual IP Support**: Displays both IPv4 and IPv6 addresses
- 🌐 **Geolocation Details**: City, region, country, timezone, and coordinates
- 🔌 **Network Info**: ISP/organization and ASN details
- 🎨 **Modern UI**: Clean, Google Maps-inspired interface with floating info cards
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Setup

1. **Install Python 3.9+**

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

Dependencies include:

- `Flask` - Web framework
- `requests` - HTTP library for API calls
- `tabulate` - Table formatting
- `colorama` - Terminal colors

3. **No API key required** - Uses free APIs from ipify.org and ipapi.co

## Run

Start the web server:

```bash
python ip_info.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

The application will:

- Fetch your public IPv4 address via [ipify.org](https://ipify.org)
- Fetch your public IPv6 address via [ipify.org](https://ipify.org) (if available)
- Query [ipapi.co](https://ipapi.co) for geolocation details (prefers IPv4; falls back to IPv6)
- Display everything on an interactive map with detailed information cards

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Map**: Leaflet.js with OpenStreetMap tiles
- **APIs**:
  - ipify.org (IP address lookup)
  - ipapi.co (geolocation data)

## Notes

- The application runs in debug mode by default
- ipapi.co free tier may have rate limits for anonymous requests
- If IPv6 is unavailable on your network, only IPv4 will be displayed
- Map requires valid latitude/longitude coordinates from the API
