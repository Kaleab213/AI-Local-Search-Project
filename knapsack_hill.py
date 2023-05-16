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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solve the knapsack problem using hill climbing.')
    parser.add_argument('--algorithm', type=str, default='hill_climbing',
                        help='The algorithm to use (hill_climbing or simulated_annealing).')
    parser.add_argument('--file', type=str, required=True,
                        help='The file containing the items.')
    args = parser.parse_args()

    with open(args.file) as f:
        max_weight = int(f.readline().strip())
        items = []
        f.readline()  # Ignore header line.
        for line in f:
            parts = line.strip().split(',')
            items.append((int(parts[2]), float(parts[1]), int(parts[3])))

    if args.algorithm == 'hill_climbing':
        result, value = hill_climbing(items, max_weight)
        print(f'result: {result}')
        print(f'Value: {value}')


# run the following code using terminal

        # enter      python knapsack_Hillclimbing.py  --file items.txt
