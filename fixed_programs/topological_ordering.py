def topological_ordering(nodes):
    ordered_nodes = []
    visited = set()
    recursion_stack = set()

    def visit(node):
        if node in recursion_stack:
            raise ValueError("Cycle detected")
        if node in visited:
            return

        visited.add(node)
        recursion_stack.add(node)

        for next_node in node.outgoing_nodes:
            visit(next_node)

        recursion_stack.remove(node)
        ordered_nodes.insert(0, node)  # Prepend to build reverse topological order

    for node in nodes:
        if node not in visited:
            visit(node)

    return ordered_nodes
"""
Topological Sort

Input:
    nodes: A list of directed graph nodes
 
Precondition:
    The input graph is acyclic

Output:
    An OrderedSet containing the elements of nodes in an order that puts each node before all the nodes it has edges to
"""
