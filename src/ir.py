'''
ir.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 28 NOV 22

Generates 3-Address Code Intermediate Representation (IR) from AST
'''

ir = ""
def generate_ir(ast):
    for function in ast:
        unpack_function(ast, function)
    return ir

def unpack_function(ast, function):
    global ir
    function = ast[function]
    for variable in function:   # Do top-level variable assignment last
        if not type(function[variable]) == dict: continue
        unpack_variable(function, variable)
    for variable in function:
        if type(function[variable]) == dict: continue
        if variable == 'return':
            add_returnCode(function['return'])
        else:
            add_assignmentCode(function, variable)

def unpack_variable(function, variable):
    expression = function[variable]
    unpack_expression(variable, expression)

def unpack_expression(variable, expression):
    global ir
    # print(variable)
    # print(expression)
    operator, operands = list(expression.keys())[0], list(expression.values())[0]
    operand1 = operands[0]
    operand2 = operands[1]
    # print(operator)
    # print(operands)

    maincode = variable + " = "
    # print(maincode)

    #operand1
    if type(operand1) == dict:
        maincode += str(list(operand1.keys())[0]) + " "
        code = str(list(operand1.keys())[0]) + " = " + str(list(operand1.values())[0]) + "\n"
        if code not in ir:
            ir += code
        # print(code)
    else:
        maincode += operand1 + " "

    maincode += operator + " "

    #operand2
    if type(operand2) == dict:
        maincode += str(list(operand2.keys())[0]) + " "
        code = str(list(operand2.keys())[0]) + " = " + str(list(operand2.values())[0]) + "\n"
        if code not in ir:
            ir += code
        # print(code)
    else:
        maincode += operand2 + "\n"

    maincode += "\n"
    if maincode not in ir:
        ir += maincode
    # print(maincode)
    # print()

def add_assignmentCode(function, variable):
    global ir
    code = str(variable) + " = " + str(function[variable]) + "\n"
    if code not in ir:
        ir += code

def add_returnCode(returnExpression):
    global ir
    code = "return " + str(returnExpression) + "\n"
    if code not in ir:
        ir += code

class irException(Exception):
    pass

def print_ir(ir):
    print("Intermediate Representation:")
    print(str(ir) + "\n")