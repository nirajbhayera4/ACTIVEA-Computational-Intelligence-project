import random
import pandas as pd

from src.dataset import load_profiles

from src.genetic_algorithm import run_genetic_algorithm
from src.genetic_algorithm_adaptive import run_adaptive_genetic_algorithm


def run_comparison():
    

    activities = pd.read_csv("data/activities.csv")
    profiles = load_profiles("data/training_data.csv")

    seeds = [10, 20, 30, 40, 50]
    results = []

    for profile in profiles:

        for seed in seeds:

            # Original GA
            random.seed(seed)

            best, fitness, history, diversity = run_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                crossover_rate=0.8,
                mutation_rate=0.1,
                diversity_preservation=True
            )

            results.append({
                "profile": profile["profile_id"],
                "algorithm": "Original Mutation",
                "seed": seed,
                "fitness": fitness,
                "final_diversity": diversity[-1]
            })

            # Modified GA
            random.seed(seed)

            best, fitness, history, diversity = run_adaptive_genetic_algorithm(
                activities,
                profile,
                population_size=50,
                generations=50,
                crossover_rate=0.8,
                mutation_rate=0.1,
                diversity_preservation=True
            )

            results.append({
                "profile": profile["profile_id"],
                "algorithm": "Two-Scale Mutation",
                "seed": seed,
                "fitness": fitness,
                "final_diversity": diversity[-1]
            })

    df = pd.DataFrame(results)

    df.to_csv(
        "experiments/mutation_comparison_results.csv",
        index=False
    )

    summary = df.groupby("algorithm").agg({
        "fitness": ["mean", "std"],
        "final_diversity": "mean"
    })

    print("\nMutation Comparison Summary:")
    print(summary)

    summary.to_csv("experiments/mutation_comparison_summary.csv")


if __name__ == "__main__":
    run_comparison()