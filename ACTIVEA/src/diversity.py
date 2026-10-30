
import numpy as np

def calculate_population_diversity(population):
    """
    Measure average variation in activity durations
    across the population.
    """
    if len(population) < 2:
        return 0.0

    population_array = np.array(population, dtype=float)

    # Standard deviation for each activity gene
    gene_diversity = np.std(population_array, axis=0)

    # Normalise using maximum duration of 60 minutes
    normalised_diversity = gene_diversity / 60

    return float(np.mean(normalised_diversity))


if __name__ == "__main__":
    from src.population import create_population

    population = create_population(30)

    diversity = calculate_population_diversity(population)

    print("Population Diversity:", round(diversity, 4))
