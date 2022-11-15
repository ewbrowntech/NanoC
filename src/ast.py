'''
ast.py

@Author - Shanti Upadhyay - spu0004@auburn.edu

@Version - 15 NOV 22

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
    print("\nAbstract Syntax Tree:")
    print(ast)

def add_funcDef(functionDefinition): # Begin descending down functionDefinition
    functionDefNode = {}
    compoundStatement = functionDefinition['compoundStatement']
    functionDefNode[functionDefinition['ID']['contents']] = add_CompoundStatement(None, compoundStatement)
    return functionDefNode

def add_CompoundStatement(compoundStatementNode, compoundStatement):
    if compoundStatementNode == None:
        compoundStatementNode = {}
    statementKeys = compoundStatement.keys()
    if 'localDeclarations' in statementKeys and compoundStatement['localDeclarations'] != None:
        localDeclarations = compoundStatement['localDeclarations']
        compoundStatementNode = add_LocalDeclarations(compoundStatementNode, localDeclarations) 
    if 'primaryStatement' in statementKeys and compoundStatement['primaryStatement'] != None:
        primaryStatement = compoundStatement['primaryStatement']
        if 'returnStatement' in primaryStatement.keys():
            returnStatement = primaryStatement['returnStatement']
            compoundStatementNode = add_ReturnStatemenet(compoundStatementNode, returnStatement)
        elif 'assignmentExpression' in primaryStatement.keys():
            assignmentExpression = primaryStatement['assignmentExpression']
            identifier = assignmentExpression['identifier']
            nodeKeys = compoundStatementNode.keys()
            if identifier['contents'] in nodeKeys:
                expression = assignmentExpression['expression']
                compoundStatementNode[identifier['contents']] = add_Expression(expression)
        else:
            raise astException 
    if compoundStatement['compoundStatement'] != None:
        compoundStatementNode = add_CompoundStatement(compoundStatementNode, compoundStatement['compoundStatement'])  
    return compoundStatementNode                                                        

def add_LocalDeclarations(compoundStatementNode, localDeclarations): # this is recursive
    variableDeclaration = localDeclarations['variableDeclaration']
    identifier = variableDeclaration['ID']
    contents = identifier['contents']
    compoundStatementNode[contents] = {}
    nestedLocalDeclarations = localDeclarations['localDeclarations']
    if nestedLocalDeclarations != None:
        compoundStatementNode = add_LocalDeclarations(compoundStatementNode, nestedLocalDeclarations)
    # Currently, variable assignment is not functioning correctly in the parser
    # idContents = identifier['contents']
    # primaryStatement = variableDeclaration['primaryStatement']
    # expression = primaryStatement['expression']
    # constant = expression['contents']
    # constContents = constant['contents']
    # compoundStatementNode[idContents] = {}
    # compoundStatementNode[idContents][constContents] = {}
    # print("\n" + str(localDeclarations))  
    # print("\n" + str(variableDeclaration))
    # print("\n" + str(identifier))
    # print("\n" + str(contents))
    # print("\n" + str(nestedLocalDeclarations))
    return compoundStatementNode

def add_Expression(expression):
    expressionNode = {}
    expressionKeys = expression.keys()
    constant = expression['constant']
    if constant['type'] == 'constant':
        expressionNode[constant['contents']] = {} 
    if 'op' in expressionKeys:
        expressionNode[expression['op']] = {} # This will be changed such that expressionNodes are lists instead of dictionaries
        expressionNode[expression['expression']['constant']['contents']] = {}
    return expressionNode

def add_ReturnStatemenet(compoundStatementNode, returnStatement): # right now primary statement is 
    expression = returnStatement['contents']                      # only a return statement
    constant = expression['constant']                             # no arithmetic yet
    compoundStatementNode['return'] = add_Constant(constant)
    return compoundStatementNode   

def add_Constant(constant):
    constantNode = {}
    constantNode[constant['contents']] = {}
    return constantNode           
    