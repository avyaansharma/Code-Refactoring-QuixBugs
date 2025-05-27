def depth_first_search(startnode, goalnode):
    """
    Depth-first Search

    Input:
        startnode: A digraph node
        goalnode: A digraph node

    Output:
        Whether goalnode is reachable from startnode
    """
    nodesvisited = set()

    def search_from(node):
        if node is None:
            return False  # Handle None node case
        if node in nodesvisited:
            return False
        if node == goalnode:
            return True
        nodesvisited.add(node)  # Mark node as visited *before* exploring successors
        if hasattr(node, 'successors'): # Check if node has successors attribute
            if node.successors is None:
                return False
            return any(search_from(nextnode) for nextnode in node.successors)
        else:
            return False # Node does not have successor so not reachable

    if startnode is None or goalnode is None:
        return False

    return search_from(startnode)
