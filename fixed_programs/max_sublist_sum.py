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
    max_ending_here = 0
    max_so_far = 0

    if not arr:
        return 0

    all_negative = True
    max_element = float('-inf')

    for x in arr:
        if x > 0:
            all_negative = False
        max_element = max(max_element, x)
        
    if all_negative:
        return max_element

    for x in arr:
        max_ending_here = max_ending_here + x
        if max_ending_here < 0:
            max_ending_here = 0
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far
