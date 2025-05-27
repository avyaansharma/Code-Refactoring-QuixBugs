from collections import deque as Queue
 
def breadth_first_search(startnode, goalnode):
    """
    Breadth-First Search

    Input:
        startnode: A digraph node
        goalnode: A digraph node

    Output:
        Whether goalnode is reachable from startnode
    """
    if startnode is None or goalnode is None:
        return False

    queue = Queue()
    queue.append(startnode)

    nodes_seen = set()
    nodes_seen.add(startnode)

    while queue:
        node = queue.popleft()

        if node == goalnode:
            return True
        
        if hasattr(node, 'successors'): #Check if the node has successors attribute
            successors = node.successors
            if successors:
                for successor in successors:
                    if successor not in nodes_seen:
                        queue.append(successor)
                        nodes_seen.add(successor)
        
    return False
