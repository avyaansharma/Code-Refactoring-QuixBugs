def sqrt(x, epsilon):
    """
    Square Root

    Newton-Raphson method implementation.


    Input:
        x: A float
        epsilon: A float

    Precondition:
        x >= 0 and epsilon > 0

    Output:
        A float in the interval [sqrt(x) - epsilon, sqrt(x) + epsilon]

    Example:
        >>> sqrt(2, 0.01)
        1.4166666666666665
    """
    if x < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    if epsilon <= 0:
        raise ValueError("Epsilon must be greater than zero.")

    if x == 0:
        return 0.0

    approx = x / 2.0  # Initial guess
    while True:
        next_approx = 0.5 * (approx + x / approx)
        if abs(approx - next_approx) < epsilon:
            return next_approx
        approx = next_approx
