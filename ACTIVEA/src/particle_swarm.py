
import random

from src.chromosome import create_random_chromosome
from src.fitness import calculate_fitness

NUMBER_OF_ACTIVITIES = 7
MAX_TOTAL_DURATION = 90
MAX_DURATION = 60


def repair_particle(position):
    """Convert a particle into valid integer activity durations."""
    position = [max(0, min(MAX_DURATION, x)) for x in position]

    total = sum(position)

    if total > MAX_TOTAL_DURATION:
        scale = MAX_TOTAL_DURATION / total
        position = [x * scale for x in position]

    position = [round(x) for x in position]

    while sum(position) > MAX_TOTAL_DURATION:
        index = position.index(max(position))
        position[index] -= 1

    if sum(position) == 0:
        position[0] = 10

    return position


def run_particle_swarm(
    activities,
    profile,
    swarm_size=30,
    iterations=50,
    w=0.7,
    c1=1.5,
    c2=1.5
):
    # Create initial particles
    particles = [
        create_random_chromosome()
        for _ in range(swarm_size)
    ]

    # Initial velocities
    velocities = [
        [random.uniform(-5, 5) for _ in range(NUMBER_OF_ACTIVITIES)]
        for _ in range(swarm_size)
    ]

    personal_best = [p.copy() for p in particles]
    personal_best_scores = [
        calculate_fitness(p, activities, profile)["fitness"]
        for p in particles
    ]

    best_index = personal_best_scores.index(max(personal_best_scores))
    global_best = personal_best[best_index].copy()
    global_best_score = personal_best_scores[best_index]

    history = []

    for iteration in range(iterations):

        for i in range(swarm_size):

            # Evaluate current particle
            current = repair_particle(particles[i])
            particles[i] = current

            score = calculate_fitness(
                current, activities, profile
            )["fitness"]

            # Update personal best
            if score > personal_best_scores[i]:
                personal_best_scores[i] = score
                personal_best[i] = current.copy()

            # Update global best
            if score > global_best_score:
                global_best_score = score
                global_best = current.copy()

        # Update particle velocities and positions
        for i in range(swarm_size):
            for j in range(NUMBER_OF_ACTIVITIES):

                r1 = random.random()
                r2 = random.random()

                velocities[i][j] = (
                    w * velocities[i][j]
                    + c1 * r1 * (personal_best[i][j] - particles[i][j])
                    + c2 * r2 * (global_best[j] - particles[i][j])
                )

                # Limit velocity
                velocities[i][j] = max(
                    -10, min(10, velocities[i][j])
                )

                particles[i][j] += velocities[i][j]

        history.append(global_best_score)

        print(
            f"Iteration {iteration + 1}: "
            f"Best Fitness = {global_best_score:.4f}"
        )

    return global_best, global_best_score, history


if __name__ == "__main__":
    import pandas as pd
    from src.activity import load_activities

    activities = pd.read_csv("data/activities.csv")
    profile = {
        "target_calories": 400,
        "met_range": (4, 7),
        "rpe_range": (4, 6),
        "hr_range": (64, 77),
        "desired_domains": ["CV", "ST", "ME", "FM"]
    }

    best, score, history = run_particle_swarm(
        activities, profile
    )

    print("\nBest PSO Solution:", best)
    print("Best Fitness:", score)
    print("Total Duration:", sum(best), "minutes")
