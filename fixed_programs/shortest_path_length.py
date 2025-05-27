from heapq import *

def shortest_path_length(length_by_edge, startnode, goalnode):
    unvisited_nodes = [(0, startnode)]  # Priority queue containing (distance, node) pairs
    heapify(unvisited_nodes)
    visited_nodes = set()

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

            new_distance = distance + length_by_edge[(node, nextnode)]
            
            found = False
            for i in range(len(unvisited_nodes)):
                if unvisited_nodes[i][1] == nextnode:
                    if new_distance < unvisited_nodes[i][0]:
                        unvisited_nodes[i] = (new_distance, nextnode)
                        heapify(unvisited_nodes)  # Re-heapify after update
                    found = True
                    break

            if not found:
                heappush(unvisited_nodes, (new_distance, nextnode))

    return float('inf')


def get_neighbors(node, length_by_edge):
    neighbors = set()
    for start, end in length_by_edge:
        if start == node:
            neighbors.add(end)
    return neighbors
