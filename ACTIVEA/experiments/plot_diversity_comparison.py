
import pandas as pd
import matplotlib.pyplot as plt

# Load comparison summary
df = pd.read_csv(
    "experiments/diversity_comparison_summary.csv"
)

# Plot average diversity
plt.figure(figsize=(8, 5))

plt.bar(df["algorithm"], df["average_diversity"])

plt.title("Average Population Diversity Comparison")
plt.xlabel("Algorithm")
plt.ylabel("Average Diversity")

plt.tight_layout()
plt.savefig("experiments/average_diversity_comparison.png")
plt.show()


# Plot best fitness
plt.figure(figsize=(8, 5))

plt.bar(df["algorithm"], df["best_fitness"])

plt.title("Best Fitness Comparison")
plt.xlabel("Algorithm")
plt.ylabel("Best Fitness")

plt.tight_layout()
plt.savefig("experiments/best_fitness_comparison.png")
plt.show()


print("Comparison graphs saved successfully!")
