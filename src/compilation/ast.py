'''
ast.py

@Author - Shanti Upadhyay - spu0004@auburn.edu
@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 NOV 22

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
    compoundStatement = functionDefinition['compoundStatement']
    functionDefNode[functionDefinition['ID']['contents']] = add_compoundStatement(compoundStatement)
    return functionDefNode

def add_compoundStatement(compoundStatement):
    compoundStatementNode = []
    if 'localDeclarations' in compoundStatement and compoundStatement['localDeclarations'] != None:
        pass
    elif 'primaryStatement' in compoundStatement and compoundStatement['primaryStatement'] != None:
        primaryStatement = compoundStatement['primaryStatement']
        compoundStatementNode.append(add_primaryStatement(primaryStatement))
    else:
        raise astException

    if compoundStatement['compoundStatement'] != None:
        compoundStatementNode += add_compoundStatement(compoundStatement['compoundStatement'])

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

def add_primaryStatement(primaryStatment):
    if 'assignmentExpression' in primaryStatment:
        assignmentExpression = primaryStatment['assignmentExpression']
        primaryStatementNode = add_assignmentExpression(assignmentExpression)
    elif 'returnStatement' in primaryStatment:
        returnStatement = primaryStatment['returnStatement']
        primaryStatementNode = add_returnStatement(returnStatement)
    else:
        raise astException
    return primaryStatementNode

def add_assignmentExpression(assignmentExpression):
    identifier = assignmentExpression['identifier']['contents']
    expression = add_expression(assignmentExpression['expression'])
    assignmentExpressionNode = identifier + " = " + expression
    return assignmentExpressionNode


def add_expression(expression):
    if 'constant' in expression:
        expressionNode = add_constant(expression['constant'])
    elif 'identifier' in expression:
        expressionNode = add_identifier(expression['identifier'])
    elif 'binaryExpression' in expression:
        expressionNode = add_binaryExpression(expression['binaryExpression'])
    elif 'containedExpression' in expression:
        expressionNode = add_containedExpression(expression['containedExpression'])
    elif expression['type'] == 'containedExpression':
        expressionNode = add_containedExpression(expression)
    else:
        raise astException
    return expressionNode

def add_binaryExpression(binaryExpression):
    op = binaryExpression['op']['contents']
    expression1 = binaryExpression['expression1']
    expression2 = binaryExpression['expression2']
    binaryExpressionNode = add_expression(expression1) + " " + op + " " + add_expression(expression2)
    return binaryExpressionNode

def add_containedExpression(containedExpression):
    expression = containedExpression['expression']
    containedExpressionNode = "(" + add_expression(expression) + ")"
    return containedExpressionNode

def add_returnStatement(returnStatement):
    expression = add_expression(returnStatement['contents'])
    returnStatementNode = "return " + expression
    return returnStatementNode

def add_constant(constant):
    return constant['contents']

def add_identifier(identifier):
    return identifier['contents']
    