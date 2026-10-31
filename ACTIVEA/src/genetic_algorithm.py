
import random
import pandas as pd

from src.population import create_population
from src.selection import tournament_selection
from src.crossover import single_point_crossover
from src.mutation import mutate
from src.fitness import calculate_fitness
from src.chromosome import create_random_chromosome
from src.diversity import calculate_population_diversity
from src.fitness import calculate_fitness, calculate_improved_fitness

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
    mutation_rate=0.1,
    diversity_preservation=True,
    fitness_function=calculate_fitness
):

    # Generate initial population
    population = create_population(population_size)

    best_solution = None
    best_fitness = float("-inf")

    history = []
    diversity_history = []

    for generation in range(generations):

        # 1. Evaluate fitness
        fitness_scores = [
            fitness_function(chromosome, activities, profile)["fitness"]
            for chromosome in population
        ]

        # 2. Find the best individual
        best_index = fitness_scores.index(max(fitness_scores))

        generation_best = population[best_index]
        generation_best_fitness = fitness_scores[best_index]

        # 3. Update the global best solution
        if generation_best_fitness > best_fitness:
            best_fitness = generation_best_fitness
            best_solution = generation_best.copy()

        # 4. Calculate population diversity
        diversity = calculate_population_diversity(population)

        history.append(best_fitness)
        diversity_history.append(diversity)

        # 5. Print current generation results
        print(
            f"Generation {generation + 1}: "
            f"Best Fitness = {best_fitness:.4f}, "
            f"Diversity = {diversity:.4f}"
        )

        # 6. Elitism: preserve the best individual
        new_population = [best_solution.copy()]

        # 7. Generate offspring
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

            # Repair chromosomes
            child1 = repair_chromosome(child1)
            child2 = repair_chromosome(child2)

            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            # Add offspring
            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        # 8. Apply random immigrants if enabled
        if diversity_preservation:

            number_of_immigrants = max(
                1, int(0.10 * population_size)
            )

            for i in range(number_of_immigrants):
                new_population[-(i + 1)] = create_random_chromosome()

        # Move to the next generation
        population = new_population

    return best_solution, best_fitness, history, diversity_history


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

    best_solution, best_fitness, history, diversity_history = (
        run_genetic_algorithm(
            activities,
            profile,
            population_size=30,
            generations=50,
            fitness_function=calculate_improved_fitness
        )
    )

    print("\nBest Exercise Session:")

    activity_names = activities["activity"].tolist()

    for i, duration in enumerate(best_solution):
        if duration > 0:
            print(f"{activity_names[i]}: {duration} minutes")

    print("\nBest Fitness:", round(best_fitness, 4))
    print("Total Duration:", sum(best_solution), "minutes")

    fitness_details = calculate_improved_fitness(
        best_solution, activities, profile
    )

    print("\nFitness Breakdown:")

    for key, value in fitness_details.items():
        print(f"{key}: {value}")
