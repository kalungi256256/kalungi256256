import tkinter as tk
import random
import math

class FloatingDecoration:
    def __init__(self, canvas, symbol, start_x, start_y):
        self.canvas = canvas
        self.symbol = symbol
        self.x = start_x
        self.y = start_y
        self.size = random.randint(20, 40)
        self.speed_y = random.uniform(1, 3)  # Falling speed
        self.speed_x = random.uniform(-1, 1)  # Horizontal drift
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        
        self.text_id = self.canvas.create_text(
            self.x, self.y, text=self.symbol, font=("Arial", self.size),
            fill=self.get_color()
        )
    
    def get_color(self):
        colors = ["#FF1493", "#FFB6C1", "#FF69B4", "#FF6B9D", "#FFC0CB", "#FF4500"]
        return random.choice(colors)
    
    def update(self):
        self.y += self.speed_y  # Fall down
        self.x += self.speed_x  # Drift horizontally
        self.rotation += self.rotation_speed
        
        self.canvas.coords(self.text_id, self.x, self.y)
        
        # Check if off-screen
        if self.y > 600:
            self.canvas.delete(self.text_id)
            return False
        return True

class LoveAnimation:
    def __init__(self, root, lover_name):
        self.root = root
        self.lover_name = lover_name
        self.root.title("💖 Forever in Love 💖")
        self.root.geometry("800x600")
        self.root.config(bg="black")
        
        # Create canvas with gradient-like background
        self.canvas = tk.Canvas(root, bg="#1a0f2e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Text IDs for animation
        self.main_text_id = None
        self.secondary_text_id = None
        self.decorative_text_id = None
        
        # Animation variables
        self.time = 0
        
        # List to store floating decorations
        self.decorations = []
        
        # Start animation
        self.animate()
    
    def update_messages(self):
        # Calculate positions with wave/floating effect
        wave_offset = math.sin(self.time * 0.05) * 30
        vertical_bob = math.cos(self.time * 0.03) * 20
        
        main_x = 400 + wave_offset
        main_y = 100 + vertical_bob
        
        secondary_x = 400 + math.sin(self.time * 0.04) * 25
        secondary_y = 150 + math.cos(self.time * 0.035) * 15
        
        decorative_x = 400 + math.sin(self.time * 0.06) * 40
        decorative_y = 200 + math.cos(self.time * 0.04) * 25
        
        # Delete old text
        if self.main_text_id:
            self.canvas.delete(self.main_text_id)
        if self.secondary_text_id:
            self.canvas.delete(self.secondary_text_id)
        if self.decorative_text_id:
            self.canvas.delete(self.decorative_text_id)
        
        # Create new animated text
        self.main_text_id = self.canvas.create_text(
            main_x, main_y, text=f"Shoni is in love with {self.lover_name}",
            font=("Arial", 28, "bold"), fill="#FF1493", anchor="center"
        )
        
        self.secondary_text_id = self.canvas.create_text(
            secondary_x, secondary_y, text=f"Shoni will always cherish {self.lover_name} forever and ever!",
            font=("Arial", 18, "italic"), fill="#FFB6C1", anchor="center"
        )
        
        self.decorative_text_id = self.canvas.create_text(
            decorative_x, decorative_y, text="💖 ✨ 🌹 ✨ 💖",
            font=("Arial", 24), fill="#FF69B4", anchor="center"
        )
    
    def spawn_decoration(self):
        # Random starting position across the top
        start_x = random.randint(50, 750)
        symbols = ["❤️", "💖", "💕", "🌹", "🌸", "🌺", "🌻", "✨", "🦋", "💐"]
        symbol = random.choice(symbols)
        
        decoration = FloatingDecoration(self.canvas, symbol, start_x, 0)
        self.decorations.append(decoration)
    
    def animate(self):
        # Update time counter
        self.time += 1
        
        # Update message positions with animation
        self.update_messages()
        
        # Spawn new decorations randomly
        if random.random() < 0.3:  # 30% chance each frame
            self.spawn_decoration()
        
        # Update all decorations
        self.decorations = [d for d in self.decorations if d.update()]
        
        # Continue animation
        self.root.after(30, self.animate)

def shoni(lover):
    root = tk.Tk()
    animation = LoveAnimation(root, lover)
    root.mainloop()

# Run the animation
shoni("Kalungi")