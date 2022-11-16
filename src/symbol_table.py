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

def generate_symbolTable(psrseTree):
    symbolTable = dict()

    symbolTable = get_declarationList(psrseTree)

    return symbolTable


def get_declarationList(parseTree):
    declarationListNode = dict()

    declarationList = parseTree['declarationList']       #get the top level program from psrdstree

    if 'variableDeclaration' in declarationList:           #to check for global vsariables
        globalVariables = declarationList['variableDeclaration']
        declarationListNode[globalVariables['ID']['contents']] = get_globalVariables(globalVariables)

    else:
        print('\n------------------\n')
        print('No global variables declared: ')

 
    for key in declarationList:
        if key == 'functionDefinition':
            functionDefinition = declarationList['functionDefinition']
            declarationListNode[functionDefinition['ID']['contents']] = get_function(None, functionDefinition)

    functionDefinition = declarationList['functionDefinition']
    if 'functionDefinition' in functionDefinition:
        functiondefinition = functionDefinition['functionDefinition']
        declarationListNode[functiondefinition['ID']['contents']] = get_function[None, functiondefinition]


    return declarationListNode



#print the full symbol table
def print_symbolTable(symbolTable):
    print('Symbol Table:')
    print(symbolTable)



#parse through each function in the delcaration list 
def get_function(functionDefNode, functionDefinition):

    if functionDefNode == None:
        functionDefNode = dict()

    functionDefNode['rtype'] = functionDefinition['TYPE']['contents']

    if functionDefinition['compoundStatement'] != None:
        compoundstatements = functionDefinition['compoundStatement']
        if 'localDeclarations' in compoundstatements and compoundstatements['localDeclarations'] != None:
            functionDefNode = get_localDeclarations(functionDefNode, compoundstatements)


        

    return functionDefNode


#parse through the local declarations to get local variables in function
def get_localDeclarations(functionDefNode, compoundstatements):
    localDeclarations = compoundstatements['localDeclarations']

    if 'variableDeclaration' in localDeclarations:
        variableDeclaration = localDeclarations['variableDeclaration']
        variableName = variableDeclaration['ID']['contents']
        functionDefNode[variableName] = get_variableType(variableDeclaration)

    if 'localDeclarations' in localDeclarations and localDeclarations['localDeclarations'] !=None:
        functionDefNode = get_localDeclarations(functionDefNode, localDeclarations)

    #check for variable declaration before use
    if 'compoundStatement' in compoundstatements and compoundstatements['compoundStatement'] != None:
        check_expressions(functionDefNode, compoundstatements)
        
    return functionDefNode



def check_expressions(functionDefNode, compoundstatements):

        compoundStatement = compoundstatements['compoundStatement']
        primaryStatement = compoundStatement['primaryStatement']
        assignmentExpression = primaryStatement['assignmentExpression']
        assignedVar = assignmentExpression['identifier']['contents']
        check_VarDeclaration(functionDefNode, assignedVar)

        if 'compoundStatement' in compoundStatement and compoundStatement['compoundStatement'] != None:
            check_expressions(functionDefNode, compoundStatement)



#go through the variable declaration list to get each variable in function
def get_variableType(variableDeclaration):
    variableType = dict()
    var_type = variableDeclaration['TYPE']
    variableType['type'] = var_type['contents']

    return variableType


#variable declaration checker
def check_VarDeclaration(functionDefNode, assignedVar):
    if assignedVar != None:
        if assignedVar not in functionDefNode:
            raise Exception('assigned variable "{}" was never declared \n' .format(assignedVar))
            

#add global variables to symbol table
def get_globalVariables(globalVariables):
    globalVariableNode  = {'scope':'global'}

  
    return None





    



















