def rpn_eval(tokens):
    def op(symbol, a, b):
        if symbol == '+':
            return a + b
        elif symbol == '-':
            return b - a
        elif symbol == '*':
            return a * b
        elif symbol == '/':
            if a == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return b / a
        else:
            raise ValueError("Invalid operator: {}".format(symbol))

    stack = []

    for token in tokens:
        if isinstance(token, (int, float)):
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise ValueError("Not enough operands for operator: {}".format(token))
            a = stack.pop()
            b = stack.pop()
            stack.append(op(token, a, b))

    if len(stack) == 0:
        raise ValueError("Empty expression")
    if len(stack) > 1:
        raise ValueError("Too many operands")

    return stack.pop()
"""
Reverse Polish Notation

Four-function calculator with input given in Reverse Polish Notation (RPN).

Input:
    A list of values and operators encoded as floats and strings

Precondition:
    all(
        isinstance(token, float) or token in ('+', '-', '*', '/') for token in tokens
    )

Example:
    >>> rpn_eval([3.0, 5.0, '+', 2.0, '/'])
    4.0
"""
