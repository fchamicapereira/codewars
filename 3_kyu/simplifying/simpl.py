# https://www.codewars.com/kata/57f2b753e3b78621da0020e8

import re

def simplify(examples, formula):
    
    reduced = dict()
    variables = []
    final_var = ''

    def get_variables(expression):
        v = []

        expression = expression.replace(' ', '')
        splitted = expression.split('=')

        if len(splitted) > 1:
            left, right = splitted

            v += re.findall(r'([a-zA-Z]+)', left)
            
            if right:
                v.append(right)
                reduced[right] = left
        else:
            v += re.findall(r'([a-zA-Z]+)', expression)

        return set(v)

    def reduce(expression, final_var):
        if expression[0] not in ['+', '-']: expression = '+' + expression
        multiplier = 0

        for g in expression.split(final_var):
            if len(g) == 0: continue
            if g == '+': multiplier += 1
            elif g == '-': multiplier -= 1
            else: multiplier += int(g)

        return multiplier

    for example in examples:
        variables += list(get_variables(example))
    variables = set(variables)

    for v in  variables:
        if v not in reduced.keys():
            final_var = v
            break

    current_vars = get_variables(formula)
    while len(current_vars) > 1 or (len(current_vars) == 1 and final_var not in current_vars):
        for v in current_vars:
            if v == final_var: continue
            formula = formula.replace(v, '('+reduced[v]+')')
            formula = formula.replace(' ', '')
        current_vars = get_variables(formula)

    stack = []
    groups = []
    changed = True
    while changed:
        changed = False
        for idx, c in enumerate(formula):
            if c == '(':
                stack.append(idx)
            if c == ')':
                start = stack.pop()
                end = idx

                expression = formula[start+1:idx]
                multiplier = reduce(expression, final_var)

                group_multiplier_greedy = re.findall(r'([\+|-][0-9]*)$', formula[:start])
                group_multiplier = re.findall(r'([0-9]+)$', formula[:start])

                if group_multiplier_greedy or group_multiplier:
                    prefix_multiplier = group_multiplier_greedy[0] if group_multiplier_greedy else group_multiplier[0]
                    start -= len(prefix_multiplier)

                    if prefix_multiplier == '+': prefix_multiplier = '+1'
                    elif prefix_multiplier == '-': prefix_multiplier = '-1'

                    prefix_multiplier = int(prefix_multiplier)
                    multiplier *= prefix_multiplier

                formula = formula[:start]+str(multiplier)+final_var+formula[end+1:]

                changed = True
                break

    multiplier = reduce(formula, final_var)

    return str(multiplier)+final_var