```python
def detect_cycle(node):
    if not node:
        return False
    
    hare = node
    tortoise = node
    
    while hare and hare.successor:
        tortoise = tortoise.successor
        hare = hare.successor.successor
        
        if hare == tortoise:
            return True
            
    return False
```