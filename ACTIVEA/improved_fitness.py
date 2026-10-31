# improved_fitness.py

def calculate_domain_coverage(plan, activities, desired_domains):
    """
    Calculate how many of the user's desired fitness
    domains are covered by the selected exercises.
    """

    if not desired_domains:
        return 1.0

    covered_domains = set()

    for i, duration in enumerate(plan):
        if duration > 0:
            domains = activities[i]["domains"]

            for domain in domains:
                covered_domains.add(domain)

    matched = covered_domains.intersection(set(desired_domains))

    return len(matched) / len(desired_domains)


def calculate_domain_penalty(plan, activities, desired_domains):
    """
    Penalise exercise plans that fail to cover
    the user's desired fitness domains.
    """

    coverage = calculate_domain_coverage(
        plan,
        activities,
        desired_domains
    )

    return 1.0 - coverage


def original_fitness(
    calorie_score,
    met_score,
    rpe_score,
    heart_rate_score,
    domain_score
):
    """
    Original ACTIVEA fitness function.
    """

    fitness = (
        0.40 * calorie_score +
        0.15 * met_score +
        0.15 * rpe_score +
        0.15 * heart_rate_score +
        0.15 * domain_score
    )

    return fitness


def improved_fitness(
    calorie_score,
    met_score,
    rpe_score,
    heart_rate_score,
    domain_score,
    plan,
    activities,
    desired_domains,
    penalty_strength=0.10
):
    """
    Improved ACTIVEA fitness function.
    Adds a penalty for missing desired fitness domains.
    """

    base_fitness = original_fitness(
        calorie_score,
        met_score,
        rpe_score,
        heart_rate_score,
        domain_score
    )

    penalty = calculate_domain_penalty(
        plan,
        activities,
        desired_domains
    )

    new_fitness = base_fitness - (
        penalty_strength * penalty
    )

    # Keep fitness between 0 and 1.
    return max(0.0, min(1.0, new_fitness))