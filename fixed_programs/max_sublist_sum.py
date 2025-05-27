def max_sublist_sum(arr):
    """
    Max Sublist Sum

    Efficient equivalent to max(sum(arr[i:j]) for 0 <= i <= j <= len(arr))

    Algorithm source: WordAligned.org by Thomas Guest


    Input:
        arr: A list of ints

    Output:
        The maximum sublist sum

    Example:
        >>> max_sublist_sum([4, -5, 2, 1, -1, 3])
        5
    """
    if not arr:
        return 0  # Handle empty list case

    max_ending_here = 0
    max_so_far = float('-inf')  # Initialize to negative infinity to handle all negative numbers

    for x in arr:
        max_ending_here = max_ending_here + x
        if max_ending_here < 0:
            max_ending_here = 0  # Reset if current sum is negative
        max_so_far = max(max_so_far, max_ending_here)

    if max_so_far == 0 and all(x <= 0 for x in arr):  # Handle all negative or zero case
        return max(arr) # Return the least negative number or 0 if all are 0

    return max_so_far
