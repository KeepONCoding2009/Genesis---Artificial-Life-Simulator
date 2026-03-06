import tkinter as tk
import random
import math
import time
from entities.boid import Boid
from entities.environment import Environment
from core.genetic_algo import GeneticAlgorithm

# Setup
WIDTH = 1000
HEIGHT = 700
FPS = 60
POPULATION_SIZE = 150
FOOD_COUNT = 80
PREDATOR_COUNT = 3
TARGET_FRAME_TIME = 1.0 / FPS

BG_COLOR = "#0f0f14"
FOOD_COLOR = "#00ff96"
PRED_COLOR = "#ff3232"
TEXT_COLOR = "#c8c8c8"

class GenesisSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Genesis - Artificial Life Simulator")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        
        self.ga = GeneticAlgorithm(POPULATION_SIZE)
        self.env = Environment(WIDTH, HEIGHT, FOOD_COUNT, PREDATOR_COUNT)
        
        self.boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(POPULATION_SIZE)]
        
        self.generation_frames = 0
        self.max_frames_per_gen = 60 * 15 
        
        self.best_fitness_history = []
        
        self.running = True
        
        self.stats_text = self.canvas.create_text(10, 10, anchor="nw", fill=TEXT_COLOR, font=("Arial", 14))
        
        self.update_loop()
        
    def reset_generation(self):
        new_brains = self.ga.next_generation(self.boids)
        best_fit = max(self.boids, key=lambda b: b.fitness).fitness
        self.best_fitness_history.append(best_fit)
        
        self.boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT), brain=brain) for brain in new_brains]
        self.generation_frames = 0
        self.env = Environment(WIDTH, HEIGHT, FOOD_COUNT, PREDATOR_COUNT)
        
    def update_loop(self):
        start_time = time.time()
        
        if not self.running:
            return
            
        self.env.step(self.boids)
        
        alive_count = 0
        for boid in self.boids:
            boid.think(self.env.foods, self.env.predators)
            boid.update(WIDTH, HEIGHT)
            if boid.alive:
                alive_count += 1
                
        self.generation_frames += 1
        
        if self.generation_frames >= self.max_frames_per_gen or alive_count == 0:
            self.reset_generation()
            
        self.canvas.delete("dynamic")
        
        for food in self.env.foods:
            self.canvas.create_oval(
                food.x - food.radius, food.y - food.radius, 
                food.x + food.radius, food.y + food.radius, 
                fill=FOOD_COLOR, outline="", tags="dynamic"
            )
            
        for pred in self.env.predators:
            self.canvas.create_oval(
                pred.x - pred.radius - 4, pred.y - pred.radius - 4, 
                pred.x + pred.radius + 4, pred.y + pred.radius + 4, 
                fill="", outline="#640000", width=2, tags="dynamic"
            )
            self.canvas.create_oval(
                pred.x - pred.radius, pred.y - pred.radius, 
                pred.x + pred.radius, pred.y + pred.radius, 
                fill=PRED_COLOR, outline="", tags="dynamic"
            )
            
        for boid in self.boids:
            if not boid.alive: continue
            
            front_x = boid.x + math.cos(boid.angle) * boid.radius * 2
            front_y = boid.y + math.sin(boid.angle) * boid.radius * 2
            left_x = boid.x + math.cos(boid.angle - 2.5) * boid.radius
            left_y = boid.y + math.sin(boid.angle - 2.5) * boid.radius
            right_x = boid.x + math.cos(boid.angle + 2.5) * boid.radius
            right_y = boid.y + math.sin(boid.angle + 2.5) * boid.radius
            
            color = boid.hex_color if boid.energy > 20 else "#505050"
            
            self.canvas.create_polygon(
                front_x, front_y, left_x, left_y, right_x, right_y,
                fill=color, outline="white", tags="dynamic"
            )
            
        text_str = f"Generation: {self.ga.generation}\nAlive: {alive_count}/{POPULATION_SIZE}\nTime Left: {(self.max_frames_per_gen - self.generation_frames) // 60}s"
        self.canvas.itemconfig(self.stats_text, text=text_str)
        
        elapsed = time.time() - start_time
        delay = max(1, int((TARGET_FRAME_TIME - elapsed) * 1000))
        self.root.after(delay, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    sim = GenesisSim(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
