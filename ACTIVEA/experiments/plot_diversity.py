
import random
import matplotlib.pyplot as plt

from src.genetic_algorithm import run_genetic_algorithm
from experiments.config import load_activities, load_default_profile

random.seed(42)

# Load shared configuration
activities = load_activities()
profile = load_default_profile()

best_solution, best_fitness, fitness_history, diversity_history = (
    run_genetic_algorithm(
        activities,
        profile,
        population_size=30,
        generations=50,
        crossover_rate=0.8,
        mutation_rate=0.1
    )
)

# Create two graphs
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Fitness graph
axes[0].plot(
    range(1, len(fitness_history) + 1),
    fitness_history,
    marker="o",
    markersize=3
)
axes[0].set_title("Best Fitness Across Generations")
axes[0].set_xlabel("Generation")
axes[0].set_ylabel("Best Fitness")
axes[0].grid(True)

# Diversity graph
axes[1].plot(
    range(1, len(diversity_history) + 1),
    diversity_history,
    marker="o",
    markersize=3
)
axes[1].set_title("Population Diversity Across Generations")
axes[1].set_xlabel("Generation")
axes[1].set_ylabel("Diversity")
axes[1].grid(True)

plt.tight_layout()

plt.savefig("experiments/fitness_diversity.png")
plt.show()

print("Graphs saved successfully!")
print("Best Fitness:", best_fitness)
