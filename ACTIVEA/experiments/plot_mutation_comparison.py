import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "experiments/mutation_comparison_results.csv"
)

# Average fitness comparison
fitness = df.groupby("algorithm")["fitness"].mean()

plt.figure(figsize=(8, 5))
fitness.plot(kind="bar")
plt.title("Average Fitness: Mutation Comparison")
plt.ylabel("Average Fitness")
plt.xlabel("Mutation Operator")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("experiments/mutation_fitness_comparison.png")
plt.close()

# Final diversity comparison
diversity = df.groupby("algorithm")["final_diversity"].mean()

plt.figure(figsize=(8, 5))
diversity.plot(kind="bar")
plt.title("Final Diversity: Mutation Comparison")
plt.ylabel("Average Final Diversity")
plt.xlabel("Mutation Operator")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("experiments/mutation_diversity_comparison.png")
plt.close()

print("Mutation comparison graphs saved successfully!")