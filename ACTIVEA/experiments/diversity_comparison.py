
import random
import pandas as pd

from src.dataset import load_profiles
from src.genetic_algorithm import run_genetic_algorithm

# Load activities and training profiles
activities = pd.read_csv("data/activities.csv")
profiles = load_profiles("data/training_data.csv")

results = []

# Use multiple random seeds for reliable comparison
seeds = [10, 20, 30, 40, 50]

for profile in profiles:

    print("\nPROFILE:", profile["profile_id"])

    for seed in seeds:

        # Run original GA without random immigrants
        random.seed(seed)

        original_best, original_fitness, original_history, original_diversity = (
            run_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                crossover_rate=0.8,
                mutation_rate=0.1,
                diversity_preservation=False
            )
        )

        results.append({
            "profile_id": profile["profile_id"],
            "seed": seed,
            "algorithm": "Original GA",
            "best_fitness": original_fitness,
            "average_diversity": sum(original_diversity) / len(original_diversity),
            "final_diversity": original_diversity[-1]
        })

        # Run enhanced GA with random immigrants
        random.seed(seed)

        enhanced_best, enhanced_fitness, enhanced_history, enhanced_diversity = (
            run_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                crossover_rate=0.8,
                mutation_rate=0.1,
                diversity_preservation=True
            )
        )

        results.append({
            "profile_id": profile["profile_id"],
            "seed": seed,
            "algorithm": "Enhanced GA",
            "best_fitness": enhanced_fitness,
            "average_diversity": sum(enhanced_diversity) / len(enhanced_diversity),
            "final_diversity": enhanced_diversity[-1]
        })

# Save detailed results
results_df = pd.DataFrame(results)

results_df.to_csv(
    "experiments/diversity_comparison_results.csv",
    index=False
)

# Calculate average performance for each algorithm
summary = results_df.groupby("algorithm")[
    ["best_fitness", "average_diversity", "final_diversity"]
].mean()

print("\nDIVERSITY COMPARISON SUMMARY")
print(summary)

summary.to_csv("experiments/diversity_comparison_summary.csv")

print("\nComparison completed!")
