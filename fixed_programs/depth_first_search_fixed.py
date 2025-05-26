```python
def depth_first_search(startnode, goalnode):
    nodesvisited = set()

    def search_from(node):
        if node is None:
            return False
        if node in nodesvisited:
            return False
        elif node == goalnode:
            return True
        else:
            nodesvisited.add(node)
            if hasattr(node, 'successors'):
                return any(search_from(nextnode) for nextnode in node.successors)
            else:
                return False

    return search_from(startnode)
```