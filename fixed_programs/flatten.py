import collections.abc

def flatten(arr):
    for x in arr:
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x
