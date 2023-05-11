import random
import math

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
cities = [(60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
          (100, 160), (200, 160), (140, 140), (40, 120), (100, 120),
          (180, 100), (60, 80), (120, 80), (180, 60), (20, 40),
          (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
start_temp = 100
end_temp = 0.1
cooling_rate = 0.99
num_iterations = 1000

# Initialize current solution
current_route = list(range(len(cities)))
random.shuffle(current_route)
current_cost = cost(current_route, cities)

# Define simulated annealing algorithm
def simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations):
    best_route = current_route
    best_cost = current_cost
    temp = start_temp
    for i in range(num_iterations):
        neighbor_route = list(current_route)
        # Swap two random cities
        index1 = random.randint(0, len(neighbor_route) - 1)
        index2 = random.randint(0, len(neighbor_route) - 1)
        neighbor_route[index1], neighbor_route[index2] = neighbor_route[index2], neighbor_route[index1]
        neighbor_cost = cost(neighbor_route, cities)
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

# Run simulated annealing
best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations)

# Print solution
print("Best route found: ", best_route)
print("Cost of best route: ", best_cost)