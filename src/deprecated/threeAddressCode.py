"""
   This file contains the program for generating 3 address code from AST
   3 address code ia an intermediate code which can be converted to machine code. 
   it makes use of at most 3 addresses and one operator to represent an expression.
   General representation: "a = b op c"

   @Author: Paul Atilola
   @version: Nov 28, 2022

"""

# function to generate 3 address code
def generate_3AC(AST):
    functionsAdrCodes = list()

    for function in AST:
        listOfExpressions = unpack_function(AST[function])
        functionsAdrCodes.append(listOfExpressions)


    return functionsAdrCodes


#function unpacked to get variables
def unpack_function(function):
    adrCodeLines = list()

    for variable in function:
        if type(function[variable]) == dict and variable != 'return':
            adrCodeLines = unpack_variables(variable, function, adrCodeLines)

    for variable in function:
        if type(function[variable]) is not dict and variable != 'return':
            adrCodeLines = assign_variable(variable, function, adrCodeLines)

        elif variable == 'return':
            adrCodeLines = add_return(variable, function, adrCodeLines)


    return adrCodeLines


#function unpacks variables for 3 address code
def unpack_variables(variable, function, adrCodeLines):
    expression = function[variable]
    operator = list(expression.keys())[0]
    operands = list(expression.values())[0]

    operand1 = operands[0]
    operand2 = operands[1]


    

    if type(operand1) == dict:
        assignExpr = str(list(operand1.keys())[0]) + " = " + str(list(operand1.values())[0])
        op1 = list(operand1.keys())[0]
        if assignExpr not in adrCodeLines:
            adrCodeLines.append(assignExpr)
    else:
        op1 = operand1


    if type(operand2) == dict:
        assignExpr = str(list(operand2.keys())[0]) + " = " + str(list(operand2.values())[0])
        op2 = list(operand2.keys())[0]
        if assignExpr not in adrCodeLines:
            adrCodeLines.append(assignExpr)
    else:
        op2 = operand2


    assignExpr = str(variable) + " = " + str(op1) +" " + str(operator) +" "+ str(op2)
    if assignExpr not in adrCodeLines:
        adrCodeLines.append(assignExpr)



    return adrCodeLines


#assign variable function to generate  the 3 adress code
def assign_variable(variable, function, adrCodeLines):
    rExpr = function[variable]

    assignExpr = str(variable) + " = " + str(rExpr)
    if assignExpr not in adrCodeLines:
        adrCodeLines.append(assignExpr)


    return adrCodeLines


#fubction generates the 3 adrees code for return statement
def add_return(variable, function, adrCodeLines):
    expression = function[variable]

    if type(expression) == dict:
        result = list(expression.keys())[0]
        rExpr = list(expression.values())[0]
        if type(rExpr) == dict:
            operator = list(rExpr.keys())[0]
            operands = list(rExpr.values())[0]

            operand1 = operands[0]
            operand2 = operands[1]

            if type(operand1) == dict:
                assignExpr = str(list(operand1.keys())[0]) + " = " + str(list(operand1.values())[0])
                op1 = list(operand1.keys())[0]
                if assignExpr not in adrCodeLines:
                    adrCodeLines.append(assignExpr)
            else:
                op1 = operand1

            if type(operand2) == dict:
                assignExpr = str(list(operand2.keys())[0]) + " = " + str(list(operand2.values())[0])
                op2 = list(operand2.keys())[0]
                if assignExpr not in adrCodeLines:
                    adrCodeLines.append(assignExpr)

            else:
                op2 = operand2


            assignExpr = str(result) + " = " + str(op1) +" " + str(operator) +" " +str(op2)
            if assignExpr in adrCodeLines:
                assignExpr = str(variable) + " " + str(result)
                adrCodeLines.append(assignExpr)
            else:
                assignExpr = str(variable) + " "+  assignExpr
                adrCodeLines.append(assignExpr)


        else:
            assignExpr = str(result) + " = " + str(rExpr)
            if assignExpr in adrCodeLines:
                assignExpr = str(variable) +" "+ str(result)
                if assignExpr not in adrCodeLines:
                    adrCodeLines.append(assignExpr)


    else:
        assignExpr = str(variable) + " " + str(result)
        adrCodeLines.append(assignExpr)


    return adrCodeLines



#print function
def print_addressCodes(functionAdrCodes):
    print('Three Address COde:')
    print(functionAdrCodes)















