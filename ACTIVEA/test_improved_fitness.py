from improved_fitness import (
    calculate_domain_coverage,
    calculate_domain_penalty,
    original_fitness,
    improved_fitness
)

# Example activities
activities = [
    {"name": "Jogging", "domains": ["CV", "ME", "FM"]},
    {"name": "Bodyweight squats", "domains": ["ST", "ME", "BA", "FM"]},
    {"name": "Cycling", "domains": ["CV", "ME", "FM"]},
    {"name": "Yoga", "domains": ["FL", "BA", "ME"]}
]

# User wants these domains
desired_domains = ["CV", "ST", "ME", "FM"]

# Example exercise plan
# Jogging = 10 minutes
# Squats = 0 minutes
# Cycling = 15 minutes
# Yoga = 0 minutes

plan = [10, 0, 15, 0]

# Example component scores
calorie_score = 0.95
met_score = 0.90
rpe_score = 0.90
heart_rate_score = 0.95
domain_score = 0.90

coverage = calculate_domain_coverage(
    plan, activities, desired_domains
)

penalty = calculate_domain_penalty(
    plan, activities, desired_domains
)

old_score = original_fitness(
    calorie_score,
    met_score,
    rpe_score,
    heart_rate_score,
    domain_score
)

new_score = improved_fitness(
    calorie_score,
    met_score,
    rpe_score,
    heart_rate_score,
    domain_score,
    plan,
    activities,
    desired_domains
)

print("Domain Coverage:", coverage)
print("Domain Penalty:", penalty)
print("Original Fitness:", old_score)
print("Improved Fitness:", new_score)