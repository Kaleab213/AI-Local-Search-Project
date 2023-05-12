import random
import math
from tsp import graph
from tsp_genetic import cities


def tsp_fitness(individual, graph):
    
    distance = 0
    for i in range(len(individual)-1):
        current_node = individual[i]
        next_node = individual[i+1]
        edge_weight = graph[current_node][next_node]
        distance += edge_weight
    return distance

def get_successor(graph):
    population = []
    current = random.choice(cities)
    goal = current
    for _ in range(5):

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
            good_neighbors = [neighbor for neighbor in neighbors if neighbor in unvisited_cities]

            if good_neighbors:
                random_neighbor = random.choice(good_neighbors)
            else:
                random_neighbor = random.choice(neighbors)

            path.append(random_neighbor)
            current = random_neighbor
            allvisited += 1
        
        population.append((tsp_fitness(path, graph), allvisited, path) )
    return sorted(population)[0]

# Define distance function
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Define cost function
def cost(route, cities):
    total = 0
    for i in range(len(route)):
        total += distance(cities[route[i]], cities[route[(i + 1) % len(route)]])
    return total

# Initialize cities and parameters
# cities = [(60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
#           (100, 160), (200, 160), (140, 140), (40, 120), (100, 120),
#           (180, 100), (60, 80), (120, 80), (180, 60), (20, 40),
#           (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
num_iterations = 500

# Initialize current solution
current_cost, visted, current_route = get_successor(graph)


# Define hill climbing algorithm
def hill_climbing(current_route, current_cost, num_iterations, graph):
    best_route = current_route
    best_cost = current_cost
    for i in range(num_iterations):
        neighbor_route = list(current_route)
        # Swap two random cities
        # index1 = random.randint(0, len(neighbor_route) - 1)
        # index2 = random.randint(0, len(neighbor_route) - 1)
        # neighbor_route[index1], neighbor_route[index2] = neighbor_route[index2], neighbor_route[index1]
        # neighbor_cost = cost(neighbor_route, cities)
        # Accept the neighbor if it has a lower cost
        neighbor_cost, all_visited, neighbor_route = get_successor(graph)
        if neighbor_cost < current_cost:
            current_route = neighbor_route
            current_cost = neighbor_cost
        # Update the best solution if necessary
        if current_cost < best_cost:
            best_route = current_route
            best_cost = current_cost
    return best_route, best_cost


if __name__ == "__main__":

    # Run hill climbing
    best_route, best_cost = hill_climbing(current_route, current_cost, num_iterations, graph)

    # Print solution
    print("Best route found: ", best_route)
    print("Cost of best route: ", best_cost)