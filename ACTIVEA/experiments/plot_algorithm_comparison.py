
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "experiments/algorithm_comparison_summary.csv"
)

metrics = [
    ("average_fitness", "Average Fitness", "fitness_comparison.png"),
    ("average_duration", "Average Duration (minutes)", "duration_comparison.png"),
    ("average_calories", "Average Calories", "calories_comparison.png")
]

for metric, ylabel, filename in metrics:

    for dataset in ["Training", "Testing"]:

        subset = df[df["dataset"] == dataset]

        plt.figure(figsize=(7, 5))
        plt.bar(subset["algorithm"], subset[metric])

        if metric == "average_fitness":
            plt.ylim(0.999, 1.0001)

        plt.title(f"{ylabel}: {dataset} Profiles")
        plt.xlabel("Algorithm")
        plt.ylabel(ylabel)
        plt.tight_layout()

        output_path = f"experiments/{dataset.lower()}_{filename}"
        plt.savefig(output_path, dpi=300)
        plt.close()

        print("Saved:", output_path)

print("\nAll 6 comparison graphs generated successfully!")
