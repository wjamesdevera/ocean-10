import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from datetime import datetime
import webbrowser
import threading

def get_ip_address(version="ipv4"):
    """Retrieve public IPv4 or IPv6 address using ipify."""
    try:
        if version == "ipv6":
            res = requests.get("https://api6.ipify.org?format=json", timeout=5)
        else:
            res = requests.get("https://api.ipify.org?format=json", timeout=5)
        res.raise_for_status()
        return res.json().get("ip")
    except requests.exceptions.RequestException:
        return None

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

class IPLocationFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Location Finder")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Professional color scheme
        self.colors = {
            'bg_primary': '#F5F7FA',
            'bg_secondary': '#FFFFFF',
            'accent_blue': '#2563EB',
            'accent_blue_hover': '#1D4ED8',
            'accent_green': '#10B981',
            'accent_red': '#EF4444',
            'text_primary': '#1F2937',
            'text_secondary': '#6B7280',
            'border': '#E5E7EB',
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EF4444'
        }
        
        # Set background color
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'])
        
        style.configure('Body.TLabel',
                       font=('Segoe UI', 10),
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'])
        
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10),
                       background=self.colors['accent_blue'],
                       foreground='white')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['accent_blue_hover']),
                            ('pressed', self.colors['accent_blue_hover'])])
        
        style.configure('Secondary.TButton',
                        font=('Segoe UI', 10),
                        padding=(15, 8))
        
        style.configure('Card.TLabelframe',
                       background=self.colors['bg_secondary'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'])
        
        style.configure('Card.TLabelframe.Label',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'])
        
        # Main container with padding
        main_frame = tk.Frame(root, bg=self.colors['bg_primary'], padx=25, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section with title and subtitle
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        title_label = ttk.Label(header_frame, text="🌍 IP Location Finder", 
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Discover IP address information and geolocation data",
                                  font=('Segoe UI', 10),
                                  background=self.colors['bg_primary'],
                                  foreground=self.colors['text_secondary'])
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Search card
        search_card = ttk.LabelFrame(main_frame, text="  IP Lookup  ", 
                                     style='Card.TLabelframe', padding=20)
        search_card.pack(fill=tk.X, pady=(0, 15))
        search_card.columnconfigure(1, weight=1)
        
        # IP Address label and entry
        ip_label = ttk.Label(search_card, text="IP Address:", style='Body.TLabel')
        ip_label.grid(row=0, column=0, padx=(0, 12), pady=5, sticky=tk.W)
        
        self.ip_entry = ttk.Entry(search_card, width=45, font=('Segoe UI', 12))
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 12), pady=5)
        self.ip_entry.bind('<Return>', lambda e: self.lookup_ip())
        
        # Buttons with better styling
        button_frame = tk.Frame(search_card, bg=self.colors['bg_secondary'])
        button_frame.grid(row=0, column=2, sticky=tk.W)
        
        self.lookup_btn = ttk.Button(button_frame, text="🔍 Lookup", 
                                    command=self.lookup_ip, style='Primary.TButton')
        self.lookup_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.my_ip_btn = ttk.Button(button_frame, text="📍 My IP", 
                                   command=self.get_my_ip, style='Secondary.TButton')
        self.my_ip_btn.pack(side=tk.LEFT)
        
        # Status indicator with icon
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_icon = ttk.Label(status_frame, text="●", 
                                     font=('Segoe UI', 12),
                                     background=self.colors['bg_primary'],
                                     foreground=self.colors['success'])
        self.status_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.status_label = ttk.Label(status_frame, text="Ready", 
                                     font=('Segoe UI', 10),
                                     background=self.colors['bg_primary'],
                                     foreground=self.colors['text_secondary'])
        self.status_label.pack(side=tk.LEFT)
        
        # Results card
        results_card = ttk.LabelFrame(main_frame, text="  IP Information  ", 
                                     style='Card.TLabelframe', padding=15)
        results_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        results_card.columnconfigure(0, weight=1)
        results_card.rowconfigure(0, weight=1)
        
        # Text widget with better styling
        self.results_text = scrolledtext.ScrolledText(
            results_card, 
            width=80, 
            height=28,
            wrap=tk.WORD, 
            font=('Consolas', 10),
            bg='#FAFBFC',
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=15,
            selectbackground=self.colors['accent_blue'],
            selectforeground='white'
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_text.config(state=tk.DISABLED)
        
        # Bottom section with map button and timestamp
        bottom_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        bottom_frame.pack(fill=tk.X)
        
        self.map_btn = ttk.Button(bottom_frame, text="🗺️  View on Map", 
                                 command=self.open_map, 
                                 state=tk.DISABLED,
                                 style='Secondary.TButton')
        self.map_btn.pack(side=tk.LEFT)
        
        self.timestamp_label = ttk.Label(bottom_frame, text="", 
                                         font=('Segoe UI', 9),
                                         background=self.colors['bg_primary'],
                                         foreground=self.colors['text_secondary'])
        self.timestamp_label.pack(side=tk.RIGHT)
        
        # Store current data
        self.current_data = None
        self.current_lat = None
        self.current_lon = None
        
    def update_status(self, message, color="success"):
        """Update status label with icon."""
        color_map = {
            'success': self.colors['success'],
            'error': self.colors['error'],
            'warning': self.colors['warning'],
            'blue': self.colors['accent_blue'],
            'black': self.colors['text_primary']
        }
        status_color = color_map.get(color, self.colors['text_secondary'])
        self.status_icon.config(foreground=status_color)
        self.status_label.config(text=message, foreground=status_color)
        self.root.update_idletasks()
    
    def update_timestamp(self):
        """Update timestamp label."""
        fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Last fetched: {fetch_time}")
    
    def display_results(self, ipv4, ipv6, data, lookup_ip=None):
        """Display IP information in the text widget with enhanced formatting."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if data:
            # IP Addresses section
            self.results_text.insert(tk.END, "╔" + "═" * 68 + "╗\n", 'header')
            self.results_text.insert(tk.END, "║" + " " * 25 + "IP ADDRESSES" + " " * 32 + "║\n", 'header')
            self.results_text.insert(tk.END, "╚" + "═" * 68 + "╝\n", 'header')
            self.results_text.insert(tk.END, "\n")
            if ipv4:
                self.results_text.insert(tk.END, f"  IPv4:  ", 'label')
                self.results_text.insert(tk.END, f"{ipv4}\n", 'value')
            if ipv6:
                self.results_text.insert(tk.END, f"  IPv6:  ", 'label')
                self.results_text.insert(tk.END, f"{ipv6}\n", 'value')
            self.results_text.insert(tk.END, "\n\n")
            
            # Location Details section
            self.results_text.insert(tk.END, "╔" + "═" * 68 + "╗\n", 'header')
            self.results_text.insert(tk.END, "║" + " " * 23 + "LOCATION DETAILS" + " " * 30 + "║\n", 'header')
            self.results_text.insert(tk.END, "╚" + "═" * 68 + "╝\n", 'header')
            self.results_text.insert(tk.END, "\n")
            self.results_text.insert(tk.END, f"  City:         ", 'label')
            self.results_text.insert(tk.END, f"{data.get('city', 'N/A')}\n", 'value')
            self.results_text.insert(tk.END, f"  Region:       ", 'label')
            self.results_text.insert(tk.END, f"{data.get('region', 'N/A')}\n", 'value')
            self.results_text.insert(tk.END, f"  Country:      ", 'label')
            self.results_text.insert(tk.END, f"{data.get('country_name', 'N/A')} ({data.get('country', 'N/A')})\n", 'value')
            self.results_text.insert(tk.END, f"  Postal Code:  ", 'label')
            self.results_text.insert(tk.END, f"{data.get('postal', 'N/A')}\n", 'value')
            self.results_text.insert(tk.END, f"  Timezone:     ", 'label')
            self.results_text.insert(tk.END, f"{data.get('timezone', 'N/A')}\n", 'value')
            self.results_text.insert(tk.END, "\n\n")
            
            # Coordinates section
            self.results_text.insert(tk.END, "╔" + "═" * 68 + "╗\n", 'header')
            self.results_text.insert(tk.END, "║" + " " * 26 + "COORDINATES" + " " * 31 + "║\n", 'header')
            self.results_text.insert(tk.END, "╚" + "═" * 68 + "╝\n", 'header')
            self.results_text.insert(tk.END, "\n")
            lat = data.get('latitude')
            lon = data.get('longitude')
            self.results_text.insert(tk.END, f"  Latitude:     ", 'label')
            self.results_text.insert(tk.END, f"{lat if lat else 'N/A'}\n", 'value')
            self.results_text.insert(tk.END, f"  Longitude:    ", 'label')
            self.results_text.insert(tk.END, f"{lon if lon else 'N/A'}\n", 'value')
            self.results_text.insert(tk.END, "\n\n")
            
            # Network Information section
            self.results_text.insert(tk.END, "╔" + "═" * 68 + "╗\n", 'header')
            self.results_text.insert(tk.END, "║" + " " * 19 + "NETWORK INFORMATION" + " " * 30 + "║\n", 'header')
            self.results_text.insert(tk.END, "╚" + "═" * 68 + "╝\n", 'header')
            self.results_text.insert(tk.END, "\n")
            self.results_text.insert(tk.END, f"  ISP/Organization:  ", 'label')
            self.results_text.insert(tk.END, f"{data.get('org', 'N/A')}\n", 'value')
            self.results_text.insert(tk.END, f"  ASN:              ", 'label')
            self.results_text.insert(tk.END, f"{data.get('asn', 'N/A')}\n", 'value')
            
            # Configure text tags for styling
            self.results_text.tag_config('header', foreground=self.colors['accent_blue'], font=('Consolas', 10, 'bold'))
            self.results_text.tag_config('label', foreground=self.colors['text_secondary'], font=('Consolas', 10))
            self.results_text.tag_config('value', foreground=self.colors['text_primary'], font=('Consolas', 10, 'bold'))
            
            # Store coordinates for map
            self.current_lat = lat
            self.current_lon = lon
            if lat and lon:
                self.map_btn.config(state=tk.NORMAL)
            else:
                self.map_btn.config(state=tk.DISABLED)
        else:
            # Error display
            self.results_text.insert(tk.END, "╔" + "═" * 68 + "╗\n", 'error_header')
            self.results_text.insert(tk.END, "║" + " " * 28 + "ERROR" + " " * 36 + "║\n", 'error_header')
            self.results_text.insert(tk.END, "╚" + "═" * 68 + "╝\n", 'error_header')
            self.results_text.insert(tk.END, "\n")
            if lookup_ip:
                self.results_text.insert(tk.END, f"  Could not find information for IP: ", 'error_label')
                self.results_text.insert(tk.END, f"{lookup_ip}\n\n", 'error_value')
                self.results_text.insert(tk.END, "  Possible reasons:\n", 'error_label')
                self.results_text.insert(tk.END, "    • Invalid IP address format\n", 'error_text')
                self.results_text.insert(tk.END, "    • API rate limiting (try again in a few minutes)\n", 'error_text')
                self.results_text.insert(tk.END, "    • IP address not found in database\n", 'error_text')
            else:
                self.results_text.insert(tk.END, "  Unable to retrieve IP location information.\n\n", 'error_label')
                self.results_text.insert(tk.END, "  Possible reasons:\n", 'error_label')
                self.results_text.insert(tk.END, "    • API rate limiting (try again in a few minutes)\n", 'error_text')
                self.results_text.insert(tk.END, "    • Network connectivity issues\n", 'error_text')
                self.results_text.insert(tk.END, "    • Temporary API unavailability\n", 'error_text')
            
            # Configure error text tags
            self.results_text.tag_config('error_header', foreground=self.colors['error'], font=('Consolas', 10, 'bold'))
            self.results_text.tag_config('error_label', foreground=self.colors['text_primary'], font=('Consolas', 10, 'bold'))
            self.results_text.tag_config('error_value', foreground=self.colors['error'], font=('Consolas', 10, 'bold'))
            self.results_text.tag_config('error_text', foreground=self.colors['text_secondary'], font=('Consolas', 10))
            
            self.map_btn.config(state=tk.DISABLED)
        
        self.results_text.config(state=tk.DISABLED)
        self.current_data = data
    
    def lookup_ip(self):
        """Lookup a specific IP address."""
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("Warning", "Please enter an IP address to lookup.")
            return
        
        self.update_status("Looking up IP address...", "blue")
        self.lookup_btn.config(state=tk.DISABLED)
        self.my_ip_btn.config(state=tk.DISABLED)
        
        # Run in thread to avoid freezing GUI
        thread = threading.Thread(target=self._lookup_ip_thread, args=(ip,))
        thread.daemon = True
        thread.start()
    
    def _lookup_ip_thread(self, ip):
        """Thread function for IP lookup."""
        try:
            lookup_ipv4 = ip if ":" not in ip else None
            lookup_ipv6 = ip if ":" in ip else None
            info_data = get_ip_info(ip)
            
            self.root.after(0, self._lookup_complete, lookup_ipv4, lookup_ipv6, info_data, ip)
        except Exception as e:
            self.root.after(0, self._lookup_error, str(e))
    
    def _lookup_complete(self, ipv4, ipv6, info_data, lookup_ip):
        """Callback after lookup completes."""
        self.display_results(ipv4, ipv6, info_data, lookup_ip)
        self.update_timestamp()
        if info_data:
            self.update_status("Lookup completed successfully!", "green")
        else:
            self.update_status("Lookup failed. See details above.", "red")
        self.lookup_btn.config(state=tk.NORMAL)
        self.my_ip_btn.config(state=tk.NORMAL)
    
    def _lookup_error(self, error_msg):
        """Callback for lookup error."""
        self.update_status(f"Error: {error_msg}", "red")
        self.lookup_btn.config(state=tk.NORMAL)
        self.my_ip_btn.config(state=tk.NORMAL)
    
    def get_my_ip(self):
        """Get user's own IP addresses."""
        self.ip_entry.delete(0, tk.END)
        self.update_status("Detecting your IP addresses...", "blue")
        self.lookup_btn.config(state=tk.DISABLED)
        self.my_ip_btn.config(state=tk.DISABLED)
        
        # Run in thread to avoid freezing GUI
        thread = threading.Thread(target=self._get_my_ip_thread)
        thread.daemon = True
        thread.start()
    
    def _get_my_ip_thread(self):
        """Thread function for getting user's IP."""
        try:
            ipv4 = get_ip_address("ipv4")
            ipv6 = get_ip_address("ipv6")
            
            # Try to get geolocation info - prefer IPv4, fallback to IPv6
            info_data = None
            if ipv4:
                info_data = get_ip_info(ipv4)
            if not info_data and ipv6:
                info_data = get_ip_info(ipv6)
            
            self.root.after(0, self._my_ip_complete, ipv4, ipv6, info_data)
        except Exception as e:
            self.root.after(0, self._my_ip_error, str(e))
    
    def _my_ip_complete(self, ipv4, ipv6, info_data):
        """Callback after getting user's IP completes."""
        self.display_results(ipv4, ipv6, info_data)
        self.update_timestamp()
        if info_data:
            self.update_status("IP detection completed successfully!", "green")
        else:
            self.update_status("IP detection failed. See details above.", "red")
        self.lookup_btn.config(state=tk.NORMAL)
        self.my_ip_btn.config(state=tk.NORMAL)
    
    def _my_ip_error(self, error_msg):
        """Callback for getting user's IP error."""
        self.update_status(f"Error: {error_msg}", "red")
        self.lookup_btn.config(state=tk.NORMAL)
        self.my_ip_btn.config(state=tk.NORMAL)
    
    def open_map(self):
        """Open location in web browser map."""
        if self.current_lat and self.current_lon:
            # Open in OpenStreetMap
            url = f"https://www.openstreetmap.org/?mlat={self.current_lat}&mlon={self.current_lon}&zoom=12"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Warning", "No coordinates available to display on map.")

def main():
    root = tk.Tk()
    app = IPLocationFinderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

