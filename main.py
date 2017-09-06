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

        print(e) # dummy code

        if is_list(e):

            result.append(to_list(e))

        elif e != '':

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

def get_value(sym):
    '''
    Given a symbol in Lisp (+, square, -, etc.),
    this function retrieves the corresponding
    value that is currently bound to this symbol
    '''

    pass
