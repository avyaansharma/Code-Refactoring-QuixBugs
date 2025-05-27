from collections import defaultdict
import heapq

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.val})"

def shortest_path_length(length_by_edge, start, end):
    """
    Find the shortest path length between two nodes in a graph.

    Args:
        length_by_edge (dict): A dictionary where keys are tuples of nodes
                              representing edges and values are the lengths of
                              the edges.
        start (Node): The starting node.
        end (Node): The ending node.

    Returns:
        int: The shortest path length between the start and end nodes.
             Returns float('inf') if no path exists.
    """

    graph = defaultdict(list)
    for (u, v), weight in length_by_edge.items():
        graph[u].append((v, weight))

    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    pq = [(0, start)]  # Priority queue: (distance, node)

    while pq:
        dist, u = heapq.heappop(pq)

        if dist > distances[u]:
            continue

        if u == end:
            return dist

        for v, weight in graph[u]:
            if distances[v] > distances[u] + weight:
                distances[v] = distances[u] + weight
                heapq.heappush(pq, (distances[v], v))

    return float('inf')


def main():
 
    node1 = Node("1")
    node5 = Node("5")
    node4 = Node("4", None, [node5])
    node3 = Node("3", None, [node4])
    node2 = Node("2", None, [node1, node3, node4])
    node0 = Node("0", None, [node2, node5])

    length_by_edge = {
        (node0, node2): 3,
        (node0, node5): 10,
        (node2, node1): 1,
        (node2, node3): 2,
        (node2, node4): 4,
        (node3, node4): 1,
        (node4, node5): 1
    }

    # Case 1: One path
    # Output: 4
    result =  shortest_path_length(length_by_edge, node0, node1)
    print(result)

    # Case 2: Multiple path
    # Output: 7
    result = shortest_path_length(length_by_edge, node0, node5)
    print(result)

    # Case 3: Start point is same as end point
    # Output: 0
    result = shortest_path_length(length_by_edge, node2, node2)
    print(result)

    # Case 4: Unreachable path
    # Output: INT_MAX
    result = shortest_path_length(length_by_edge, node1, node5)
    print(result)

if __name__ == "__main__":
    main()
