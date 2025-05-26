```python
from collections import defaultdict

def topological_ordering(nodes):
    in_degree = defaultdict(int)
    graph = defaultdict(list)

    for node in nodes:
        for neighbor in node.outgoing_nodes:
            graph[node].append(neighbor)
            in_degree[neighbor] += 1

    queue = [node for node in nodes if in_degree[node] == 0]
    ordered_nodes = []

    while queue:
        node = queue.pop(0)
        ordered_nodes.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered_nodes) != len(nodes):
        return [] 

    return ordered_nodes
```