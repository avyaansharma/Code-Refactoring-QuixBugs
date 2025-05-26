```python
from collections import deque

class Node:
    def __init__(self, name, visited=False, successors=None):
        self.name = name
        self.visited = visited
        self.successors = successors if successors is not None else []

def breadth_first_search(start_node, goal_node):
    if start_node is None or goal_node is None:
        return False
    
    if start_node == goal_node:
        return True

    queue = deque([start_node])
    visited = {start_node}

    while queue:
        node = queue.popleft()

        for successor in node.successors:
            if successor == goal_node:
                return True
            if successor not in visited:
                queue.append(successor)
                visited.add(successor)

    return False

def main():
    # Case 1: Strongly connected graph
    # Output: Path found!
    station1 = Node("Westminster")
    station2 = Node("Waterloo", False, [station1])
    station3 = Node("Trafalgar Square", False, [station1, station2])
    station4 = Node("Canary Wharf", False, [station2, station3])
    station5 = Node("London Bridge", False, [station4, station3])
    station6 = Node("Tottenham Court Road", False, [station5, station4])

    if breadth_first_search(station6, station1):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 2: Branching graph
    # Output: Path found!
    nodef =  Node("F")
    nodee =  Node("E")
    noded =  Node("D")
    nodec =  Node("C", False, [nodef])
    nodeb =  Node("B", False, [nodee])
    nodea =  Node("A", False, [nodeb, nodec, noded])

    if breadth_first_search(nodea, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 3: Two unconnected nodes in graph
    # Output: Path not found
    if breadth_first_search(nodef, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 4: One node graph
    # Output: Path found!
    if breadth_first_search(nodef, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    # Case 5: Graph with cycles
    # Output: Path found!
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4", False, [node1])
    node5 = Node("5", False, [node2])
    node6 = Node("6", False, [node5, node4, node3])

    node2.successors = [node6]

    if breadth_first_search(node6, node1):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

if __name__ == "__main__":
    main()
```