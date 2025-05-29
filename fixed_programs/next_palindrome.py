def next_palindrome(digit_list):
    n = len(digit_list)
    mid = n // 2
    left = digit_list[:mid]
    right = digit_list[n - mid:]
    
    if n % 2 == 0:
        middle_digits = []
    else:
        middle_digits = [digit_list[mid]]
        
    if left == right[::-1]:
        i = mid - 1
        
        if n % 2 == 1:
            middle_digits[0] += 1
            if middle_digits[0] > 9:
                middle_digits[0] = 0
                
                carry = 1
                while i >= 0:
                    left[i] += carry
                    if left[i] > 9:
                        left[i] = 0
                    else:
                        carry = 0
                        break
                    i -= 1
                if carry == 1:
                    left = [1] + left
                    right = left[::-1]
                    return left + right
                right = left[::-1]
                return left + middle_digits + right
            else:
                right = left[::-1]
                return left + middle_digits + right
        else:
            carry = 1
            while i >= 0:
                left[i] += carry
                if left[i] > 9:
                    left[i] = 0
                else:
                    carry = 0
                    break
                i -= 1
            if carry == 1:
                left = [1] + left
                right = left[::-1]
                return left + right
            right = left[::-1]
            return left + right
    else:
        if left > right[::-1]:
            right = left[::-1]
            return left + middle_digits + right
        else:
            i = mid - 1
        
            if n % 2 == 1:
                middle_digits[0] += 1
                if middle_digits[0] > 9:
                    middle_digits[0] = 0
                    
                    carry = 1
                    while i >= 0:
                        left[i] += carry
                        if left[i] > 9:
                            left[i] = 0
                        else:
                            carry = 0
                            break
                        i -= 1
                    if carry == 1:
                        left = [1] + left
                        right = left[::-1]
                        return left + right
                    right = left[::-1]
                    return left + middle_digits + right
                else:
                    right = left[::-1]
                    return left + middle_digits + right
            else:
                carry = 1
                while i >= 0:
                    left[i] += carry
                    if left[i] > 9:
                        left[i] = 0
                    else:
                        carry = 0
                        break
                    i -= 1
                if carry == 1:
                    left = [1] + left
                    right = left[::-1]
                    return left + right
                right = left[::-1]
                return left + right
