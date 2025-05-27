def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    def find(node):
        if node not in group_by_node:
            group_by_node[node] = node
            return node
        if group_by_node[node] == node:
            return node
        group_by_node[node] = find(group_by_node[node])
        return group_by_node[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            group_by_node[root1] = root2

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        if find(u) != find(v):
            mst_edges.add(edge)
            union(u, v)

    return mst_edges
```