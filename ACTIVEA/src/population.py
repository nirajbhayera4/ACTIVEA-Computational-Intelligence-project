import random
from src.chromosome import create_random_chromosome, validate_chromosome


def create_population(population_size):
    population = []

    for _ in range(population_size):
        chromosome = create_random_chromosome()

        if validate_chromosome(chromosome):
            population.append(chromosome)

    return population


if __name__ == "__main__":
    population = create_population(10)

    print("Initial Population:")

    for i, chromosome in enumerate(population):
        print(f"Individual {i + 1}: {chromosome}")