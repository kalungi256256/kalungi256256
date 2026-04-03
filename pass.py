# file: nexus_isp_manager.py
"""
NEXUS ISP ALL-IN-ONE MANAGEMENT SYSTEM
Author: Your Business Name
Purpose: Monitor networks + manage router users/passwords
"""

import time
import json
import base64
import logging
import webbrowser
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pywifi
from pywifi import const
import sys

from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize color support
init(autoreset=True)

# =============================
# YOUR BUSINESS CONFIGURATION
# =============================
BUSINESS_NAME = "NEXUS ISP"  # Your company name
BUILDING_ZONES = {
    "BldgA": {"location": "Main Street", "router_ip": "192.168.1.1", "model": "TP-Link Archer C7"},
    "BldgB": {"location": "Oak Avenue", "router_ip": "192.168.2.1", "model": "Netgear R7000"},
    "BldgC": {"location": "Maple Drive", "router_ip": "192.168.3.1", "model": "Ubiquiti UDM"},
    # Add your buildings here...
}
SCAN_INTERVAL = 15  # Seconds
PASSWORD_VAULT_FILE = "nexus_vault.enc"
MASTER_PASSWORD_HINT = "Your business license number"  # Shown if password is forgotten
ADMIN_CREDENTIALS = {}  # Will be loaded from vault

# =============================
# SECURE PASSWORD VAULT
# =============================
class SecureVault:
    def __init__(self):
        self.vault = {}
        self.key = None
        self.load_vault()

    def derive_key(self, master_password: str) -> bytes:
        """Derive encryption key from master password"""
        salt = b'nexus_isp_vault_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    def unlock_vault(self, master_password: str) -> bool:
        """Unlock vault with master password"""
        try:
            self.key = self.derive_key(master_password)
            fernet = Fernet(self.key)
            
            # Test decryption
            test_encrypted = fernet.encrypt(b"test")
            fernet.decrypt(test_encrypted)
            
            # Load actual vault
            self.load_vault()
            return True
        except Exception:
            return False

    def load_vault(self):
        """Load and decrypt password vault"""
        if not self.key:
            return
            
        try:
            with open(PASSWORD_VAULT_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            fernet = Fernet(self.key)
            decrypted = fernet.decrypt(encrypted_data)
            self.vault = json.loads(decrypted)
        except (FileNotFoundError, json.JSONDecodeError):
            self.vault = {
                "buildings": {},
                "admin_credentials": {}
            }

    def save_vault(self):
        """Encrypt and save password vault"""
        if not self.key:
            return
            
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(json.dumps(self.vault).encode())
        
        with open(PASSWORD_VAULT_FILE, 'wb') as f:
            f.write(encrypted)

    def add_building_credential(self, building: str, ssid: str, password: str, is_wireless: bool = True):
        """Add new credential for building network"""
        if building not in BUILDING_ZONES:
            return "Invalid building"
        
        if building not in self.vault["buildings"]:
            self.vault["buildings"][building] = {}
        
        self.vault["buildings"][building][ssid] = {
            "password": password,
            "is_wireless": is_wireless,
            "last_updated": time.time()
        }
        self.save_vault()
        return "Credentials saved securely"

    def add_admin_credential(self, building: str, username: str, password: str):
        """Add router admin credentials"""
        if building not in BUILDING_ZONES:
            return "Invalid building"
        
        self.vault["admin_credentials"][building] = {
            "username": username,
            "password": password,
            "last_updated": time.time()
        }
        self.save_vault()
        return "Admin credentials saved"

    def get_building_credential(self, building: str, ssid: str) -> Optional[str]:
        """Retrieve network password"""
        if (building in self.vault["buildings"] and 
            ssid in self.vault["buildings"][building]):
            return self.vault["buildings"][building][ssid]["password"]
        return None

    def get_admin_credential(self, building: str) -> Optional[Dict]:
        """Retrieve admin credentials"""
        return self.vault["admin_credentials"].get(building)

# =============================
# ROUTER ADMINISTRATION
# =============================
class RouterManager:
    def __init__(self, vault: SecureVault):
        self.vault = vault
        self.building_zones = BUILDING_ZONES

    def open_admin_page(self, building: str):
        """Open router admin page with stored credentials"""
        admin = self.vault.get_admin_credential(building)
        if not admin:
            self.prompt_admin_credentials(building)
            return
            
        ip = self.building_zones[building]["router_ip"]
        url = f"http://{ip}"
        
        # Show credentials to user
        self.show_credentials(building, admin)
        
        # Open browser
        webbrowser.open(url)
        self.log_info(f"🌐 Opening admin page for {building} ({url})")

    def show_credentials(self, building: str, admin: Dict):
        """Display credentials with security warning"""
        messagebox.showinfo(
            f"{BUSINESS_NAME} - {building} Admin",
            f"Router Admin Credentials:\n\n"
            f"URL: http://{self.building_zones[building]['router_ip']}\n"
            f"Username: {admin['username']}\n"
            f"Password: {admin['password']}\n\n"
            " Do not share these credentials!\n"
            "They will be hidden after 10 seconds."
        )
        
        # Clear password from clipboard after 10 seconds
        def clear_clipboard():
            try:
                subprocess.run(['clip', ''], check=True, text=True)
            except:
                pass
        
        root = tk.Tk()
        root.withdraw()
        root.after(10000, clear_clipboard)
        root.destroy()

    def prompt_admin_credentials(self, building: str):
        """Securely prompt for admin credentials"""
        root = tk.Tk()
        root.withdraw()
        
        username = simpledialog.askstring(
            f"{BUSINESS_NAME} - {building} Admin",
            f"Enter admin username for {building} ({self.building_zones[building]['router_ip']}):",
            initialvalue="admin"
        )
        if not username:
            return
            
        password = simpledialog.askstring(
            f"{BUSINESS_NAME} - {building} Admin",
            f"Enter admin password for {building}:",
            show='*'
        )
        if not password:
            return
            
        self.vault.add_admin_credential(building, username, password)
        self.log_success(f"Admin credentials saved for {building}")

    def manage_users(self, building: str):
        """Launch user management interface for building"""
        self.open_admin_page(building)
        
        # Show management guide based on router model
        model = self.building_zones[building]["model"]
        guide = self.get_management_guide(model)
        
        messagebox.showinfo(
            f"{BUSINESS_NAME} - {building} User Management",
            f"User Management Guide for {model}:\n\n{guide}\n\n"
            "Follow these steps to manage users:\n"
            "1. Log in to the admin page (already opened)\n"
            "2. Use the steps above to reset passwords\n"
            "3. Press OK when done to return to monitoring"
        )

    def get_management_guide(self, model: str) -> str:
        """Get model-specific management guide"""
        guides = {
            "TP-Link Archer C7": (
                "1. Go to Advanced > Security > Parental Controls\n"
                "2. Select the user to manage\n"
                "3. Reset password: System Tools > Password\n"
                "4. Block user: Security > Access Control"
            ),
            "Netgear R7000": (
                "1. Go to Advanced > User Management\n"
                "2. Select user > Reset Password\n"
                "3. To block: Security > Access Control > Add Rule"
            ),
            "Ubiquiti UDM": (
                "1. Go to Settings > User Management\n"
                "2. Select user > Edit > Reset Password\n"
                "3. To block: Settings > Profiles > Create Block Policy"
            ),
            "Default": (
                "1. Log in to router admin page\n"
                "2. Look for 'User Management' or 'Attached Devices'\n"
                "3. Select user to reset password\n"
                "4. Use 'Block' option to restrict access"
            )
        }
        return guides.get(model, guides["Default"])

    def log_info(self, message: str):
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

    def log_success(self, message: str):
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

# =============================
# NETWORK MONITORING SYSTEM
# =============================
class NetworkMonitor:
    def __init__(self):
        self.vault = SecureVault()
        self.router_manager = RouterManager(self.vault)
        self.master_password = None
        self.setup_logging()
        self.interface = self._select_interface()
        self.known_networks = {}
        self.building_zones = BUILDING_ZONES

    def setup_logging(self):
        self.logger = logging.getLogger("nexus_isp")
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler("nexus_monitor.log")
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        self.log_info(f"✅ {BUSINESS_NAME} Monitoring System Started")

    def _select_interface(self):
        """Select best interface for monitoring (fixed for pywifi 1.1.12)"""
        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()
        
        if not interfaces:
            self.log_error("No Wi-Fi interfaces found! Connect a wireless adapter")
            sys.exit(1)
        
        # Prioritize interfaces with active connections
        connected_interfaces = [i for i in interfaces if i.status() == const.IFACE_CONNECTED]
        return connected_interfaces[0] if connected_interfaces else interfaces[0]

    def log_info(self, message: str):
        self.logger.info(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

    def log_warning(self, message: str):
        self.logger.warning(f"{Fore.YELLOW}  {message}{Style.RESET_ALL}")

    def log_error(self, message: str):
        self.logger.error(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

    def log_success(self, message: str):
        self.logger.info(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

    def authenticate(self):
        """Authenticate with master password"""
        if self.master_password:
            return True
            
        self.log_info(f"🔒 {BUSINESS_NAME} Secure Access")
        self.log_info(f"Hint: {MASTER_PASSWORD_HINT}")
        
        for _ in range(3):
            password = input(f"Enter master password [{BUSINESS_NAME}]: ")
            if self.vault.unlock_vault(password):
                self.master_password = password
                self.log_success("Access granted!")
                return True
            self.log_error("Invalid password. Try again.")
        
        self.log_error("Access denied. Exiting for security.")
        sys.exit(1)

    def get_building_by_ssid(self, ssid: str) -> Optional[str]:
        """Map SSID to building zone"""
        for building, info in self.building_zones.items():
            if building in ssid or ssid.startswith(BUSINESS_NAME):
                return building
        return None

    def get_security(self, profile) -> str:
        """Determine security type from WiFi profile"""
        # Handle case where profile.akm might be None
        if not hasattr(profile, 'akm') or profile.akm is None:
            return "UNKNOWN"
        
        # Check if akm is empty or not a list
        if not isinstance(profile.akm, list) or len(profile.akm) == 0:
            return "OPEN"
        
        # Safely check for each security type without causing errors
        security_types = {
            "WPA3-PSK": lambda: hasattr(const, 'AKM_TYPE_WPA3PSK') and const.AKM_TYPE_WPA3PSK in profile.akm,
            "WPA2-PSK": lambda: hasattr(const, 'AKM_TYPE_WPA2PSK') and const.AKM_TYPE_WPA2PSK in profile.akm,
            "WPA-PSK": lambda: hasattr(const, 'AKM_TYPE_WPAPSK') and const.AKM_TYPE_WPAPSK in profile.akm,
            "OPEN": lambda: hasattr(const, 'AKM_TYPE_NONE') and const.AKM_TYPE_NONE in profile.akm
        }
        
        # Check in order of security strength
        for security, check in security_types.items():
            try:
                if check():
                    return security
            except:
                continue
        
        return "UNKNOWN"


    def scan_networks(self) -> Dict[str, dict]:
        """Scan for networks with building identification"""
        networks = {}
        try:
            self.interface.scan()
            time.sleep(3)
            results = self.interface.scan_results()
            
            for profile in results:
                ssid = profile.ssid or "<HIDDEN>"
                bssid = profile.bssid
                
                # Map to building
                building = self.get_building_by_ssid(ssid)
                is_owned = bool(building)
                
                networks[bssid] = {
                    "ssid": ssid,
                    "bssid": bssid,
                    "signal": profile.signal,
                    "freq": profile.freq,
                    "security": self.get_security(profile),
                    "building": building,
                    "is_owned": is_owned,
                    "password": self.vault.get_building_credential(building, ssid) if building else None,
                    "admin_creds": self.vault.get_admin_credential(building) if building else None
                }
            return networks
        except Exception as e:
            self.log_error(f"Scan failed: {str(e)}")
            return {}

    def display_networks(self, networks: Dict[str, dict]):
        """Display networks with building identification and management options"""
        table_data = []
        for net in networks.values():
            # Signal quality
            if net["signal"] >= -50:
                signal_color = Fore.GREEN
            elif net["signal"] >= -65:
                signal_color = Fore.YELLOW
            elif net["signal"] >= -80:
                signal_color = Fore.LIGHTYELLOW_EX
            else:
                signal_color = Fore.RED
                
            # Password status
            password_status = "●" if net["password"] else "○"
            password_color = Fore.GREEN if net["password"] else Fore.LIGHTBLACK_EX
            
            # Building identification
            building = net["building"] or "Unknown"
            building_color = Fore.MAGENTA if net["is_owned"] else Fore.LIGHTBLACK_EX
            
            # Management option
            manage_str = "M" if net["is_owned"] else ""
            manage_color = Fore.CYAN if net["is_owned"] else Fore.LIGHTBLACK_EX
            
            table_data.append([
                f"{building_color}{building}{Style.RESET_ALL}",
                net["ssid"],
                f"{signal_color}{net['signal']} dBm{Style.RESET_ALL}",
                f"{password_color}{password_status}{Style.RESET_ALL}",
                net["security"],
                f"{manage_color}{manage_str}{Style.RESET_ALL}"
            ])
        
        # Sort by building (your networks first)
        table_data.sort(key=lambda x: (x[0] == "Unknown", x[0]))
        
        print("\n" + tabulate(
            table_data,
            headers=["Building", "SSID", "Signal", "Password", "Security", "Mgmt"],
            tablefmt="fancy_grid",
            maxcolwidths=[15, 25, None, None, None, None]
        ))

    def handle_new_network(self, net: dict):
        """Handle new network detection with business logic"""
        if net["is_owned"]:
            self.log_info(f"🔍 New network in {net['building']}: {net['ssid']}")
            
            # Check if we have password for it
            if net["password"]:
                self.log_success(f"✅ Password known for {net['ssid']}")
            else:
                self.log_warning(f"⚠️ New network detected - no password stored")
                self.prompt_for_password(net)
        else:
            self.log_warning(f"🚨 New external network: {net['ssid']}")

    def prompt_for_password(self, net: dict):
        """Securely prompt for new password"""
        print(f"\n{Fore.YELLOW}SECURE PASSWORD ENTRY FOR {net['building']}{Style.RESET_ALL}")
        print(f"Network: {net['ssid']}")
        print("This password will be encrypted and stored securely.")
        
        while True:
            password = input("Enter password (min 8 chars): ")
            if len(password) < 8:
                print(f"{Fore.RED}Password too short!{Style.RESET_ALL}")
                continue
                
            confirm = input("Confirm password: ")
            if password == confirm:
                self.vault.add_building_credential(
                    net["building"],
                    net["ssid"],
                    password,
                    is_wireless=True
                )
                self.log_success(f"Password saved for {net['ssid']}")
                break
            print(f"{Fore.RED}Passwords don't match!{Style.RESET_ALL}")

    def monitor(self):
        """Main monitoring loop with business features"""
        self.authenticate()  # First, authenticate with master password
        
        self.log_info(f"Starting monitoring for {len(self.building_zones)} buildings")
        self.log_info("Press 'm' to manage a network | Press CTRL+C to stop")
        self.log_info(f"Password vault: {PASSWORD_VAULT_FILE}")
        
        try:
            while True:
                current_networks = self.scan_networks()
                if not current_networks:
                    time.sleep(5)
                    continue
                
                # Display networks with business context
                self.display_networks(current_networks)
                
                # Check for new networks
                for bssid, net in current_networks.items():
                    if bssid not in self.known_networks:
                        self.handle_new_network(net)
                
                self.known_networks = current_networks
                
                # Handle user input for management
                if platform.system() == "Windows":
                    import msvcrt
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8').lower()
                        if key == 'm':
                            self.handle_management_request()
                else:
                    # Non-Windows implementation would use other methods
                    time.sleep(0.1)
                
                # Status line
                owned_count = sum(1 for n in current_networks.values() if n["is_owned"])
                print(f"\n{Fore.CYAN}Monitoring {len(current_networks)} networks | "
                      f"Your networks: {owned_count} | "
                      f"Press 'm' to manage | Last scan: {time.strftime('%H:%M:%S')}{Style.RESET_ALL}", 
                      end='\r')
                
                time.sleep(SCAN_INTERVAL)
                
        except KeyboardInterrupt:
            self.log_info("\nMonitoring stopped by user")
            sys.exit(0)

    def handle_management_request(self):
        """Handle management request from user"""
        print("\n" + "="*50)
        print("  BUILDING MANAGEMENT MENU")
        print("="*50)
        
        # List all buildings with their status
        for i, (building, info) in enumerate(self.building_zones.items(), 1):
            status = "ONLINE" if self.check_router_status(building) else "OFFLINE"
            status_color = Fore.GREEN if status == "ONLINE" else Fore.RED
            print(f"{i}. {building} ({info['location']}) - {status_color}{status}{Style.RESET_ALL}")
        
        print(f"{len(self.building_zones)+1}. Return to monitoring")
        print("="*50)
        
        choice = input(f"Select building to manage (1-{len(self.building_zones)+1}): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.building_zones):
                building = list(self.building_zones.keys())[choice-1]
                self.manage_building(building)
            # Choice len+1 returns to monitoring
        except:
            pass

    def check_router_status(self, building: str) -> bool:
        """Check if router is online"""
        ip = self.building_zones[building]["router_ip"]
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', ip]
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

    def manage_building(self, building: str):
        """Management workflow for a building"""
        print(f"\n{Fore.MAGENTA}MANAGING {building}{Style.RESET_ALL}")
        print(f"Location: {self.building_zones[building]['location']}")
        print(f"Router: {self.building_zones[building]['model']} at {self.building_zones[building]['router_ip']}")
        
        # Check admin credentials
        admin = self.vault.get_admin_credential(building)
        if not admin:
            print(f"{Fore.YELLOW}⚠️ Admin credentials not stored. You'll need to enter them manually.{Style.RESET_ALL}")
        
        while True:
            print("\nOptions:")
            print("1. Open Router Admin Page")
            print("2. Manage Users (reset passwords/block users)")
            print("3. Update Admin Credentials")
            print("4. Update Wi-Fi Password")
            print("5. Back to monitoring")
            
            choice = input("Select option: ")
            if choice == '1':
                self.router_manager.open_admin_page(building)
            elif choice == '2':
                self.router_manager.manage_users(building)
            elif choice == '3':
                self.router_manager.prompt_admin_credentials(building)
            elif choice == '4':
                self.prompt_for_password({
                    "building": building,
                    "ssid": input("Enter SSID: ")
                })
            elif choice == '5':
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")

# =============================
# MAIN EXECUTION
# =============================
def main():
    print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}")
    print(f"  {BUSINESS_NAME} NETWORK MANAGEMENT SYSTEM")
    print(f"  Buildings: {len(BUILDING_ZONES)} | Secure Vault: {PASSWORD_VAULT_FILE}")
    print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}")
    
    # Check dependencies
    dependencies = [
        ("colorama", "colorama"),
        ("tabulate", "tabulate"),
        ("cryptography", "cryptography"),
        ("pywifi", "pywifi"),
        ("tkinter", "tkinter")
    ]
    
    missing = []
    for name, module in dependencies:
        try:
            __import__(module)
        except ImportError:
            missing.append(name)
    
    if missing:
        print(f"{Fore.RED}❌ Missing dependencies: {', '.join(missing)}{Style.RESET_ALL}")
        print(f"Install with: pip install {', '.join(missing)}")
        sys.exit(1)
    
    # Initialize and run monitor
    monitor = NetworkMonitor()
    monitor.monitor()

if __name__ == "__main__":
    main()
