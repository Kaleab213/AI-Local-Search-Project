import random
import math
from tsp import graph, cities
from tsp_genetic import tsp_fitness

# function to intialize the frist path to start with
def get_initial_path(graph):
    population = []
    current = random.choice(cities)
    goal = current
    for _ in range(20):

        unvisited_cities = set(cities)
        unvisited_cities.remove(current)
        path = [current]
        allvisited = 0

        while unvisited_cities:
            neighbors = list(graph[current].keys())
            good_neighbors = [neighbor for neighbor in neighbors if neighbor in unvisited_cities]

            if good_neighbors:
                random_neighbor = random.choice(good_neighbors)
                unvisited_cities.remove(random_neighbor)
            else:
                random_neighbor = random.choice(neighbors)

            path.append(random_neighbor)
            current = random_neighbor
            allvisited += 1

        while current != goal:
            neighbors = list(graph[current].keys())

          
            random_neighbor = random.choice(neighbors)

            path.append(random_neighbor)
            current = random_neighbor
            allvisited += 1
        
        population.append((tsp_fitness(path, graph), allvisited, path) )
    return sorted(population)[0]


# function to get successors from given path
def get_successor(graph, prev_path):
    successors = []
    
    goal = prev_path[0]
    for _ in range(10):
        # choose one random index
        rand_ind = random.randint(1, len(prev_path) - 1)
        path = prev_path[:rand_ind]     # intilzing path with prev_path upto selected index
        current = prev_path[rand_ind - 1]

        # intialize unvisted cities
        unvisited_cities = set(cities).difference(set(path)) 
        allvisited = 0

        while unvisited_cities:
            neighbors = list(graph[current].keys())
            good_neighbors = [neighbor for neighbor in neighbors if neighbor in unvisited_cities]

            if good_neighbors:
                random_neighbor = random.choice(good_neighbors)
                unvisited_cities.remove(random_neighbor)
            else:
                random_neighbor = random.choice(neighbors)

            path.append(random_neighbor)
            current = random_neighbor
            allvisited += 1

        while current != goal:
            neighbors = list(graph[current].keys())

          
            random_neighbor = random.choice(neighbors)

            path.append(random_neighbor)
            current = random_neighbor
            allvisited += 1
        
        successors.append((tsp_fitness(path, graph), allvisited, path) )
    return sorted(successors)[0]







# Define hill climbing algorithm
def hill_climbing(current_route, current_cost, num_iterations, graph):
    best_route = current_route
    best_cost = current_cost
    for i in range(num_iterations):
        neighbor_cost, all_visited, neighbor_route = get_successor(graph, best_route)
        if neighbor_cost < current_cost:
            current_route = neighbor_route
            current_cost = neighbor_cost
        # Update the best solution if necessary
        if current_cost < best_cost:
            best_route = current_route
            best_cost = current_cost
    return best_route, best_cost


if __name__ == "__main__":

    num_iterations = 500

    # Initialize current solution
    current_cost, visted, current_route = get_initial_path(graph)

    # Run hill climbing
    best_route, best_cost = hill_climbing(current_route, current_cost, num_iterations, graph)

    # Print solution
    print("Best route found: ", best_route)
    print("Cost of best route: ", best_cost)