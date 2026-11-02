

import pandas as pd
import pytest

from src.fitness import (
    calculate_fitness,
    calculate_improved_fitness,
    calculate_calories,
    calculate_domain_score,
    range_score,
)


@pytest.fixture
def activities():
    """Provide a small activity dataset for predictable tests."""

    return pd.DataFrame([
        {
            "activity": "Jogging",
            "calories_per_min": 8.0,
            "MET": 6.0,
            "target_RPE": 5.0,
            "target_HR": "120-140",
            "fitness_domains": "CV;ME",
        },
        {
            "activity": "Yoga",
            "calories_per_min": 3.0,
            "MET": 3.0,
            "target_RPE": 3.0,
            "target_HR": "90-110",
            "fitness_domains": "BA;FL",
        },
    ])


@pytest.fixture
def profile():
    """Provide a known target profile."""

    return {
        "target_calories": 160,
        "met_range": (4.0, 7.0),
        "rpe_range": (3.0, 5.0),
        "hr_range": (100.0, 140.0),
        "desired_domains": ["CV", "ME"],
    }


def test_calculate_calories(activities):
    """Check total calories for a known chromosome."""

    chromosome = [10, 0]

    assert calculate_calories(chromosome, activities) == 80.0


def test_range_score_inside_range():
    """A value inside the target range should score 1."""

    assert range_score(5, (4, 6)) == 1.0


def test_range_score_outside_range():
    """A value outside the range should receive a lower score."""

    assert range_score(3, (4, 6)) == 0.5


def test_domain_score_full_coverage(activities):
    """Check that all desired domains are covered."""

    chromosome = [10, 0]
    desired_domains = {"CV", "ME"}

    score = calculate_domain_score(
        chromosome, activities, desired_domains
    )

    assert score == 1.0


def test_domain_score_partial_coverage(activities):
    """Check that missing domains reduce the domain score."""

    chromosome = [10, 0]
    desired_domains = {"CV", "ME", "BA", "FL"}

    score = calculate_domain_score(
        chromosome, activities, desired_domains
    )

    assert score == 0.5


def test_calculate_fitness_returns_required_metrics(
    activities, profile
):
    """Check the structure of the fitness result."""

    result = calculate_fitness(
        [10, 0], activities, profile
    )

    required_keys = {
        "fitness",
        "calories",
        "MET",
        "RPE",
        "heart_rate",
        "calorie_score",
        "met_score",
        "rpe_score",
        "hr_score",
        "domain_score",
    }

    assert required_keys.issubset(result.keys())


def test_fitness_is_between_zero_and_one(activities, profile):
    """Fitness must remain within its expected range."""

    result = calculate_fitness(
        [10, 0], activities, profile
    )

    assert 0.0 <= result["fitness"] <= 1.0


def test_zero_duration_chromosome(activities, profile):
    """An empty exercise plan should be evaluated safely."""

    result = calculate_fitness(
        [0, 0], activities, profile
    )

    assert result["calories"] == 0
    assert result["MET"] == 0
    assert result["RPE"] == 0
    assert result["heart_rate"] == 0


def test_improved_fitness_applies_domain_penalty(
    activities, profile
):
    """Missing domains should reduce improved fitness."""

    chromosome = [10, 0]

    original = calculate_fitness(
        chromosome, activities, profile
    )

    improved = calculate_improved_fitness(
        chromosome,
        activities,
        profile,
        penalty_strength=0.10,
    )

    assert improved["domain_coverage"] == 1.0
    assert improved["domain_penalty"] == 0.0
    assert improved["fitness"] == pytest.approx(
        original["fitness"]
    )


def test_improved_fitness_penalises_missing_domains(
    activities, profile
):
    """The additional penalty should apply when domains are missing."""

    # Jogging covers CV and ME, but the profile below also requests BA.
    modified_profile = profile.copy()
    modified_profile["desired_domains"] = ["CV", "ME", "BA"]

    chromosome = [10, 0]

    original = calculate_fitness(
        chromosome, activities, modified_profile
    )

    improved = calculate_improved_fitness(
        chromosome,
        activities,
        modified_profile,
        penalty_strength=0.10,
    )

    assert improved["domain_coverage"] == pytest.approx(2 / 3)
    assert improved["domain_penalty"] == pytest.approx(1 / 3)
    assert improved["fitness"] < original["fitness"]
