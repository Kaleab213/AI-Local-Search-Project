import argparse
import random


def knapsack(items, max_weight):
    # Generate a random initial result
    result = [random.randint(0, 1) for _ in range(len(items))]

    # Calculate the value and weight of the initial result
    value = sum([items[i][0] * result[i] for i in range(len(items))])
    weight = sum([items[i][1] * result[i] for i in range(len(items))])

    # Keep track of the best result found so far
    best_value = value
    best_result = result

    # Iterate until no further improvements can be made
    while True:
        # Generate all neighbors of the current result
        neighbors = []
        for i in range(len(items)):
            neighbor = list(result)
            neighbor[i] = 1 - neighbor[i]
            neighbors.append(neighbor)

        # Evaluate all neighbors and select the best one
        found_better_neighbor = False
        for neighbor in neighbors:
            neighbor_value = sum([items[i][0] * neighbor[i]
                                 for i in range(len(items))])
            neighbor_weight = sum([items[i][1] * neighbor[i]
                                  for i in range(len(items))])
            if neighbor_weight <= max_weight and neighbor_value > best_value:
                best_value = neighbor_value
                best_result = neighbor
                found_better_neighbor = True

        # If no better neighbor was found, return the best result found so far
        if not found_better_neighbor:
            return (best_result, best_value)


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
        result, value = knapsack(items, max_weight)
        print(f'result: {result}')
        print(f'Value: {value}')


# run the following code using terminal

        # enter      python knapsack_Hillclimbing.py  --file items.txt
