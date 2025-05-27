
def lis(arr):
    if not arr:
        return 0
    
    ends = {}
    longest = 0

    for i, val in enumerate(arr):
        prefix_lengths = [j for j in range(1, longest + 1) if j in ends and arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or (length + 1 in ends and val < arr[ends[length + 1]]) or length+1 not in ends:
            ends[length + 1] = i
            if length == longest:
                longest = length + 1

    return longest
