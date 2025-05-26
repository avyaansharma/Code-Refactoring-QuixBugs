```python
def lcs_length(s, t):
    from collections import defaultdict

    dp = defaultdict(lambda: 0)
    max_length = 0

    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            if s[i-1] == t[j-1]:
                dp[i, j] = dp[i - 1, j - 1] + 1
                max_length = max(max_length, dp[i, j])
            else:
                dp[i, j] = 0

    return max_length
```