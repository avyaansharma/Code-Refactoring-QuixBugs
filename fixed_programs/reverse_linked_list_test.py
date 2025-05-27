from node import Node
from reverse_linked_list import reverse_linked_list


"""
Driver to test reverse linked list
"""
def main():
    # Case 1: 5-node list input
    # Expected Output: 1 2 3 4 5
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)

    node5.successor = node4
    node4.successor = node3
    node3.successor = node2
    node2.successor = node1
    

    result = reverse_linked_list(node5)

    current = result
    head = node1
    reversed_flag = True
    while current and head:
      if current.value != head.value:
        reversed_flag = False
        break
      current = current.successor
      head = head.successor

    if reversed_flag:
        print("Reversed!", end=" ")
    else:
        print("Not Reversed!", end=" ")
    current = result
    while current:
        print(current.value, end=" ")
        current = current.successor
    print()
 
    # Case 2: 1-node list input
    # Expected Output: 0
    node = Node(0)
    result = reverse_linked_list(node)
    
    if result == node:
        print("Reversed!", end=" ")
    else:
        print("Not Reversed!", end=" ")
    current = result
    while current:
        print(current.value, end=" ")
        current = current.successor
    print()

    # Case 3: None input
    # Expected Output: None
    result = reverse_linked_list(None)
    if result == None:
        print("Reversed!", end=" ")
    else:
        print("Not Reversed!", end=" ")

    current = result
    while current:
        print(current.value)
        current = current.successor
    print()

if __name__ == "__main__":
    main()
