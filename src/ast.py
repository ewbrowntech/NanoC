'''
ast.py

@Author - Shanti Upadhyay - spu0004@auburn.edu

@Version - 08 NOV 22

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
    functionDefNode[functionDefinition['ID']['contents']] = add_CompoundStatement(compoundStatement)
    return functionDefNode

def add_CompoundStatement(compoundStatement):
    compoundStatementNode = {}
    if compoundStatement['localDeclarations'] != None:
        localDeclarations = compoundStatement['localDeclarations']
        compoundStatementNode = add_LocalDeclarations(compoundStatementNode, localDeclarations) # modifying existing
    primaryStatement = compoundStatement['primaryStatement']                                    # compound statement
    returnStatement = primaryStatement['returnStatement']
    compoundStatementNode = add_ReturnStatemenet(compoundStatementNode, returnStatement) # modifying existing
    return compoundStatementNode                                                         # compound statement

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
    print("\n" + str(localDeclarations))  
    print("\n" + str(variableDeclaration))
    print("\n" + str(identifier))
    print("\n" + str(contents))
    print("\n" + str(nestedLocalDeclarations))
    return compoundStatementNode

def add_ReturnStatemenet(compoundStatementNode, returnStatement): # right now primary statement is 
    expression = returnStatement['contents']                      # only a return statement
    constant = expression['contents']                             # no arithmetic yet
    compoundStatementNode['return'] = add_Constant(constant)
    return compoundStatementNode   

def add_Constant(constant):
    constantNode = {}
    constantNode[constant['contents']] = {}
    return constantNode           

