```python
def max_sublist_sum(arr):
    max_ending_here = 0
    max_so_far = float('-inf')

    if not arr:
        return 0

    for x in arr:
        max_ending_here = max_ending_here + x
        if max_ending_here < x:
            max_ending_here = x
        if max_so_far < max_ending_here:
            max_so_far = max_ending_here

    return max_so_far
```