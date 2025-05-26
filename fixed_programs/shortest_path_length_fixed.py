```python
from heapq import *

def shortest_path_length(length_by_edge, startnode, goalnode):
    unvisited_nodes = [(0, startnode)]
    heapify(unvisited_nodes)
    visited_nodes = set()
    node_distances = {startnode: 0}

    while unvisited_nodes:
        distance, node = heappop(unvisited_nodes)

        if node == goalnode:
            return distance

        if node in visited_nodes:
            continue

        visited_nodes.add(node)

        for nextnode in get_neighbors(node, length_by_edge):
            if (node, nextnode) not in length_by_edge:
                continue
            
            new_distance = distance + length_by_edge[node, nextnode]

            if nextnode not in node_distances or new_distance < node_distances[nextnode]:
                node_distances[nextnode] = new_distance
                heappush(unvisited_nodes, (new_distance, nextnode))

    return float('inf')


def get_neighbors(node, length_by_edge):
    neighbors = set()
    for (start, end) in length_by_edge:
        if start == node:
            neighbors.add(end)
    return neighbors
```