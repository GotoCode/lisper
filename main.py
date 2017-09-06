#
# main.py
#
# this file contains the core interpreter logic for
# the Lisper project and also contains some helper
# functions
#

import re

def to_list(s, result, curr_i):
    '''
    This function transforms a list in Lisp,
    given as a string of characters, into
    a nested list of strings in Python
    '''

    # (/ (+ (+ 1 1) 10) (- 4 1))
    # ^

    # result : [['/ ', ['+ ', ['+ 1 1'], ' 10'], ' ', ['- 4 1']]]
    # 

    # curr_elem : ''

    curr_elem = ''

    i = curr_i

    while i < len(s):

        ch = s[i]

        if ch == '(':

            inner_elem = curr_elem.split()

            if len(inner_elem) > 0:

                result.append(inner_elem)
                curr_elem = ''

            nested = []

            result.append(nested)
            i += 1

            (i, _) = to_list(s, nested, i)

        elif ch == ')':

            inner_list = curr_elem.split()

            if len(inner_list) > 0:

                result.append(inner_list)
                curr_elem = ''

            i += 1

            return (i, result)

        else:

            curr_elem += ch
            i += 1

    return (i, result)

def get_list(s):
    '''
    Given a string representing a Lisp list,
    this function returns a Python list
    representation
    '''

    result = []

    to_list(s, result, 0)

    return result[0]

def get_value(sym):
    '''
    Given a symbol in Lisp (+, square, -, etc.),
    this function retrieves the corresponding
    value that is currently bound to this symbol
    '''

    pass
