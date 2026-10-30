
import random
import pandas as pd
import matplotlib.pyplot as plt

from src.genetic_algorithm import run_genetic_algorithm

random.seed(42)

activities = pd.read_csv("data/activities.csv")

profile = {
    "target_calories": 400,
    "met_range": (4, 7),
    "rpe_range": (4, 6),
    "hr_range": (64, 77),
    "desired_domains": ["CV", "ST", "ME", "FM"]
}

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
    range(1, 51),
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
    range(1, 51),
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
