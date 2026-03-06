import random
import math
from core.neural_net import NeuralNetwork

class Boid:
    TOPOLOGY = [5, 8, 2] 
    
    def __init__(self, x, y, brain=None):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.base_speed = 3.0
        self.speed = self.base_speed
        
        self.radius = 6
        self.energy = 100.0
        self.alive = True
        self.fitness = 0.0
        
        if brain:
            self.brain = brain
        else:
            self.brain = NeuralNetwork(self.TOPOLOGY)
            
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.hex_color = '#%02x%02x%02x' % self.color
        
    def get_distance_and_angle(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_target = math.atan2(dy, dx)
        
        relative_angle = angle_to_target - self.angle
        relative_angle = (relative_angle + math.pi) % (2 * math.pi) - math.pi
        
        return dist, relative_angle
        
    def find_closest(self, items):
        if not items:
            return -1, 0
            
        closest_dist = float('inf')
        closest_angle = 0
        
        for item in items:
            if not getattr(item, 'alive', True): continue
            
            dist, angle = self.get_distance_and_angle(item.x, item.y)
            if dist < closest_dist:
                closest_dist = dist
                closest_angle = angle
                
        if closest_dist == float('inf'):
            return -1, 0
            
        return closest_dist, closest_angle
        
    def think(self, foods, predators):
        if not self.alive:
            return
            
        food_dist, food_angle = self.find_closest(foods)
        pred_dist, pred_angle = self.find_closest(predators)
        
        max_dist = 1000.0
        norm_food_dist = 1.0 if food_dist == -1 else food_dist / max_dist
        norm_food_angle = food_angle / math.pi
        
        norm_pred_dist = 1.0 if pred_dist == -1 else pred_dist / max_dist
        norm_pred_angle = pred_angle / math.pi
        
        norm_energy = self.energy / 100.0
        
        inputs = [norm_food_dist, norm_food_angle, norm_pred_dist, norm_pred_angle, norm_energy]
        
        outputs = self.brain.predict(inputs)
        
        thrust = outputs[0]
        steering = outputs[1]
        
        self.angle += steering * 0.1
        self.speed = self.base_speed + (thrust * 2.0)
        self.speed = max(0.5, self.speed)
        
    def update(self, width, height):
        if not self.alive:
            return
            
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        self.energy -= 0.1 + (abs(self.speed - self.base_speed) * 0.05)
        
        if self.energy <= 0:
            self.alive = False
            
        if self.x < 0: self.x += width
        if self.x > width: self.x -= width
        if self.y < 0: self.y += height
        if self.y > height: self.y -= height
        
        self.fitness += 0.01

