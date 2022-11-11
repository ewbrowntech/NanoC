"""
# This file contains the symbol_table egenrator program
#@Author: Paul Atilola - poa0002@qburn.edu
# @version  - Nov. 10. 2022
"""
'''
    this function generates the symbol table. it checks from program level for:
    function defintions, variable declarations. for each function/variable,
    the table keeps record of the scope (variable), name, type, constants,
    parameters (function), and variables properties under each function
'''

def generate_symbolTable(AST):
    symbolTable = dict()

    symbolTable['declarationList'] = get_declarationList(AST)

    return symbolTable


def get_declarationList(AST):
    declarationListNode = dict()

    declarationList = AST['declarationList']       #get the top level program from AST

    #if variableDeclaration in declarationList:      #to check for global vsariables
     #   globalVariables = declarationList['variableDeclaration']
      #  declarationListNode['variableDeclarations'] = get_globalVariables(globalVariables)

 
    for key in declarationList.keys():
        if key == 'functionDefinition':
            functionDefinition = declarationList['functionDefinition']
            declarationListNode['functionDefinition'] = get_functions(functionDefinition)


    return declarationListNode



#print the full symbol table
def print_symbolTable(symbolTable):
    print('\n Symbol Table \n')
    print(symbolTable)



#parse through each function in the delcaration list 
def get_functions(functionDefinition):     #descends through the AST to fetch each function
    functionDefNode = dict()
    functionDefNode['ID'] = functionDefinition['ID']['contents']
    functionDefNode['type'] = functionDefinition['TYPE']['contents']

    if functionDefinition['compoundStatement'] != None:
        functionDefNode['localDeclarations'] = get_localDeclarations(functionDefinition['compoundStatement'])

        key = 'functionDefinition'
        if key in functionDefinition.keys():
            functionDefNode['functionDefinition'] = get_functions(functionDefinition)
        

    return functionDefNode


#parse through the local declarations to get local variables in function
def get_localDeclarations(compoundStatement):
    localVariableNode = {'scope':'local'}

   
   
    localDeclarations = compoundStatement['localDeclarations']

    if localDeclarations != None:
        key = 'variableDeclaration'
        if key in localDeclarations.keys():
            localVariableNode['Variable'] = get_variableDeclarations(localDeclarations['variableDeclaration'])

        key = 'localDeclarations'
        if key in localDeclarations.keys():
           if localDeclarations['localDeclarations'] != None:
                localVariableNode['localDeclarations'] = get_localDeclarations(localDeclarations)


    return localVariableNode



#go through the variable declaration list to get each variable in function
def get_variableDeclarations(variableDeclaration):
    variable = dict()

    variable['ID'] = variableDeclaration['ID']['contents']
    variable['TYPE'] = get_variableTypeandScope(variableDeclaration['TYPE'])


    return variable


#get each local variable's type ans scope
def get_variableTypeandScope(variableType):
    TypeandScope = dict()

    TypeandScope['type'] = variableType['contents']
    TypeandScope['scope'] = 'local'


    return TypeandScope



#add global variables to symbol table
def get_globalVariables(globalVariables):
  
    return None





    



















