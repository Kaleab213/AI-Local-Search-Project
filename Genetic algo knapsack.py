def genetic_algorithm(items, max_weight, length=100, total_generation=1000):
    # Initialize the total population
    total_total_population = []
    for i in range(length):
        for item in item:
            individual = [random.randint(0,item.n_items)]
        total_population.append(individual)

    counter = 0
    while counter < total_generation:
        # do the selection here
        fitness_values = [fitness(individual, items, max_weight) for individual in total_population]
        parents_indices = np.argsort(fitness_values)[-2:]
        parents = [total_population[j] for j in parents_indices]

        # do the crossover
        crossover_point = random.randint(1, len(items) - 1)
        child1 = parents[0][:crossover_point] + parents[1][crossover_point:]
        child2 = parents[1][:crossover_point] + parents[0][crossover_point:]

        # Mutate it
        index_mutation = random.randint(0, len(items) - 1)
        child1[index_mutation] = random.randint(0, items[index_mutation].n_items)
        child2[index_mutation] = random.randint(0, items[index_mutation].n_items)

        # Replace it
        total_population[-2:] = [child1, child2]
        counter += 1

    # Finally the best solution is returned
    best_solution = max(total_population, key=lambda s: fitness(s, items, max_weight))
    return best_solution
