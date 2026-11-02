import pandas as pd

ACTIVITIES_PATH = "data/activities.csv"


def load_activities():
    return pd.read_csv(ACTIVITIES_PATH)


def load_default_profile():
    return {
        "target_calories": 400,
        "met_range": (4, 7),
        "rpe_range": (4, 6),
        "hr_range": (64, 77),
        "desired_domains": ["CV", "ST", "ME", "FM"]
    }