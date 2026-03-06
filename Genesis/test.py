import tkinter as tk
from main import GenesisSim
import time

try:
    root = tk.Tk()
    sim = GenesisSim(root)
    for i in range(500):
        sim.env.step(sim.boids)
        for boid in sim.boids:
            boid.think(sim.env.foods, sim.env.predators)
            boid.update(1000, 700)
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
