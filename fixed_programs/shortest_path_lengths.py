from collections import defaultdict

def shortest_path_lengths(n, length_by_edge):
    """
    Calculates the length of the shortest path connecting every ordered pair of nodes in a directed graph using the Floyd-Warshall algorithm.

    Args:
        n: The number of nodes in the graph. The nodes are assumed to have ids 0..n-1.
        length_by_edge: A dict containing edge lengths keyed by an ordered pair of node ids (e.g., {(0, 1): 5, (1, 2): 3}).

    Returns:
        A dict containing shortest path lengths keyed by an ordered pair of node ids.  If no path exists between two nodes, the value will be float('inf').

    Raises:
        ValueError: If n is not a positive integer.
        TypeError: If length_by_edge is not a dictionary.
    """

    if not isinstance(n, int) or n <= 0:
        raise ValueError("The number of nodes 'n' must be a positive integer.")

    if not isinstance(length_by_edge, dict):
        raise TypeError("length_by_edge must be a dictionary.")
        
    length_by_path = defaultdict(lambda: float('inf'))

    # Initialize the shortest path lengths.  The distance from a node to itself is 0.  Distances corresponding to provided edges are initialized, too.
    for i in range(n):
        length_by_path[i, i] = 0

    for (u, v), length in length_by_edge.items():
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"Edge ({u}, {v}) contains invalid node indices. Node indices must be between 0 and n-1.")
        length_by_path[u, v] = length  # Initial edge lengths

    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Relax the distance between node i and node j through node k
                length_by_path[i, j] = min(
                    length_by_path[i, j],
                    length_by_path[i, k] + length_by_path[k, j]
                )

    return length_by_path
