from math import ceil, floor
import random
from tsp import graph

cities = ["Eforie", "Mehadia", "Hirsova", "Drobeta", "Vaslui", "Craiova", "Sibiu", "Iasi", "Rimnicu Vilcea", "Neamt", "Fagaras", "Zerind", "Pitesti", "Oradea", "Giurgiu", "Arad", "Bucharest", "Timisoara", "Urziceni", "Lugoj"]
cities = list(set(cities))

population = []
current = random.choice(cities)
goal = current
for _ in range(201):

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
    
    
    population.append((path,allvisited) )

(individual,val) = random.choice(population)

def tsp_fitness(individual, graph):
    
    distance = 0
    for i in range(len(individual)-1):
        current_node = individual[i]
        next_node = individual[i+1]
        edge_weight = graph[current_node][next_node]
        distance += edge_weight
    return distance

def reproduce(x:list, y:list):
    slicer1 = 0
    slicer2 = 0
    for tup in population:
        if tup[0] == x:
            slicer1 = tup[1]
        if tup[0] == y:
            slicer2 = tup[1]
    while True:
        for i in range(slicer1, len(x)):
            for j in range(slicer2, len(y)):
                if x[i] in graph[y[j]]:
                    return x[: i+1] + y[j:]
        return x

def mutate(individual, graph):
    slicer = 0
    for i in range(len(individual)):
        if set(cities).issubset(set(individual[:i+1])):
            slicer = i + 1
            break
    mutated_individual = individual.copy()
    if len(mutated_individual) - 2 > slicer:
        index = random.randint(slicer, len(mutated_individual) - 2)
    elif len(mutated_individual) - 2 == slicer:
        index = slicer
    else:
        return mutated_individual
    city = mutated_individual[index]
    prev_city = mutated_individual[index - 1]
    next_city = mutated_individual[index + 1]
    neighbors = graph[city]
    # find a neighbor of city that is adjacent to both prev_city and next_city
    for neighbor in neighbors:
        if neighbor != prev_city and neighbor != next_city and \
           neighbor in graph[prev_city] and neighbor in graph[next_city]:
            # replace city with the neighbor
            mutated_individual[index] = neighbor
            break
    return mutated_individual

def randomSelection(popWithScores):
    length = len(popWithScores)
    y, _, _ = popWithScores[random.randint(0, length-1)]
    return y

def geneticAlgorithm(population, fitnessFn, graph):
    noOfIter = 0
    while noOfIter < 1000:
        newPopulation = list()
        popWithScores = []
        for i in range(len(population)-1):
            individual = population[i][0]
            allvisited = population[i][1]
            if isinstance(individual, list):
                val = fitnessFn(individual, graph)
                popWithScores.append((individual, val, allvisited))
        
        popWithScores.sort(key=lambda a:a[1])
        leng = len(popWithScores)
        halfway = floor(leng * 0.5)

        selectedPops = popWithScores[:halfway]
            
        newPopulation.extend([(x[0], x[2]) for x in selectedPops])
        for i in range(0, len(population) - halfway):
            x = randomSelection(selectedPops)
            y = randomSelection(selectedPops)

            child = reproduce(x, y)
            if(random.randint(1, 100) < 10):    # 10% probability
                child = mutate(child, graph)
            issubset = False
            for i in range(len(child)):
                if set(cities).issubset(set(child[:i+1])):
                    allvisited = i + 1
                    issubset = True
                    break
            if issubset:
                newPopulation.append((child, allvisited))

        population = newPopulation
        if len(population) == 0:
            return "Fail"
        noOfIter += 1
    return selectedPops[0]


if __name__ == "__main__":
    (individual, total_distance, _) = geneticAlgorithm(population, tsp_fitness, graph)
    print("total_distance_travelled: ", total_distance)
    print("the_fit_individual: ", individual)

