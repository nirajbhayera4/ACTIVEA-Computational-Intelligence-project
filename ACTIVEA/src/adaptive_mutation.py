
import random

MAX_DURATION = 60
MAX_TOTAL_DURATION = 90


def adaptive_mutate(chromosome, mutation_rate=0.1):
    """
    Adaptive mutation:
    - Small changes for local exploration.
    - Larger changes for broader exploration.
    """

    mutated = chromosome.copy()

    for i in range(len(mutated)):

        if random.random() < mutation_rate:

            if random.random() < 0.7:
                # Small change
                change = random.randint(-5, 5)
            else:
                # Large change
                change = random.randint(-20, 20)

            mutated[i] += change

            # Keep duration within allowed limits
            mutated[i] = max(
                0, min(MAX_DURATION, mutated[i])
            )

    # Repair total duration
    while sum(mutated) > MAX_TOTAL_DURATION:

        active_genes = [
            i for i, duration in enumerate(mutated)
            if duration > 0
        ]

        if not active_genes:
            break

        index = random.choice(active_genes)
        mutated[index] -= 1

    return mutated


if __name__ == "__main__":

    chromosome = [10, 20, 15, 5, 10, 0, 0]

    print("Original:", chromosome)

    result = adaptive_mutate(
        chromosome,
        mutation_rate=0.5
    )

    print("After adaptive mutation:", result)
    print("Total duration:", sum(result))
