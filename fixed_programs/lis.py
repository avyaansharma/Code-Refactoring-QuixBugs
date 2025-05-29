def lis(arr):
    """
    Longest Increasing Subsequence
    longest-increasing-subsequence


    Input:
        arr: A sequence of ints

    Precondition:
        The ints in arr are unique

    Output:
        The length of the longest monotonically increasing subsequence of arr

    Example:
        >>> lis([4, 1, 5, 3, 7, 6, 2])
        3
    """
    if not arr:
        return 0

    tails = []  # Store the smallest tail of all increasing subsequences with length i+1 in tails[i].
    predecessors = {}  # Store the predecessor of each element in the LIS.

    for number in arr:
        if not tails or number > tails[-1]:
            # Extend the longest increasing subsequence.
            if tails:
                predecessors[number] = tails[-1]
            tails.append(number)
        else:
            # Find the first tail that is greater than or equal to number
            l, r = 0, len(tails) - 1
            while l <= r:
                mid = (l + r) // 2
                if tails[mid] < number:
                    l = mid + 1
                else:
                    r = mid - 1

            # Update the tail
            if l > 0:
                predecessors[number] = tails[l - 1]
            tails[l] = number

    return len(tails)
