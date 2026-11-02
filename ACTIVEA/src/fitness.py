
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
    Enhanced fitness function.

    Penalises:
    1. Missing preferred fitness domains.
    2. Activities that do not match any preferred domain.
    """

    # Calculate original fitness
    result = calculate_fitness(chromosome, activities, profile)

    desired_domains = set(profile["desired_domains"])

    total_duration = 0
    unsuitable_duration = 0

    # Check every selected activity
    for i, duration in enumerate(chromosome):

        if duration <= 0:
            continue

        activity_domains = set(
            str(activities.iloc[i]["fitness_domains"])
            .split(";")
        )

        activity_domains = {
            domain.strip() for domain in activity_domains
        }

        total_duration += duration

        # Activity is unsuitable if it matches no preferred domain
        if not activity_domains.intersection(desired_domains):
            unsuitable_duration += duration

    # Calculate unsuitable activity penalty
    if total_duration > 0:
        unsuitable_penalty = unsuitable_duration / total_duration
    else:
        unsuitable_penalty = 0.0

    # Calculate missing preferred domain penalty
    missing_domain_penalty = 1.0 - result["domain_score"]

    # Combine both penalties
    combined_penalty = (
        missing_domain_penalty + unsuitable_penalty
    ) / 2

    # Apply penalty to original fitness
    improved_score = (
        result["fitness"]
        - penalty_strength * combined_penalty
    )

    result["fitness"] = max(0.0, min(1.0, improved_score))

    # Store additional information for experiments
    result["domain_coverage"] = result["domain_score"]
    result["missing_domain_penalty"] = missing_domain_penalty
    result["unsuitable_activity_penalty"] = unsuitable_penalty
    result["unsuitable_duration"] = unsuitable_duration
    result["combined_penalty"] = combined_penalty
    result["penalty_strength"] = penalty_strength
    result["domain_penalty"] = missing_domain_penalty

    return result

if __name__ == "__main__":

    activities = pd.read_csv("data/activities.csv")

    profile = {
        "target_calories": 400,
        "met_range": (4, 7),
        "rpe_range": (4, 6),
        "hr_range": (64, 77),
        "desired_domains": ["CV", "FM"]
    }

    # Jogging supports CV and FM.
    # Yoga does not support either CV or FM.
    jogging_index = activities[
        activities["activity"] == "Jogging"
    ].index[0]

    yoga_index = activities[
        activities["activity"] == "Yoga"
    ].index[0]

    chromosome = [0] * len(activities)
    chromosome[jogging_index] = 20
    chromosome[yoga_index] = 10

    result = calculate_improved_fitness(
        chromosome, activities, profile
    )

    print("\nTASK 8: UNSUITABLE ACTIVITY PENALTY TEST")

    for key, value in result.items():
        print(f"{key}: {value}")