
# https://www.codewars.com/kata/52ffcfa4aff455b3c2000750

import re

class ParseError(Exception):
    def __init__(self, node, tokens):
        self.node = node
        self.tokens = tokens

    @classmethod
    def handle(cls, best_effort, node, tokens):
        if not best_effort: raise ParseError(node, tokens)
        return None

    def __str__(self):
        return "ERROR: unable to parse {} with tokens {}".format(self.node, self.tokens)

class EvaluationError(Exception):
    def __init__(self, expr, vars, funcs):
        self.expr = expr
        self.vars = vars
        self.funcs = funcs

    def __str__(self):
        expr_str = str(self.expr)
        vars_str = "{ " + ",".join([ "{}: {}".format(k, str(v)) for k, v in self.vars.items() ]) + " }"
        funcs_str = ",".join([ fn.name for fn in self.funcs ])
        return "ERROR: insufficient data for complete eval [expr={}, vars={}, funcs=[{}]]".format(expr_str, vars_str, funcs_str)

class IdentifierError(Exception):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "ERROR: Invalid identifier. No variable with name '{}' was found.".format(self.identifier)

class InvalidNumberOfArguments(Exception):
    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

    def __str__(self):
        return "ERROR: Invalid number of arguments (func={}, expected={}, given={})".format(self.fn.name, len(self.fn.args), len(self.args))

class Conflict(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "ERROR: Conflict in name {} (already defined)".format(self.name)

class Assignment(object):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        if len(tokens) >= 3 and tokens[1] == "=":
            lvalue = Identifier.parse(funcs, tokens[:1], False)           
            rvalue = Expression.parse(funcs, tokens[2:], False)
            return Assignment(lvalue, rvalue)

        return ParseError.handle(best_effort, "assignment", tokens)

    def eval(self, vars, funcs):
        rvalue, vars, funcs = self.rvalue.eval(vars, funcs)
        lvalue = self.lvalue
        
        if not isinstance(lvalue, Identifier): raise EvaluationError(self, vars, funcs)

        if isinstance(rvalue, Fn) and lvalue in vars.keys(): raise Conflict(lvalue.name)
        if not isinstance(rvalue, Fn) and lvalue in funcs.keys(): raise Conflict(lvalue.name)

        vars[lvalue] = rvalue
        return lvalue.eval(vars, funcs)

    def __str__(self):
        return "{} = {}".format(str(self.lvalue), str(self.rvalue))

class Identifier(object):
    regex = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    def __init__(self, name):
        self.name = name

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        if len(tokens) == 1:
            if cls.regex.match(tokens[0]): return Identifier(tokens[0])

        return ParseError.handle(best_effort, "identifier", tokens)

    def eval(self, vars, funcs):
        if self in vars.keys():
            if not isinstance(vars[self], Number): raise IdentifierError(self.name)
            return (vars[self], vars, funcs)

        if self in funcs.keys():
            return funcs[self].eval([], vars, funcs)

        raise EvaluationError(self, vars, funcs)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Identifier): return other.name == self.name
        return False

    def __hash__(self):
        return hash(self.name)

class Number(object):
    regex = re.compile(r"^[0-9]*\.?[0-9]*$")

    def __init__(self, value):
        self.value = value

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        if len(tokens) == 1:
            if cls.regex.match(tokens[0]):
                n = float(tokens[0]) if str(float(tokens[0])) == tokens[0] else int(tokens[0])
                return Number(n)

        return ParseError.handle(best_effort, "number", tokens)

    def eval(self, vars, funcs):
        return (self, vars, funcs)

    def __str__(self):
        return str(self.value)

class FnCall(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        fn_name = Identifier.parse(funcs, [tokens[0]])
        if not fn_name or fn_name not in funcs.keys():
            return ParseError.handle(best_effort, "fn_call", tokens)

        exprs = []
        funcs_names = [ fn.name for fn in funcs ]

        token_idx = 1
        while token_idx < len(tokens):
            token = tokens[token_idx]

            # nested function calls
            if token in funcs_names:
                fn = funcs[list(funcs.keys())[funcs_names.index(token)]]
                n_args = len(fn.args)
                fn_call_tokens = tokens[token_idx:token_idx+n_args+1]
                fn_call = FnCall.parse(funcs, fn_call_tokens)

                if fn_call:
                    exprs.append(fn_call)
                    token_idx += len(fn_call_tokens)
                    continue

            new_expr = Expression.parse(funcs, [token], True)
            if not new_expr:
                return ParseError.handle(best_effort, "fn call", tokens)

            exprs.append(new_expr)
            token_idx += 1

        return FnCall(fn_name, exprs)

    def eval(self, vars, funcs):
        if self.name not in funcs.keys():
            raise EvaluationError(self, vars, funcs)
        return funcs[self.name].eval(vars, funcs, self.args)

class Fn(object):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        if tokens[0] != "fn": return ParseError.handle(best_effort, "function", tokens)

        if len(tokens) < 4 or tokens.index("=>") < 2 or tokens.index("=>") == len(tokens) - 1:
            raise ParseError("function", tokens)
        
        name = Identifier.parse(funcs, [tokens[1]], False)
        args = []
        for token in tokens[2:]:
            if token == "=>": break
            new_arg = Identifier.parse(funcs, [token], False)

            if new_arg in args: raise Conflict(new_arg.name)

            args.append(new_arg)

        body = Expression.parse(funcs, tokens[tokens.index("=>") + 1:], False)
        return Fn(name, args, body)

    def eval(self, vars, funcs, args=None):
        internal_vars = {}

        if args == None:
            if self.name in vars.keys(): raise Conflict(self.name)
            
            # ugly hack
            tmp_args = []
            for i in range(len(self.args)): tmp_args.append(Number(0))
            self.eval(vars, funcs, tmp_args)

            funcs[self.name] = self
            return (self, vars, funcs)

        if len(args) != len(self.args):
            raise InvalidNumberOfArguments(self, args)

        # global vars
        #for k, v in vars.items():
        #    internal_vars[k] = v

        for idx, var_arg in enumerate(self.args):
            internal_vars[var_arg] = args[idx].eval(vars, funcs)[0]

        vars_str = "{ " + ",".join([ "{}: {}".format(k, str(v)) for k, v in internal_vars.items() ]) + " }"
        
        o, v, f = self.body.eval(internal_vars, funcs)

        return (o, vars, funcs)

    def __str__(self):
        return "fn {} {} => {}".format(self.name, " ".join([str(arg) for arg in self.args]), self.body)

class Factor(object):

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        parsed = Number.parse(funcs, tokens)
        if parsed: return parsed

        # function call
        parsed = FnCall.parse(funcs, tokens)
        if parsed: return parsed

        parsed = Identifier.parse(funcs, tokens)
        if parsed: return parsed

        parsed = Assignment.parse(funcs, tokens)
        if parsed: return parsed

        # check if is between parenthesis
        if len(tokens) >= 3 and tokens[0] == "(" and tokens[-1] == ")":
            level = 0
            for idx, token in enumerate(tokens):
                if token == "(": level += 1
                if token == ")": level -= 1

                if level == 0 and idx not in [0, len(tokens) - 1]:
                    return ParseError.handle(best_effort, "factor", tokens)

            parsed = Expression.parse(funcs, tokens[1:-1], False)
            if parsed: return parsed

        return ParseError.handle(best_effort, "factor", tokens)

class BinaryOp(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        operations = [Add, Sub, Mul, Div, Remainder]

        for operation in operations:
            parsed = operation.parse(funcs, tokens)
            if parsed: return parsed

        return ParseError.handle(best_effort, "binaryOp", tokens)

class Mul(BinaryOp):
    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "*" and parse:
                left = Expression.parse(funcs, tokens[:idx], False)
                if not left:
                    return ParseError.handle(best_effort, "mul", tokens)

                right = Expression.parse(funcs, tokens[idx+1:], False)
                if not right:
                    return ParseError.handle(best_effort, "mul", tokens)

                return Mul(left, right)

        return ParseError.handle(best_effort, "mul", tokens)

    def eval(self, vars, funcs):
        left, vars, funcs = self.left.eval(vars, funcs)
        right, vars, funcs = self.right.eval(vars, funcs)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars, funcs)

        return (Number(left.value * right.value), vars, funcs)

    def __str__(self):
        return "({} * {})".format(str(self.left), str(self.right))

class Div(BinaryOp):
    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "/" and parse:
                left = Expression.parse(funcs, tokens[:idx], False)
                if not left:
                    return ParseError.handle(best_effort, "mul", tokens)

                right = Expression.parse(funcs, tokens[idx+1:], False)
                if not right:
                    return ParseError.handle(best_effort, "mul", tokens)

                return Div(left, right)

        return ParseError.handle(best_effort, "div", tokens)

    def eval(self, vars, funcs):
        left, vars, funcs = self.left.eval(vars, funcs)
        right, vars, funcs = self.right.eval(vars, funcs)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars, funcs)


        result = int(left.value / right.value) if left.value % right.value == 0 else left.value / right.value
        return (Number(result), vars, funcs)

    def __str__(self):
        return "({} / {})".format(str(self.left), str(self.right))

class Remainder(BinaryOp):
    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "%" and parse:
                left = Expression.parse(funcs, tokens[:idx], False)
                if not left:
                    return ParseError.handle(best_effort, "mul", tokens)

                right = Expression.parse(funcs, tokens[idx+1:], False)
                if not right:
                    return ParseError.handle(best_effort, "mul", tokens)

                return Remainder(left, right)

        return ParseError.handle(best_effort, "remainder", tokens)

    def eval(self, vars, funcs):
        left, vars, funcs = self.left.eval(vars, funcs)
        right, vars, funcs = self.right.eval(vars, funcs)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars, funcs)

        return (Number(left.value % right.value), vars, funcs)

    def __str__(self):
        return "({} % {})".format(str(self.left), str(self.right))

class Add(BinaryOp):
    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True

            if token == "+" and parse:
                left = Expression.parse(funcs, tokens[:idx], False)
                if not left:
                    return ParseError.handle(best_effort, "mul", tokens)

                right = Expression.parse(funcs, tokens[idx+1:], False)
                if not right:
                    return ParseError.handle(best_effort, "mul", tokens)

                return Add(left, right)

        return ParseError.handle(best_effort, "add", tokens)

    def eval(self, vars, funcs):
        left, vars, funcs = self.left.eval(vars, funcs)
        right, vars, funcs = self.right.eval(vars, funcs)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars, funcs)

        return (Number(left.value + right.value), vars, funcs)

    def __str__(self):
        return "({} + {})".format(str(self.left), str(self.right))

class Sub(BinaryOp):
    @classmethod
    def parse(cls, funcs, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True

            if token == "-" and parse:
                left = Expression.parse(funcs, tokens[:idx], False)
                if not left:
                    return ParseError.handle(best_effort, "mul", tokens)

                right = Expression.parse(funcs, tokens[idx+1:], False)
                if not right:
                    return ParseError.handle(best_effort, "mul", tokens)

                return Sub(left, right)

        return ParseError.handle(best_effort, "sub", tokens)

    def eval(self, vars, funcs):
        left, vars, funcs = self.left.eval(vars, funcs)
        right, vars, funcs = self.right.eval(vars, funcs)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars, funcs)

        return (Number(left.value - right.value), vars, funcs)

    def __str__(self):
        return "({} - {})".format(str(self.left), str(self.right))

class Expression(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, funcs, tokens, best_effort=False):
        if len(tokens) == 1 and isinstance(tokens[0], Expression): return tokens[0]
        if not tokens: return None

        parsed = Factor.parse(funcs, tokens)
        if parsed: return parsed

        parsed = BinaryOp.parse(funcs, tokens)
        if parsed: return parsed

        return ParseError.handle(best_effort, "expression", tokens)

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

        self.expressions = []

    def input(self, expression):
        print("> {}".format(expression))

        tokens = tokenize(expression)
        if not tokens: return ""        
        
        expr = Fn.parse(self.funcs, tokens)
        if not expr:
            expr = Expression.parse(self.funcs, tokens)
        
        self.expressions.append(expr)

        output, vars, funcs = expr.eval(self.vars, self.funcs)

        self.vars = vars
        self.funcs = funcs


        if isinstance(output, Fn): return ""

        print(output)

        return output.value

interpreter = Interpreter()
code = [
    "x = 1"
]

for line in code:
    try:
        interpreter.input(line)
    except Exception as e:
        print(e)