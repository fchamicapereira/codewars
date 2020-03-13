# https://www.codewars.com/kata/54ba84be607a92aa900000f1/python

def is_isogram(string):
    letters = []
    for c in string:
        if c.lower() not in letters:
            letters.append(c.lower())
        else:
            return False
    return True
