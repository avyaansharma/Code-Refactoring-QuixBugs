```python
def longest_common_subsequence(a, b):
    if not a or not b:
        return ''

    if a[0] == b[0]:
        return a[0] + longest_common_subsequence(a[1:], b[1:])

    else:
        subsequence1 = longest_common_subsequence(a, b[1:])
        subsequence2 = longest_common_subsequence(a[1:], b)
        if len(subsequence1) >= len(subsequence2):
            return subsequence1
        else:
            return subsequence2
```