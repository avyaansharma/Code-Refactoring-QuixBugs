import collections

def topological_ordering(nodes):
    in_degree = {}
    for node in nodes:
        in_degree[node] = 0

    for node in nodes:
        for neighbor in node.outgoing_nodes:
            in_degree[neighbor] += 1

    queue = collections.deque([node for node in nodes if in_degree[node] == 0])
    ordered_nodes = []

    while queue:
        node = queue.popleft()
        ordered_nodes.append(node)

        for neighbor in node.outgoing_nodes:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered_nodes) != len(nodes):
        return None 

    return ordered_nodes
