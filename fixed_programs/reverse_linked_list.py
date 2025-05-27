def reverse_linked_list(node):
    prevnode = None
    currentnode = node
    while currentnode:
        nextnode = currentnode.successor
        currentnode.successor = prevnode
        prevnode = currentnode
        currentnode = nextnode
    return prevnode
