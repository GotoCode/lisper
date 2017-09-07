#
# main.py
#
# this file contains the core interpreter logic for
# the Lisper project and also contains some helper
# functions
#

import re

# HELPER FUNCTIONS #

# List Parser #

def lisp_format(x):

    result = str(x)

    if type(x) is list:

        result = result.replace("'", '')
        result = result.replace('"', '')
        result = result.replace(',', '')
        result = result.replace('[', '(')
        result = result.replace(']', ')')

        return result

    return result

def is_list(e):

    return e.startswith('(') and e.endswith(')')

# REQUIRES: s is a syntactically valid list in Lisp
def to_list(s):

    i = 1

    result = []

    while i < len(s) - 1:

        i, e = next_elem(s, i)

        if is_list(e):

            result.append(to_list(e))

        elif e != '':

            if re.match(r'-?\d+', e):

                result.append(int(e))

            else:

                result.append(e)

    return result

def next_elem(s, start):

    i = start

    curr_elem = ''

    while i < len(s):

        ch = s[i]

        if ch == '(':

            #i, curr_elem = next_list(s, i)
            return next_list(s, i)

        elif ch.isspace() or ch == ')':

            i += 1
            break

        else:

            curr_elem += ch

        i += 1

    return (i, curr_elem)

def next_list(s, start):

    num_lparens = 0

    curr_list = ''

    i = start

    while i < len(s):

        curr_list += s[i]

        if s[i] == '(':

            num_lparens += 1

        elif s[i] == ')':

            num_lparens -= 1

        if num_lparens == 0:

            break

        i += 1

    return (i, curr_list)

# Symbol Table #

# built-in operations

def add(*args):

    total = 0

    for num in args:

        total += num

    return total

def sub(*args):

    total = args[0] if len(args) > 0 else 0

    for i in range(1, len(args)):

        total -= args[i]

    return total

def mul(*args):

    total = 1

    for num in args:

        total *= num

    return total

def div(*args):

    total = args[0] if len(args) > 0 else 0

    for i in range(1, len(args)):

        total //= args[i]

    return total

def eq(*args):

    return all(map(lambda x: x == args[0], args))

def quote(*args):

    if len(args) != 1:

        msg = "'quote' takes 1 argument, {} given"
    
        raise RuntimeError(msg.format(len(args)))

    return args[0]

def cons(*args):

    if len(args) != 2:

        msg = "'cons' takes 2 arguments, {} given"

        raise RuntimeError(msg.format(len(args)))

    first  = args[0]
    second = args[1]

    if type(first) is list or type(second) is not list:

        raise RuntimeError("Invalid argument types for 'cons'")

    result = [first]
    result.extend(second)

    return result

def car(*args):

    if len(args) != 1:

        raise RuntimeError("'car' takes 1 argument, {} given".format(len(args)))

    arg = args[0]

    if type(arg) is not list:

        raise RuntimeError("Argument to 'car' is not a list")

    if len(arg) == 0:

        raise RuntimeError("'car' of empty list does not exist")

    return arg[0]

def cdr(*args):

    if len(args) != 1:

        raise RuntimeError("'cdr' takes 1 argument, {} given".format(len(args)))

    arg = args[0]

    if type(arg) is not list:

        raise RuntimeError("Argument to 'cdr' is not a list")

    return arg[1:]

def atom(*args):

    if len(args) != 1:

        raise RuntimeError("'atom?' takes 1 argument, {} given".format(len(args)))

    arg = args[0]

    is_symbol = re.match(r'\w+', str(arg)) is not None
    is_number = re.match(r'\d+', str(arg)) is not None

    return is_symbol or is_number

def define(*args):

    if len(args) != 2:

        raise RuntimeError("'define' takes 2 arguments, {} given".format(len(args)))

    is_symbol = re.match(r'\w+', str(args[0])) is not None

    if not is_symbol:

        raise RuntimeError("cannot bind '{}' to a value".format(args[0]))

    if type(args[1]) is list:

        sym_table[args[0]] = evaluate(args[1])

    else:

        sym_table[args[0]] = args[1]

# symbol table structure

sym_table = {
    '+' : add,
    '-' : sub,
    '*' : mul,
    '/' : div,
    'eq?' : eq,
    'quote' : quote,
    'cons' : cons,
    'car' : car,
    'cdr' : cdr,
    'atom?' : atom,
    'define' : define,
    }

special_sym = {
    'quote',
    'define',
    }

def get_value(sym):
    '''
    Given a symbol in Lisp (+, square, -, etc.),
    this function retrieves the corresponding
    value that is currently bound to this symbol
    '''

    if sym in sym_table:

        return sym_table[sym]

    if re.match(r'\d+', str(sym)):

        return None # symbol is not a function, but an integer constant

    raise RuntimeError("Symbol '{}' is undefined".format(sym))

# Evaluation #

def evaluate(expr):
    '''
    Given a Lisp expression, represented as
    a nested list of values in Python, this
    function evaluates it and returns the final
    value

    NOTE: this function currently only supports
          Lisp normal form expressions
    '''

    if type(expr) is int:

        return expr

    sym = expr[0]
    val = get_value(sym)

    if val is None:

        return expr

    if type(val) is list or type(val) is int:

        return val

    if sym in special_sym:

        return val(*expr[1:])
    
    args = []

    for i in range(1, len(expr)):

        curr_arg = expr[i]

        if type(curr_arg) is list:

            args.append(evaluate(curr_arg))

        else:

            args.append(evaluate(curr_arg))

    return val(*args)


# Testing Code #
if __name__ == '__main__':

    e = input('lisper > ')

    while e != 'quit':

        expr = to_list(e) if is_list(e) else e.strip()
        
        result = evaluate(expr)

        if result is not None:
            
            print('==> {}'.format(lisp_format(result)))

        e = input('lisper > ')
