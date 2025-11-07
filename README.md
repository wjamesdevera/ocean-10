Your manager has received a request from the engineering department for a prototype of a new application that will provide IP addressing information to network technicians.

Search the internet for REST APIs that retrieve a user's current public IPv4 address and IPv6 address, such as ipapi.co or ipstack.com. Using the public APIs, create a Python application that displays and formats the computer’s current public IP addressing information.

Depending on the API you select, you may also obtain geolocation information, the provider (ISP), the ASN (Autonomous System Number) of the ISP, and country code.

Your manager would also like a list of other enhancements for a future revision. These are called backlog items. This backlog will be used for Project Activity 4.

**Note:** The objectives and specific tasks of your project will depend on the options provided by the IP information API you choose.

**Rubric/Deliverable:** The application that your team will work on and the reasons for your choice.


# IP Location Finder 🌍

A desktop GUI and web application that displays your public IPv4 and IPv6 addresses along with detailed geolocation information.

## Features

- 🖥️ **Desktop GUI**: Native Tkinter application (no browser required)
- 🌐 **Web Version**: Browser-based interface with interactive map
- 📍 **Dual IP Support**: Displays both IPv4 and IPv6 addresses
- 🔍 **IP Lookup**: Search for any IP address location and information
- 🌍 **Geolocation Details**: City, region, country, timezone, and coordinates
- 🔌 **Network Info**: ISP/organization and ASN details
- ⏰ **Timestamp Display**: Shows when IP data was last fetched
- 🗺️ **Map Integration**: View location on OpenStreetMap (web version has interactive map)
- 🔄 **Fallback API**: Automatically switches to backup API if primary fails
- 🎨 **Modern UI**: Clean, user-friendly interface

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

### GUI Version (Recommended)

Run the desktop GUI application:

```bash
python ip_info_gui.py
```

This opens a native desktop window with:
- IP address input field
- "My IP" button to auto-detect your IP
- "Lookup" button to search any IP address
- Detailed information display
- "View on Map" button to open location in browser
- Timestamp showing when data was fetched

### Web Version

Alternatively, start the web server:

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

- **GUI Version**: Tkinter (Python built-in)
- **Web Version**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (web version only)
- **Map**: Leaflet.js with OpenStreetMap tiles (web version) / OpenStreetMap links (GUI version)
- **APIs**:
  - ipify.org (IP address lookup)
  - ipapi.co (geolocation data - primary)
  - ip-api.com (geolocation data - fallback)

## Notes

- The application runs in debug mode by default
- ipapi.co free tier may have rate limits for anonymous requests
- If IPv6 is unavailable on your network, only IPv4 will be displayed
- Map requires valid latitude/longitude coordinates from the API
