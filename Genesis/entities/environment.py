import random
import math

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.energy_value = 30.0

class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.speed = 1.5
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, width, height, target_boids):
        if not target_boids:
            return
            
        closest_dist = float('inf')
        closest_boid = None
        
        for boid in target_boids:
            if not boid.alive: continue
            dist = math.sqrt((self.x - boid.x)**2 + (self.y - boid.y)**2)
            if dist < closest_dist:
                closest_dist = dist
                closest_boid = boid
                
        if closest_boid:
            dx = closest_boid.x - self.x
            dy = closest_boid.y - self.y
            angle_to_target = math.atan2(dy, dx)
            
            self.angle_to_target = angle_to_target
            self.angle += (angle_to_target - self.angle) * 0.05
            
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        if self.x < 0: self.x += width
        if self.x > width: self.x -= width
        if self.y < 0: self.y += height
        if self.y > height: self.y -= height

class Environment:
    def __init__(self, width, height, food_count, predator_count):
        self.width = width
        self.height = height
        self.foods = []
        self.predators = []
        self.max_food = food_count
        
        for _ in range(food_count):
            self.spawn_food()
            
        for _ in range(predator_count):
            self.predators.append(Predator(random.randint(0, width), random.randint(0, height)))
            
    def spawn_food(self):
        self.foods.append(Food(random.randint(0, self.width), random.randint(0, self.height)))
        
    def step(self, boids):
        while len(self.foods) < self.max_food:
            self.spawn_food()
            
        for pred in self.predators:
            pred.update(self.width, self.height, boids)
            
        for boid in boids:
            if not boid.alive: continue
            
            foods_to_remove = []
            for food in self.foods:
                dist = math.sqrt((boid.x - food.x)**2 + (boid.y - food.y)**2)
                if dist < boid.radius + food.radius:
                    boid.energy = min(100.0, boid.energy + food.energy_value)
                    boid.fitness += 10.0 
                    foods_to_remove.append(food)
                    
            for f in foods_to_remove:
                if f in self.foods:
                    self.foods.remove(f)
                    
            for pred in self.predators:
                dist = math.sqrt((boid.x - pred.x)**2 + (boid.y - pred.y)**2)
                if dist < boid.radius + pred.radius:
                    boid.alive = False 
                    boid.fitness -= 5.0 
