from  graph import Graph
from math import ceil, floor
import random
import argparse


# Create the command line argument parser
parser = argparse.ArgumentParser(description="TSP Solver")
parser.add_argument("--algorithm", type=str, default="ga", help="algorithm to be used (default: ga: genetic, sa: simulated anneheling, hc: hill climbing )")
parser.add_argument("--file", type=str, default="cities.txt", help="file containing city list (default: cities.txt)")

# Parse the provided command line arguments
args = parser.parse_args()

# Access the arguments using args.algorithm and args.file
cities_file = open(args.file, "r")
cities = []
cities_graph =Graph()

for line in cities_file:
    arr = line.split()
    if len(arr) == 3:
        city, latitude, longitude = arr
    else:
        latitude, longitude = arr[-2:]
        city = ""
        for _ in arr[:-3]:
            city += _ +  " "
        city += arr[-3]
    cities.append(city)
    node = cities_graph.create_node(city, float(latitude), float(longitude))
    cities_graph.insert_node(node)


# manually adding edges beteween the cities in romania from page 83rd of the textbook

cities_graph.insert_edge_by_item('Oradea',151,'Sibiu')
cities_graph.insert_edge_by_item('Oradea',71,'Zerind')
cities_graph.insert_edge_by_item('Zerind',75,'Arad')
cities_graph.insert_edge_by_item('Arad',140,'Sibiu')
cities_graph.insert_edge_by_item('Arad',118,'Timisoara')
cities_graph.insert_edge_by_item('Sibiu',99,'Fagaras')
cities_graph.insert_edge_by_item('Sibiu',80,'Rimnicu Vilcea')
cities_graph.insert_edge_by_item('Timisoara',111,'Lugoj')
cities_graph.insert_edge_by_item('Lugoj',70,'Mehadia')
cities_graph.insert_edge_by_item('Mehadia',75,'Drobeta')
cities_graph.insert_edge_by_item('Drobeta',120,'Craiova')
cities_graph.insert_edge_by_item('Craiova',138,'Pitesti')
cities_graph.insert_edge_by_item('Rimnicu Vilcea',97,'Pitesti')
cities_graph.insert_edge_by_item('Rimnicu Vilcea',146,'Craiova')
cities_graph.insert_edge_by_item('Fagaras',211,'Bucharest')
cities_graph.insert_edge_by_item('Pitesti',101,'Bucharest')
cities_graph.insert_edge_by_item('Bucharest',90,'Urziceni')
cities_graph.insert_edge_by_item('Urziceni',98,'Hirsova')
cities_graph.insert_edge_by_item('Urziceni',142,'Vaslui')
cities_graph.insert_edge_by_item('Hirsova',86,'Eforie')
cities_graph.insert_edge_by_item('Vaslui',92,'Iasi')
cities_graph.insert_edge_by_item('Iasi',87,'Neamt')
cities_graph.insert_edge_by_item('Giurgiu',90,'Bucharest')

graph = cities_graph.graphdict()
def tsp_fitness(individual, graph):
    
    distance = 0
    for i in range(len(individual)-1):
        current_node = individual[i]
        next_node = individual[i+1]
        edge_weight = graph[current_node][next_node]
        distance += edge_weight
    return distance

def get_intial_path(graph):
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


if __name__ == "__main__":
    from tsp_genetic import *
    from tsp_simulated import simulated_annealing
    from tsp_optimal import optimal_algorithm
    from tsp_hill import hill_climbing
    if args.algorithm == 'ga':
        path, cost, visited = geneticAlgorithm(population, tsp_fitness, graph)
        print("genetic algorithm")
        print("cost for best route: ", cost)
        print("path for best route: ", path)
    if args.algorithm == 'sa':
        # Initialize current solution

        current_cost, visited,  current_route = get_intial_path(graph)

        start_temp = 100
        end_temp = 0.1
        cooling_rate = 0.99
        num_iterations = 10000
        # Run simulated annealing
        best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations)

        # Print solution
        print("simulated anneheling algorithm")
        print("cost for best route: ", best_cost)
        print("path for best route: ", best_route)
    if args.algorithm == 'hc':
        num_iterations = 500

        # Initialize current solution
        current_cost, visted, current_route = get_intial_path(graph)

        cost, path= hill_climbing(current_route, current_cost, num_iterations, graph)
        print("hill climbing algorithm")
        print("cost for best route: ", cost)
        print("path for best route: ", path)
    if args.algorithm == 'opt':
        node = random.choice(cities)
        cost, visited, path = optimal_algorithm(graph, node)
        print("optimal algorithm")
        print("cost for best route: ", cost)
        print("path for best route: ", path)




