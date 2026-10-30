
import random
import pandas as pd

from src.population import create_population
from src.selection import tournament_selection
from src.crossover import single_point_crossover
from src.mutation import mutate
from src.fitness import calculate_fitness


MAX_TOTAL_DURATION = 90


def repair_chromosome(chromosome):
    """Ensure the chromosome respects duration constraints."""

    repaired = chromosome.copy()

    while sum(repaired) > MAX_TOTAL_DURATION:
        active_genes = [
            i for i, duration in enumerate(repaired)
            if duration > 0
        ]

        if not active_genes:
            break

        index = random.choice(active_genes)
        repaired[index] -= 1

    return repaired


def run_genetic_algorithm(
    activities,
    profile,
    population_size=30,
    generations=50,
    crossover_rate=0.8,
    mutation_rate=0.1
):
    # Generate initial population
    population = create_population(population_size)

    best_solution = None
    best_fitness = float("-inf")
    history = []

    for generation in range(generations):

        # Evaluate fitness of every individual
        fitness_scores = [
            calculate_fitness(chromosome, activities, profile)["fitness"]
            for chromosome in population
        ]

        # Find the best individual in this generation
        best_index = fitness_scores.index(max(fitness_scores))
        generation_best = population[best_index]
        generation_best_fitness = fitness_scores[best_index]

        # Update the best solution found so far
        if generation_best_fitness > best_fitness:
            best_fitness = generation_best_fitness
            best_solution = generation_best.copy()

        history.append(best_fitness)

        print(
            f"Generation {generation + 1}: "
            f"Best Fitness = {best_fitness:.4f}"
        )

        # Preserve the best individual (elitism)
        new_population = [best_solution.copy()]

        # Create the remaining individuals
        while len(new_population) < population_size:

            parent1 = tournament_selection(
                population, fitness_scores
            )

            parent2 = tournament_selection(
                population, fitness_scores
            )

            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = single_point_crossover(
                    parent1, parent2
                )
            else:
                child1 = parent1.copy()
                child2 = parent2.copy()

            # Repair crossover results
            child1 = repair_chromosome(child1)
            child2 = repair_chromosome(child2)

            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    return best_solution, best_fitness, history


if __name__ == "__main__":

    random.seed(42)

    activities = pd.read_csv("data/activities.csv")

    profile = {
        "target_calories": 400,
        "met_range": (4, 7),
        "rpe_range": (4, 6),
        "hr_range": (64, 77),
        "desired_domains": ["CV", "ST", "ME", "FM"]
    }

    best_solution, best_fitness, history = run_genetic_algorithm(
        activities,
        profile
    )

    print("\nBest Exercise Session:")

    activity_names = activities["activity"].tolist()

    for i, duration in enumerate(best_solution):
        if duration > 0:
            print(f"{activity_names[i]}: {duration} minutes")

    print("\nBest Fitness:", round(best_fitness, 4))
    print("Total Duration:", sum(best_solution), "minutes")
    fitness_details = calculate_fitness(best_solution, activities, profile)
    print("\nFitness Breakdown:")
    for key, value in fitness_details.items():
        print(f"{key}: {value}")



    
