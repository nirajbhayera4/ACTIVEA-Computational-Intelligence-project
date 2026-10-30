
import pandas as pd
import random


# Each chromosome represents 7 exercise activities.
NUMBER_OF_ACTIVITIES = 7

# Duration limits for each activity, in minutes.
MIN_DURATION = 0
MAX_DURATION = 60
MAX_TOTAL_DURATION = 90

def validate_total_duration(chromosome):
    return sum(chromosome) <= MAX_TOTAL_DURATION


def create_random_chromosome():
    chromosome = [0] * NUMBER_OF_ACTIVITIES

    remaining = MAX_TOTAL_DURATION

    for i in range(NUMBER_OF_ACTIVITIES):
        duration = random.randint(0, min(30, remaining))
        chromosome[i] = duration
        remaining -= duration

    if all(duration == 0 for duration in chromosome):
        chromosome[random.randint(0, NUMBER_OF_ACTIVITIES - 1)] = 10

    return chromosome


def validate_chromosome(chromosome):
    if len(chromosome) != NUMBER_OF_ACTIVITIES:
        return False

    for duration in chromosome:
        if not isinstance(duration, int):
            return False
        if duration < MIN_DURATION or duration > MAX_DURATION:
            return False

    return validate_total_duration(chromosome)



import pandas as pd


def display_chromosome(chromosome, activities):
    """Display selected exercises and their durations."""

    if not validate_chromosome(chromosome):
        raise ValueError("Invalid chromosome")

    print("\nExercise Session:")

    for i, duration in enumerate(chromosome):

        if duration > 0:
            print(activities[i], ":", duration, "minutes")




if __name__ == "__main__":

    chromosome = create_random_chromosome()

    print("Generated Chromosome:", chromosome)

    print("Is Valid:", validate_chromosome(chromosome))

    # Read all seven activity names from CSV.
    df = pd.read_csv("data/activities.csv")

    activity_names = df["activity"].tolist()

    display_chromosome(chromosome, activity_names)

