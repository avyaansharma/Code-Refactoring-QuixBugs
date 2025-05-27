
from collections import defaultdict
import heapq

def shortest_paths(start, graph):
    distances = {node: float('inf') for edge in graph for node in edge}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        dist, u = heapq.heappop(pq)

        if dist > distances[u]:
            continue

        for edge, weight in graph.items():
            if edge[0] == u:
                v = edge[1]
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    heapq.heappush(pq, (distances[v], v))

    return distances


"""
Test shortest paths
""" 
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
    for path in sorted(result.keys()):
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
    for path in sorted(result.keys()):
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
    for path in sorted(result.keys()):
        print(path, result[path], end=" ")
    print()


if __name__ == "__main__":
    main()
