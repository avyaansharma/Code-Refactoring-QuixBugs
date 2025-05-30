def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start > end:
            return -1
        mid = (start + end) // 2
        if x < arr[mid]:
            return binsearch(start, mid - 1)
        elif x > arr[mid]:
            return binsearch(mid + 1, end)
        else:
            return mid

    return binsearch(0, len(arr) - 1)
