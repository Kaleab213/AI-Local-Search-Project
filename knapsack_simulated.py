import argparse
import random
import math
from knapsack import generate_random_solution, evaluate_fitness, generate_neighbor_solution


def simulated_annealing(max_weight, items, initial_temperature=1000, cooling_rate=0.95, num_iterations=1000):
    current_solution = generate_random_solution(items)
    current_fitness = evaluate_fitness(current_solution, items, max_weight)
    best_solution = current_solution
    best_fitness = current_fitness
    temperature = initial_temperature

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
        else:
            # Accept worse solution with a probability
            acceptance_prob = math.exp(
                (neighbor_fitness - current_fitness) / temperature)
            if random.random() < acceptance_prob:
                current_solution = neighbor_solution
                current_fitness = neighbor_fitness

        # Update best solution
        if current_fitness > best_fitness:
            best_solution = current_solution
            best_fitness = current_fitness

        # Cool down temperature
        temperature *= cooling_rate

    return best_solution



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solve the knapsack problem using simulated annealing.')
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

    result, value = simulated_annealing(items, max_weight)
    print(f'result: {result}')
    print(f'Value: {value}')


# run the following code using terminal

    # enter      python knapsack_SimulatedAnnealing.py  --file items.txt
