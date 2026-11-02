
import random
import pandas as pd

from src.genetic_algorithm import run_genetic_algorithm
from experiments.config import load_activities, load_default_profile

random.seed(42)

# Load shared configuration
activities = load_activities()
profile = load_default_profile()

results = []

# Test different population sizes
for population_size in [20, 30, 50]:

    best_solution, best_fitness, history, diversity_history = run_genetic_algorithm(
        activities,
        profile,
        population_size=population_size,
        generations=50
    )

    results.append({
        "population_size": population_size,
        "generations": 50,
        "best_fitness": best_fitness,
        "total_duration": sum(best_solution)
    })

# Convert results into a DataFrame
df = pd.DataFrame(results)

# Save results
df.to_csv("experiments/experiment_results.csv", index=False)

print("\nExperiment Results:")
print(df)
print("\nResults saved successfully!")
