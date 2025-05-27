def bitcount(n):
    """
    Bitcount

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
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    count = 0
    while n > 0:
        n &= (n - 1)  # Efficiently clear the least significant bit
        count += 1
    return count
