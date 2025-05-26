```python
class Node:
    def __init__(self, name, visited=False, successors=None):
        self.name = name
        self.visited = visited
        self.successors = successors if successors is not None else []

def depth_first_search(start_node, target_node):
    """
    Performs a recursive depth-first search to find a path from a start node to a target node.

    Args:
        start_node: The node to start the search from.
        target_node: The node to search for.

    Returns:
        True if a path is found, False otherwise.
    """
    if start_node is None or target_node is None:
        return False

    # Mark the current node as visited
    start_node.visited = True

    # If the current node is the target node, we're done
    if start_node == target_node:
        return True

    # Recursively search the successors of the current node
    for successor in start_node.successors:
        if not successor.visited:
            if depth_first_search(successor, target_node):
                return True

    # If we've searched all successors and haven't found the target node, backtrack
    return False

def main():
    # Case 1: Strongly connected graph
    # Output: Path found!
    station1 = Node("Westminster")
    station2 = Node("Waterloo", False, [station1])
    station3 = Node("Trafalgar Square", False, [station1, station2])
    station4 = Node("Canary Wharf",  False, [station2, station3])
    station5 = Node("London Bridge",  False, [station4, station3])
    station6 = Node("Tottenham Court Road",  False, [station5, station4])

    if depth_first_search(station6, station1):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Reset visited flags
    station1.visited = False
    station2.visited = False
    station3.visited = False
    station4.visited = False
    station5.visited = False
    station6.visited = False

    # Case 2: Branching graph
    # Output: Path found!
    nodef =  Node("F")
    nodee =  Node("E")
    noded =  Node("D")
    nodec =  Node("C", False, [nodef])
    nodeb =  Node("B", False, [nodee])
    nodea =  Node("A", False, [nodeb, nodec, noded])

    if depth_first_search(nodea, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Reset visited flags
    nodea.visited = False
    nodeb.visited = False
    nodec.visited = False
    noded.visited = False
    nodee.visited = False
    nodef.visited = False

    # Case 3: Two unconnected nodes in graph
    # Output: Path not found
    if depth_first_search(nodef, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()
    
    # Reset visited flags
    nodea.visited = False
    nodeb.visited = False
    nodec.visited = False
    noded.visited = False
    nodee.visited = False
    nodef.visited = False

    # Case 4: One node graph
    # Output: Path found!
    if depth_first_search(nodef, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Reset visited flags
    nodea.visited = False
    nodeb.visited = False
    nodec.visited = False
    noded.visited = False
    nodee.visited = False
    nodef.visited = False

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
```