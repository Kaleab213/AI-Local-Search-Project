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

# Define succesor function

def get_successor(graph):
    population = []
    current = random.choice(cities)
    goal = current
    for _ in range(50):

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

# Initialize cities and parameters
# cities = [(60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
#           (100, 160), (200, 160), (140, 140), (40, 120), (100, 120),
#           (180, 100), (60, 80), (120, 80), (180, 60), (20, 40),
#           (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]




# Define simulated annealing algorithm
def simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations):
    best_route = current_route
    best_cost = current_cost
    temp = start_temp
    for i in range(num_iterations):
        # get succosor route and cost
        neighbor_cost, allvisted, neighbor_route = get_successor(graph)

        # Accept the neighbor if it has a lower cost or with a certain probability according to the temperature
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temp):
            current_route = neighbor_route
            current_cost = neighbor_cost
        # Update the best solution if necessary
        if current_cost < best_cost:
            best_route = current_route
            best_cost = current_cost
        # Cool down the temperature
        temp *= cooling_rate
        if temp < end_temp:
            break
    return best_route, best_cost

if __name__ == "__main__":
    # Initialize current solution

    current_cost, visited,  current_route = get_successor(graph)

    start_temp = 100
    end_temp = 0.1
    cooling_rate = 0.69
    num_iterations = 10000
    # Run simulated annealing
    best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations)

    # Print solution
    print("Best route found: ", best_route)
    print("Cost of best route: ", best_cost)