import argparse
import random

from knapsack import generate_random_solution, evaluate_fitness, generate_neighbor_solution


def hill_climbing(max_weight, items, num_iterations=1000):
    current_solution = generate_random_solution(items)
    current_fitness = evaluate_fitness(current_solution, items, max_weight)

    for i in range(num_iterations):
        # Generate neighbor solution
        neighbor_solution = generate_neighbor_solution(current_solution, items)

        # Evaluate fitness of neighbor solution
        neighbor_fitness = evaluate_fitness(
            neighbor_solution, items, max_weight)

        # If neighbor is better, update current solution
        if neighbor_fitness > current_fitness:
            current_solution = neighbor_solution
            current_fitness = neighbor_fitness

    return current_solution



