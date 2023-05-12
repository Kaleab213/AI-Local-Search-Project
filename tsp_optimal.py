from tsp import graph




def optimal_algorithm(graph, node):
    edge_dict = graph
    unvisited_node = set([node for node in graph])
    start = node
    def helper(node, start, prev_cost, prev_visited, path):
        if node == start and not unvisited_node:
            return prev_cost, prev_visited, path.copy()
        cost, visited, main_path = float("inf"), float("inf"), []
        items = list(edge_dict[node].items())
        for neigh, val in items:
            del edge_dict[node][neigh]
            removed = False
            if neigh in unvisited_node:
                unvisited_node.remove(neigh)
                removed = True
            path.append(neigh)
            new_cost, new_visited, new_path = helper(neigh, start, prev_cost + val, prev_visited + 1, path)
            cost, visited, main_path = min((cost, visited, main_path), (new_cost, new_visited, new_path))
            edge_dict[node][neigh] = val
            if removed:
                unvisited_node.add(neigh)
            path.pop()
        return cost, visited, main_path
    return helper(node, node, 0, 0, [])



if __name__ == "__main__":
    cost, visited, path = optimal_algorithm(graph, "Arad")
    print("cost of best route: ", cost)
    print("path of best route: ", path)
    print("num of visted nodes of best route: ", visited)

    
    




