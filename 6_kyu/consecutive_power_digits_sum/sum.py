# https://www.codewars.com/kata/5626b561280a42ecc50000d1

def sum_dig_pow(a, b): # range(a, b + 1) will be studied by the function
    result = []
    
    def check(n):
        sum = 0
        p = 1
        for c in str(n):
            sum += pow(int(c), p)
            p += 1
        return sum == n
        
    for n in range(a, b + 1):
        if check(n):
            result.append(n)
            
    return result
