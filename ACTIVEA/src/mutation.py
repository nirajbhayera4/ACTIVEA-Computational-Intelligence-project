
import random

MIN_DURATION = 0
MAX_DURATION = 60
MAX_TOTAL_DURATION = 90


def mutate(chromosome, mutation_rate=0.1):
    mutated = chromosome.copy()

    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(
                MIN_DURATION,
                MAX_DURATION
            )

    # Repair the chromosome if total duration exceeds 90
    while sum(mutated) > MAX_TOTAL_DURATION:
        active_genes = [
            i for i, duration in enumerate(mutated)
            if duration > 0
        ]

        if not active_genes:
            break

        index = random.choice(active_genes)
        mutated[index] = max(0, mutated[index] - 1)

    return mutated


if __name__ == "__main__":
    chromosome = [20, 10, 30, 0, 10, 0, 0]

    result = mutate(chromosome, mutation_rate=0.5)

    print("Original Chromosome:", chromosome)
    print("Mutated Chromosome:", result)
    print("Total Duration:", sum(result))
