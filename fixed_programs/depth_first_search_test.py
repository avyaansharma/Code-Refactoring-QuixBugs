from .node import Node

def depth_first_search(start_node, target_node, visited = None):
    """
    Performs a depth-first search to find a path from a start node to a target node.

    Args:
        start_node: The node to start the search from.
        target_node: The node to search for.
        visited: A set to keep track of visited nodes (used for cycle detection).

    Returns:
        True if a path is found, False otherwise.
    """
    if visited is None:
        visited = set()

    if start_node == target_node:
        return True

    if start_node in visited:
        return False

    visited.add(start_node)

    if hasattr(start_node, 'successors') and start_node.successors:
        for neighbor in start_node.successors:
            if depth_first_search(neighbor, target_node, visited):
                return True

    return False

"""
Driver to test depth first search
"""
def main():
    # Case 1: Strongly connected graph
    # Output: Path found!
    station1 = Node("Westminster")
    station2 = Node("Waterloo", None, [station1])
    station3 = Node("Trafalgar Square", None, [station1, station2])
    station4 = Node("Canary Wharf",  None, [station2, station3])
    station5 = Node("London Bridge",  None, [station4, station3])
    station6 = Node("Tottenham Court Road",  None, [station5, station4])

    if depth_first_search(station6, station1):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 2: Branching graph
    # Output: Path found!
    nodef =  Node("F")
    nodee =  Node("E")
    noded =  Node("D")
    nodec =  Node("C", None, [nodef])
    nodeb =  Node("B", None, [nodee])
    nodea =  Node("A", None, [nodeb, nodec, noded])

    if depth_first_search(nodea, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 3: Two unconnected nodes in graph
    # Output: Path not found
    if depth_first_search(nodef, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 4: One node graph
    # Output: Path found!
    if depth_first_search(nodef, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 5: Graph with cycles
    # Output: Path found!
    nodee.successors = [nodea]

    if depth_first_search(nodea, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

if __name__ == "__main__":
    main()
