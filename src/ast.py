'''
ast.py

@Author - Shanti Upadhyay - spu0004@auburn.edu
@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 28 NOV 22

Generates AST from Parse Tree
'''

def astGen(parseTree): # Generates AST
    declarationList = parseTree['declarationList']
    functionDefinition = declarationList['functionDefinition'] # For now, a program will always be a function def
    ast = add_funcDef(functionDefinition)                      # so we can descend directly into function def
    return ast

class astException(Exception):
    pass

def print_ast(ast):
    print("Abstract Syntax Tree:")
    print(str(ast) + "\n")

def add_funcDef(functionDefinition): # Begin descending down functionDefinition
    functionDefNode = {}
    localVariables = [] # Local symbol table just to get this working properly. This should be made to work with symboltable.py
    compoundStatement = functionDefinition['compoundStatement']
    functionDefNode[functionDefinition['ID']['contents']] = add_compoundStatement(None, compoundStatement, localVariables)
    return functionDefNode

def add_compoundStatement(compoundStatementNode, compoundStatement, localVariables):
    if compoundStatementNode == None:
        compoundStatementNode = {}
    statementKeys = compoundStatement.keys()
    if 'localDeclarations' in statementKeys and compoundStatement['localDeclarations'] != None:
        localDeclarations = compoundStatement['localDeclarations']
        compoundStatementNode, localVariables = add_localDeclarations(compoundStatementNode, localDeclarations, localVariables)
    if 'primaryStatement' in statementKeys and compoundStatement['primaryStatement'] != None:
        primaryStatement = compoundStatement['primaryStatement']
        if 'returnStatement' in primaryStatement.keys():
            returnStatement = primaryStatement['returnStatement']
            compoundStatementNode = add_returnStatement(compoundStatementNode, returnStatement, localVariables)
        elif 'assignmentExpression' in primaryStatement.keys():
            assignmentExpression = primaryStatement['assignmentExpression']
            compoundStatementNode = add_assignmentExpression(compoundStatementNode, assignmentExpression, localVariables)
        else:
            raise astException 
    if compoundStatement['compoundStatement'] != None:
        compoundStatementNode = add_compoundStatement(compoundStatementNode, compoundStatement['compoundStatement'], localVariables)
    return compoundStatementNode

def add_localDeclarations(compoundStatementNode, localDeclarations, localVariables): # this is recursive
    variableDeclaration = localDeclarations['variableDeclaration']
    identifier = variableDeclaration['ID']
    contents = identifier['contents']
    localVariables.append(contents)
    compoundStatementNode[contents] = {}
    nestedLocalDeclarations = localDeclarations['localDeclarations']
    if nestedLocalDeclarations != None:
        compoundStatementNode, localVariables = add_localDeclarations(compoundStatementNode, nestedLocalDeclarations, localVariables)
    return compoundStatementNode, localVariables

def add_assignmentExpression(compoundStatementNode, assignmentExpression, variables):
    identifier = assignmentExpression['identifier']['contents']
    if identifier in variables:
        expression = assignmentExpression['expression']
        compoundStatementNode[identifier] = add_expression(expression, compoundStatementNode, variables)
    else:
        raise astException
    return compoundStatementNode

def add_expression(expression, localNode, variables):
    expressionNode = {}
    if 'binaryExpression' in expression:
        binaryExpression = expression['binaryExpression']
        expressionNode = add_binaryExpression(binaryExpression, localNode, variables)
    elif 'constant' in expression:
        expressionNode = add_constant(expression['constant'])
    elif 'identifier' in expression:
        identifier = expression['identifier']['contents']
        if identifier in variables:
            expressionNode = {identifier: localNode[identifier]}
        else:
            raise astException
    return expressionNode

def add_binaryExpression(binaryExpression, localNode, variables):
    binaryExpressionNode = {}
    op = binaryExpression['op']['contents']
    expression1 = binaryExpression['expression1']
    expression2 = binaryExpression['expression2']
    binaryExpressionNode[op] = [add_expression(expression1, localNode, variables), add_expression(expression2, localNode, variables)]
    return binaryExpressionNode

def add_returnStatement(compoundStatementNode, returnStatement, localVariables):
    expression = returnStatement['contents']
    compoundStatementNode['return'] = add_expression(expression, compoundStatementNode, localVariables)
    return compoundStatementNode   

def add_constant(constant):
    return constant['contents']
    