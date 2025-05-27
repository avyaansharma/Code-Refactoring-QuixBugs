def kth(arr, k):
    """
    QuickSelect

    This is an efficient equivalent to sorted(arr)[k].

    Input:
        arr: A list of ints
        k: An int

    Precondition:
        0 <= k < len(arr)

    Output:
        The kth-lowest element of arr (0-based)
    """
    if not arr:
        return None  # Handle empty array case

    if k < 0 or k >= len(arr):
        return None  # Handle invalid k

    pivot = arr[0]
    below = [x for x in arr[1:] if x < pivot]
    above = [x for x in arr[1:] if x > pivot]
    equal = [x for x in arr if x == pivot]  # Handle duplicate pivots

    num_below = len(below)

    if k < num_below:
        return kth(below, k)
    elif k < num_below + len(equal):
        return pivot  # kth element is one of the pivots
    else:
        return kth(above, k - num_below - len(equal))
