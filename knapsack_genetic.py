import argparse
import random

from knapsack import initialize_population, evaluate_fitness, read_input_file


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



