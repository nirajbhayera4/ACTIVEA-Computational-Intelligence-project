
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

seeds = [10, 20, 30, 40, 50]
results = []

for seed in seeds:
    random.seed(seed)

    best_solution, best_fitness, history = run_genetic_algorithm(
        activities,
        profile,
        population_size=50,
        generations=50,
        crossover_rate=0.80,
        mutation_rate=0.10
    )

    results.append({
        "seed": seed,
        "best_fitness": best_fitness,
        "total_duration": sum(best_solution)
    })

df = pd.DataFrame(results)

df.to_csv("experiments/repeated_run_results.csv", index=False)

print("\nIndividual Run Results:")
print(df)

print("\nStatistical Summary:")
print("Average fitness:", df["best_fitness"].mean())
print("Standard deviation:", df["best_fitness"].std())
print("Highest fitness:", df["best_fitness"].max())
print("Lowest fitness:", df["best_fitness"].min())

print("\nResults saved successfully!")
