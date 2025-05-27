def lcs_length(s, t):
    from collections import defaultdict

    dp = defaultdict(lambda: 0)
    max_length = 0

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                if i == 0 or j == 0:
                    dp[i, j] = 1
                else:
                    dp[i, j] = dp[i - 1, j - 1] + 1
                max_length = max(max_length, dp[i, j])
            else:
                dp[i, j] = 0  # Reset length if characters don't match

    return max_length
