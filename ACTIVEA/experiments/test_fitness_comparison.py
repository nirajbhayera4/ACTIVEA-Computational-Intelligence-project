
import random
import pandas as pd

from experiments.config import load_activities
from src.dataset import load_profiles
from src.genetic_algorithm import run_genetic_algorithm
from src.fitness import (
    calculate_fitness,
    calculate_improved_fitness
)


# Load activities and testing profiles
activities = load_activities()
testing_profiles = load_profiles("data/testing_data.csv")

SEEDS = [10, 20, 30, 40, 50]
results = []


for profile in testing_profiles:

    print("\nTesting profile:", profile["profile_id"])

    for seed in SEEDS:

        for name, fitness_function in [
            ("Original GA", calculate_fitness),
            ("Improved GA", calculate_improved_fitness)
        ]:

            # Use the same seed for a fair comparison
            random.seed(seed)

            best, fitness, history, diversity = run_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                crossover_rate=0.8,
                mutation_rate=0.1,
                fitness_function=fitness_function
            )

            # Evaluate the selected workout
            details = fitness_function(best, activities, profile)

            # Evaluate preference metrics consistently
            preference_details = calculate_improved_fitness(
                best, activities, profile
            )

            results.append({
                "profile": profile["profile_id"],
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
                "calories": details["calories"],
                "duration": sum(best)
            })


# Save detailed results
df = pd.DataFrame(results)

df.to_csv(
    "experiments/testing_fitness_comparison_results.csv",
    index=False
)


# Calculate summary statistics for each profile and algorithm
summary = df.groupby(["profile", "algorithm"]).agg({
    "fitness": ["mean", "std"],
    "domain_coverage": "mean",
    "missing_domain_penalty": "mean",
    "unsuitable_activity_penalty": "mean",
    "combined_penalty": "mean",
    "calories": "mean",
    "duration": "mean"
})


print("\nTASK 8: TESTING DATA COMPARISON")
print(summary)


# Save summary
summary.to_csv(
    "experiments/testing_fitness_comparison_summary.csv"
)

print("\nTesting comparison completed!")
print("Detailed results saved successfully!")
print("Summary saved successfully!")
