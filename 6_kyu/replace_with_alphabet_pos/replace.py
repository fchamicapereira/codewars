# https://www.codewars.com/kata/546f922b54af40e1e90001da

def alphabet_position(text):
    res = []
    for c in text.lower():
        if ord(c) < ord('a') or ord(c) > ord('z'):
            continue
        res.append(str(ord(c) - ord('a') + 1))
    return ' '.join(res)
