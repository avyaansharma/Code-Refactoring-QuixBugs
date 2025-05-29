from collections import defaultdict

def shortest_paths(start, graph):
    """
    Compute shortest paths from start node to all other nodes in the graph.

    Args:
        start: The starting node.
        graph: A dictionary representing the graph where keys are tuples of (node1, node2)
               representing an edge, and values are the edge weights.

    Returns:
        A dictionary where keys are nodes and values are the shortest path distances
        from the start node.  Returns None if a negative cycle is detected.
    """

    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0

    nodes = set()
    for u, v in graph:
        nodes.add(u)
        nodes.add(v)
    
    # Bellman-Ford Algorithm
    for _ in range(len(nodes) - 1):
        for (u, v), weight in graph.items():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    # Check for negative cycles
    for (u, v), weight in graph.items():
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            return None  # Negative cycle detected

    return dict(distances)

def main():
    # Case 1: Graph with multiple paths
    # Output: {'A': 0, 'C': 3, 'B': 1, 'E': 5, 'D': 10, 'F': 4}
    graph = {
        ('A', 'B'): 3,
        ('A', 'C'): 3,
        ('A', 'F'): 5,
        ('C', 'B'): -2,
        ('C', 'D'): 7,
        ('C', 'E'): 4,
        ('D', 'E'): -5,
        ('E', 'F'): -1
    }
    result =  shortest_paths('A', graph)
    for path in result:
        print(path, result[path], end=" ")
    print()

    # Case 2: Graph with one path
    # Output: {'A': 0, 'C': 3, 'B': 1, 'E': 5, 'D': 6, 'F': 9}
    graph2 = {
        ('A', 'B'): 1,
        ('B', 'C'): 2,
        ('C', 'D'): 3,
        ('D', 'E'): -1,
        ('E', 'F'): 4
    }
    result =  shortest_paths('A', graph2)
    for path in result:
        print(path, result[path], end=" ")
    print()

    # Case 3: Graph with cycle
    # Output: {'A': 0, 'C': 3, 'B': 1, 'E': 1, 'D': 0, 'F': 5}
    graph3 = {
        ('A', 'B'): 1,
        ('B', 'C'): 2,
        ('C', 'D'): 3,
        ('D', 'E'): -1,
        ('E', 'D'): 1,
        ('E', 'F'): 4
    }
    result =  shortest_paths('A', graph3)
    for path in result:
        print(path, result[path], end=" ")
    print()


if __name__ == "__main__":
    main()
