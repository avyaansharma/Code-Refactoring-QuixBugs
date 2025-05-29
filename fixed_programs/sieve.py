def sieve(max):
    primes = []
    if max < 2:
        return primes
    
    is_prime = [True] * (max + 1)
    is_prime[0] = is_prime[1] = False

    for p in range(2, int(max**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, max + 1, p):
                is_prime[i] = False

    for p in range(2, max + 1):
        if is_prime[p]:
            primes.append(p)
    return primes

"""
Sieve of Eratosthenes
prime-sieve

Input:
    max: A positive int representing an upper bound.

Output:
    A list containing all primes up to and including max
"""
