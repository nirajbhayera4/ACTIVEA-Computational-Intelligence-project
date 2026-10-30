
import random

def single_point_crossover(parent1, parent2):
    if len(parent1) != len(parent2):
        raise ValueError("Parents must have the same length")

    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


if __name__ == "__main__":
    parent1 = [20, 10, 30, 0, 10, 0, 0]
    parent2 = [10, 20, 0, 15, 0, 20, 0]

    child1, child2 = single_point_crossover(parent1, parent2)

    print("Parent 1:", parent1)
    print("Parent 2:", parent2)
    print("Child 1:", child1)
    print("Child 2:", child2)
