import pandas as pd
from src.fitness import calculate_fitness, calculate_improved_fitness

activities = pd.read_csv("data/activities.csv")

profile = {
    "target_calories": 400,
    "met_range": (4, 7),
    "rpe_range": (4, 6),
    "hr_range": (64, 77),
    "desired_domains": ["CV", "ST", "ME", "FM"]
}

# Jogging and cycling do not cover the ST domain
chromosome = [10, 0, 10, 0, 0, 0, 0]

original = calculate_fitness(chromosome, activities, profile)
improved = calculate_improved_fitness(chromosome, activities, profile)

print("Original fitness:", original["fitness"])
print("Improved fitness:", improved["fitness"])
print("Domain coverage:", improved["domain_coverage"])
print("Domain penalty:", improved["domain_penalty"])