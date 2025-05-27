def kheapsort(arr, k):
    import heapq

    if not arr:
        return  # Handle empty array case

    heap = []
    for i in range(min(k + 1, len(arr))): # corrected initialization
        heapq.heappush(heap, arr[i])

    for i in range(k + 1, len(arr)):
        yield heapq.heappushpop(heap, arr[i])

    while heap:
        yield heapq.heappop(heap)
