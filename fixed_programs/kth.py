import random

def kth(arr, k):
    if not arr:
        return None

    if not 0 <= k < len(arr):
        return None

    pivot = random.choice(arr)
    below = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    above = [x for x in arr if x > pivot]

    num_below = len(below)
    num_equal = len(equal)


    if k < num_below:
        return kth(below, k)
    elif k < num_below + num_equal:
        return pivot
    else:
        return kth(above, k - num_below - num_equal)
