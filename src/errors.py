""" This file defines all errors that can be used for checking the correctness
    of code parsing, syntax tree generation, and symbol table build.
    The following errors are covered:
    1. VAriable not defined error
    2. syntax error
    3. parse error
    4. other errors

    @ Author: Paul Atilola
    @version: Nov 18, 2022
"""


# ERROR WHEN VARIABLE IS NOT DECLARED BEFORE USE
def variableNotDeclared(listOfVariables):
    if listOfVariables:
        for funcName, varlist in listOfVariables.items():
            if varlist:
                for var in varlist:
                    print('Error: "{}" not declared before use in "{}"'.format(var, funcName))


