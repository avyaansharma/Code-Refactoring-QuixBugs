
from collections import deque
import sys

class Node:
    def __init__(self, name, value=None, children=None):
        self.name = name
        self.value = value
        self.children = children if children is not None else []

def shortest_path_length(length_by_edge, start_node, end_node):
    """
    Calculate the shortest path length between two nodes in a graph.

    Args:
        length_by_edge (dict): A dictionary representing the graph where keys are tuples of nodes (u, v)
                                and values are the edge lengths.
        start_node (Node): The starting node.
        end_node (Node): The destination node.

    Returns:
        int: The shortest path length between the start and end nodes. Returns sys.maxsize if no path exists.
    """

    if start_node is end_node:
        return 0

    distances = {start_node: 0}
    queue = deque([start_node])

    while queue:
        current_node = queue.popleft()

        for (u, v), length in length_by_edge.items():
            if u is current_node and v not in distances:
                distances[v] = distances[u] + length
                queue.append(v)
            elif v is current_node and u not in distances:
                 distances[u] = distances[v] + length
                 queue.append(u)

    return distances.get(end_node, sys.maxsize)


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
