import tkinter as tk
from tkinter import messagebox
import random

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")
        self.root.geometry("700x900")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, bg="skyblue", highlightthickness=0, width=700, height=900)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.score = 0
        self.game_over = False
        self.bird_y = 300
        self.bird_x = 50
        self.velocity = 0
        self.gravity = 0.4  # Reduced gravity for slower falling
        self.pipe_gap = 200
        self.pipes = []
        
        self.score_text = self.canvas.create_text(20, 20, text=f"Score: {self.score}", font=("Arial", 16), fill="black", anchor="nw")
        self.bird = self.canvas.create_oval(self.bird_x, self.bird_y, self.bird_x + 20, self.bird_y + 20, fill="yellow")
        
        self.root.bind("<space>", self.flap)
        self.root.bind("<Button-1>", self.flap)
        
        self.spawn_pipe()
        self.update()
    
    def flap(self, event=None):
        if not self.game_over:
            self.velocity = -10
    
    def spawn_pipe(self):
        pipe_x = 400
        gap_start = random.randint(50, 450)
        self.pipes.append({"x": pipe_x, "gap_start": gap_start})
    
    def update(self):
        if self.game_over:
            return
        
        # Physics
        self.velocity += self.gravity
        self.bird_y += self.velocity
        self.canvas.coords(self.bird, self.bird_x, self.bird_y, self.bird_x + 20, self.bird_y + 20)
        
        # Boundaries
        if self.bird_y > 580 or self.bird_y < 0:
            self.end_game()
        
        # Update pipes
        for pipe in self.pipes[:]:
            pipe["x"] -= 2  # Reduced pipe speed for slower gameplay
            
            # Check collision
            if self.bird_x + 20 > pipe["x"] and self.bird_x < pipe["x"] + 50:
                if self.bird_y < pipe["gap_start"] or self.bird_y + 20 > pipe["gap_start"] + self.pipe_gap:
                    self.end_game()
            
            # Score
            if pipe["x"] == self.bird_x:
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            
            # Remove off-screen pipes
            if pipe["x"] < -50:
                self.pipes.remove(pipe)
                self.spawn_pipe()
        
        # Draw pipes
        self.canvas.delete("pipe")
        for pipe in self.pipes:
            self.canvas.create_rectangle(pipe["x"], 0, pipe["x"] + 50, pipe["gap_start"], fill="green", tags="pipe")
            self.canvas.create_rectangle(pipe["x"], pipe["gap_start"] + self.pipe_gap, pipe["x"] + 50, 600, fill="green", tags="pipe")
        
        self.root.after(60, self.update)  # Increased delay (60ms) for slower game loop
    
    def end_game(self):
        self.game_over = True
        messagebox.showinfo("Game Over", f"Final Score: {self.score}\n\nPress OK to restart")
        self.reset()
    
    def reset(self):
        self.score = 0
        self.bird_y = 300
        self.velocity = 0
        self.game_over = False
        self.pipes = []
        self.canvas.delete("pipe")
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.spawn_pipe()
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBirdGame(root)
    root.mainloop()