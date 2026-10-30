
import pandas as pd

REQUIRED_COLUMNS = [
    "profile_id",
    "target_calories",
    "met_min",
    "met_max",
    "rpe_min",
    "rpe_max",
    "hr_min",
    "hr_max",
    "desired_domains"
]

def load_profiles(file_path):
    """Load exercise target profiles from a CSV file."""

    df = pd.read_csv(file_path)

    # Check that all required columns exist
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Check for missing values
    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Dataset contains missing values")

    profiles = []

    for _, row in df.iterrows():

        profile = {
            "profile_id": row["profile_id"],
            "target_calories": float(row["target_calories"]),
            "met_range": (
                float(row["met_min"]),
                float(row["met_max"])
            ),
            "rpe_range": (
                float(row["rpe_min"]),
                float(row["rpe_max"])
            ),
            "hr_range": (
                float(row["hr_min"]),
                float(row["hr_max"])
            ),
            "desired_domains": [
                domain.strip()
                for domain in str(row["desired_domains"]).split(";")
            ]
        }

        if profile["target_calories"] <= 0:
            raise ValueError("Target calories must be positive")

        profiles.append(profile)

    return profiles


if __name__ == "__main__":

    training_profiles = load_profiles("data/training_data.csv")
    testing_profiles = load_profiles("data/testing_data.csv")

    print("TRAINING PROFILES")

    for profile in training_profiles:
        print(profile)

    print("\nTESTING PROFILES")

    for profile in testing_profiles:
        print(profile)

    print("\nDataset loading successful!")
    print("Training profiles:", len(training_profiles))
    print("Testing profiles:", len(testing_profiles))
