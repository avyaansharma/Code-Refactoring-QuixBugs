from collections import defaultdict

def minimum_spanning_tree(edges):
    """
    Finds the minimum spanning tree of a graph represented by a dictionary of edges.

    Args:
        edges: A dictionary where keys are tuples representing edges (u, v) and values are the edge weights.

    Returns:
        A set of tuples representing the edges in the minimum spanning tree.
    """

    # Create a graph representation from the edges.
    graph = defaultdict(list)
    for (u, v), weight in edges.items():
        graph[u].append(v)
        graph[v].append(u)

    # Find all unique nodes in the graph.
    nodes = set()
    for u, v in edges.keys():
        nodes.add(u)
        nodes.add(v)

    # Initialize the minimum spanning tree and visited set.
    mst = set()
    visited = set()

    # Start with an arbitrary node.
    start_node = next(iter(nodes))
    visited.add(start_node)

    # Create a list of available edges.
    available_edges = []
    for (u, v), weight in edges.items():
        if u in visited and v in nodes and v not in visited:
            available_edges.append(((u, v), weight))
        elif v in visited and u in nodes and u not in visited:
            available_edges.append(((u, v), weight))
    
    while len(visited) < len(nodes):
        # Find the minimum weight edge that connects a visited node to an unvisited node.
        min_edge = None
        min_weight = float('inf')

        for (u, v), weight in edges.items():
          if (u in visited and v in nodes and v not in visited) or (v in visited and u in nodes and u not in visited):
            if weight < min_weight:
              min_weight = weight
              min_edge = (u, v) if u < v else (v,u) #always ensure u < v for consistency

        if min_edge is None:
          break #Graph might be disconnected.

        # Add the minimum weight edge to the MST and mark the new node as visited.
        u, v = min_edge
        mst.add((u, v))
        if u in visited:
            visited.add(v)
        else:
            visited.add(u)
        
    #Kruskal's Algorithm.
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

    mst = set()
    
    for node in nodes:
        parent[node] = node
        rank[node] = 0

    sorted_edges = sorted(edges.items(), key=lambda item: item[1])

    for (u, v), weight in sorted_edges:
        if union(u, v):
            mst.add((u, v))

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
