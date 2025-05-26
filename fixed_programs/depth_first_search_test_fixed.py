```python
from collections import deque

class Node:
    def __init__(self, name, value=None, successors=None):
        self.name = name
        self.value = value
        self.successors = successors if successors is not None else []

def depth_first_search(start_node, target_node):
    if start_node is None or target_node is None:
        return False

    visited = set()
    stack = [start_node]

    while stack:
        node = stack.pop()

        if node == target_node:
            return True

        if node in visited:
            continue

        visited.add(node)

        if node.successors:
            for successor in reversed(node.successors):
                if successor not in visited:
                    stack.append(successor)

    return False


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
    nodef = Node("F") 
    if depth_first_search(nodef, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 5: Graph with cycles
    # Output: Path found!
    nodee = Node("E")
    nodea = Node("A", None, [nodee])
    nodef = Node("F")
    nodee.successors = [nodea]
    nodea.successors.append(nodef)

    if depth_first_search(nodea, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

if __name__ == "__main__":
    main()
```