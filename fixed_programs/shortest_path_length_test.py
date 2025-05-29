from collections import defaultdict
import heapq

class Node:
    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = children if children is not None else []

    def __repr__(self):
        return f"Node({self.name})"

INT_MAX = float('inf')

def shortest_path_length(length_by_edge, start_node, end_node):
    """
    Calculate the shortest path length between two nodes in a graph.

    Args:
        length_by_edge (dict): A dictionary where keys are tuples of nodes representing edges,
                                and values are the lengths of those edges.
        start_node (Node): The starting node.
        end_node (Node): The destination node.

    Returns:
        int: The shortest path length, or INT_MAX if no path exists.
    """

    if start_node == end_node:
        return 0

    # Build the graph as an adjacency list
    graph = defaultdict(list)
    for (u, v), weight in length_by_edge.items():
        graph[u].append((v, weight))

    # Initialize distances with infinity for all nodes except the start node
    distances = {node: INT_MAX for node in graph}
    distances[start_node] = 0

    # Use Dijkstra's algorithm to find the shortest path
    priority_queue = [(0, start_node)]  # (distance, node)

    while priority_queue:
        dist, current_node = heapq.heappop(priority_queue)

        if dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            new_dist = distances[current_node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))

    # Return the shortest distance to the end node, or INT_MAX if unreachable
    return distances.get(end_node, INT_MAX)
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
    result = shortest_path_length(length_by_edge, node1, node5)
    print(result)

if __name__ == "__main__":
    main()
