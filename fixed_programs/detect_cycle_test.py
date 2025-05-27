```python
from node import Node
from detect_cycle import detect_cycle

 
"""
Driver to test reverse linked list
"""
def main():
    # Case 1: 5-node list input with no cycle
    # Expected Output: Cycle not detected!
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node1.successor = node2
    node2.successor = node3
    node3.successor = node4
    node4.successor = node5

    if detect_cycle(node1):
        print("Cycle detected!", end=" ")
    else:
        print("Cycle not detected!", end=" ")
    print()

    # Case 2: 5-node list input with cycle
    # Expected Output: Cycle detected!
    node5.successor = node1

    if detect_cycle(node1):
        print("Cycle detected!", end=" ")
    else:
        print("Cycle not detected!", end=" ")
    print()

    # Case 3: 2-node list with cycle
    # Expected Output: Cycle detected!
    node1.successor = node2
    node2.successor = node1

    if detect_cycle(node1):
        print("Cycle detected!", end=" ")
    else:
        print("Cycle not detected!", end=" ")
    print()

    # Case 4: 2-node list with no cycle
    # Expected Output: Cycle not detected!
    node6 = Node(6)
    node7 = Node(7)
    node6.successor = node7

    if detect_cycle(node6):
        print("Cycle detected!", end=" ")
    else:
        print("Cycle not detected!", end=" ")
    print()

    # Case 5: 1-node list
    # Expected Output: Cycle not detected!
    node = Node(0)
    if detect_cycle(node):
        print("Cycle detected!", end=" ")
    else:
        print("Cycle not detected!", end=" ")
    print()

    # Case 6: 5 nodes in total. the last 2 nodes form a cycle. input the first node
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node1.successor = node2
    node2.successor = node3
    node3.successor = node4
    node4.successor = node5
    node5.successor = node4

    if detect_cycle(node1):
        print("Cycle detected!", end=" ")
    else:
        print("Cycle not detected!", end=" ")
    print()


if __name__ == "__main__":
    main()
```