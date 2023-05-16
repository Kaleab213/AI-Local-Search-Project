import random
import math
from tsp import graph
from tsp_genetic import tsp_fitness
from tsp_hill import get_successor, get_initial_path



def tsp_fitness(individual, graph):
    
    distance = 0
    for i in range(len(individual)-1):
        current_node = individual[i]
        next_node = individual[i+1]
        edge_weight = graph[current_node][next_node]
        distance += edge_weight
    return distance


# Define simulated annealing algorithm
def simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations):
    best_route = current_route
    best_cost = current_cost
    temp = start_temp
    for i in range(num_iterations):
        # get succosor route and cost
        neighbor_cost, allvisted, neighbor_route = get_successor(graph, best_route)

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

    current_cost, visited,  current_route = get_initial_path(graph)

    start_temp = 100
    end_temp = 0.1
    cooling_rate = 0.99
    num_iterations = 10000
    # Run simulated annealing
    best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations)

    # Print solution
    print("Best route found: ", best_route)
    print("Cost of best route: ", best_cost)