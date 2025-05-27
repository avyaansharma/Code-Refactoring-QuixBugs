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
            return False  # Node already visited, avoid cycles
        
        nodesvisited.add(node)  # Mark node as visited before exploring

        if node == goalnode:
            return True  # Goal node found

        if hasattr(node, 'successors') and isinstance(node.successors, (list, tuple)):
            for nextnode in node.successors:
                if search_from(nextnode):
                    return True
            return False  # No path found from this node
        else:
            return False  # No successors, dead end
    

    if startnode is None or goalnode is None:
        return False
    
    return search_from(startnode)
