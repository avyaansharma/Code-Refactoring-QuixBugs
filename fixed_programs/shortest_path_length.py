from heapq import *

def shortest_path_length(length_by_edge, startnode, goalnode):
    unvisited_nodes = [(0, startnode)]
    heapify(unvisited_nodes)
    visited_nodes = set()
 
    while unvisited_nodes:
        distance, node = heappop(unvisited_nodes)
        if node == goalnode:
            return distance

        if node in visited_nodes:
            continue

        visited_nodes.add(node)

        for nextnode in get_neighbors(length_by_edge, node):
            if nextnode in visited_nodes:
                continue

            new_distance = distance + length_by_edge.get((node, nextnode), float('inf'))

            found = False
            for i, (dist, n) in enumerate(unvisited_nodes):
                if n == nextnode:
                    if new_distance < dist:
                        unvisited_nodes[i] = (new_distance, nextnode)
                        heapify(unvisited_nodes)
                    found = True
                    break
            
            if not found:
                heappush(unvisited_nodes, (new_distance, nextnode))
    return float('inf')

def get_neighbors(length_by_edge, node):
    neighbors = []
    for (u, v) in length_by_edge:
        if u == node:
            neighbors.append(v)
    return neighbors
