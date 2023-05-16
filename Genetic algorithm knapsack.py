import sys
import argparse
import random
import numpy as np
import copy

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        max_weight = float(lines[0].strip())
        items = [Item(*line.strip().split(',')) for line in lines[2:]]
        for item in items:
            item.weight = float(item.weight)
            item.value = float(item.value)
            item.n_items = int(item.n_items)
    return max_weight, items





def fitness(solution, items, max_weight):
    total_weight = sum([item.weight * count for item, count in zip(items, solution)])
    total_value = sum([item.value * count for item, count in zip(items, solution)])

    if total_weight <= max_weight:
        return total_value
    else:
        return -1

def genetic_algorithm(items, max_weight, population_size=100, generations=1000):
    # Initialization
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, item.n_items) for item in items]
        population.append(individual)

    for gen in range(generations):
        # Selection
        fitness_values = [fitness(individual, items, max_weight) for individual in population]
        parents_indices = np.argsort(fitness_values)[-2:]
        parents = [population[i] for i in parents_indices]

        # Crossover
        crossover_point = random.randint(1, len(items) - 1)
        child1 = parents[0][:crossover_point] + parents[1][crossover_point:]
        child2 = parents[1][:crossover_point] + parents[0][crossover_point:]

        # Mutation
        mutation_index = random.randint(0, len(items) - 1)
        child1[mutation_index] = random.randint(0, items[mutation_index].n_items)
        child2[mutation_index] = random.randint(0, items[mutation_index].n_items)

        # Replacement
        population[-2:] = [child1, child2]

    # Return the best solution
    best_solution = max(population, key=lambda s: fitness(s, items, max_weight))
    return best_solution


