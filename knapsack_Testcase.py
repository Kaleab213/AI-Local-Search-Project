import argparse
import csv
import random
import math
import time

class Item:
    def __init__(self, name, weight, value, n_items):
        self.name = name
        self.weight = weight
        self.value = value
        self.n_items = n_items


def generate_random_items(num_items):
    items = []
    for i in range(num_items):
        name = f"Item{i+1}"
        weight = random.uniform(1, 10)
        value = random.randint(1, 100)
        n_items = random.randint(0, 5)
        item = Item(name, weight, value, n_items)
        items.append(item)
    return items


def read_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    max_weight = int(lines[0].strip())

    items = []
    for line in lines[2:]:
        line = line.strip()
        if line:
            name, weight, value, n_items = line.split(',')
            item = Item(name, float(weight), int(value), int(n_items))
            items.append(item)

    return max_weight, items

def initialize_population(items, population_size):
    population = []
    for _ in range(population_size):
        chromosome = []
        for item in items:
            n = random.randint(0, item.n_items)
            chromosome.append(n)
        population.append(chromosome)
    return population


def evaluate_fitness(chromosome, items, max_weight):
    total_weight = 0
    total_value = 0
    for i in range(len(chromosome)):
        n = chromosome[i]
        item = items[i]
        total_weight += n * item.weight
        total_value += n * item.value
    if total_weight > max_weight:
        total_value = 0
    return total_value


def selection(population, items, max_weight):
    fitness_values = [evaluate_fitness(
        chromosome, items, max_weight) for chromosome in population]
    max_fitness = max(fitness_values)
    total_fitness = sum(fitness_values)

    if total_fitness == 0:
        # Assign equal probabilities if total fitness is zero
        probabilities = [1 / len(population)] * len(population)
    else:
        probabilities = [fitness / total_fitness for fitness in fitness_values]

    selected = []
    for _ in range(len(population)):
        r = random.random()
        index = 0
        while r > 0:
            r -= probabilities[index]
            index += 1
        selected.append(population[index - 1])
    return selected


def crossover(parent1, parent2):
    if len(parent1) <= 2:
        return parent1, parent2

    crossover_point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(chromosome, items, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.randint(0, items[i].n_items)
    return chromosome


def genetic_algorithm(max_weight, items, population_size=100, num_generations=100, mutation_rate=0.1):
    population = initialize_population(items, population_size)
    best_solution = None
    best_fitness = 0

    for generation in range(num_generations):
        # Evaluate fitness of each chromosome
        fitness_values = [evaluate_fitness(
            chromosome, items, max_weight) for chromosome in population]

        # Find the best solution in the current generation
        max_fitness = max(fitness_values)
        if max_fitness > best_fitness:
            best_solution = population[fitness_values.index(max_fitness)]
            best_fitness = max_fitness

        # Perform selection
        selected = selection(population, items, max_weight)

        # Create new population through crossover
        offspring = []
        while len(offspring) < population_size:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Apply mutation
        for i in range(len(offspring)):
            offspring[i] = mutate(offspring[i], items, mutation_rate)

        # Replace the old population with the new offspring
        population = offspring

    return best_solution


def generate_random_solution(items):
    solution = []
    for item in items:
        n = random.randint(0, item.n_items)
        solution.append(n)
    return solution


def generate_neighbor_solution(solution, items):
    neighbor = solution.copy()
    index = random.randint(0, len(solution) - 1)
    item = items[index]
    neighbor[index] = random.randint(0, item.n_items)
    return neighbor


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
# To find Solution Quality 
def calculate_total_value(solution, items):
    total_value = 0
    for i, count in enumerate(solution):
        item = items[i]
        total_value += count * item.value
    return total_value



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', help='Algorithm to use (ga, hc, sa)')
    parser.add_argument('--num_items', type=int, help='Number of items')
    parser.add_argument('--file', help='Input file name')
    args = parser.parse_args()

    if args.file:
        max_weight, items = read_input_file(args.file)
    else:
        max_weight = 100
        items = generate_random_items(args.num_items)

    if args.algorithm == 'ga':
        start_time = time.time()
        solution = genetic_algorithm(max_weight, items)
        end_time = time.time()
        total_value = evaluate_fitness(solution, items, max_weight)
        print("Items:")
        for i, count in enumerate(solution):
            item = items[i]
            print(f"{item.name}: {count}  its value: {count * item.value}")
        print(f"Total value: {total_value}")
        print(f"Execution time: {end_time - start_time:.3f} seconds")
    elif args.algorithm == 'hc':
        start_time = time.time()
        solution = hill_climbing(max_weight, items)
        end_time = time.time()
        total_value = evaluate_fitness(solution, items, max_weight)
        print("Items:")
        for i, count in enumerate(solution):
            item = items[i]
            print(f"{item.name}: {count}  its value: {count * item.value}")
        print(f"Total value: {total_value}")
        print(f"Execution time: {end_time - start_time:.3f} seconds")
        total_value = calculate_total_value(solution, items)
        print(f"Total Value: {total_value}")
    elif args.algorithm == 'sa':
        start_time = time.time()
        solution = simulated_annealing(max_weight, items)
        end_time = time.time()
        total_value = evaluate_fitness(solution, items, max_weight)
        print("Items:")
        for i, count in enumerate(solution):
            item = items[i]
            print(f"{item.name}: {count}  its value: {count * item.value}")
        print(f"Total value: {total_value}")
        print(f"Execution time: {end_time - start_time:.3f} seconds")
    else:
        print("Invalid algorithm specified.")
        return

if __name__ == '__main__':
    main()
    
    
# To run the program use 
#   choose your algorithm from hc, sa, ga  and tell number items in last row

 #       this command   python knapsack_Testcase.py --algorithm ga --num_items 20