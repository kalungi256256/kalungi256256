import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import hashlib
import threading
import subprocess
import os
import sys
import random
import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import binascii
import re
from datetime import datetime

# ====================== DEVICE DETECTION (No USB Libraries) ======================
class DeviceDetector:
    """Detects Android devices using ADB and system commands only"""
    
    def __init__(self):
        self.devices = []
    
    def detect_all_devices(self):
        """Detect devices using standard methods (no external libraries)"""
        devices = []
        
        # Method 1: ADB detection (most reliable)
        devices.extend(self.detect_adb_devices())
        
        # Method 2: Network scanning for ADB ports
        devices.extend(self.detect_network_devices())
        
        # Method 3: Windows device detection
        if sys.platform == 'win32':
            devices.extend(self.detect_windows_devices())
        
        # Remove duplicates
        unique_devices = []
        seen_ids = set()
        for device in devices:
            device_id = device.get('serial', device.get('id', ''))
            if device_id and device_id not in seen_ids:
                seen_ids.add(device_id)
                unique_devices.append(device)
        
        self.devices = unique_devices
        return unique_devices
    
    def detect_adb_devices(self):
        """Standard ADB device detection"""
        devices = []
        try:
            # Check if ADB exists
            result = subprocess.run(['adb', 'version'], capture_output=True, text=True, timeout=3)
            if result.returncode != 0:
                return devices
                
            # Get devices
            result = subprocess.run(['adb', 'devices', '-l'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')[1:]
            
            for line in lines:
                if line.strip() and 'device' in line:
                    parts = line.split()
                    serial = parts[0]
                    
                    # Get device model
                    model = "Unknown"
                    try:
                        model_result = subprocess.run(['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'],
                                                    capture_output=True, text=True, timeout=3)
                        if model_result.stdout.strip():
                            model = model_result.stdout.strip()
                    except:
                        pass
                    
                    devices.append({
                        'type': 'adb',
                        'serial': serial,
                        'id': serial,
                        'name': model,
                        'status': 'connected',
                        'method': 'ADB'
                    })
        except subprocess.CalledProcessError:
            pass
        except FileNotFoundError:
            pass
        except Exception:
            pass
        
        return devices
    
    def detect_network_devices(self):
        """Simple network scan for ADB ports"""
        devices = []
        try:
            # Try common local IP patterns
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip_parts = local_ip.split('.')
            
            if len(ip_parts) == 4:
                base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
                
                # Scan last octet from 1 to 254
                for i in range(1, 255):
                    ip = f"{base_ip}.{i}"
                    for port in [5555, 5556]:  # Common ADB ports
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.3)
                            result = sock.connect_ex((ip, port))
                            if result == 0:
                                devices.append({
                                    'type': 'network',
                                    'id': f"{ip}:{port}",
                                    'name': f"Network Device at {ip}",
                                    'ip': ip,
                                    'port': port,
                                    'method': 'Network',
                                    'status': 'available'
                                })
                            sock.close()
                        except:
                            pass
        except:
            pass
        
        return devices
    
    def detect_windows_devices(self):
        """Windows-specific device detection using WMIC"""
        devices = []
        if sys.platform == 'win32':
            try:
                result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 'get', 'Name', 'DeviceID'],
                                      capture_output=True, text=True, timeout=5, shell=True)
                for line in result.stdout.split('\n'):
                    if 'Android' in line or 'ADB' in line or 'Phone' in line:
                        devices.append({
                            'type': 'windows',
                            'id': line[:50],
                            'name': line.strip()[:50],
                            'method': 'Windows',
                            'status': 'detected'
                        })
            except:
                pass
        return devices

# ====================== OPTIMIZED PATTERN GENERATOR ======================
def get_valid_moves(pos, used):
    """Ultra-fast move generation"""
    r, c = divmod(pos, 3)
    moves = []
    
    # All possible moves including diagonals
    for dr, dc in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nxt = nr * 3 + nc
            if not used[nxt]:
                moves.append(nxt)
    
    # Jump moves (over already used dots)
    for dr, dc in [(-2,-2), (-2,0), (-2,2), (0,-2), (0,2), (2,-2), (2,0), (2,2)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            mid_r = (r + nr) // 2
            mid_c = (c + nc) // 2
            mid = mid_r * 3 + mid_c
            nxt = nr * 3 + nc
            if used[mid] and not used[nxt]:
                moves.append(nxt)
    
    return moves

def generate_patterns_fast():
    """Fast pattern generator with caching"""
    for start in range(9):
        path = [start]
        used = [False] * 9
        used[start] = True
        yield from backtrack_fast(path, used)

def backtrack_fast(path, used):
    """Optimized backtracking"""
    if len(path) >= 4:
        yield tuple(divmod(p, 3) for p in path)
    
    if len(path) == 9:
        return
    
    for nxt in get_valid_moves(path[-1], used):
        path.append(nxt)
        used[nxt] = True
        yield from backtrack_fast(path, used)
        path.pop()
        used[nxt] = False

def hash_pattern(pattern):
    """Fast pattern hashing"""
    return hashlib.sha1(str(pattern).encode('utf-8')).hexdigest().upper()

# ====================== BRUTAL CRACKER GUI ======================
class BrutalCracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💀 BRUTAL PATTERN CRACKER 💀")
        self.geometry("1100x850")
        self.configure(bg='#0a0a0a')
        
        self.detector = DeviceDetector()
        self.devices = []
        self.selected_device = None
        self.cracking = False
        self.crack_thread = None
        
        self.setup_ui()
        self.scan_devices()  # Initial scan
        
        # Start background device monitoring
        self.monitor_devices()
    
    def setup_ui(self):
        """Setup the UI"""
        # Title
        title_frame = tk.Frame(self, bg='#000000', height=100)
        title_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(title_frame, text="💀 BRUTAL PATTERN CRACKER 💀", 
                                    font=("Arial Black", 26, "bold"), 
                                    bg='#000000', fg='#ff0000')
        self.title_label.pack(pady=20)
        
        subtitle = tk.Label(title_frame, text="Multi-Device Detection | Fast Pattern Cracking | ADB Integration",
                           font=("Arial", 11), bg='#000000', fg='#ff6666')
        subtitle.pack()
        
        # Main container
        main_frame = tk.Frame(self, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel - Devices
        left_panel = tk.LabelFrame(main_frame, text="📱 CONNECTED DEVICES", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#0a0a0a', fg='#ff0000', padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Device list
        self.device_listbox = tk.Listbox(left_panel, height=12, bg='#1a1a1a', 
                                         fg='#00ff00', font=("Consolas", 10),
                                         selectbackground='#ff0000', selectforeground='white')
        self.device_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg='#0a0a0a')
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.scan_btn = tk.Button(btn_frame, text="🔍 RESCAN DEVICES", 
                                  command=self.scan_devices, bg='#2196F3', fg='white',
                                  font=("Arial", 10, "bold"), height=2)
        self.scan_btn.pack(fill=tk.X, pady=2)
        
        self.select_btn = tk.Button(btn_frame, text="⚡ SELECT DEVICE", 
                                    command=self.select_device, bg='#ff0000', fg='white',
                                    font=("Arial", 10, "bold"), height=2)
        self.select_btn.pack(fill=tk.X, pady=2)
        
        # Device info
        info_frame = tk.LabelFrame(left_panel, text="DEVICE INFO", 
                                   font=("Arial", 10, "bold"), 
                                   bg='#0a0a0a', fg='#ff0000', padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.info_text = tk.Text(info_frame, height=8, bg='#1a1a1a', fg='#00ff00',
                                 font=("Consolas", 9), wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Attack
        right_panel = tk.Frame(main_frame, bg='#0a0a0a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Hash input
        hash_frame = tk.LabelFrame(right_panel, text="🎯 TARGET HASH", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#0a0a0a', fg='#ff0000', padx=10, pady=10)
        hash_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.hash_entry = tk.Entry(hash_frame, font=("Consolas", 11), bg='#1a1a1a',
                                   fg='#00ff00', insertbackground='white')
        self.hash_entry.pack(fill=tk.X, pady=5)
        
        # Attack options
        options_frame = tk.LabelFrame(right_panel, text="⚙️ ATTACK OPTIONS", 
                                      font=("Arial", 12, "bold"), 
                                      bg='#0a0a0a', fg='#ff0000', padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.test_pattern_btn = tk.Button(options_frame, text="🎲 GENERATE TEST PATTERN", 
                                         command=self.generate_test, bg='#FF9800', fg='white',
                                         font=("Arial", 10, "bold"), height=2)
        self.test_pattern_btn.pack(fill=tk.X, pady=5)
        
        self.read_device_btn = tk.Button(options_frame, text="📱 READ FROM DEVICE", 
                                        command=self.read_from_device, bg='#4CAF50', fg='white',
                                        font=("Arial", 10, "bold"), height=2)
        self.read_device_btn.pack(fill=tk.X, pady=5)
        
        # Attack button
        self.attack_btn = tk.Button(options_frame, text="💀 START BRUTAL ATTACK 💀", 
                                   command=self.start_attack, bg='#ff0000', fg='white',
                                   font=("Arial", 13, "bold"), height=2)
        self.attack_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = tk.Button(options_frame, text="⛔ STOP ATTACK", 
                                 command=self.stop_attack, bg='#333333', fg='white',
                                 font=("Arial", 11, "bold"), height=2,
                                 state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        # Results
        results_frame = tk.LabelFrame(right_panel, text="💀 RESULTS 💀", 
                                      font=("Arial", 12, "bold"), 
                                      bg='#0a0a0a', fg='#ff0000', padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12,
                                                      font=("Consolas", 9),
                                                      bg='#000000', fg='#00ff00',
                                                      insertbackground='white')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="💀 SYSTEM READY - SCAN FOR DEVICES 💀")
        status_bar = tk.Label(self, textvariable=self.status_var, font=("Arial", 10),
                             bg='#1a1a1a', fg='#ff0000', bd=1, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)
    
    def monitor_devices(self):
        """Background device monitoring"""
        def monitor():
            while True:
                if not self.cracking:
                    self.scan_devices()
                time.sleep(15)  # Scan every 15 seconds
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def scan_devices(self):
        """Scan for connected devices"""
        self.status_var.set("🔍 SCANNING FOR DEVICES...")
        self.device_listbox.delete(0, tk.END)
        
        devices = self.detector.detect_all_devices()
        self.devices = devices
        
        if not devices:
            self.device_listbox.insert(tk.END, "❌ NO DEVICES FOUND")
            self.status_var.set("💀 NO DEVICES - CONNECT AND ENABLE USB DEBUGGING 💀")
        else:
            for device in devices:
                name = device.get('name', device.get('serial', 'Unknown'))
                method = device.get('method', 'Unknown')
                display = f"[{method}] {name[:40]}"
                self.device_listbox.insert(tk.END, display)
            
            self.status_var.set(f"✅ {len(devices)} DEVICE(S) DETECTED")
    
    def select_device(self):
        """Select a device for attack"""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device first!")
            return
        
        self.selected_device = self.devices[selection[0]]
        
        # Display device info
        self.info_text.delete(1.0, tk.END)
        info = "="*40 + "\n"
        info += "SELECTED DEVICE\n"
        info += "="*40 + "\n\n"
        for key, value in self.selected_device.items():
            info += f"{key.upper()}: {value}\n"
        self.info_text.insert(1.0, info)
        
        self.status_var.set(f"🎯 TARGET: {self.selected_device.get('name', 'Unknown')}")
        
        # Flash feedback
        self.info_text.config(bg='#330000')
        self.update()
        time.sleep(0.1)
        self.info_text.config(bg='#1a1a1a')
    
    def generate_test(self):
        """Generate test pattern and hash"""
        # Get a few patterns for test
        patterns = []
        for i, pattern in enumerate(generate_patterns_fast()):
            if i < 100:  # First 100 patterns
                patterns.append(pattern)
            else:
                break
        
        if patterns:
            test_pattern = random.choice(patterns)
            test_hash = hash_pattern(test_pattern)
            
            self.hash_entry.delete(0, tk.END)
            self.hash_entry.insert(0, test_hash)
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "🎲 TEST PATTERN GENERATED\n")
            self.results_text.insert(tk.END, "="*50 + "\n")
            self.results_text.insert(tk.END, f"Pattern: {test_pattern}\n")
            self.results_text.insert(tk.END, f"Hash: {test_hash}\n")
            self.results_text.insert(tk.END, "="*50 + "\n")
            self.results_text.insert(tk.END, "Click START BRUTAL ATTACK to crack!\n")
            
            self.status_var.set("🎲 Test pattern ready!")
            messagebox.showinfo("Test Pattern Generated", 
                               f"Test pattern created!\nPattern: {test_pattern}\n\nClick 'Start Brutal Attack' to crack it.")
    
    def read_from_device(self):
        """Read gesture.key from selected device"""
        if not self.selected_device:
            messagebox.showwarning("No Device", "Select a device first!")
            return
        
        if self.selected_device.get('type') != 'adb':
            messagebox.showwarning("Not ADB", "Selected device doesn't support ADB!")
            return
        
        serial = self.selected_device.get('serial')
        
        self.status_var.set("📱 Reading from device...")
        self.progress.start()
        
        def read_thread():
            try:
                # Try to pull gesture.key
                result = subprocess.run(['adb', '-s', serial, 'pull', '/data/system/gesture.key', 'gesture.key'],
                                      capture_output=True, timeout=10)
                
                if os.path.exists('gesture.key') and os.path.getsize('gesture.key') > 0:
                    with open('gesture.key', 'rb') as f:
                        hash_hex = f.read().hex().upper()
                    
                    self.after(0, lambda: self.hash_entry.delete(0, tk.END))
                    self.after(0, lambda: self.hash_entry.insert(0, hash_hex))
                    self.after(0, lambda: self.results_text.insert(tk.END, f"✅ Hash read: {hash_hex}\n"))
                    self.after(0, lambda: self.status_var.set("✅ Hash loaded from device"))
                    
                    os.remove('gesture.key')
                else:
                    self.after(0, lambda: self.results_text.insert(tk.END, "❌ Cannot read gesture.key (needs root)\n"))
                    self.after(0, lambda: self.status_var.set("❌ Read failed - device may need root"))
            except Exception as e:
                self.after(0, lambda: self.results_text.insert(tk.END, f"❌ Error: {e}\n"))
            finally:
                self.after(0, self.progress.stop)
        
        threading.Thread(target=read_thread, daemon=True).start()
    
    def start_attack(self):
        """Start the brutal attack"""
        target_hash = self.hash_entry.get().strip().upper()
        if not target_hash:
            messagebox.showwarning("No Hash", "Enter a hash or generate a test pattern!")
            return
        
        if self.cracking:
            messagebox.showwarning("Attack Running", "Attack already in progress!")
            return
        
        self.cracking = True
        self.attack_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "💀💀💀 BRUTAL ATTACK INITIATED 💀💀💀\n")
        self.results_text.insert(tk.END, "="*50 + "\n")
        self.results_text.insert(tk.END, f"Target Hash: {target_hash}\n")
        self.results_text.insert(tk.END, "Checking all possible patterns...\n\n")
        
        self.crack_thread = threading.Thread(target=self.crack_thread, args=(target_hash,))
        self.crack_thread.daemon = True
        self.crack_thread.start()
    
    def crack_thread(self, target_hash):
        """Brute force cracking thread"""
        start_time = time.time()
        found = None
        count = 0
        
        try:
            for pattern in generate_patterns_fast():
                count += 1
                
                if count % 5000 == 0:
                    elapsed = time.time() - start_time
                    speed = count / elapsed if elapsed > 0 else 0
                    self.after(0, lambda c=count, s=speed: self.update_status(c, s))
                
                if hash_pattern(pattern) == target_hash:
                    found = pattern
                    break
                
                if not self.cracking:
                    break
            
            elapsed = time.time() - start_time
            self.after(0, lambda: self.show_result(found, count, elapsed))
        except Exception as e:
            self.after(0, lambda: self.show_result(None, count, 0, str(e)))
    
    def update_status(self, count, speed):
        """Update status message"""
        self.status_var.set(f"💀 CRACKING: {count:,} patterns checked ({speed:.0f} patterns/sec)")
    
    def show_result(self, pattern, count, elapsed, error=None):
        """Show cracking results"""
        self.cracking = False
        self.progress.stop()
        self.attack_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.results_text.insert(tk.END, "\n" + "="*50 + "\n")
        
        if error:
            self.status_var.set("❌ Attack failed!")
            self.results_text.insert(tk.END, f"❌ ERROR: {error}\n")
        elif pattern:
            self.status_var.set(f"✅ PATTERN FOUND in {elapsed:.2f} seconds!")
            self.results_text.insert(tk.END, "💀💀💀 PATTERN SUCCESSFULLY CRACKED! 💀💀💀\n")
            self.results_text.insert(tk.END, "="*50 + "\n")
            self.results_text.insert(tk.END, f"PATTERN: {pattern}\n")
            self.results_text.insert(tk.END, f"SEQUENCE: {[p[0]*3 + p[1] + 1 for p in pattern]}\n")
            self.results_text.insert(tk.END, f"TIME: {elapsed:.2f} seconds\n")
            self.results_text.insert(tk.END, f"CHECKED: {count:,} patterns\n")
            
            # Victory flash
            for _ in range(5):
                self.title_label.config(fg='#00ff00')
                self.update()
                time.sleep(0.1)
                self.title_label.config(fg='#ff0000')
                self.update()
                time.sleep(0.1)
        else:
            self.status_var.set("❌ Pattern not found!")
            self.results_text.insert(tk.END, f"❌ PATTERN NOT FOUND\n")
            self.results_text.insert(tk.END, f"Checked {count:,} patterns\n")
    
    def stop_attack(self):
        """Stop the attack"""
        if self.cracking:
            self.cracking = False
            self.status_var.set("⛔ ATTACK STOPPED")
            self.results_text.insert(tk.END, "\n⛔ Attack stopped by user\n")

# ====================== MAIN ======================
if __name__ == "__main__":
    try:
        print("💀 BRUTAL PATTERN CRACKER 💀")
        print("="*50)
        print("Starting application...")
        
        app = BrutalCracker()
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")