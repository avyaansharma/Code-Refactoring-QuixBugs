class Node:
    def __init__(self, value=None):
        self.value = value
        self.incoming_nodes = []
        self.outgoing_nodes = []

    def add_incoming(self, node):
        if node not in self.incoming_nodes:
            self.incoming_nodes.append(node)

    def add_outgoing(self, node):
        if node not in self.outgoing_nodes:
            self.outgoing_nodes.append(node)


def topological_ordering(nodes):
    """
    Performs a topological sort on a list of nodes.

    Args:
        nodes: A list of Node objects.  Each node must have its incoming_nodes
               and outgoing_nodes attributes correctly populated.

    Returns:
        A list of nodes in topological order.  Returns an empty list if the
        input is empty. Returns None if a cycle is detected.
    """

    if not nodes:
        return []

    # Create a copy of the nodes list to work with
    nodes = list(nodes)  # Create a shallow copy

    # Nodes with no incoming edges
    independent_nodes = [node for node in nodes if not node.incoming_nodes]

    ordered_nodes = []
    while independent_nodes:
        node = independent_nodes.pop(0)  # Treat as a queue (FIFO)
        ordered_nodes.append(node)

        for nextnode in list(node.outgoing_nodes):  # Iterate over a copy to allow modification
            nextnode.incoming_nodes.remove(node)  # Remove the edge
            if not nextnode.incoming_nodes:
                independent_nodes.append(nextnode)  # Add if no more incoming edges

    # Cycle detection (if not all nodes were visited, there's a cycle)
    if len(ordered_nodes) != len(nodes):
        return None  # Indicate cycle

    return ordered_nodes
