from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


EXPERIMENTS = Path("experiments")
ALGORITHMS = ["Original GA", "Improved GA"]
COLORS = {"Original GA": "#286477", "Improved GA": "#D66A4A"}


def load_runs(results_file, profiles_file):
    results = pd.read_csv(EXPERIMENTS / results_file)
    profiles = pd.read_csv(Path("data") / profiles_file)
    results = results.merge(
        profiles[["profile_id", "target_calories"]],
        left_on="profile",
        right_on="profile_id",
        validate="many_to_one",
    )
    results["absolute_calorie_difference"] = (
        results["calories"] - results["target_calories"]
    ).abs()
    return results


def grouped_bars(axis, frame, group_column, metric, groups, ylabel, title):
    summary = frame.groupby([group_column, "algorithm"])[metric].agg(
        ["mean", "std"]
    )
    positions = np.arange(len(groups))
    width = 0.34

    for index, algorithm in enumerate(ALGORITHMS):
        means = [summary.loc[(group, algorithm), "mean"] for group in groups]
        deviations = [summary.loc[(group, algorithm), "std"] for group in groups]
        lower_deviations = [
            min(deviation, mean) for mean, deviation in zip(means, deviations)
        ]
        axis.bar(
            positions + (index - 0.5) * width,
            means,
            width,
            yerr=np.array([lower_deviations, deviations]),
            capsize=4,
            color=COLORS[algorithm],
            label=algorithm,
        )

    axis.set_xticks(positions, groups)
    axis.set_ylabel(ylabel)
    axis.set_title(title)
    axis.grid(axis="y", alpha=0.25)
    axis.set_axisbelow(True)
    axis.set_ylim(bottom=0)


def plot_fitness(training, testing):
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    grouped_bars(
        axes[0], training, "split", "fitness", ["Training"],
        "Mean best fitness (error bars: SD)", "Training profiles",
    )
    grouped_bars(
        axes[1], testing, "profile", "fitness", ["E1", "E2"],
        "Mean best fitness (error bars: SD)", "Held-out testing profiles",
    )

    for axis, frame, groups, group_column in [
        (axes[0], training, ["Training"], "split"),
        (axes[1], testing, ["E1", "E2"], "profile"),
    ]:
        summary = frame.groupby([group_column, "algorithm"])["fitness"].agg(
            ["mean", "std"]
        )
        values = [
            summary.loc[(group, algorithm), "mean"]
            + summary.loc[(group, algorithm), "std"]
            for group in groups
            for algorithm in ALGORITHMS
        ]
        lower = min(
            summary.loc[(group, algorithm), "mean"]
            - summary.loc[(group, algorithm), "std"]
            for group in groups
            for algorithm in ALGORITHMS
        )
        axis.set_ylim(max(0.99, lower - 0.0001), min(1.0001, max(values) + 0.0001))
        axis.yaxis.set_major_formatter(FormatStrFormatter("%.5f"))

    axes[0].legend(frameon=False)
    figure.suptitle("Original vs Enhanced GA: Fitness Comparison")
    figure.tight_layout()
    figure.savefig(EXPERIMENTS / "ga_fitness_function_comparison.png", dpi=220)
    plt.close(figure)


def plot_calorie_adherence(training, testing):
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    grouped_bars(
        axes[0], training, "split", "absolute_calorie_difference",
        ["Training"], "Mean absolute difference (calories)",
        "Training profiles",
    )
    grouped_bars(
        axes[1], testing, "profile", "absolute_calorie_difference",
        ["E1", "E2"], "Mean absolute difference (calories)",
        "Held-out testing profiles",
    )
    axes[0].legend(frameon=False)
    figure.suptitle("Calorie Target Adherence by Fitness Function")
    figure.tight_layout()
    figure.savefig(EXPERIMENTS / "ga_calorie_adherence_comparison.png", dpi=220)
    plt.close(figure)


def plot_preference_penalties(testing):
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    grouped_bars(
        axes[0], testing, "profile", "unsuitable_activity_penalty",
        ["E1", "E2"], "Mean penalty", "Unsuitable-activity penalty",
    )
    grouped_bars(
        axes[1], testing, "profile", "combined_penalty",
        ["E1", "E2"], "Mean penalty", "Combined preference penalty",
    )
    axes[0].legend(frameon=False)
    figure.suptitle("Preference Penalties on Held-Out Testing Profiles")
    figure.text(
        0.5,
        0.015,
        "All runs achieved full domain coverage; missing-domain penalty was zero.",
        ha="center",
    )
    figure.tight_layout(rect=(0, 0.05, 1, 0.93))
    figure.savefig(EXPERIMENTS / "ga_preference_penalty_comparison.png", dpi=220)
    plt.close(figure)


def plot_rate_sweeps():
    mutation = pd.read_csv(EXPERIMENTS / "mutation_results.csv")
    crossover = pd.read_csv(EXPERIMENTS / "crossover_results.csv")
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    for axis, frame, rate_column, label, title in [
        (axes[0], mutation, "mutation_rate", "Mutation rate", "Mutation-rate sweep"),
        (axes[1], crossover, "crossover_rate", "Crossover rate", "Crossover-rate sweep"),
    ]:
        axis.plot(
            frame[rate_column],
            frame["best_fitness"],
            marker="o",
            linewidth=2,
            color=COLORS["Original GA"],
        )
        axis.set_xlabel(label)
        axis.set_ylabel("Recorded best fitness")
        axis.set_title(title)
        axis.set_xticks(frame[rate_column])
        axis.set_ylim(
            frame["best_fitness"].min() - 0.00005,
            min(1.0001, frame["best_fitness"].max() + 0.00005),
        )
        axis.grid(alpha=0.25)

    figure.suptitle("Recorded Best Fitness Across Parameter-Rate Sweeps")
    figure.tight_layout()
    figure.savefig(EXPERIMENTS / "parameter_rate_sweeps_comparison.png", dpi=220)
    plt.close(figure)


def main():
    training = load_runs(
        "improved_fitness_results.csv", "training_data.csv"
    )
    training["split"] = "Training"
    testing = load_runs(
        "testing_fitness_comparison_results.csv", "testing_data.csv"
    )

    plot_fitness(training, testing)
    plot_calorie_adherence(training, testing)
    plot_preference_penalties(testing)
    plot_rate_sweeps()


if __name__ == "__main__":
    main()