def sieve(max):
    """
    Sieve of Eratosthenes
    prime-sieve

    Input:
        max: A positive int representing an upper bound.

    Output:
        A list containing all primes up to and including max
    """
    if not isinstance(max, int) or max < 2:
        return []

    primes = []
    is_prime = [True] * (max + 1)
    is_prime[0] = is_prime[1] = False

    for n in range(2, int(max**0.5) + 1):
        if is_prime[n]:
            for i in range(n*n, max + 1, n):
                is_prime[i] = False

    for n in range(2, max + 1):
        if is_prime[n]:
            primes.append(n)

    return primes
