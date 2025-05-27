def find_in_sorted(arr, x):
    """
    Binary Search

    Input:
        arr: A sorted list of ints
        x: A value to find

    Output:
        An index i such that arr[i] == x, or -1 if x not in arr

    Example:
        >>> find_in_sorted([3, 4, 5, 5, 5, 5, 6], 5)
        2
    """
    def binsearch(start, end):
        if start > end:
            return -1
        
        mid = (start + end) // 2
        
        if arr[mid] == x:
            return mid
        elif x < arr[mid]:
            return binsearch(start, mid - 1)
        else:
            return binsearch(mid + 1, end)

    if not arr:
        return -1

    return binsearch(0, len(arr) - 1)
