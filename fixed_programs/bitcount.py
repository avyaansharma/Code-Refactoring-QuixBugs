def bitcount(n):
    """
    Bitcount
    bitcount


    Input:
        n: a nonnegative int

    Output:
        The number of 1-bits in the binary encoding of n

    Examples:
        >>> bitcount(127)
        7
        >>> bitcount(128)
        1
    """
    count = 0
    if not isinstance(n, int) or n < 0:
        return 0  # Handle invalid input: non-integer or negative

    while n:
        count += 1
        n &= (n - 1)  # Efficiently clear the least significant set bit
    return count
