
import random
import pandas as pd

from src.genetic_algorithm import run_genetic_algorithm

activities = pd.read_csv("data/activities.csv")

profile = {
    "target_calories": 400,
    "met_range": (4, 7),
    "rpe_range": (4, 6),
    "hr_range": (64, 77),
    "desired_domains": ["CV", "ST", "ME", "FM"]
}

mutation_rates = [0.05, 0.10, 0.20, 0.30]
results = []

for rate in mutation_rates:
    random.seed(42)

    best_solution, best_fitness, history = run_genetic_algorithm(
        activities,
        profile,
        population_size=50,
        generations=50,
        crossover_rate=0.8,
        mutation_rate=rate
    )

    results.append({
        "mutation_rate": rate,
        "best_fitness": best_fitness,
        "total_duration": sum(best_solution)
    })

df = pd.DataFrame(results)

df.to_csv("experiments/mutation_results.csv", index=False)

print("\nMutation Experiment Results:")
print(df)

print("\nResults saved successfully!")
