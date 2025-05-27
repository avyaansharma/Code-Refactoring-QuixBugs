from collections import deque as Queue
 
def breadth_first_search(startnode, goalnode):
    queue = Queue()
    queue.append(startnode)

    nodes_seen = set()
    nodes_seen.add(startnode)

    while queue:
        node = queue.popleft()

        if node is goalnode:
            return True
        
        if hasattr(node, 'successors'):
            successors = node.successors
            if successors:
                for successor in successors:
                    if successor not in nodes_seen:
                        queue.append(successor)
                        nodes_seen.add(successor)

    return False
