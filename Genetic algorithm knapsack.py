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


def hill_climbing(items, max_weight, iterations=1000):
    current_solution = [random.randint(0, item.n_items) for item in items]

    for _ in range(iterations):
        neighbor = copy.deepcopy(current_solution)
        mutation_index = random.randint(0, len(items) - 1)
        neighbor[mutation_index] = random.randint(0, items[mutation_index].n_items)

        if fitness(neighbor, items, max_weight) > fitness(current_solution, items, max_weight):
            current_solution = neighbor

    return current_solution


def simulated_annealing(items, max_weight, initial_temperature=100, cooling_rate=0.99, iterations=1000):
    current_solution = [random.randint(0, item.n_items) for item in items]
    temperature = initial_temperature

    for _ in range(iterations):
        neighbor = copy.deepcopy(current_solution)
        mutation_index = random.randint(0, len(items) - 1)
        neighbor[mutation_index] = random.randint(0, items[mutation_index].n_items)

        delta_fitness = fitness(neighbor, items, max_weight) - fitness(current_solution, items, max_weight)

        if delta_fitness > 0 or random.random() < np.exp(delta_fitness / temperature):
            current_solution = neighbor

        temperature *= cooling_rate

    return current_solution
