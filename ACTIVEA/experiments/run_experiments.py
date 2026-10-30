
import random
import pandas as pd

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

results = []

for population_size in [20, 30, 50]:
    best_solution, best_fitness, history = run_genetic_algorithm(
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

df = pd.DataFrame(results)

df.to_csv("experiments/experiment_results.csv", index=False)

print("\nExperiment Results:")
print(df)
print("\nResults saved successfully!")
