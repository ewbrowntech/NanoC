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

import errors


def generate_symbolTable(psrseTree):
    symbolTable = dict()

    symbolTable, undeclaredList = get_declarationList(psrseTree)

    if not undeclaredList:
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
        print('\n')
        #print('\n----------------'\n)
        print('No global variables declared: ')

 
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

    if functionDefNode == None:
        functionDefNode = dict()

    functionDefNode['returnType'] = functionDefinition['TYPE']['contents']

    if functionDefinition['compoundStatement'] != None:
        compoundstatements = functionDefinition['compoundStatement']
        if 'localDeclarations' in compoundstatements and compoundstatements['localDeclarations'] != None:
            functionDefNode, undeclaredVars = get_localDeclarations(functionDefNode, compoundstatements, undeclaredVars)


        

    return functionDefNode, undeclaredVars


#parse through the local declarations to get local variables in function
def get_localDeclarations(functionDefNode, compoundstatements, undeclaredVars):
    localDeclarations = compoundstatements['localDeclarations']

    if 'variableDeclaration' in localDeclarations:
        variableDeclaration = localDeclarations['variableDeclaration']
        variableName = variableDeclaration['ID']['contents']
        functionDefNode[variableName] = get_variableType(variableDeclaration)

    if 'localDeclarations' in localDeclarations and localDeclarations['localDeclarations'] !=None:
        functionDefNode, undeclaredVars = get_localDeclarations(functionDefNode, localDeclarations, undeclaredVars)

    #check for variable declaration before use
    if 'compoundStatement' in compoundstatements and compoundstatements['compoundStatement'] != None:
        undeclaredVars = check_expressions(functionDefNode, compoundstatements, undeclaredVars)
        
    return functionDefNode, undeclaredVars



def check_expressions(functionDefNode, compoundstatements, undeclaredVars):

        compoundStatement = compoundstatements['compoundStatement']
        primaryStatement = compoundStatement['primaryStatement']
        if 'assignmentExpression' in primaryStatement:
            assignmentExpression = primaryStatement['assignmentExpression']
            assignedVar = assignmentExpression['identifier']['contents']
            undeclaredVars = check_VarDeclaration(functionDefNode, assignedVar, undeclaredVars)

            if 'expression' in assignmentExpression:
                expression = assignmentExpression['expression']
                undeclaredVars = check_rExpression(functionDefNode, expression, undeclaredVars)

        if 'compoundStatement' in compoundStatement and compoundStatement['compoundStatement'] != None:
            undeclaredVars = check_expressions(functionDefNode, compoundStatement, undeclaredVars)


        return undeclaredVars





#go through the variable declaration list to get each variable in function
def get_variableType(variableDeclaration):
    variableType = dict()
    var_type = variableDeclaration['TYPE']
    variableType['type'] = var_type['contents']

    return variableType




#check right hand expressions for varible being declared
def check_rExpression(functionDefNode, expression, undeclaredVars):
    if 'expression' in expression:
        expr = expression['expression']
        exprVar = expr['contents']['contents']
        undeclaredVars = check_VarDeclaration(functionDefNode, exprVar, undeclaredVars)

        if 'expression' in expr:
            undeclaredVars = check_rExpression(functionDefNode, expr, undeclaredVars)

    return undeclaredVars




#variable declaration checker
def check_VarDeclaration(functionDefNode, assignedVar, undeclaredVars):
    if assignedVar != None:
        if assignedVar not in functionDefNode:
            undeclaredVars.append(assignedVar)

    return undeclaredVars
           
            

#add global variables to symbol table
def get_globalVariables(globalVariables):
    globalVariableNode  = {'scope':'global'}

  
    return None





    



















