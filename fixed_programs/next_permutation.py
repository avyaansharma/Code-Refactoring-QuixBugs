def next_permutation(perm):
    n = len(perm)
    i = n - 2
    while i >= 0 and perm[i] >= perm[i + 1]:
        i -= 1
    if i == -1:
        perm.reverse()
        return perm
    j = n - 1
    while perm[j] <= perm[i]:
        j -= 1
    perm[i], perm[j] = perm[j], perm[i]
    perm[i + 1:] = reversed(perm[i + 1:])
    return perm
