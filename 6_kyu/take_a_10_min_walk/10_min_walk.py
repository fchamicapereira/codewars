# https://www.codewars.com/kata/54da539698b8a2ad76000228/solutions/python

import collections 

def isValidWalk(walk):
    if len(walk) != 10:
        return False
    freq = collections.Counter(walk)
    return freq['n'] == freq['s'] and freq['e'] == freq['w']
