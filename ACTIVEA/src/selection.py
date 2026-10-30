import random


def tournament_selection(population, fitness_scores, tournament_size=3):
    selected_indices = random.sample(
        range(len(population)),
        tournament_size
    )

    best_index = max(
        selected_indices,
        key=lambda i: fitness_scores[i]
    )

    return population[best_index]


if __name__ == "__main__":
    population = [
        [20, 10, 0, 0, 0, 0, 0],
        [15, 15, 10, 0, 0, 0, 0],
        [10, 20, 10, 5, 0, 0, 0],
        [25, 5, 0, 10, 0, 0, 0],
        [30, 10, 0, 0, 0, 0, 0]
    ]

    fitness_scores = [0.45, 0.82, 0.61, 0.70, 0.55]

    parent = tournament_selection(
        population,
        fitness_scores
    )

    print("Selected Parent:", parent)