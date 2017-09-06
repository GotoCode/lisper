#
# main.py
#
# this file contains the core interpreter logic for
# the Lisper project and also contains some helper
# functions
#

import re

def get_elements(elems):
    '''
    This function transforms a list in Lisp,
    given as a string of characters, into
    a list of strings in Python
    '''

    return re.findall(r'\((.*)\)', elems)[0].split()

