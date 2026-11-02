
from experiments.config import load_activities
from src.fitness import calculate_fitness, calculate_improved_fitness


# Load activity catalogue
activities = load_activities()

# Define a sample training profile
profile = {
    "target_calories": 400,
    "met_range": (4, 7),
    "rpe_range": (4, 6),
    "hr_range": (64, 77),
    "desired_domains": ["CV", "ST", "ME", "FM"]
}

# Sample chromosome with incomplete domain coverage
chromosome = [10, 0, 10, 0, 0, 0, 0]

# Calculate fitness using both methods
original = calculate_fitness(chromosome, activities, profile)

improved = calculate_improved_fitness(
    chromosome,
    activities,
    profile
)

# Display comparison
print("Original fitness:", original["fitness"])
print("Improved fitness:", improved["fitness"])
print("Domain coverage:", improved["domain_coverage"])
print("Domain penalty:", improved["domain_penalty"])
