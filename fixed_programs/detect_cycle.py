def detect_cycle(node):
    """
    Linked List Cycle Detection using the Tortoise and Hare algorithm.

    Args:
        node: The head node of a linked list.  Can be None if the list is empty.

    Returns:
        True if the linked list is cyclic, False otherwise.  Returns False if the input node is None.
    """

    if node is None:
        return False

    hare = node
    tortoise = node

    while hare is not None and hare.successor is not None:
        tortoise = tortoise.successor
        hare = hare.successor.successor

        if hare == tortoise:
            return True

    return False
