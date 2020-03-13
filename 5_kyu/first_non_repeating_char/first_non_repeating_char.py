# https://www.codewars.com/kata/52bc74d4ac05d0945d00054e/python

def first_non_repeating_letter(string):
    for c in string:
        if string.lower().count(c.lower()) > 1:
            continue
        return c
    return ''
