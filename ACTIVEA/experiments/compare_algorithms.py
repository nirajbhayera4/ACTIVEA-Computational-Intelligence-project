
import random
import pandas as pd

from src.genetic_algorithm import run_genetic_algorithm
from src.particle_swarm import run_particle_swarm
from src.dataset import load_profiles
from src.fitness import calculate_calories

# Load the same activities for both algorithms
activities = pd.read_csv("data/activities.csv")

training_profiles = load_profiles("data/training_data.csv")
testing_profiles = load_profiles("data/testing_data.csv")

seeds = [10, 20, 30, 40, 50]

results = []

datasets = [
    ("Training", training_profiles),
    ("Testing", testing_profiles)
]

for dataset_name, profiles in datasets:

    for profile in profiles:

        for seed in seeds:

            # Run Genetic Algorithm
            random.seed(seed)

            ga_solution, ga_score, _, _ = run_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                crossover_rate=0.8,
                mutation_rate=0.1,
                diversity_preservation=True
            )

            results.append({
                "dataset": dataset_name,
                "profile_id": profile["profile_id"],
                "algorithm": "Enhanced GA",
                "seed": seed,
                "best_fitness": ga_score,
                "duration": sum(ga_solution),
                "calories": calculate_calories(ga_solution, activities)
            })

            # Run Particle Swarm Optimization
            random.seed(seed)

            pso_solution, pso_score, _ = run_particle_swarm(
                activities,
                profile,
                swarm_size=50,
                iterations=50
            )

            results.append({
                "dataset": dataset_name,
                "profile_id": profile["profile_id"],
                "algorithm": "PSO",
                "seed": seed,
                "best_fitness": pso_score,
                "duration": sum(pso_solution),
                "calories": calculate_calories(pso_solution, activities)
            })

# Save individual experiment results
df = pd.DataFrame(results)
df.to_csv("experiments/algorithm_comparison_results.csv", index=False)

# Calculate average results for each algorithm and dataset
summary = df.groupby(
    ["dataset", "algorithm"]
).agg(
    average_fitness=("best_fitness", "mean"),
    average_duration=("duration", "mean"),
    average_calories=("calories", "mean")
).reset_index()

summary.to_csv(
    "experiments/algorithm_comparison_summary.csv",
    index=False
)

print("\nALGORITHM COMPARISON SUMMARY")
print(summary.to_string(index=False))

print("\nComparison completed successfully!")
