
import pandas as pd


class Activity:
    """Stores information about an individual exercise activity."""

    def __init__(
        self,
        name,
        calories_per_min,
        met,
        target_rpe,
        target_hr,
        fitness_domains
    ):
        self.name = name
        self.calories_per_min = calories_per_min
        self.met = met
        self.target_rpe = target_rpe
        self.target_hr = target_hr
        self.fitness_domains = fitness_domains


def load_activities(file_path):
    """Load exercise activities from a CSV dataset."""

    df = pd.read_csv(file_path)

    activities = []

    for _, row in df.iterrows():

        if pd.isna(row["calories_per_min"]):
            continue

        activity = Activity(
            name=row["activity"],
            calories_per_min=float(row["calories_per_min"]),
            met=float(row["MET"]),
            target_rpe=float(row["target_RPE"]),
            target_hr=str(row["target_HR"]),
            fitness_domains=row["fitness_domains"].split(";")
        )

        activities.append(activity)

    return activities


if __name__ == "__main__":

    exercises = load_activities("data/activities.csv")

    print("Available activities:")

    for exercise in exercises:
        print(
            exercise.name,
            "| Calories/min:", exercise.calories_per_min,
            "| MET:", exercise.met
        )
