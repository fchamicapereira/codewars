# https://www.codewars.com/kata/52e88b39ffb6ac53a400022e/python

def int32_to_ip(int32):
    return "{}.{}.{}.{}".format(
        (int32 >> 24) & ((2<<7)-1),
        (int32 >> 16) & ((2<<7)-1),
        (int32 >> 8)  & ((2<<7)-1),
        int32         & ((2<<7)-1))