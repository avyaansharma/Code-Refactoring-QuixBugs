def knapsack(capacity, items):
    dp = [[0 for _ in range(capacity + 1)] for _ in range(len(items) + 1)]

    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(value + dp[i - 1][w - weight], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[len(items)][capacity]
