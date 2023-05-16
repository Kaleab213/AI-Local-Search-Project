import argparse
import csv
import random
import math

class Item:
    def __init__(self, name, weight, value, n_items):
        self.name = name
        self.weight = weight
        self.value = value
        self.n_items = n_items


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




# Genetic Algorithm

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






# To find Solution Quality 
def calculate_total_value(solution, items):
    total_value = 0
    for i, count in enumerate(solution):
        item = items[i]
        total_value += count * item.value
    return total_value
def main():
    from knapsack_simulated import simulated_annealing
    from knapsack_hill import hill_climbing
    from knapsack_genetic import genetic_algorithm
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', default="ga", help='Algorithm to use (ga, hc, sa)')
    parser.add_argument('--file', default="items.txt", help='Input file name')
    args = parser.parse_args()

    max_weight, items = read_input_file(args.file)

    if args.algorithm == 'ga':
        solution = genetic_algorithm(max_weight, items)
        total_value = evaluate_fitness(solution, items, max_weight)
        print("Items:")
        for i, count in enumerate(solution):
            item = items[i]
            print(f"{item.name}: {count}  its value: {count * item.value}")
        print(f"Total value: {total_value}")
    elif args.algorithm == 'hc':
        solution = hill_climbing(max_weight, items)
        total_value = evaluate_fitness(solution, items, max_weight)
        print("Items:")
        for i, count in enumerate(solution):
            item = items[i]
            print(f"{item.name}: {count}  its value: {count * item.value}")
        print(f"Total value: {total_value}")
        
        
    elif args.algorithm == 'sa':
        solution = simulated_annealing(max_weight, items)
        total_value = evaluate_fitness(solution, items, max_weight)
        print("Items:")
        for i, count in enumerate(solution):
            item = items[i]
            print(f"{item.name}: {count}  its value: {count * item.value}")
        print(f"Total value: {total_value}")
    else:
        print("Invalid algorithm specified.")
        return



if __name__ == '__main__':
    main()



