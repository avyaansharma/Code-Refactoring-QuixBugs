def next_palindrome(digit_list):
    n = len(digit_list)
    mid = n // 2
    
    # Convert list to integer
    num = 0
    for digit in digit_list:
        num = num * 10 + digit

    # Handle edge case where input list is empty
    if not digit_list:
        return [1]
    
    # Handle edge case of all zeros
    if all(digit == 0 for digit in digit_list):
        return [1]

    # Create a copy to avoid modifying the original list directly
    digit_list_copy = digit_list[:] 

    # Increment the middle digit(s)
    if n % 2 == 0:
        digit_list_copy[mid - 1] += 1
        digit_list_copy[mid] += 1  # Ensure mirroring after increment
    else:
        digit_list_copy[mid] += 1
    
    # Handle carry-over from middle digit(s) increment
    i = mid - 1
    j = mid if n % 2 == 0 else mid + 1
    carry = 0
    
    if n % 2 == 0 and digit_list_copy[mid - 1] > 9:
        digit_list_copy[mid - 1] = 0
        digit_list_copy[mid] = 0
        carry = 1
    elif n % 2 != 0 and digit_list_copy[mid] > 9:
        digit_list_copy[mid] = 0
        carry = 1

    while i >= 0:
        digit_list_copy[i] += carry
        if digit_list_copy[i] > 9:
            digit_list_copy[i] = 0
            carry = 1
        else:
            carry = 0
            break
        i -= 1

    if carry == 1:
        return [1] + [0] * n

    # Mirror the left half to the right half
    i = mid - 1
    j = mid if n % 2 == 0 else mid + 1
    while i >= 0:
        digit_list_copy[j] = digit_list_copy[i]
        i -= 1
        j += 1

    # If the new number is still equal or smaller than initial
    new_num = 0
    for digit in digit_list_copy:
        new_num = new_num * 10 + digit
    
    if new_num <= num:
        # Revert to incrementing from right
        digits = list(map(int, str(num+1)))

        
        if len(digits)> n:
            return digits
        
        digits_padded = [0] * (n - len(digits)) + digits

        digit_list_copy = digits_padded
        
        mid_copy = n // 2 
        
        for i in range(mid_copy):
            digit_list_copy[n-1-i] = digit_list_copy[i]

        
        new_num = 0
        for digit in digit_list_copy:
            new_num = new_num * 10 + digit

        if new_num <= num:
            
            return [1]+[0]*(n-1)+[1]

    return digit_list_copy
