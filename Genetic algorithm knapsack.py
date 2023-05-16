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


