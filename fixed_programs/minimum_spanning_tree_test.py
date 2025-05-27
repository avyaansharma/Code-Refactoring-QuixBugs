from collections import defaultdict

def minimum_spanning_tree(graph):
    """
    Finds a minimum spanning tree in a graph.

    Args:
        graph: A dict of the form { (u, v): w, ... } where (u, v) is an edge
            between u and v and w is the weight of that edge.
            Ensure the graph is undirected by representing each edge in both directions if necessary.
            If the graph is empty or contains no edges, it returns an empty list.
    Returns:
        A set of edges in the minimum spanning tree.
        Returns an empty set if the graph is empty.
    """
    if not graph:
        return set()

    nodes = set()
    for edge in graph:
        u, v = edge
        nodes.add(u)
        nodes.add(v)

    if not nodes:
      return set()

    mst = set()
    edges = sorted(graph.items(), key=lambda item: item[1])  # Sort edges by weight

    parent = {node: node for node in nodes}  # Initialize parent for each node (Disjoint Set)

    def find(node):
        """Find the set that a node belongs to (with path compression)."""
        if parent[node] != node:
            parent[node] = find(parent[node])  # Path compression
        return parent[node]

    def union(node1, node2):
        """Merge the sets that node1 and node2 belong to."""
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            parent[root1] = root2
            return True
        return False

    for edge, weight in edges:
        u, v = edge
        if union(u, v):
            mst.add(edge)

    return mst
"""
Driver to test minimum spanning tree
"""
def main():
    # Case 1: Simple tree input.
    # Output: (1, 2) (3, 4) (1, 4)
    result = minimum_spanning_tree({
        (1, 2): 10,
        (2, 3): 15,
        (3, 4): 10,
        (1, 4): 10})
    for edge in result:
        print(edge),
    print()
 
    # Case 2: Strongly connected tree input.
    # Output: (2, 5) (1, 3) (2, 3) (4, 6) (3, 6)
    result = minimum_spanning_tree({
        (1, 2): 6,
        (1, 3): 1,
        (1, 4): 5,
        (2, 3): 5,
        (2, 5): 3,
        (3, 4): 5,
        (3, 5): 6,
        (3, 6): 4,
        (4, 6): 2,
        (5, 6): 6})
    for edge in result:
        print(edge),
    print()

    # Case 3: Minimum spanning tree input.
    # Output: (1, 2) (1, 3) (2, 4)
    result = minimum_spanning_tree({
            (1, 2): 6,
            (1, 3): 1,
            (2, 4): 2})
    for edge in result:
        print(edge),
    print()


if __name__ == "__main__":
    main()
