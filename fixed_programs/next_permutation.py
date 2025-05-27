def next_permutation(perm):
    """
    Finds the next lexicographically greater permutation of a list of integers.

    Args:
        perm: A list of integers.

    Returns:
        The next permutation of the input list, or None if the input is already the last permutation.
    """
    n = len(perm)
    if n <= 1:
        return None  # No next permutation for single or empty lists

    # Find the first decreasing element from the right
    i = n - 2
    while i >= 0 and perm[i] >= perm[i + 1]:
        i -= 1

    if i < 0:
        return None # Array is in descending order (last permutation)

    # Find the smallest element to the right of i that is greater than perm[i]
    j = n - 1
    while j > i and perm[j] <= perm[i]:
        j -= 1

    # Swap perm[i] and perm[j]
    perm[i], perm[j] = perm[j], perm[i]

    # Reverse the sublist to the right of i
    perm[i + 1:] = reversed(perm[i + 1:])
    return list(perm)
