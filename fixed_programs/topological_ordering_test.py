from collections import deque

from .node import Node


def topological_ordering(graph):
    """
    Performs a topological sort on a directed acyclic graph (DAG).

    Args:
        graph: A list of Node objects representing the graph.  Each node
               should have outgoing_nodes and incoming_nodes attributes
               that are lists of other Node objects.

    Returns:
        A list of Node objects in topological order, or None if the graph
        is not a DAG (i.e., contains cycles).
    """

    in_degree = {}
    for node in graph:
        in_degree[node] = 0

    for node in graph:
        for neighbor in node.outgoing_nodes:
            in_degree[neighbor] += 1

    queue = deque()
    for node in graph:
        if in_degree[node] == 0:
            queue.append(node)

    ordered_nodes = []
    while queue:
        node = queue.popleft()
        ordered_nodes.append(node)

        for neighbor in node.outgoing_nodes:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered_nodes) != len(graph):
        raise ValueError("Graph contains a cycle, topological sort not possible.")

    return ordered_nodes


"""
Driver to test topological ordering
"""
def main():
    # Case 1: Wikipedia graph
    # Output: 5 7 3 11 8 10 2 9
    
    five = Node(5)
    seven = Node(7)
    three = Node(3)
    eleven = Node(11)
    eight = Node(8)
    two = Node(2)
    nine = Node(9)
    ten = Node(10)
 
    five.outgoing_nodes = [eleven]
    eleven.incoming_nodes.append(five)
    seven.outgoing_nodes = [eleven, eight]
    eleven.incoming_nodes.append(seven)
    eight.incoming_nodes.append(seven)
    three.outgoing_nodes = [eight, ten]
    eight.incoming_nodes.append(three)
    ten.incoming_nodes.append(three)
    eleven.outgoing_nodes = [two, nine, ten]
    two.incoming_nodes.append(eleven)
    nine.incoming_nodes.append(eleven)
    ten.incoming_nodes.append(eleven)
    eight.outgoing_nodes = [nine]
    nine.incoming_nodes.append(eight)
    ten.incoming_nodes = [eleven, three]

    try:
        [print(x.value, end=" ") for x in topological_ordering([five, seven, three, eleven, eight, two, nine, ten])]
    except Exception as e:
        print(e)
    print()


    # Case 2: GeekforGeeks example
    # Output: 4 5 0 2 3 1

    five = Node(5)
    zero = Node(0)
    four = Node(4)
    one = Node(1)
    two = Node(2)
    three = Node(3)

    five.outgoing_nodes = [two, zero]
    two.incoming_nodes.append(five)
    zero.incoming_nodes.append(five)
    four.outgoing_nodes = [zero, one]
    zero.incoming_nodes.append(four)
    one.incoming_nodes.append(four)
    two.outgoing_nodes = [three]
    three.incoming_nodes.append(two)
    three.outgoing_nodes = [one]
    one.incoming_nodes.append(three)

    try:
        [print(x.value, end=" ") for x in topological_ordering([zero, one, two, three, four, five])]
    except Exception as e:
        print(e)
    print()
    

    # Case 3: Cooking with InteractivePython
    # Output:

    milk = Node("3/4 cup milk")
    egg = Node("1 egg")
    oil = Node("1 Tbl oil")
    mix = Node("1 cup mix")
    syrup = Node("heat syrup")
    griddle = Node("heat griddle")
    pour = Node("pour 1/4 cup")
    turn = Node("turn when bubbly")
    eat = Node("eat")

    milk.outgoing_nodes = [mix]
    mix.incoming_nodes.append(milk)
    egg.outgoing_nodes = [mix]
    mix.incoming_nodes.append(egg)
    oil.outgoing_nodes = [mix]
    mix.incoming_nodes.append(oil)
    mix.outgoing_nodes = [syrup, pour]
    syrup.incoming_nodes.append(mix)
    pour.incoming_nodes.append(mix)
    griddle.outgoing_nodes = [pour]
    pour.incoming_nodes.append(griddle)
    pour.outgoing_nodes = [turn]
    turn.incoming_nodes.append(pour)
    turn.outgoing_nodes = [eat]
    eat.incoming_nodes.append(turn)
    syrup.outgoing_nodes = [eat]
    eat.incoming_nodes.append(syrup)

    try:
        [print(x.value, end=" ") for x in topological_ordering([milk, egg, oil, mix, syrup, griddle, pour, turn, eat])]
    except Exception as e:
        print(e)
    print()


if __name__ == "__main__":
    main()
