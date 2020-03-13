# https://www.codewars.com/kata/5266876b8f4bf2da9b000362/python

def likes(names):
    if len(names) == 0:
        return "no one likes this"
    if len(names) == 1:
        return "{} likes this".format(names[0])
    if len(names) == 2:
        return "{} and {} like this".format(names[0], names[1])
    
    last = names[2] if len(names) == 3 else "{} others".format(len(names) - 2)
    
    return "{}, {} and {} like this".format(names[0], names[1], last)  
