# https://www.codewars.com/kata/525c65e51bf619685c000059/python

from math import inf

def cakes(recipe, available):
    amount = inf
    for ingrediant, qtt in recipe.items():
        if ingrediant not in available.keys():
            return 0
        amount = min(amount, int(available[ingrediant] / qtt))
    return amount
