```python
from collections import defaultdict

def minimum_spanning_tree(graph):
    """
    Kruskal's algorithm to find the minimum spanning tree of a graph.

    Args:
        graph: A dictionary where keys are tuples representing edges (u, v)
               and values are the corresponding edge weights.

    Returns:
        A list of tuples representing the edges in the minimum spanning tree.
    """

    parent = {}
    rank = {}

    def find(i):
        if parent[i] == i:
            return i
        return find(parent[i])

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    mst = []
    edges = sorted(graph.items(), key=lambda item: item[1])

    # Initialize parent and rank for each node
    nodes = set()
    for edge in graph:
        u, v = edge
        nodes.add(u)
        nodes.add(v)

    for node in nodes:
        parent[node] = node
        rank[node] = 0

    for edge, weight in edges:
        u, v = edge
        if union(u, v):
            mst.append(edge)

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
```