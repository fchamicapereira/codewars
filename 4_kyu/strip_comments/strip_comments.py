# https://www.codewars.com/kata/51c8e37cee245da6b40000bd/python

import re
def solution(string,markers):
    if len(markers) == 0:
        return string
    return re.sub(r" *[{}][^\n]*".format(''.join([re.escape(m) for m in markers])), "", string)