# https://www.codewars.com/kata/584daf7215ac503d5a0001ae/python

import re

class Add(): pass
class Sub(): pass
class Mul(): pass
class Div(): pass
class Pow(): pass
class Cos(): pass
class Sin(): pass
class Tan(): pass
class Exp(): pass
class Ln():  pass

class Node(object):
    
    def __init__(self, expr):
        self.content = None

        ops = { "+": Add, "-": Sub, "*": Mul, "/": Div, "^": Pow, "cos": Cos, "sin": Sin, "tan": Tan, "exp": Exp, "ln": Ln, }

        patterns = [
            (r"\((\S+) (\(.+\)) (\(.+\))\)", Node, Node),              # (op expression expression)
            (r"\((\S+) ([\d|\.]+) ([\d|\.]+)\)", Literal, Literal),    # (op literal literal)
            (r"\((\S+) ([a-zA-Z_]\w*) ([a-zA-Z_]\w*)\)", Var, Var),    # (op var var)

            (r"\((\S*) ([\d|\.]+) (\(.+\))\)", Literal, Node),         # (op literal expression)
            (r"\((\S*) (\(.+\)) ([\d|\.]+)\)", Node, Literal),         # (op expression literal)

            (r"\((\S*) ([a-zA-Z_]\w*) ([\d|\.]+)\)", Var, Literal),    # (op var literal)
            (r"\((\S*) ([\d|\.]+) ([a-zA-Z_]\w*)\)", Literal, Var),    # (op literal var)

            (r"\((\S*) ([a-zA-Z_]\w*) (\(.+\))\)", Var, Node),         # (op var expression)
            (r"\((\S*) (\(.+\)) ([a-zA-Z_]\w*)\)", Node, Var),         # (op expression var)

            (r"\((\S+) ([\d|\.]+)\)", Literal, None),                  # (op literal)
            (r"\((\S+) ([a-zA-Z_]\w*)\)", Var, None),                  # (op var)
            (r"\((\S+) (\(.+\))\)", Node, None),                       # (op expression)

            (r"([a-zA-Z_]\w*)", Var, None),                            # var
            (r"([\d|\.]+)", Literal, None),                            # literal
        ]

        for (pattern, node1, node2) in patterns:
            match = re.match(pattern, expr)
            if match:

                if len(match.groups()) == 1:
                    self.content = node1(match.groups()[0])
                elif len(match.groups()) == 2:
                    node_op = ops[match.groups()[0]]
                    self.content = node_op(node1(match.groups()[1]))
                elif len(match.groups()) == 3:
                    node_op = ops[match.groups()[0]]
                    self.content = node_op(node1(match.groups()[1]), node2(match.groups()[2]))

                assert(self.content)
                return

        # something went wrong
        assert(False)

    def __str__(self):
        return str(self.content)

    def derive(self):
        return self.content.derive()

    def eval(self):
        return self.content.eval()

class Var(Node):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
        
    def derive(self):
        return Literal(1)

    def eval(self):
        return self

class Literal(Node):

    def __init__(self, value):
        if isinstance(value, str):
            self.value = float(value) if str(float(value)) == value else int(value)
        else:
            self.value = value

    def __str__(self):
        return str(self.value)

    def derive(self):
        return Literal(0)

    def eval(self):
        return self

class Mul(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(* {} {})".format(self.left, self.right)

    def derive(self):
        left = self.left.eval()
        right = self.right.eval()

        return Add(Mul(left.derive(), right), Mul(left, right.derive())).eval()

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        # times 0 = 0
        if (isinstance(left, Literal) and left.value == 0) or (isinstance(right, Literal) and right.value == 0): return Literal(0)

        # times 1 nothing changes
        if isinstance(left, Literal) and left.value == 1  : return right
        if isinstance(right, Literal) and right.value == 1: return left

        # literal * literal
        if isinstance(left, Literal) and isinstance(right, Literal):
            return Literal(left.value * right.value)

        # var * var
        if isinstance(left, Var) and isinstance(right, Var) and left.name == right.name:
            return Pow(left, Literal(2)).eval()

        # div * node
        if isinstance(left, Div):
            return Div(Mul(left.numerator, right), left.denominator).eval()

        # node * div
        if isinstance(right, Div):
            return Div(Mul(right.numerator, left), right.denominator).eval()

        # div * div
        if isinstance(left, Div) and isinstance(right, Div):
            return Div(Mul(left.numerator, right.numerator), Mul(left.denominator, right.denominator)).eval()

        return Mul(left, right)

class Div(Node):

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return "(/ {} {})".format(self.numerator, self.denominator)

    def derive(self):
        numerator = self.numerator.eval()
        denominator = self.denominator.eval()

        return Div(Sub(Mul(numerator.derive(), denominator), Mul(numerator, denominator.derive())), Pow(denominator, Literal(2))).eval()

    def eval(self):
        numerator = self.numerator.eval()
        denominator = self.denominator.eval()

        # numerator = 0 results in 0
        if (isinstance(numerator, Literal) and numerator.value == 0): return Literal(0)

        # denominator = 1 results in numerator
        if (isinstance(denominator, Literal) and denominator.value == 1): return self.numerator

        # literal / literal and literal % literal == 0
        if isinstance(numerator, Literal) and isinstance(denominator, Literal):
            return Literal(int(numerator.value / denominator.value)) if numerator.value % denominator.value == 0 else Literal(numerator.value / denominator.value)

        # missing a bunch of them, related with var simplification

        return Div(numerator, denominator)

class Add(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(+ {} {})".format(self.left, self.right)

    def derive(self):
        left = self.left.eval()
        right = self.right.eval()

        return Add(left.derive(), right.derive()).eval()

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        # + 0 changes nothing
        if isinstance(left, Literal) and left.value == 0:   return right
        if isinstance(right, Literal) and right.value == 0: return left

        # literal + literal
        if isinstance(left, Literal) and isinstance(right, Literal):
            return Literal(left.value + right.value)

        # missing a bunch of them, related with divs

        return Add(left, right)

class Sub(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(- {} {})".format(self.left, self.right)

    def derive(self):
        left = self.left.eval()
        right = self.right.eval()

        return Sub(left.derive(), right.derive()).eval()

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        # literal - literal
        if isinstance(left, Literal) and isinstance(right, Literal):
            return Literal(left.value - right.value)

        # missing a bunch of them, related with divs

        return Sub(left, right)

class Pow(Node):

    def __init__(self, base, power):
        self.base = base
        self.power = power

    def __str__(self):
        return "(^ {} {})".format(self.base, self.power)

    def derive(self):
        base = self.base.eval()
        power = self.power.eval()

        # u ^ P
        if isinstance(power, Literal):
            return Mul(base.derive(), Mul(power, Pow(base, Sub(power, Literal(1))))).eval()

        raise NotImplementedError()

    def eval(self):
        base = self.base.eval()
        power = self.power.eval()

        if isinstance(power, Literal) and power.value == 0: return Literal(1)
        if isinstance(power, Literal) and power.value == 1: return base

        if isinstance(base, Literal) and isinstance(power, Literal):
            return Literal(base.value ** power.value)

        return Pow(base, power)

class Cos(Node):

    def __init__(self, ang):
        self.ang = ang

    def __str__(self):
        return "(cos {})".format(self.ang)

    def derive(self):
        ang = self.ang.eval()
        return Mul(Mul(Literal(-1), ang.derive()), Sin(ang)).eval()

    def eval(self):
        ang = self.ang.eval()
        return Cos(ang)

class Sin(Node):

    def __init__(self, ang):
        self.ang = ang

    def __str__(self):
        return "(sin {})".format(self.ang)

    def derive(self):
        ang = self.ang.eval()
        return Mul(ang.derive(), Cos(ang)).eval()

    def eval(self):
        ang = self.ang.eval()
        return Sin(ang)

class Tan(Node):

    def __init__(self, ang):
        self.ang = ang

    def __str__(self):
        return "(tan {})".format(self.ang)

    def derive(self):
        ang = self.ang.eval()
        return Mul(ang.derive(), Div(Literal(1), Pow(Cos(ang), Literal(2)))).eval()

    def eval(self):
        ang = self.ang.eval()
        return Tan(ang)

class Exp(Node):

    def __init__(self, power):
        self.power = power

    def __str__(self):
        return "(exp {})".format(self.power)

    def derive(self):
        power = self.power.eval()
        return Mul(power.derive(), Exp(power)).eval()

    def eval(self):
        power = self.power.eval()

        if isinstance(power, Literal) and power.value == 0: return Literal(1)

        return Exp(power)

class Ln(Node):

    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "(ln {})".format(self.arg)

    def derive(self):
        arg = self.arg.eval()
        return Div(arg.derive(), arg).eval()

    def eval(self):
        arg = self.arg.eval()
        return Ln(arg)

def diff(s):
    return str(Node(s).derive())