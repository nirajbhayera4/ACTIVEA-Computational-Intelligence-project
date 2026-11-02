
import random
import matplotlib.pyplot as plt

from src.genetic_algorithm import run_genetic_algorithm
from experiments.config import load_activities, load_default_profile

# Reproduce the same experiment
random.seed(42)

activities = load_activities()
profile = load_default_profile()

best_solution, best_fitness, history, diversity_history = run_genetic_algorithm(
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
