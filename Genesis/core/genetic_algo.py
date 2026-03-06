import random

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate=0.1, mutation_strength=0.5):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.generation = 1
        
    def next_generation(self, boids):
        if not boids:
            return []
            
        boids.sort(key=lambda b: b.fitness, reverse=True)
        
        survivors_count = max(2, self.population_size // 2)
        survivors = boids[:survivors_count]
        
        new_population_brains = []
        
        best_brain = survivors[0].brain
        
        for i in range(self.population_size):
            parent_a = random.choice(survivors)
            parent_b = random.choice(survivors)
            
            child_brain = parent_a.brain.crossover(parent_b.brain)
            
            if i != 0:
                child_brain.mutate(self.mutation_rate, self.mutation_strength)
                
            new_population_brains.append(child_brain)
            
        self.generation += 1
        return new_population_brains
