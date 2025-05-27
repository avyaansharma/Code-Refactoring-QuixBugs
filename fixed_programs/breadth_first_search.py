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
    if not startnode or not goalnode:
        return False
    
    queue = Queue()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while queue:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            if hasattr(node, 'successors'):
                successors = [successor for successor in node.successors if successor not in nodesseen]
                queue.extend(successors)
                nodesseen.update(successors)

    return False
