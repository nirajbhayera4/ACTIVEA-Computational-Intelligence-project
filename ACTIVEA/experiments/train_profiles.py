
import random
import pandas as pd

from src.dataset import load_profiles
from src.genetic_algorithm import run_genetic_algorithm
from src.fitness import calculate_fitness

# Load activity catalogue and training profiles
activities = pd.read_csv("data/activities.csv")
training_profiles = load_profiles("data/training_data.csv")

results = []

# Run the GA separately for each training profile
for profile in training_profiles:

    print("\nProcessing profile:", profile["profile_id"])

    random.seed(42)

    best_solution, best_fitness, history, diversity_history = (
        run_genetic_algorithm(
            activities,
            profile,
            population_size=50,
            generations=50,
            crossover_rate=0.8,
            mutation_rate=0.1
        )
    )

    # Calculate detailed fitness results
    details = calculate_fitness(
        best_solution,
        activities,
        profile
    )

    result = {
        "profile_id": profile["profile_id"],
        "best_fitness": best_fitness,
        "total_duration": sum(best_solution),
        "calories": details["calories"],
        "MET": details["MET"],
        "RPE": details["RPE"],
        "heart_rate": details["heart_rate"],
        "session": str(best_solution)
    }

    results.append(result)

    print("Best fitness:", round(best_fitness, 4))
    print("Total duration:", sum(best_solution), "minutes")
    print("Calories:", round(details["calories"], 2))
    print("Session:", best_solution)

# Save all results
results_df = pd.DataFrame(results)
results_df.to_csv(
    "experiments/training_results.csv",
    index=False
)

print("\nAll training experiments completed!")
print(results_df)
print("\nResults saved to experiments/training_results.csv")
