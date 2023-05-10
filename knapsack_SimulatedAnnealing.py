import argparse
import random
import math


def knapsack(items, max_weight):
    
    result = [random.randint(0, 1) for _ in range(len(items))] # Generate a random initial result

    # Calculate the value and weight of the initial result
    value = sum([items[i][0] * result[i] for i in range(len(items))])
    weight = sum([items[i][1] * result[i] for i in range(len(items))])

    best_value = value
    best_result = result

    # Set the initial temperature and cooling rate
    temperature = 1000.0
    cooling_rate = 0.95

    # Iterate until the temperature is too low
    while temperature > 1.0:
        # Generate a random neighbor of the current result
        neighbor = list(result)
        index = random.randint(0, len(items) - 1)
        neighbor[index] = 1 - neighbor[index]

        # Calculate the value and weight of the neighbor result
        neighbor_value = sum([items[i][0] * neighbor[i]
                             for i in range(len(items))])
        neighbor_weight = sum([items[i][1] * neighbor[i]
                              for i in range(len(items))])

        # If the neighbor is better, accept it
        if neighbor_weight <= max_weight and neighbor_value > value:
            result = neighbor
            value = neighbor_value
            weight = neighbor_weight

            # If this is the best result found so far, remember it
            if value > best_value:
                best_value = value
                best_result = result

        # If the neighbor is worse, accept it with a certain probability based on the temperature
        else:
            delta = neighbor_value - value
            probability = math.exp(delta / temperature)
            if random.random() < probability:
                result = neighbor
                value = neighbor_value
                weight = neighbor_weight

        # Decrease the temperature according to the cooling rate
        temperature *= cooling_rate

    return (best_result, best_value)


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

    result, value = knapsack(items, max_weight)
    print(f'result: {result}')
    print(f'Value: {value}')


# run the following code using terminal

    # enter      python knapsack_SimulatedAnnealing.py  --file items.txt
