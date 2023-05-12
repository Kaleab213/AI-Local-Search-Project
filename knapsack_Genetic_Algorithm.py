import argparse
import random


def read_input_file(file_path):
    if file_path is None:
        raise ValueError("File path is None")
    with open(file_path, 'r') as f:
        max_weight = float(next(f).strip())
        next(f)  # skip header line
        items = []
        for line in f:
            name, weight, value, n_items = line.strip().split(',')
            items.append((name, float(weight), int(value), int(n_items)))
    return max_weight, items


def create_initial_population(population_size, items):
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(len(items))]
        population.append(individual)
    return population


def fitness(individual, items, max_weight):
    total_weight = 0
    total_value = 0
    for i in range(len(items)):
        if individual[i] == 1:
            total_weight += items[i][1]
            total_value += items[i][2]
            if total_weight > max_weight:
                return 0
    return total_value


def selection(population, items, max_weight):
    fitness_values = [fitness(individual, items, max_weight) for individual in population]
    selected_individuals = []
    for i in range(len(population)):
        individual_1 = random.choices(population, weights=fitness_values)[0]
        individual_2 = random.choices(population, weights=fitness_values)[0]
        child = crossover(individual_1, individual_2)
        mutated_child = mutation(child)
        selected_individuals.append(mutated_child)
    return selected_individuals


def crossover(individual_1, individual_2):
    crossover_point = random.randint(0, len(individual_1) - 1)
    child = individual_1[:crossover_point] + individual_2[crossover_point:]
    return child


def mutation(individual, mutation_probability=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_probability:
            individual[i] = 1 - individual[i]
    return individual


def ga(max_weight, items, population_size=100, generations=100):
    population = create_initial_population(population_size, items)
    for i in range(generations):
        population = selection(population, items, max_weight)
    best_individual = max(population, key=lambda x: fitness(x, items, max_weight))
    best_value = fitness(best_individual, items, max_weight)
    return best_individual, best_value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', type=str, default='ga')
    parser.add_argument('--file', type=str)
    args = parser.parse_args()
    max_weight, items = read_input_file('items.txt')
    best_individual, best_value = ga(max_weight, items)
    print('Best individual:', best_individual)
    print('Best value:', best_value)
