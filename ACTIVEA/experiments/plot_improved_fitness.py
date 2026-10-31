import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "experiments/improved_fitness_results.csv"
)

summary = df.groupby("algorithm").agg({
    "fitness": "mean",
    "domain_coverage": "mean"
})

# Graph 1: Average fitness
plt.figure(figsize=(8, 5))

summary["fitness"].plot(
    kind="bar",
    rot=0
)

plt.title("Original vs Improved Fitness Function")
plt.ylabel("Average Fitness")
plt.xlabel("Algorithm")

plt.tight_layout()
plt.savefig(
    "experiments/improved_fitness_comparison.png",
    dpi=300
)
plt.close()

# Graph 2: Domain coverage
plt.figure(figsize=(8, 5))

summary["domain_coverage"].plot(
    kind="bar",
    rot=0
)

plt.title("Domain Coverage Comparison")
plt.ylabel("Average Domain Coverage")
plt.xlabel("Algorithm")

plt.tight_layout()
plt.savefig(
    "experiments/domain_coverage_comparison.png",
    dpi=300
)
plt.close()

print("Both comparison graphs saved successfully.")