```python
def next_palindrome(digit_list):
    n = len(digit_list)
    mid = n // 2
    i = mid - 1
    j = mid + (n % 2)
    
    while i >= 0 and digit_list[i] == digit_list[j]:
        i -= 1
        j += 1
    
    if i < 0 or digit_list[i] < digit_list[j]:
        i = mid - 1
        j = mid + (n % 2)
        carry = 1
        while i >= 0:
            digit_list[i] += carry
            carry = digit_list[i] // 10
            digit_list[i] %= 10
            digit_list[j] = digit_list[i]
            i -= 1
            j += 1
        if carry:
            return [1] + [0] * n
    else:
        i = mid - 1
        j = mid + (n % 2)
        while i >= 0:
            digit_list[j] = digit_list[i]
            i -= 1
            j += 1
    return digit_list
```