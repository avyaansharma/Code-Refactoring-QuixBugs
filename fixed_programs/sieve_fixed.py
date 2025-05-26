```python
def sieve(max):
    primes = []
    if max <= 1:
        return primes
    
    marked = [False] * (max + 1)
    
    for n in range(2, max + 1):
        if not marked[n]:
            primes.append(n)
            for i in range(n * n, max + 1, n):
                marked[i] = True
    return primes

"""
Sieve of Eratosthenes
prime-sieve

Input:
    max: A positive int representing an upper bound.

Output:
    A list containing all primes up to and including max
"""
```