import collections

def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    def find(node):
        if node not in group_by_node:
            group_by_node[node] = node
        if group_by_node[node] != node:
            group_by_node[node] = find(group_by_node[node])
        return group_by_node[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            group_by_node[root1] = root2
            return True
        return False

    sorted_edges = sorted(weight_by_edge.items(), key=lambda item: item[1])

    for edge, weight in sorted_edges:
        u, v = edge
        if union(u, v):
            mst_edges.add(edge)

    return mst_edges
