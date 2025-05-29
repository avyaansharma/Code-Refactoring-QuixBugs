def next_permutation(perm):
    """
    Next Permutation

    Input:
        perm: A list of ints

    Output:
        The lexicographically next permutation of the elements of perm.
        Returns None if the input is already the last permutation or invalid.

    Example:
        >>> next_permutation([3, 2, 4, 1])
        [3, 4, 1, 2]
    """
    if not perm or len(perm) <= 1:
        return None  # No next permutation for empty or single-element list

    # Find the first decreasing element from the right
    i = len(perm) - 2
    while i >= 0 and perm[i] >= perm[i + 1]:
        i -= 1

    if i < 0:
        return None  # Already the last permutation

    # Find the smallest element to the right of i that is greater than perm[i]
    j = len(perm) - 1
    while j > i and perm[j] <= perm[i]:
        j -= 1

    # Swap perm[i] and perm[j]
    perm = list(perm) # create mutable list
    perm[i], perm[j] = perm[j], perm[i]

    # Reverse the sublist to the right of i
    perm[i + 1:] = reversed(perm[i + 1:])

    return perm
