
from .node import Node
from .breadth_first_search import breadth_first_search

 
"""
Driver to test breadth first search
"""
def main():
    # Case 1: Strongly connected graph
    # Output: Path found!
    station1 = Node("Westminster")
    station2 = Node("Waterloo")
    station3 = Node("Trafalgar Square")
    station4 = Node("Canary Wharf")
    station5 = Node("London Bridge")
    station6 = Node("Tottenham Court Road")

    station2.successors = [station1]
    station3.successors = [station1, station2]
    station4.successors = [station2, station3]
    station5.successors = [station4, station3]
    station6.successors = [station5, station4]
    
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
    nodec =  Node("C")
    nodeb =  Node("B")
    nodea =  Node("A")

    nodec.successors = [nodef]
    nodeb.successors = [nodee]
    nodea.successors = [nodeb, nodec, noded]
    
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
    node4 = Node("4")
    node5 = Node("5")
    node6 = Node("6")

    node4.successors = [node1]
    node5.successors = [node2]
    node6.successors = [node5, node4, node3]
    node2.successors = [node6]

    if breadth_first_search(node6, node1):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

if __name__ == "__main__":
    main()
