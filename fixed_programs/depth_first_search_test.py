
from node import Node
from depth_first_search import depth_first_search

 
"""
Driver to test depth first search
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
    nodec =  Node("C")
    nodeb =  Node("B")
    nodea =  Node("A")
    
    nodec.successors = [nodef]
    nodeb.successors = [nodee]
    nodea.successors = [nodeb, nodec, noded]

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
