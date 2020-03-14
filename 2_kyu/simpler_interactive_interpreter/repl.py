
# https://www.codewars.com/kata/53005a7b26d12be55c000243/python

import re

class ParseError(Exception):
    def __init__(self, node, tokens):
        self.node = node
        self.tokens = tokens

    def __str__(self):
        return "ERROR: unable to parse {} with tokens {}".format(self.node, self.tokens)

class EvaluationError(Exception):
    def __init__(self, expr, vars):
        self.expr = expr
        self.vars = vars

    def __str__(self):
        expr_str = str(self.expr)
        vars_str = "{ " + ",".join([ "{}: {}".format(k, str(v)) for k, v in self.vars.items() ]) + " }"
        return "ERROR: insufficient data for complete eval [expr={}, vars={}]".format(self.expr_str, self.vars_str)

class IdentifierError(Exception):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "ERROR: Invalid identifier. No variable with name '{}' was found.".format(self.identifier)

class Assignment(object):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    @classmethod
    def parse(cls, tokens, best_effort=True):
        if len(tokens) >= 3 and tokens[1] == "=":
            lvalue = Identifier.parse(tokens[:1], False)           
            rvalue = Expression.parse(tokens[2:], False)
            return Assignment(lvalue, rvalue)

        if best_effort: return None
        raise ParseError("assignment", tokens)

    def eval(self, vars):
        rvalue, vars = self.rvalue.eval(vars)
        if not isinstance(rvalue, Number): raise EvaluationError(self, vars)
        vars[self.lvalue.name] = rvalue
        return self.lvalue.eval(vars)

    def __str__(self):
        return "{} = {}".format(str(self.lvalue), str(self.rvalue))

class Identifier(object):
    regex = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    def __init__(self, name):
        self.name = name

    @classmethod
    def parse(cls, tokens, best_effort=True):
        if len(tokens) == 1:
            if cls.regex.match(tokens[0]): return Identifier(tokens[0])

        if best_effort: return None
        raise ParseError("identifier", tokens)

    def eval(self, vars):
        if self.name not in vars.keys(): raise IdentifierError(self.name)
        if not isinstance(vars[self.name], Number): raise IdentifierError(self.name)

        return (vars[self.name], vars)

    def __str__(self):
        return self.name

class Number(object):
    regex = re.compile(r"^[0-9]*\.?[0-9]*$")

    def __init__(self, value):
        self.value = value

    @classmethod
    def parse(cls, tokens, best_effort=True):
        if len(tokens) == 1:
            if cls.regex.match(tokens[0]):
                n = float(tokens[0]) if str(float(tokens[0])) == tokens[0] else int(tokens[0])
                return Number(n)

        if best_effort: return None
        raise ParseError("number", tokens)

    def eval(self, vars):
        return (self, vars)

    def __str__(self):
        return str(self.value)

class Factor(object):

    @classmethod
    def parse(cls, tokens, best_effort=True):
        parsed = Number.parse(tokens)
        if parsed: return parsed

        parsed = Identifier.parse(tokens)
        if parsed: return parsed

        parsed = Assignment.parse(tokens)
        if parsed: return parsed

        # check if is between parenthesis
        if len(tokens) >= 3 and tokens[0] == "(" and tokens[-1] == ")":
            level = 0
            for idx, token in enumerate(tokens):
                if token == "(": level += 1
                if token == ")": level -= 1

                if level == 0 and idx not in [0, len(tokens) - 1]:
                    if best_effort: return None
                    raise ParseError("factor", tokens)

            parsed = Expression.parse(tokens[1:-1], False)
            if parsed: return parsed

        if best_effort: return None
        raise ParseError("factor", tokens)

class BinaryOp(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @classmethod
    def parse(cls, tokens, best_effort=True):
        operations = [Add, Sub, Mul, Div, Remainder]

        for operation in operations:
            parsed = operation.parse(tokens)
            if parsed: return parsed

        if best_effort: return None
        raise ParseError("binaryOp", tokens)

class Mul(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "*" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Mul(left, right)

        if best_effort: return None
        raise ParseError("mul", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value * right.value), vars)

    def __str__(self):
        return "({} * {})".format(str(self.left), str(self.right))

class Div(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "/" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Div(left, right)

        if best_effort: return None
        raise ParseError("div", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)


        result = int(left.value / right.value) if left.value % right.value == 0 else left.value / right.value
        return (Number(result), vars)

    def __str__(self):
        return "({} / {})".format(str(self.left), str(self.right))

class Remainder(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "%" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Remainder(left, right)

        if best_effort: return None
        raise ParseError("remainder", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value % right.value), vars)

    def __str__(self):
        return "({} % {})".format(str(self.left), str(self.right))

class Add(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True

            if token == "+" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Add(left, right)

        if best_effort: return None
        raise ParseError("add", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value + right.value), vars)

    def __str__(self):
        return "({} + {})".format(str(self.left), str(self.right))

class Sub(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True

            if token == "-" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Sub(left, right)

        if best_effort: return None
        raise ParseError("sub", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value - right.value), vars)

    def __str__(self):
        return "({} - {})".format(str(self.left), str(self.right))

class Expression(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, tokens, best_effort=False):
        if len(tokens) == 1 and isinstance(tokens[0], Expression): return tokens[0]

        parsed = Factor.parse(tokens)
        if parsed: return parsed

        parsed = BinaryOp.parse(tokens)
        if parsed: return parsed

        raise ParseError("expression", tokens)

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

        self.expressions = []

    def input(self, expression):
        print("> {}".format(expression))

        tokens = tokenize(expression)
        if not tokens: return ""

        expr = Expression.parse(tokens)
        self.expressions.append(expr)

        output, vars = expr.eval(self.vars)

        self.vars = vars

        print(output)

        return output.value

interpreter = Interpreter()
code = [
    "(8 - (4 + 2)) * 3",
    "x = -1",
    "x"
]

for line in code:
    try:
        interpreter.input(line)
    except Exception as e:
        print(e)
