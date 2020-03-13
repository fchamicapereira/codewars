# https://www.codewars.com/kata/525f50e3b73515a6db000b83/python

def create_phone_number(n):
    s = [ str(x) for x in n ]
    return '({}) {}-{}'.format(''.join(s[:3]), ''.join(s[3:6]), ''.join(s[6:10]))
