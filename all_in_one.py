import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import hashlib
import threading
import random
import time
import itertools

# ====================== PATTERN GENERATOR ======================
def get_valid_moves(pos, used):
    """Get valid next moves for pattern lock"""
    r, c = divmod(pos, 3)
    moves = []
    
    # Adjacent moves
    for dr, dc in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nxt = nr * 3 + nc
            if not used[nxt]:
                moves.append(nxt)
    
    # Jump moves
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

def generate_patterns():
    """Generate all valid patterns (4-9 points)"""
    for start in range(9):
        path = [start]
        used = [False] * 9
        used[start] = True
        yield from backtrack(path, used)

def backtrack(path, used):
    """Backtracking pattern generator"""
    if len(path) >= 4:
        yield tuple(divmod(p, 3) for p in path)
    
    if len(path) == 9:
        return
    
    for nxt in get_valid_moves(path[-1], used):
        path.append(nxt)
        used[nxt] = True
        yield from backtrack(path, used)
        path.pop()
        used[nxt] = False

# ====================== PIN GENERATOR ======================
def generate_pins():
    """Generate common PINs and all PINs"""
    # Common PINs first
    common = ['1234', '0000', '1111', '2580', '0852', '5555', '1212', '1998', '2001',
              '7777', '1004', '2000', '2020', '1122', '1313', '4444', '6969', '8888',
              '4321', '5683', '9999', '6666', '12345', '123456', '654321', '111111']
    
    for pin in common:
        yield pin
    
    # Then all possible PINs
    for length in range(4, 7):
        for pin in itertools.product('0123456789', repeat=length):
            yield ''.join(pin)

# ====================== PASSWORD GENERATOR ======================
def generate_passwords():
    """Generate common passwords"""
    common = [
        'password', '123456', '12345678', '1234', 'qwerty', 'abc123',
        'monkey', 'dragon', 'letmein', 'admin', 'welcome', 'master',
        'sunshine', 'password1', 'princess', 'football', 'iloveyou',
        'admin123', 'root123', 'toor', 'passw0rd', 'password123',
        'android', 'samsung', 'google', 'qwerty123'
    ]
    
    for pwd in common:
        yield pwd

# ====================== MAIN APPLICATION ======================
class PatternCracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔓 Android Pattern/PIN/Password Cracker")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        self.cracking = False
        self.crack_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title = tk.Label(self.root, text="ANDROID LOCK CRACKER", 
                        font=("Arial", 24, "bold"), bg='#2c3e50', fg='white')
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="Crack Pattern Locks | PIN Codes | Passwords",
                           font=("Arial", 11), bg='#2c3e50', fg='#ecf0f1')
        subtitle.pack()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Attack type selection
        type_frame = tk.LabelFrame(main_frame, text="Attack Type", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#34495e', fg='white', padx=10, pady=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.attack_type = tk.StringVar(value="pattern")
        
        tk.Radiobutton(type_frame, text="🔒 Pattern Lock", variable=self.attack_type, 
                      value="pattern", bg='#34495e', fg='white', selectcolor='#2c3e50',
                      font=("Arial", 11)).pack(anchor=tk.W, pady=2)
        
        tk.Radiobutton(type_frame, text="🔢 PIN Code (4-6 digits)", variable=self.attack_type, 
                      value="pin", bg='#34495e', fg='white', selectcolor='#2c3e50',
                      font=("Arial", 11)).pack(anchor=tk.W, pady=2)
        
        tk.Radiobutton(type_frame, text="🔑 Password", variable=self.attack_type, 
                      value="password", bg='#34495e', fg='white', selectcolor='#2c3e50',
                      font=("Arial", 11)).pack(anchor=tk.W, pady=2)
        
        # Target hash
        hash_frame = tk.LabelFrame(main_frame, text="Target SHA1 Hash", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#34495e', fg='white', padx=10, pady=10)
        hash_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.hash_entry = tk.Entry(hash_frame, font=("Consolas", 11), 
                                   bg='#ecf0f1', fg='#2c3e50')
        self.hash_entry.pack(fill=tk.X, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(hash_frame, bg='#34495e')
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Test buttons
        tk.Button(btn_frame, text="Test Pattern", command=self.test_pattern,
                 bg='#e67e22', fg='white', font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="Test PIN", command=self.test_pin,
                 bg='#e67e22', fg='white', font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="Test Password", command=self.test_password,
                 bg='#e67e22', fg='white', font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=2)
        
        # Attack buttons
        attack_frame = tk.Frame(main_frame, bg='#2c3e50')
        attack_frame.pack(fill=tk.X, pady=10)
        
        self.crack_btn = tk.Button(attack_frame, text="💀 START CRACKING 💀", 
                                   command=self.start_cracking,
                                   bg='#c0392b', fg='white', font=("Arial", 14, "bold"),
                                   height=2)
        self.crack_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = tk.Button(attack_frame, text="⛔ STOP", 
                                  command=self.stop_cracking,
                                  bg='#7f8c8d', fg='white', font=("Arial", 11),
                                  height=1, state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X)
        
        # Status
        self.status_label = tk.Label(main_frame, text="Ready", 
                                     font=("Arial", 10), bg='#2c3e50', fg='#ecf0f1')
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Results area
        result_frame = tk.LabelFrame(main_frame, text="Results", 
                                     font=("Arial", 12, "bold"), 
                                     bg='#34495e', fg='white', padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=12,
                                                     font=("Consolas", 10),
                                                     bg='#ecf0f1', fg='#2c3e50')
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    def test_pattern(self):
        """Generate a test pattern and its hash"""
        # Get a few patterns
        patterns = []
        for i, p in enumerate(generate_patterns()):
            if i < 100:
                patterns.append(p)
            else:
                break
        
        if patterns:
            test = random.choice(patterns)
            test_hash = hashlib.sha1(str(test).encode()).hexdigest().upper()
            
            self.hash_entry.delete(0, tk.END)
            self.hash_entry.insert(0, test_hash)
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "🎲 TEST PATTERN GENERATED\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.result_text.insert(tk.END, f"Pattern: {test}\n")
            self.result_text.insert(tk.END, f"Sequence: {[p[0]*3 + p[1] + 1 for p in test]}\n")
            self.result_text.insert(tk.END, f"Hash: {test_hash}\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.result_text.insert(tk.END, "\nClick 'START CRACKING' to find this pattern!\n")
            
            self.status_label.config(text="Test pattern ready - Click Start Cracking", fg='#2ecc71')
    
    def test_pin(self):
        """Generate a test PIN and its hash"""
        test_pin = random.choice(['1234', '0000', '1111', '2580', '123456'])
        test_hash = hashlib.sha1(test_pin.encode()).hexdigest().upper()
        
        self.hash_entry.delete(0, tk.END)
        self.hash_entry.insert(0, test_hash)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "🔢 TEST PIN GENERATED\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"PIN: {test_pin}\n")
        self.result_text.insert(tk.END, f"Hash: {test_hash}\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, "\nClick 'START CRACKING' to find this PIN!\n")
        
        self.status_label.config(text="Test PIN ready - Click Start Cracking", fg='#2ecc71')
    
    def test_password(self):
        """Generate a test password and its hash"""
        test_pass = random.choice(['password123', 'admin123', 'android', 'qwerty123'])
        test_hash = hashlib.sha1(test_pass.encode()).hexdigest().upper()
        
        self.hash_entry.delete(0, tk.END)
        self.hash_entry.insert(0, test_hash)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "🔑 TEST PASSWORD GENERATED\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"Password: {test_pass}\n")
        self.result_text.insert(tk.END, f"Hash: {test_hash}\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, "\nClick 'START CRACKING' to find this password!\n")
        
        self.status_label.config(text="Test password ready - Click Start Cracking", fg='#2ecc71')
    
    def start_cracking(self):
        """Start the cracking process"""
        target = self.hash_entry.get().strip().upper()
        if not target:
            messagebox.showwarning("No Target", "Please enter a hash or generate a test first!")
            return
        
        if self.cracking:
            messagebox.showwarning("Already Running", "Cracking is already in progress!")
            return
        
        self.cracking = True
        self.crack_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "💀 CRACKING STARTED 💀\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"Target: {target}\n")
        self.result_text.insert(tk.END, f"Type: {self.attack_type.get()}\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        
        # Start cracking in background thread
        self.crack_thread = threading.Thread(target=self.crack_worker, args=(target,))
        self.crack_thread.daemon = True
        self.crack_thread.start()
    
    def crack_worker(self, target_hash):
        """Worker thread for cracking"""
        start_time = time.time()
        found = None
        count = 0
        attack_type = self.attack_type.get()
        
        try:
            if attack_type == "pattern":
                self.update_result("🔒 Cracking pattern lock...\n\n")
                for pattern in generate_patterns():
                    count += 1
                    if count % 5000 == 0:
                        self.update_status(count, start_time)
                    
                    if hashlib.sha1(str(pattern).encode()).hexdigest().upper() == target_hash:
                        found = pattern
                        break
                    
                    if not self.cracking:
                        break
            
            elif attack_type == "pin":
                self.update_result("🔢 Cracking PIN code...\n\n")
                for pin in generate_pins():
                    count += 1
                    if count % 10000 == 0:
                        self.update_status(count, start_time)
                    
                    if hashlib.sha1(pin.encode()).hexdigest().upper() == target_hash:
                        found = pin
                        break
                    
                    if not self.cracking:
                        break
            
            elif attack_type == "password":
                self.update_result("🔑 Cracking password...\n\n")
                for password in generate_passwords():
                    count += 1
                    if count % 100 == 0:
                        self.update_status(count, start_time)
                    
                    if hashlib.sha1(password.encode()).hexdigest().upper() == target_hash:
                        found = password
                        break
                    
                    if not self.cracking:
                        break
            
            elapsed = time.time() - start_time
            self.root.after(0, lambda: self.show_result(found, count, elapsed))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_result(None, count, 0, str(e)))
    
    def update_result(self, text):
        """Update result text from thread"""
        self.root.after(0, lambda: self.result_text.insert(tk.END, text))
        self.root.after(0, lambda: self.result_text.see(tk.END))
    
    def update_status(self, count, start_time):
        """Update status message"""
        elapsed = time.time() - start_time
        speed = count / elapsed if elapsed > 0 else 0
        self.root.after(0, lambda: self.status_label.config(
            text=f"Cracking... {count:,} attempts | {speed:.0f}/sec"
        ))
    
    def show_result(self, found, count, elapsed, error=None):
        """Display the cracking result"""
        self.cracking = False
        self.progress.stop()
        self.crack_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
        
        if error:
            self.status_label.config(text="Error occurred!", fg='#e74c3c')
            self.result_text.insert(tk.END, f"❌ ERROR: {error}\n")
        elif found:
            self.status_label.config(text="SUCCESS! Pattern cracked!", fg='#2ecc71')
            self.result_text.insert(tk.END, "✅✅✅ SUCCESS! ✅✅✅\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.result_text.insert(tk.END, f"🔓 RESULT: {found}\n")
            self.result_text.insert(tk.END, f"⏱️ TIME: {elapsed:.2f} seconds\n")
            self.result_text.insert(tk.END, f"🔢 ATTEMPTS: {count:,}\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            
            # Flash success
            self.flash_success()
        else:
            self.status_label.config(text="Not found - Try different attack type", fg='#e74c3c')
            self.result_text.insert(tk.END, f"❌ NOT FOUND\n")
            self.result_text.insert(tk.END, f"Checked {count:,} possibilities\n")
    
    def flash_success(self):
        """Flash the window on success"""
        original_bg = self.root.cget('bg')
        for _ in range(5):
            self.root.configure(bg='#27ae60')
            self.root.update()
            time.sleep(0.1)
            self.root.configure(bg=original_bg)
            self.root.update()
            time.sleep(0.1)
    
    def stop_cracking(self):
        """Stop the cracking process"""
        if self.cracking:
            self.cracking = False
            self.status_label.config(text="Stopping...", fg='#e74c3c')
            self.result_text.insert(tk.END, "\n⛔ STOPPED BY USER\n")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

# ====================== MAIN ======================
if __name__ == "__main__":
    print("="*50)
    print("ANDROID PATTERN/PIN/PASSWORD CRACKER")
    print("="*50)
    print("Starting application...")
    print("The GUI window should appear in a moment...")
    print("If it doesn't appear, check for errors above.")
    print("="*50)
    
    try:
        app = PatternCracker()
        app.run()
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")