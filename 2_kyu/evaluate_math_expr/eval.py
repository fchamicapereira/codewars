# https://www.codewars.com/kata/52a78825cdfc2cfc87000005/python

def calc(input):

    def parse(expression):
        # trim whitespace
        expression = expression.replace(" ", "")

        print(f"parse {expression}")

        # parse
        parsed = []
        decimal = 0
        idx = 0
        neg = False
        while idx < len(expression):

            if expression[idx] == "(":

                level = 0
                for sub_idx in range(idx+1, len(expression), 1):
                    if expression[sub_idx] == ")" and level == 0:
                        result = parse(expression[idx+1:sub_idx])
                        if neg:
                            parsed.append([-1, "*", result])
                            neg = False
                        else:
                            parsed.append(result)
                        idx = sub_idx + 1
                        break
                    elif expression[sub_idx] == "(":
                        level +=1 
                    elif expression[sub_idx] == ")":
                        level -=1
                continue

            elif expression[idx] in ["+", "-", "*", "/"]:
                if neg:
                    parsed[-1] *= -1
                    neg = False

                if expression[idx] == "-" and (idx == 0 or expression[idx-1] in ["+", "-", "*", "/"]):
                    neg = True
                
                else:
                    parsed.append(expression[idx])

            # is a number not registered
            elif not parsed or (not isinstance(parsed[-1], int) and not isinstance(parsed[-1], float)):
                parsed.append(int(expression[idx]))
                decimal = 0

            elif expression[idx] == ".":
                decimal = 0.1

            # is a number registered
            else:
                if decimal != 0:
                    parsed[-1] += decimal * int(expression[idx])
                    decimal *= 0.1
                else:
                    parsed[-1] = parsed[-1] * 10 + int(expression[idx])

            idx += 1

        if neg:
            parsed[-1] *= -1

        return parsed

    def process(parsed):
        
        def add(lvalue, rvalue): return lvalue + rvalue
        def sub(lvalue, rvalue): return lvalue - rvalue
        def div(lvalue, rvalue): return lvalue / rvalue
        def mul(lvalue, rvalue): return lvalue * rvalue

        operations = {
            '+': add,
            '-': sub,
            '*': mul,
            '/': div,
        }

        print(f"process {parsed}")

        if len(parsed) == 1 and not isinstance(parsed[0], list):
            return parsed[0]

        while len(parsed) > 1:

            for ops in [['*', '/'], ['+', '-']]:

                idx = 0
                while idx < len(parsed):

                    if parsed[idx] in ops:
                        lvalue = process(parsed[idx-1]) if isinstance(parsed[idx-1], list) else parsed[idx-1]
                        rvalue = process(parsed[idx+1]) if isinstance(parsed[idx+1], list) else parsed[idx+1]

                        print("lvalue", lvalue)
                        print("rvalue", rvalue)
                        print("res", operations[parsed[idx]](lvalue, rvalue))

                        parsed = parsed[:idx-1] + [operations[parsed[idx]](lvalue, rvalue)] + parsed[idx+2:]

                        print(parsed)

                        continue

                    idx += 1

        return process(parsed[0]) if isinstance(parsed[0], list) else parsed[0]


    parsed = parse(input)
    print(f"Parsed: {parsed}")
    result = process(parsed)
    print(result)

    return result
