from collections import defaultdict

def shortest_path_lengths(n, graph):
    """
    Given a graph, return a dictionary of shortest path lengths between each pair of nodes.
    """
    dist = defaultdict(lambda: float('inf'))

    # Initialize distances
    for i in range(n):
        dist[(i, i)] = 0
    for (u, v), weight in graph.items():
        dist[(u, v)] = weight

    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[(i, j)] = min(dist[(i, j)], dist[(i, k)] + dist[(k, j)])

    # Check for negative cycles
    for i in range(n):
        if dist[(i, i)] < 0:
            return "Graph contains a negative cycle"
    
    # Filter out infinite distances for disconnected nodes.
    result = {}
    for i in range(n):
        for j in range(n):
            if dist[(i, j)] != float('inf'):
                result[(i, j)] = dist[(i, j)]

    return result


"""
Test shortest path lengths
""" 
def main():
    # Case 1: Basic graph input.
    # Output:
    graph = {
        (0, 2): 3,
        (0, 5): 5,
        (2, 1): -2,
        (2, 3): 7,
        (2, 4): 4,
        (3, 4): -5,
        (4, 5): -1
    }
    result =  shortest_path_lengths(6, graph)
    for node_pairs in result:
        print(node_pairs, result[node_pairs], end=" ")
    print()

    # Case 2: Linear graph input.
    # Output:
    graph2 = {
        (0, 1): 3,
        (1, 2): 5,
        (2, 3): -2,
        (3, 4): 7
    }
    result =  shortest_path_lengths(5, graph2)
    for node_pairs in result:
        print(node_pairs, result[node_pairs], end=" ")
    print()

    # Case 3: Disconnected graphs input.
    # Output:
    graph3 = {
        (0, 1): 3,
        (2, 3): 5
    }
    result =  shortest_path_lengths(4, graph3)
    for node_pairs in result:
        print(node_pairs, result[node_pairs], end=" ")
    print()

    # Case 4: Strongly connected graph input.
    graph4 = {
        (0, 1): 3,
        (1, 2): 5,
        (2, 0): -1
    }
    result =  shortest_path_lengths(3, graph4)
    for node_pairs in result:
        print(node_pairs, result[node_pairs], end=" ")
    print()


if __name__ == "__main__":
    main()
