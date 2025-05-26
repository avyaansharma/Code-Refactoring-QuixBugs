```python
from typing import Optional

class Node:
    def __init__(self, value, successor=None):
        self.value = value
        self.successor = successor

def reverse_linked_list(head: Optional[Node]) -> Optional[Node]:
    """
    Reverses a singly linked list.

    Args:
        head: The head of the linked list.

    Returns:
        The head of the reversed linked list.
    """
    if not head:
        return None

    prev = None
    curr = head
    while curr:
        next_node = curr.successor
        curr.successor = prev
        prev = curr
        curr = next_node

    return prev

def main():
    # Case 1: 5-node list input
    # Expected Output: 5 4 3 2 1
    node1 = Node(1)
    node2 = Node(2, node1)
    node3 = Node(3, node2)
    node4 = Node(4, node3)
    node5 = Node(5, node4)

    result = reverse_linked_list(node5)

    while result:
        print(result.value, end=" ")
        result = result.successor
    print()
 
    # Case 2: 1-node list input
    # Expected Output: 0
    node = Node(0)
    result = reverse_linked_list(node)

    while result:
        print(result.value, end=" ")
        result = result.successor
    print()

    # Case 3: None input
    # Expected Output: None
    result = reverse_linked_list(None)
    if result == None:
        print("None")
    else:
        while result:
            print(result.value)
            result = result.successor
    print()

if __name__ == "__main__":
    main()
```