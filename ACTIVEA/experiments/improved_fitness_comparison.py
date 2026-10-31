import random
import pandas as pd

from src.genetic_algorithm import run_genetic_algorithm
from src.fitness import (
    calculate_fitness,
    calculate_improved_fitness
)

activities = pd.read_csv("data/activities.csv")
profiles = pd.read_csv("data/training_data.csv")

SEEDS = [10, 20, 30, 40, 50]
results = []

for _, row in profiles.iterrows():

    profile = {
        "target_calories": row["target_calories"],
        "met_range": (row["met_min"], row["met_max"]),
        "rpe_range": (row["rpe_min"], row["rpe_max"]),
        "hr_range": (row["hr_min"], row["hr_max"]),
        "desired_domains": str(row["desired_domains"]).split(";")
    }

    for seed in SEEDS:

        for name, fitness_function in [
            ("Original GA", calculate_fitness),
            ("Improved GA", calculate_improved_fitness)
        ]:

            random.seed(seed)

            best, fitness, history, diversity = (
                run_genetic_algorithm(
                    activities,
                    profile,
                    population_size=50,
                    generations=50,
                    fitness_function=fitness_function
                )
            )

            details = fitness_function(best, activities, profile)

            results.append({
                "profile": row["profile_id"],
                "seed": seed,
                "algorithm": name,
                "fitness": fitness,
                "domain_coverage": details["domain_score"],
                "domain_penalty": details.get("domain_penalty", 0),
                "calories": details["calories"],
                "duration": sum(best)
            })

df = pd.DataFrame(results)

df.to_csv(
    "experiments/improved_fitness_results.csv",
    index=False
)

summary = df.groupby("algorithm").agg({
    "fitness": ["mean", "std"],
    "domain_coverage": "mean",
    "domain_penalty": "mean",
    "calories": "mean",
    "duration": "mean"
})

print("\nTASK 8: FITNESS FUNCTION COMPARISON")
print(summary)

summary.to_csv(
    "experiments/improved_fitness_summary.csv"
)

print("\nResults saved successfully.")