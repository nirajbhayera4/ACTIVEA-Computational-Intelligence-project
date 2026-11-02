

import random
from pathlib import Path

import pandas as pd

from src.dataset import load_profiles
from src.fitness import calculate_improved_fitness
from src.genetic_algorithm import run_genetic_algorithm


def main():
    """Load project data, run the GA and display the best plan."""

    # Find the project root, even when launched from another directory.
    project_root = Path(__file__).resolve().parent.parent

    activities_path = project_root / "data" / "activities.csv"
    training_path = project_root / "data" / "training_data.csv"
    testing_path = project_root / "data" / "testing_data.csv"

    # Check that required datasets exist.
    for file_path in (activities_path, training_path, testing_path):
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required dataset not found: {file_path}"
            )

    # Load activity and profile datasets.
    activities = pd.read_csv(activities_path)
    training_profiles = load_profiles(training_path)
    testing_profiles = load_profiles(testing_path)

    print("\n===================================")
    print(" ACTIVEA - EXERCISE PLANNING SYSTEM")
    print("===================================")

    print("\nChoose a profile dataset:")
    print("1. Training profiles")
    print("2. Testing profiles")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        profiles = training_profiles
    elif choice == "2":
        profiles = testing_profiles
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    if not profiles:
        print("No profiles found in the selected dataset.")
        return

    print("\nAvailable profiles:")
    for index, profile in enumerate(profiles, start=1):
        print(
            f"{index}. {profile['profile_id']} "
            f"(Target calories: {profile['target_calories']})"
        )

    try:
        profile_choice = int(input("\nSelect a profile number: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if not 1 <= profile_choice <= len(profiles):
        print("Invalid profile selection.")
        return

    profile = profiles[profile_choice - 1]

    # Use a fixed seed so the run can be reproduced.
    random.seed(42)

    print("\nRunning Genetic Algorithm...")
    print(f"Selected profile: {profile['profile_id']}")

    best_solution, best_fitness, history, diversity_history = (
        run_genetic_algorithm(
            activities=activities,
            profile=profile,
            population_size=50,
            generations=50,
            crossover_rate=0.8,
            mutation_rate=0.1,
            diversity_preservation=True,
            fitness_function=calculate_improved_fitness
        )
    )

    # Calculate detailed metrics for the best solution.
    result = calculate_improved_fitness(
        best_solution, activities, profile
    )

    print("\n===================================")
    print(" RECOMMENDED EXERCISE SESSION")
    print("===================================")

    total_duration = 0

    for index, duration in enumerate(best_solution):
        if duration > 0:
            activity_name = activities.iloc[index]["activity"]
            print(f"{activity_name}: {duration} minutes")
            total_duration += duration

    print("\nTotal duration:", total_duration, "minutes")
    print("Best fitness:", round(best_fitness, 5))

    print("\nFitness breakdown:")
    for key, value in result.items():
        print(f"{key}: {value:.4f}")

    print("\nFinal population diversity:",
          round(diversity_history[-1], 4))

    print("\nACTIVEA execution completed successfully.")


if __name__ == "__main__":
    main()
