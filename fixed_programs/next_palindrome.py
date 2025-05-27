def next_palindrome(digit_list):
    n = len(digit_list)
    mid = n // 2
    i = mid - 1
    j = mid + 1 if n % 2 == 0 else mid
    
    # Find the first mismatched digit from the middle outwards
    while i >= 0 and digit_list[i] == digit_list[j]:
        i -= 1
        j += 1

    # If no mismatched digit, then the number is already a palindrome or close to it
    if i < 0 or digit_list[i] < digit_list[j]:
        i = mid - 1
        j = mid + 1 if n % 2 == 0 else mid
        carry = 1

        # Add 1 to the middle digits, handling carry
        if n % 2 != 0:
            digit_list[mid] += carry
            carry = digit_list[mid] // 10
            digit_list[mid] %= 10
            
        while i >= 0:
            digit_list[i] += carry
            carry = digit_list[i] // 10
            digit_list[i] %= 10
            digit_list[j] = digit_list[i]
            i -= 1
            j += 1

        # If there's a carry left, we need to add a new digit
        if carry:
            return [1] + [0] * n + [1]
            
    else:
        # The left side is greater, so just mirror it to the right side
        i = mid - 1
        j = mid + 1 if n % 2 == 0 else mid
        while i >= 0:
            digit_list[j] = digit_list[i]
            i -= 1
            j += 1
    return digit_list
"""
Finds the next palindromic integer when given the current integer
Integers are stored as arrays of base 10 digits from most significant to least significant

Input:
    digit_list: An array representing the current palindrome

Output:
    An array which represents the next palindrome

Preconditions:
    The initial input array represents a palindrome

Example
    >>> next_palindrome([1,4,9,4,1])
    [1,5,0,5,1]
"""
