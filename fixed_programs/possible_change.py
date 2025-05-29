def possible_change(coins, total):
    dp = {}

    def solve(index, amount):
        if amount == 0:
            return 1
        if amount < 0:
            return 0
        if index >= len(coins):
            return 0

        if (index, amount) in dp:
            return dp[(index, amount)]

        include = solve(index, amount - coins[index])
        exclude = solve(index + 1, amount)

        dp[(index, amount)] = include + exclude
        return dp[(index, amount)]

    return solve(0, total)
