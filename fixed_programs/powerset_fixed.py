```python
def powerset(arr):
    if not arr:
        return [[]]
    else:
        first = arr[0]
        rest = arr[1:]
        rest_subsets = powerset(rest)
        return rest_subsets + [[first] + subset for subset in rest_subsets]
```