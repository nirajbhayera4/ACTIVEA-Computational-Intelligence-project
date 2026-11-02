
import random
import pandas as pd

from src.genetic_algorithm import run_genetic_algorithm
from src.fitness import (
    calculate_fitness,
    calculate_improved_fitness
)
from experiments.config import load_activities


# Load activities and training profiles
activities = load_activities()
profiles = pd.read_csv("data/training_data.csv")

SEEDS = [10, 20, 30, 40, 50]
results = []


for _, row in profiles.iterrows():

    profile = {
        "target_calories": row["target_calories"],
        "met_range": (row["met_min"], row["met_max"]),
        "rpe_range": (row["rpe_min"], row["rpe_max"]),
        "hr_range": (row["hr_min"], row["hr_max"]),
        "desired_domains": [
            domain.strip()
            for domain in str(row["desired_domains"]).split(";")
        ]
    }

    for seed in SEEDS:

        for name, fitness_function in [
            ("Original GA", calculate_fitness),
            ("Improved GA", calculate_improved_fitness)
        ]:

            random.seed(seed)

            best, fitness, history, diversity = run_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                fitness_function=fitness_function
            )

            # Evaluate the selected chromosome
            details = fitness_function(
                best, activities, profile
            )

            # Calculate preference metrics consistently
            # for both original and improved algorithms
            preference_details = calculate_improved_fitness(
                best, activities, profile
            )

            results.append({
                "profile": row["profile_id"],
                "seed": seed,
                "algorithm": name,
                "fitness": fitness,
                "domain_coverage": preference_details["domain_coverage"],
                "missing_domain_penalty": preference_details[
                    "domain_penalty"
                ],
                "unsuitable_activity_penalty": preference_details[
                    "unsuitable_activity_penalty"
                ],
                "combined_penalty": preference_details[
                    "combined_penalty"
                ],
                "unsuitable_duration": preference_details[
                    "unsuitable_duration"
                ],
                "calories": details["calories"],
                "duration": sum(best)
            })


# Save detailed experimental results
df = pd.DataFrame(results)

df.to_csv(
    "experiments/improved_fitness_results.csv",
    index=False
)


# Calculate summary statistics
summary = df.groupby("algorithm").agg({
    "fitness": ["mean", "std"],
    "domain_coverage": "mean",
    "missing_domain_penalty": "mean",
    "unsuitable_activity_penalty": "mean",
    "combined_penalty": "mean",
    "calories": "mean",
    "duration": "mean"
})


print("\nTASK 8: FITNESS FUNCTION COMPARISON")
print(summary)


# Save summary results
summary.to_csv(
    "experiments/improved_fitness_summary.csv"
)

print("\nResults saved successfully!")
