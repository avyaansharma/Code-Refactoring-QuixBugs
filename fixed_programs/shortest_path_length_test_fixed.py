```python
from typing import Dict, Tuple
import heapq
import math

class Node:
    def __init__(self, val, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"Node({self.val})"


def shortest_path_length(length_by_edge: Dict[Tuple[Node, Node], int], start_node: Node, end_node: Node) -> int:
    """
    Finds the shortest path length from start_node to end_node in a graph.

    Args:
        length_by_edge: A dictionary that maps an edge (u, v) to its length.
        start_node: The starting node.
        end_node: The destination node.

    Returns:
        The shortest path length, or infinity if no path exists.
    """
    dist = {node: float('inf') for node in get_all_nodes(length_by_edge)}
    dist[start_node] = 0
    pq = [(0, start_node)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v in get_neighbors(u, length_by_edge):
            weight = length_by_edge.get((u, v), float('inf'))
            if weight == float('inf'):
                continue
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))

    return dist[end_node]

def get_all_nodes(length_by_edge: Dict[Tuple[Node, Node], int]) -> set[Node]:
    """
    Gets all nodes in the graph from the length_by_edge dictionary.

    Args:
        length_by_edge: A dictionary that maps an edge (u, v) to its length.

    Returns:
        A set of all nodes in the graph.
    """
    nodes = set()
    for u, v in length_by_edge:
        nodes.add(u)
        nodes.add(v)
    return nodes

def get_neighbors(node: Node, length_by_edge: Dict[Tuple[Node, Node], int]) -> list[Node]:
    """
    Gets all neighbors of a node.

    Args:
        node: The node to get neighbors for.
        length_by_edge: A dictionary that maps an edge (u, v) to its length.

    Returns:
        A list of all neighbors of the node.
    """
    neighbors = []
    for u, v in length_by_edge:
        if u == node:
            neighbors.append(v)
    return neighbors

def main():
 
    node1 = Node("1")
    node5 = Node("5")
    node4 = Node("4")
    node3 = Node("3")
    node2 = Node("2")
    node0 = Node("0")

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
```