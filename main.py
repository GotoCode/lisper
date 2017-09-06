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

# symbol table structure

sym_table = {
    '+' : add,
    '-' : sub,
    '*' : mul,
    '/' : div,
    'eq?' : eq,
    }

def get_value(sym):
    '''
    Given a symbol in Lisp (+, square, -, etc.),
    this function retrieves the corresponding
    value that is currently bound to this symbol
    '''

    if sym in sym_table:

        return sym_table[sym]

    raise RuntimeError("Symbol '{}' is undefined".format(sym))

# Evaluation #

def evaluate(expr):
    '''
    Given a Lisp expression, represented as
    a nested list of strings in Python, this
    function evaluates it and returns the final
    value

    NOTE: this function currently only supports
          Lisp normal form expressions
    '''

    sym = expr[0]
    val = get_value(sym)
    
    args = []

    for i in range(1, len(expr)):

        curr_arg = expr[i]

        if type(curr_arg) is list:

            args.append(evaluate(curr_arg))

        else:

            args.append(curr_arg)

    return val(*args)


# Testing Code #
if __name__ == '__main__':

    e = input('lisper > ')

    while e != 'quit':

        list_expr = to_list(e)
        
        result = evaluate(list_expr)
        
        print('==> {}'.format(result))

        e = input('lisper > ')
