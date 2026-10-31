
import pandas as pd


WEIGHTS = {
    "calories": 0.40,
    "met": 0.15,
    "rpe": 0.15,
    "heart_rate": 0.15,
    "domains": 0.15
}


def range_score(value, target_range):
    """Score a value against a preferred range."""

    low, high = target_range

    if low <= value <= high:
        return 1.0

    distance = low - value if value < low else value - high

    scale = max(high - low, 1)

    return max(0.0, 1.0 - distance / scale)


def calculate_calories(chromosome, activities):
    """Calculate total calories burned."""

    total = 0

    for i, duration in enumerate(chromosome):

        if duration == 0:
            continue

        calories = activities.iloc[i]["calories_per_min"]

        if pd.isna(calories):
            raise ValueError(
                f"Missing calorie data: {activities.iloc[i]['activity']}"
            )

        total += duration * float(calories)

    return total


def weighted_average(chromosome, activities, column):
    """Calculate duration-weighted average of an exercise metric."""

    total_value = 0
    total_duration = 0

    for i, duration in enumerate(chromosome):

        if duration == 0:
            continue

        value = activities.iloc[i][column]

        if pd.isna(value):
            raise ValueError(
                f"Missing {column} data: {activities.iloc[i]['activity']}"
            )

        total_value += duration * float(value)
        total_duration += duration

    if total_duration == 0:
        return 0

    return total_value / total_duration


def calculate_heart_rate(chromosome, activities):
    """Calculate weighted average of activity HR range midpoints."""

    total = 0
    total_duration = 0

    for i, duration in enumerate(chromosome):

        if duration == 0:
            continue

        hr = activities.iloc[i]["target_HR"]

        if pd.isna(hr):
            raise ValueError(
                f"Missing heart rate data: {activities.iloc[i]['activity']}"
            )

        low, high = map(float, str(hr).split("-"))

        midpoint = (low + high) / 2

        total += duration * midpoint
        total_duration += duration

    return total / total_duration if total_duration else 0


def calculate_domain_score(chromosome, activities, desired_domains):
    """Measure coverage of the user's desired fitness domains."""

    covered_domains = set()

    for i, duration in enumerate(chromosome):

        if duration == 0:
            continue

        domains = activities.iloc[i]["fitness_domains"]

        if pd.isna(domains):
            raise ValueError(
                f"Missing fitness domains: {activities.iloc[i]['activity']}"
            )

        covered_domains.update(str(domains).split(";"))

    if not desired_domains:
        return 1.0

    matched = covered_domains.intersection(desired_domains)

    return len(matched) / len(desired_domains)


def calculate_fitness(chromosome, activities, profile):
    """
    Calculate complete exercise session fitness.

    profile contains the desired calorie, MET, RPE,
    heart-rate and fitness-domain targets.
    """

    calories = calculate_calories(chromosome, activities)

    met = weighted_average(chromosome, activities, "MET")

    rpe = weighted_average(chromosome, activities, "target_RPE")

    heart_rate = calculate_heart_rate(chromosome, activities)

    calorie_score = max(
        0,
        1 - abs(calories - profile["target_calories"])
        / profile["target_calories"]
    )

    met_score = range_score(met, profile["met_range"])

    rpe_score = range_score(rpe, profile["rpe_range"])

    hr_score = range_score(heart_rate, profile["hr_range"])

    domain_score = calculate_domain_score(
        chromosome,
        activities,
        set(profile["desired_domains"])
    )

    fitness = (
        WEIGHTS["calories"] * calorie_score
        + WEIGHTS["met"] * met_score
        + WEIGHTS["rpe"] * rpe_score
        + WEIGHTS["heart_rate"] * hr_score
        + WEIGHTS["domains"] * domain_score
    )

    return {
        "fitness": fitness,
        "calories": calories,
        "MET": met,
        "RPE": rpe,
        "heart_rate": heart_rate,
        "calorie_score": calorie_score,
        "met_score": met_score,
        "rpe_score": rpe_score,
        "hr_score": hr_score,
        "domain_score": domain_score
    }
def calculate_improved_fitness(
    chromosome,
    activities,
    profile,
    penalty_strength=0.10
):
    """
    Improved fitness function.

    Applies an additional penalty when the exercise plan
    fails to cover the user's desired fitness domains.
    """

    # Calculate the original fitness and all its components
    result = calculate_fitness(chromosome, activities, profile)

    # Existing domain score represents domain coverage
    domain_coverage = result["domain_score"]

    # Calculate penalty for missing desired domains
    domain_penalty = 1.0 - domain_coverage

    # Apply additional preference penalty
    improved_score = (
        result["fitness"]
        - penalty_strength * domain_penalty
    )

    # Keep score within the range 0 to 1
    result["fitness"] = max(0.0, min(1.0, improved_score))

    # Add details for experimental analysis
    result["domain_coverage"] = domain_coverage
    result["domain_penalty"] = domain_penalty
    result["penalty_strength"] = penalty_strength

    return result

if __name__ == "__main__":

    activities = pd.read_csv("data/activities.csv")

    chromosome = [20, 10, 0, 0, 0, 0, 0]

    profile = {
        "target_calories": 400,
        "met_range": (4, 7),
        "rpe_range": (4, 6),
        "hr_range": (64, 77),
        "desired_domains": ["CV", "ST", "ME", "FM"]
    }

    result = calculate_fitness(
        chromosome,
        activities,
        profile
    )

    print("\nExercise Evaluation")

    for key, value in result.items():
        print(f"{key}: {value:.2f}")
