def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        elif paren == ')':
            depth -= 1
            if depth < 0:
                return False
        else:
            return False

    return depth == 0
