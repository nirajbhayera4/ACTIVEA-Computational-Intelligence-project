
import random
import pandas as pd
import matplotlib.pyplot as plt

from src.genetic_algorithm import run_genetic_algorithm

# Reproduce the same experiment
random.seed(42)

activities = pd.read_csv("data/activities.csv")

profile = {
    "target_calories": 400,
    "met_range": (4, 7),
    "rpe_range": (4, 6),
    "hr_range": (64, 77),
    "desired_domains": ["CV", "ST", "ME", "FM"]
}

best_solution, best_fitness, history = run_genetic_algorithm(
    activities,
    profile,
    population_size=30,
    generations=50
)

# Plot best fitness across generations
plt.figure(figsize=(9, 5))
plt.plot(range(1, len(history) + 1), history, marker="o")

plt.title("Genetic Algorithm Fitness Progress")
plt.xlabel("Generation")
plt.ylabel("Best Fitness Score")
plt.grid(True)

plt.savefig("experiments/fitness_progress.png")
plt.show()

print("Graph saved successfully!")
