"""
# This file contains the symbol_table egenrator program
#@Author: Paul Atilola - poa0002@qburn.edu
# @version  - Nov. 17. 2022

## features to add to symbol table implementation:
    1. check a function has been defined before its called
    2. visualize in a proper table.
      
"""
'''
    this function generates the symbol table. it checks from program level for:
    function defintions, variable declarations. for each function/variable,
    the table keeps record of the scope (variable), name, type, constants,
    parameters (function), and variables properties under each function
'''

import compilation.errors as errors


def generate_symbolTable(parseTree):
    symbolTable = dict()

    symbolTable, undeclaredList = get_declarationList(parseTree)

    emptyList = all(undeclared == [] for undeclared in list(undeclaredList.values())[0])

    if emptyList is True:
        return symbolTable
    else:
        errors.variableNotDeclared(undeclaredList)


def get_declarationList(parseTree):
    declarationListNode = dict()
    undeclaredList = dict()

    declarationList = parseTree['declarationList']       #get the top level program from psrdstree

    if 'variableDeclaration' in declarationList:           #to check for global vsariables
        globalVariables = declarationList['variableDeclaration']
        declarationListNode[globalVariables['ID']['contents']] = get_globalVariables(globalVariables)

    else:
        pass
        # print('\n')
        #print('\n----------------'\n)
        # print('No global variables declared: ')

 
    for key in declarationList:
        if key == 'functionDefinition':
            functionDefinition = declarationList['functionDefinition']
            functionName = functionDefinition['ID']['contents']
            declarationListNode[functionName], undeclaredList[functionName] = get_function(None, functionDefinition)

    functionDefinition = declarationList['functionDefinition']
    if 'functionDefinition' in functionDefinition:
        functiondefinition = functionDefinition['functionDefinition']
        functionName = functionDefinition['ID']['contents']
        declarationListNode[functionName], undeclaredList[functionName] = get_function(None, functiondefinition)


    return declarationListNode, undeclaredList



#print the full symbol table
def print_symbolTable(symbolTable):
    print('Symbol Table:')
    print(symbolTable)



#parse through each function in the delcaration list 
def get_function(functionDefNode, functionDefinition):

    undeclaredVars = list()
    assignmentList = list()

    if functionDefNode == None:
        functionDefNode = dict()

    functionDefNode['returnType'] = functionDefinition['TYPE']['contents']

    if functionDefinition['compoundStatement'] != None:
        compoundstatements = functionDefinition['compoundStatement']
        if 'localDeclarations' in compoundstatements and compoundstatements['localDeclarations'] != None:
            functionDefNode, undeclaredVars, assignmentList = get_localDeclarations(functionDefNode, compoundstatements, undeclaredVars, assignmentList)


        

    return functionDefNode, undeclaredVars


#parse through the local declarations to get local variables in function
def get_localDeclarations(functionDefNode, compoundstatements, undeclaredVars, assignmentList):
    localDeclarations = compoundstatements['localDeclarations']

    if 'variableDeclaration' in localDeclarations:
        variableDeclaration = localDeclarations['variableDeclaration']
        variableName = variableDeclaration['ID']['contents']
        functionDefNode[variableName] = get_variableType(variableDeclaration)

    if 'localDeclarations' in localDeclarations and localDeclarations['localDeclarations'] !=None:
        functionDefNode, undeclaredVars, assignmentList = get_localDeclarations(functionDefNode, localDeclarations, undeclaredVars, assignmentList)

    #check for variable declaration before use
    if 'compoundStatement' in compoundstatements and compoundstatements['compoundStatement'] != None:
        undeclaredVars, assignmentList = check_expressions(functionDefNode, compoundstatements, undeclaredVars, assignmentList)
        
    return functionDefNode, undeclaredVars, assignmentList



def check_expressions(functionDefNode, compoundstatements, undeclaredVars, assignmentList):

        compoundStatement = compoundstatements['compoundStatement']
        primaryStatement = compoundStatement['primaryStatement']
        if 'assignmentExpression' in primaryStatement:
            assignmentExpression = primaryStatement['assignmentExpression']
            assignedVar = assignmentExpression['identifier']['contents']
            undeclaredVars, varState  = check_VarDeclaration(functionDefNode, assignedVar, undeclaredVars)

            if varState is True:
                assignmentList.append(assignedVar)


            if 'expression' in assignmentExpression:
                expression = assignmentExpression['expression']
                undeclaredVars = check_rExpression(functionDefNode, expression, undeclaredVars, assignmentList)


        if 'returnStatement' in primaryStatement:
            returnStatement = primaryStatement['returnStatement']
            returncontents = returnStatement['contents']
            
            if 'identifier' in returncontents:
                returnVar = returncontents['identifier']['contents']
                undeclaredVars, varState = check_VarDeclaration(functionDefNode, returnVar, undeclaredVars)

                if varState is True:
                    undeclaredVars = check_VarAssigned(assignmentList, returnVar, undeclaredVars)




        if 'compoundStatement' in compoundStatement and compoundStatement['compoundStatement'] != None:
            undeclaredVars, assignmentList = check_expressions(functionDefNode, compoundStatement, undeclaredVars, assignmentList)


        return undeclaredVars, assignmentList





#go through the variable declaration list to get each variable in function
def get_variableType(variableDeclaration):
    variableType = dict()
    var_type = variableDeclaration['TYPE']
    variableType['type'] = var_type['contents']

    return variableType




#check right hand expressions for varible being declared
def check_rExpression(functionDefNode, expression, undeclaredVars, assignmentList):

    if 'binaryExpression' in expression:
        binaryExpression = expression['binaryExpression']

        for expr in binaryExpression:
            if type(binaryExpression[expr]) == dict:
                rExpr = binaryExpression[expr]
                if 'identifier' in rExpr:
                    exprVar = rExpr['identifier']['contents']
                    undeclaredVars, varState = check_VarDeclaration(functionDefNode, exprVar, undeclaredVars)

                    if varState is True:
                        undeclaredVars = check_VarAssigned(assignmentList, exprVar, undeclaredVars)


    return undeclaredVars




#variable declaration checker
def check_VarDeclaration(functionDefNode, assignedVar, undeclaredVars):
    varState = True    # we assume all variables are dclared before being used

    if assignedVar != None:
        if assignedVar not in functionDefNode:

            undeclaredVars.append(str(assignedVar))
            varState = False


    return undeclaredVars, varState
           
            



#checks if variable on right side of expression is assigned before use
def check_VarAssigned(assignmentList, exprVar, undeclaredVars):

    if assignmentList:
        count_exist = assignmentList.count(exprVar)

        if count_exist == 0:
            str_var = str(exprVar)
            str_var = str_var + '+'
            undeclaredVars.append(str_var)


    return undeclaredVars



#add global variables to symbol table
def get_globalVariables(globalVariables):
    globalVariableNode  = {'scope':'global'}

  
    return None




# function to query the symbol table for funcction and variable
def query_symbolTable(variable, symbolTable):

    checker = 0

    for global_params in symbolTable:
        if variable == global_params:
            if type(symbolTable[global_params]) == dict:
                func_params = symbolTable[global_params]
                for params in func_params:
                    if params == 'returnType':
                        returnType = func_params[params]
                        checker = 1
                        print("function '{}' is of type '{}' \n".format(variable, returnType))

            else:
                checker = 1
                print("variable '{}' is in global scope \n".format(variable))

        else:
            func_params = symbolTable[global_params]
            for params in func_params:
                if variable == params:
                    varTypeInfo = func_params[params]
                    if type(varTypeInfo) == dict:
                        varType = list(varTypeInfo.values())[0]
                        checker = 1
                        print("variable '{}' in function '{}' is of type '{}' \n".format(variable, global_params, varType))

    if checker == 0:
        print("Error: Cannot find '{}'in the symbolTable \n ".format(variable))













    



















