import tkinter as tk
from tkinter import messagebox
import random
import math

class SpaceDefender:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Space Defender")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Game variables
        self.running = False
        self.score = 0
        self.lives = 3
        self.level = 1
        self.bullets = []
        self.enemies = []
        self.stars = []
        self.particles = []
        
        # Player ship
        self.player_x = 400
        self.player_y = 500
        self.player_speed = 5
        
        # Enemy spawn timer
        self.enemy_timer = 0
        
        # Bind keys
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.keys = set()
        
        # Create stars for background
        self.create_stars()
        
        # Start screen
        self.show_start_screen()
        
    def create_stars(self):
        """Create starry background"""
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            self.stars.append((x, y, size, f"#{brightness:02x}{brightness:02x}{brightness:02x}"))
    
    def show_start_screen(self):
        """Display start screen"""
        self.canvas.delete("all")
        
        # Draw stars
        for x, y, size, color in self.stars:
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            
        # Title
        self.canvas.create_text(400, 200, text="🚀 SPACE DEFENDER 🚀", 
                               fill="cyan", font=("Arial", 36, "bold"))
        self.canvas.create_text(400, 280, text="Defend Earth from alien invaders!", 
                               fill="white", font=("Arial", 18))
        self.canvas.create_text(400, 350, text="Controls:", 
                               fill="yellow", font=("Arial", 16, "bold"))
        self.canvas.create_text(400, 380, text="Arrow Keys: Move | Space: Shoot | P: Pause", 
                               fill="white", font=("Arial", 14))
        self.canvas.create_text(400, 450, text="Click START to begin", 
                               fill="lime", font=("Arial", 20, "bold"))
        
        # Start button
        self.start_btn = tk.Button(self.root, text="START GAME", 
                                  command=self.start_game, 
                                  font=("Arial", 16), bg="green", fg="white")
        self.start_btn.place(x=325, y=500)
        
    def show_game_over(self):
        """Display game over screen"""
        self.running = False
        
        # Game over text
        self.canvas.create_text(400, 250, text="GAME OVER", 
                               fill="red", font=("Arial", 48, "bold"))
        self.canvas.create_text(400, 320, text=f"Final Score: {self.score}", 
                               fill="white", font=("Arial", 24))
        
        # Restart button
        restart_btn = tk.Button(self.root, text="PLAY AGAIN", 
                               command=self.restart_game, 
                               font=("Arial", 16), bg="blue", fg="white")
        restart_btn.place(x=325, y=400)
        
    def start_game(self):
        """Start the game"""
        self.start_btn.place_forget()
        self.running = True
        self.score = 0
        self.lives = 3
        self.level = 1
        self.bullets = []
        self.enemies = []
        self.player_x = 400
        self.player_y = 500
        self.game_loop()
        
    def restart_game(self):
        """Restart the game"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] in ["PLAY AGAIN", "RESUME"]:
                widget.place_forget()
        self.start_game()
        
    def pause_game(self):
        """Pause the game"""
        self.running = False
        self.canvas.create_text(400, 300, text="PAUSED", 
                               fill="yellow", font=("Arial", 48, "bold"))
        resume_btn = tk.Button(self.root, text="RESUME", 
                              command=self.resume_game, 
                              font=("Arial", 16), bg="orange", fg="white")
        resume_btn.place(x=350, y=400)
        
    def resume_game(self):
        """Resume the game"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] == "RESUME":
                widget.place_forget()
        self.running = True
        self.game_loop()
        
    def key_press(self, event):
        """Handle key press"""
        self.keys.add(event.keysym)
        if event.keysym == "space" and self.running:
            self.shoot()
        elif event.keysym == "p" and self.running:
            self.pause_game()
            
    def key_release(self, event):
        """Handle key release"""
        self.keys.discard(event.keysym)
        
    def shoot(self):
        """Player shoots a bullet"""
        self.bullets.append([self.player_x, self.player_y - 20, 0, -10])  # x, y, vx, vy
        
    def update_player(self):
        """Update player position based on key presses"""
        if "Left" in self.keys or "a" in self.keys:
            self.player_x = max(20, self.player_x - self.player_speed)
        if "Right" in self.keys or "d" in self.keys:
            self.player_x = min(780, self.player_x + self.player_speed)
        if "Up" in self.keys or "w" in self.keys:
            self.player_y = max(20, self.player_y - self.player_speed)
        if "Down" in self.keys or "s" in self.keys:
            self.player_y = min(580, self.player_y + self.player_speed)
            
    def update_bullets(self):
        """Update bullet positions"""
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2]  # x += vx
            bullet[1] += bullet[3]  # y += vy
            
            # Remove bullets that go off screen
            if bullet[1] < 0 or bullet[1] > 600 or bullet[0] < 0 or bullet[0] > 800:
                self.bullets.remove(bullet)
                
    def update_enemies(self):
        """Update enemy positions"""
        self.enemy_timer += 1
        
        # Spawn new enemies
        if self.enemy_timer > 30:  # Spawn every 30 frames
            self.enemies.append([
                random.randint(30, 770),  # x
                -20,                      # y
                random.uniform(-1, 1),    # vx
                random.uniform(1, 3)      # vy
            ])
            self.enemy_timer = 0
            
        # Move enemies
        for enemy in self.enemies[:]:
            enemy[0] += enemy[2]  # x += vx
            enemy[1] += enemy[3]  # y += vy
            
            # Remove enemies that go off screen
            if enemy[1] > 620:
                self.enemies.remove(enemy)
                
    def check_collisions(self):
        """Check for collisions"""
        # Bullet-enemy collisions
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (abs(bullet[0] - enemy[0]) < 20 and 
                    abs(bullet[1] - enemy[1]) < 20):
                    # Collision detected
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    
                    # Create explosion particles
                    for _ in range(10):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(1, 3)
                        vx = math.cos(angle) * speed
                        vy = math.sin(angle) * speed
                        self.particles.append([enemy[0], enemy[1], vx, vy, 30])
                    break
                    
        # Player-enemy collisions
        for enemy in self.enemies[:]:
            if (abs(self.player_x - enemy[0]) < 25 and 
                abs(self.player_y - enemy[1]) < 25):
                self.enemies.remove(enemy)
                self.lives -= 1
                
                # Create explosion particles
                for _ in range(20):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 4)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    self.particles.append([self.player_x, self.player_y, vx, vy, 40])
                    
                if self.lives <= 0:
                    self.show_game_over()
                    
    def update_particles(self):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle[0] += particle[2]  # x += vx
            particle[1] += particle[3]  # y += vy
            particle[4] -= 1             # lifetime
            
            if particle[4] <= 0:
                self.particles.remove(particle)
                
    def draw_game(self):
        """Draw all game elements"""
        self.canvas.delete("all")
        
        # Draw stars
        for x, y, size, color in self.stars:
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            
        # Draw particles
        for x, y, vx, vy, life in self.particles:
            color = f"#{int(255*(life/30)):02x}{int(100*(life/30)):02x}00"
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color, outline="")
            
        # Draw player ship
        self.canvas.create_polygon(
            self.player_x, self.player_y-15,
            self.player_x-15, self.player_y+15,
            self.player_x+15, self.player_y+15,
            fill="blue", outline="cyan", width=2
        )
        self.canvas.create_oval(
            self.player_x-5, self.player_y-5,
            self.player_x+5, self.player_y+5,
            fill="cyan"
        )
        
        # Draw bullets
        for bullet in self.bullets:
            self.canvas.create_oval(
                bullet[0]-3, bullet[1]-3,
                bullet[0]+3, bullet[1]+3,
                fill="yellow", outline="orange"
            )
            
        # Draw enemies
        for enemy in self.enemies:
            self.canvas.create_oval(
                enemy[0]-15, enemy[1]-15,
                enemy[0]+15, enemy[1]+15,
                fill="red", outline="darkred", width=2
            )
            self.canvas.create_oval(
                enemy[0]-5, enemy[1]-5,
                enemy[0]+5, enemy[1]+5,
                fill="orange"
            )
            
        # Draw UI
        self.canvas.create_text(100, 30, text=f"Score: {self.score}", 
                               fill="white", font=("Arial", 16))
        self.canvas.create_text(700, 30, text=f"Lives: {self.lives}", 
                               fill="white", font=("Arial", 16))
        self.canvas.create_text(400, 30, text=f"Level: {self.level}", 
                               fill="white", font=("Arial", 16))
                               
    def game_loop(self):
        """Main game loop"""
        if not self.running:
            return
            
        self.update_player()
        self.update_bullets()
        self.update_enemies()
        self.check_collisions()
        self.update_particles()
        self.draw_game()
        
        # Increase level every 100 points
        self.level = max(1, self.score // 100 + 1)
        
        # Continue game loop
        self.root.after(16, self.game_loop)  # ~60 FPS
        
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    game = SpaceDefender()
    game.run()
