import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import hashlib
import threading
import subprocess
import os
import sys
import random

# ====================== PATTERN GENERATOR ======================
def get_valid_next(pos, used):
    r, c = divmod(pos, 3)
    moves = []

    # Adjacent moves (including diagonal)
    for dr, dc in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nxt = nr * 3 + nc
            if not used[nxt]:
                moves.append(nxt)

    # Jump over middle dot (only if middle is already used)
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


def backtrack(path, used):
    if len(path) >= 4:
        yield tuple(divmod(p, 3) for p in path)
    
    if len(path) == 9:
        return

    for nxt in get_valid_next(path[-1], used):
        path.append(nxt)
        used[nxt] = True
        yield from backtrack(path, used)
        path.pop()
        used[nxt] = False


def generate_patterns():
    """Generate all valid Android patterns (4-9 points)"""
    for start in range(9):
        path = [start]
        used = [False] * 9
        used[start] = True
        yield from backtrack(path, used)


def pattern_to_hash(pattern):
    """Convert pattern to SHA1 hash like gesture.key"""
    return hashlib.sha1(str(pattern).encode('utf-8')).hexdigest().upper()


def pattern_to_sequence(pattern):
    """Convert pattern coordinates to dot numbers (0-8)"""
    return [r*3 + c for r, c in pattern]


def sequence_to_pattern(sequence):
    """Convert dot numbers to coordinates"""
    return [(dot//3, dot%3) for dot in sequence]


# ====================== IMPROVED ADB FUNCTIONS ======================
def check_adb_available():
    """Check if ADB is installed and accessible"""
    import shutil
    return shutil.which('adb') is not None


def get_adb_devices():
    """Get list of connected devices"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
        devices = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip() and 'device' in line and 'unauthorized' not in line:
                device_id = line.split()[0]
                devices.append(device_id)
        return devices
    except:
        return []


def read_gesture_key_improved():
    """Improved function to read gesture.key with better error handling"""
    try:
        # Check ADB availability
        if not check_adb_available():
            return None, "❌ ADB not found!\n\nPlease install Android Platform Tools:\n• Windows: Download from developer.android.com\n• Linux: sudo apt install adb\n• Mac: brew install android-platform-tools"

        # Check connected devices
        devices = get_adb_devices()
        if not devices:
            return None, "❌ No Android device found.\n\nPlease:\n1. Enable USB Debugging on your phone\n2. Connect via USB\n3. Authorize the connection on your phone"

        device_id = devices[0]
        
        # Try to pull gesture.key
        local_file = "gesture.key"
        result = subprocess.run(['adb', '-s', device_id, 'pull', '/data/system/gesture.key', local_file],
                               capture_output=True, text=True, timeout=10)

        if os.path.exists(local_file) and os.path.getsize(local_file) > 0:
            with open(local_file, "rb") as f:
                hash_hex = f.read().hex().upper()
            os.remove(local_file)
            
            return hash_hex, f"✅ Successfully read from {device_id}!\nHash: {hash_hex}\n\nNote: This works only on rooted devices or Android < 8.0"
        else:
            return None, "❌ Cannot access gesture.key\n\nThis file requires ROOT access on Android 8+.\n\nAlternative methods:\n• Use 'Test Pattern' button below\n• Root your device\n• Use recovery mode to access the file"

    except subprocess.TimeoutExpired:
        return None, "❌ ADB command timed out. Check your connection."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


# ====================== TEST PATTERN GENERATOR ======================
def generate_test_pattern():
    """Generate a random valid pattern for testing"""
    patterns = []
    # Collect first 100 patterns for testing
    for i, pattern in enumerate(generate_patterns()):
        if i < 100:
            patterns.append(pattern)
        else:
            break
    
    if patterns:
        return random.choice(patterns)
    return ((0,0), (0,1), (0,2), (1,2))  # Default pattern


# ====================== MAIN GUI ======================
class PatternCrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Android Pattern Lock Cracker - Enhanced")
        self.geometry("800x750")
        self.resizable(True, True)
        
        # Variables
        self.cracking = False
        self.crack_thread_instance = None
        
        # Style
        self.configure(bg='#f0f0f0')
        
        # Title
        title_frame = tk.Frame(self, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="🔓 Android Pattern Lock Cracker", 
                               font=("Arial", 20, "bold"), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Hash input section
        hash_frame = tk.LabelFrame(main_frame, text="Target Hash (SHA1)", 
                                   font=("Arial", 12, "bold"), bg='#f0f0f0', padx=10, pady=10)
        hash_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.hash_entry = tk.Entry(hash_frame, width=80, font=("Consolas", 10))
        self.hash_entry.pack(fill=tk.X, pady=5)
        
        # Button section
        btn_frame = tk.Frame(hash_frame, bg='#f0f0f0')
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Row 1 buttons
        btn_row1 = tk.Frame(btn_frame, bg='#f0f0f0')
        btn_row1.pack(pady=5)
        
        self.device_btn = tk.Button(btn_row1, text="📱 Read from Device", 
                                    command=self.read_from_device, bg="#2196F3", fg="white",
                                    font=("Arial", 10, "bold"), width=18, height=2)
        self.device_btn.pack(side=tk.LEFT, padx=5)
        
        self.test_btn = tk.Button(btn_row1, text="🎲 Generate Test Pattern", 
                                  command=self.generate_test, bg="#FF9800", fg="white",
                                  font=("Arial", 10, "bold"), width=18, height=2)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.crack_btn = tk.Button(btn_row1, text="🔥 CRACK PATTERN", 
                                   command=self.start_crack, bg="#f44336", fg="white",
                                   font=("Arial", 12, "bold"), width=18, height=2)
        self.crack_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 2 buttons
        btn_row2 = tk.Frame(btn_frame, bg='#f0f0f0')
        btn_row2.pack(pady=5)
        
        self.stop_btn = tk.Button(btn_row2, text="⏹️ Stop Cracking", 
                                  command=self.stop_crack, bg="#9E9E9E", fg="white",
                                  font=("Arial", 10, "bold"), width=18, height=2, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_row2, text="🗑️ Clear", 
                 command=self.clear_all, bg="#607D8B", fg="white",
                 font=("Arial", 10, "bold"), width=18, height=2).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(main_frame, textvariable=self.status_var, 
                                     font=("Arial", 11), bg='#f0f0f0', fg='blue')
        self.status_label.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Results area
        result_frame = tk.LabelFrame(main_frame, text="Results", 
                                     font=("Arial", 12, "bold"), bg='#f0f0f0')
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 15))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pattern visualization
        viz_frame = tk.LabelFrame(main_frame, text="Pattern Visualization", 
                                  font=("Arial", 12, "bold"), bg='#f0f0f0')
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(viz_frame, width=360, height=360, bg='white', 
                                highlightthickness=2, highlightbackground="#ccc")
        self.canvas.pack(pady=10)
        self.dots = []
        self.draw_grid()
        
        # Info label
        info_label = tk.Label(main_frame, 
                              text="💡 Tip: Use 'Generate Test Pattern' to test the cracker with a random pattern",
                              font=("Arial", 9), bg='#f0f0f0', fg='#666')
        info_label.pack(pady=5)
        
        # Close handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def draw_grid(self):
        """Draw the 3x3 pattern grid"""
        self.canvas.delete("all")
        self.dots.clear()
        for i in range(3):
            for j in range(3):
                x = 80 + j * 100
                y = 80 + i * 100
                dot = self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                             fill="#3498db", outline="#2980b9", width=2)
                # Add number label
                num = i*3 + j + 1
                self.canvas.create_text(x, y, text=str(num), fill="white", 
                                       font=("Arial", 12, "bold"))
                self.dots.append(dot)

    def read_from_device(self):
        """Read hash from connected Android device"""
        self.set_buttons_state(False)
        self.status_var.set("📱 Reading from device...")
        self.progress.start()
        self.result_text.delete(1.0, tk.END)
        
        threading.Thread(target=self.read_thread, daemon=True).start()

    def read_thread(self):
        hash_val, msg = read_gesture_key_improved()
        self.after(0, self.show_read_result, hash_val, msg)

    def show_read_result(self, hash_val, msg):
        self.progress.stop()
        self.result_text.insert(tk.END, msg + "\n")
        self.result_text.see(tk.END)
        
        if hash_val:
            self.hash_entry.delete(0, tk.END)
            self.hash_entry.insert(0, hash_val)
            self.status_var.set("✅ Hash loaded from device!")
        else:
            self.status_var.set("❌ Failed to read from device")
        
        self.set_buttons_state(True)

    def generate_test(self):
        """Generate a random test pattern and its hash"""
        self.result_text.delete(1.0, tk.END)
        self.canvas.delete("lines")
        self.draw_grid()
        
        pattern = generate_test_pattern()
        pattern_hash = pattern_to_hash(pattern)
        sequence = pattern_to_sequence(pattern)
        
        self.hash_entry.delete(0, tk.END)
        self.hash_entry.insert(0, pattern_hash)
        
        self.result_text.insert(tk.END, "🎲 TEST PATTERN GENERATED\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"Pattern: {pattern}\n")
        self.result_text.insert(tk.END, f"Sequence: {sequence}\n")
        self.result_text.insert(tk.END, f"Hash: {pattern_hash}\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, "✅ Click 'CRACK PATTERN' to find this pattern!\n")
        
        self.draw_pattern(pattern)
        self.status_var.set("🎲 Test pattern generated - Ready to crack!")

    def start_crack(self):
        """Start cracking the pattern"""
        target = self.hash_entry.get().strip().upper()
        if not target:
            messagebox.showwarning("Empty Hash", "Please enter a hash or generate a test pattern first!")
            return

        if self.cracking:
            messagebox.showwarning("Busy", "Cracking already in progress! Use 'Stop' if needed.")
            return

        self.cracking = True
        self.status_var.set("🔍 Cracking... This may take a few minutes")
        self.progress.start()
        self.result_text.delete(1.0, tk.END)
        self.canvas.delete("lines")
        self.set_buttons_state(False)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.result_text.insert(tk.END, "🔍 Starting pattern cracker...\n")
        self.result_text.insert(tk.END, f"Target hash: {target}\n")
        self.result_text.insert(tk.END, "Checking all possible patterns (4-9 points)...\n\n")
        
        self.crack_thread_instance = threading.Thread(target=self.crack_thread, args=(target,), daemon=True)
        self.crack_thread_instance.start()

    def crack_thread(self, target_hash):
        """Background cracking thread"""
        try:
            found = None
            count = 0
            total_est = 389112  # Total possible patterns
            
            for pattern in generate_patterns():
                if not self.cracking:  # Check if stopped
                    break
                    
                count += 1
                if count % 5000 == 0:
                    percent = (count / total_est) * 100
                    self.after(0, self.update_status, f"Checking pattern {count:,} / {total_est:,} ({percent:.1f}%)")
                
                if pattern_to_hash(pattern) == target_hash:
                    found = pattern
                    break

            self.after(0, self.show_result, found, count)
        except Exception as e:
            self.after(0, self.show_result, None, 0, str(e))

    def stop_crack(self):
        """Stop the cracking process"""
        if self.cracking:
            self.cracking = False
            self.status_var.set("⏹️ Stopping...")
            self.result_text.insert(tk.END, "\n⚠️ Stopping crack operation...\n")

    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)

    def show_result(self, pattern, count, error=None):
        """Display cracking results"""
        self.cracking = False
        self.progress.stop()
        self.set_buttons_state(True)
        self.stop_btn.config(state=tk.DISABLED)
        
        if error:
            self.status_var.set("❌ Error occurred")
            self.result_text.insert(tk.END, f"\n❌ Error: {error}\n")
            messagebox.showerror("Error", f"An error occurred:\n{error}")
        elif pattern:
            self.status_var.set("✅ Pattern found!")
            self.result_text.insert(tk.END, "\n" + "="*50 + "\n")
            self.result_text.insert(tk.END, "✅✅✅ PATTERN FOUND! ✅✅✅\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.result_text.insert(tk.END, f"Pattern: {pattern}\n")
            self.result_text.insert(tk.END, f"Sequence: {pattern_to_sequence(pattern)}\n")
            self.result_text.insert(tk.END, f"Total patterns checked: {count:,}\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.draw_pattern(pattern)
            messagebox.showinfo("Success!", f"Pattern found!\n\n{pattern}\n\nUnlock sequence: {pattern_to_sequence(pattern)}")
        else:
            if count > 0:
                self.status_var.set("❌ Pattern not found")
                self.result_text.insert(tk.END, f"\n❌ Pattern not found in {count:,} checked patterns.\n")
            else:
                self.status_var.set("❌ Cracking stopped")
                self.result_text.insert(tk.END, f"\n⚠️ Cracking stopped after {count:,} patterns.\n")

    def draw_pattern(self, pattern):
        """Draw the pattern on the canvas"""
        try:
            pts = []
            for r, c in pattern:
                x = 80 + c * 100
                y = 80 + r * 100
                pts.append((x, y))
                idx = r * 3 + c
                if 0 <= idx < len(self.dots):
                    self.canvas.itemconfig(self.dots[idx], fill="#e74c3c", outline="#c0392b")

            for i in range(len(pts)-1):
                self.canvas.create_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
                                       fill="#e74c3c", width=8, tags="lines", arrow=tk.LAST)
        except Exception as e:
            self.result_text.insert(tk.END, f"Warning: Could not draw pattern: {e}\n")

    def clear_all(self):
        """Clear all fields"""
        self.hash_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.canvas.delete("lines")
        self.draw_grid()
        self.status_var.set("Cleared - Ready")
        if not self.cracking:
            self.set_buttons_state(True)

    def set_buttons_state(self, enabled):
        """Enable/disable buttons"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.device_btn.config(state=state)
        self.test_btn.config(state=state)
        if not self.cracking:
            self.crack_btn.config(state=state)

    def on_closing(self):
        """Handle window closing"""
        if self.cracking:
            if messagebox.askokcancel("Exit", "Cracking in progress! Are you sure you want to exit?"):
                self.cracking = False
                self.destroy()
        else:
            if messagebox.askokcancel("Exit", "Do you want to close the Pattern Cracker?"):
                self.destroy()


if __name__ == "__main__":
    try:
        print("Starting Android Pattern Cracker...")
        print("="*50)
        print("Features:")
        print("• Test with random patterns (no device needed)")
        print("• Read from connected Android device (requires root for Android 8+)")
        print("• Crack any 4-9 point pattern")
        print("="*50)
        
        app = PatternCrackerGUI()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nProgram closed by user (Ctrl+C)")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")