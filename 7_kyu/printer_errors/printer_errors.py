# https://www.codewars.com/kata/56541980fa08ab47a0000040/python

from re import sub
def printer_error(s):
    return "{}/{}".format(len(sub("[a-m]",'',s)),len(s))
