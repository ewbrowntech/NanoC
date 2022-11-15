'''
parser.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 08 NOV 22

Parses tokens
'''

class parse_exception(Exception):
    pass

localIndex = 0

def parse(tokens):
    parseTree = parse_program(tokens)
    return parseTree

def parse_program(tokens): # <program> := <declarationList>
    program = {'type': 'program'}
    program['declarationList'] = parse_DeclList(tokens)
    return program

def parse_DeclList(tokens): # <declarationList> := <functionDefinition>
    declarationList = {'type': 'declarationList'}
    declarationList['functionDefinition'] = parse_FuncDef(tokens)
    return declarationList

def parse_FuncDef(tokens): # <functionDefinition> := <type> <id> ( <parameterList> ) { <compoundStatement> }
    global localIndex
    functionDefinition = {'type': 'functionDefinition'}
    functionDefinition['TYPE'] = parse_type(tokens)
    functionDefinition['ID'] = parse_Identifier(tokens)

    if tokens[localIndex]['type'] == 'LPAR' and tokens[localIndex]['contents'] == '(':
        localIndex +=1
        functionDefinition['params'] = parse_ParamList(tokens)
    else:
        raise parse_exception

    if tokens[localIndex]['type'] == 'RPAR' and tokens[localIndex]['contents'] == ')':
        localIndex += 1
    else:
        raise parse_exception

    if tokens[localIndex]['type'] == 'LBRACE' and tokens[localIndex]['contents'] == '{':
        localIndex += 1
        functionDefinition['compoundStatement'] = parse_CompoundStatement(tokens)
    else:
        raise parse_exception

    if tokens[localIndex]['type'] == 'RBRACE' and tokens[localIndex]['contents'] == '}':
        localIndex += 1
        return functionDefinition
    else:
        raise parse_exception

def parse_type(tokens): # <type> = int
    global localIndex
    type = {'type': 'type'}
    if tokens[localIndex]['type'] == 'TYPE':
        type['contents'] = tokens[localIndex]['contents']
        localIndex += 1
    else:
        print(tokens[localIndex])
        raise parse_exception
    return type

def parse_Identifier(tokens):
    global localIndex
    identifier = {'type': 'identifier'}
    if tokens[localIndex]['type'] == 'ID':
        identifier['contents'] = tokens[localIndex]['contents']
        localIndex += 1
        return identifier
    else:
        raise parse_exception

def parse_ParamList(tokens):
    return None

def parse_CompoundStatement(tokens): # <compoundStatement> := <localDeclarations> <compoundStatement> | <primaryStatement> <compoundStatement> | None
    global localIndex
    compoundStatement = {'type': 'compoundStatement'}
    if tokens[localIndex]['type'] == 'RBRACE':
        return None
    if tokens[localIndex]['type'] == 'TYPE':
        compoundStatement['localDeclarations'] = parse_localDeclarations(tokens)
    else:
        compoundStatement['primaryStatement'] = parse_PrimaryStatement(tokens)
    compoundStatement['compoundStatement'] = parse_CompoundStatement(tokens)
    if (localIndex == len(tokens)):  # Reached the end of source code without a closing brace
        raise parse_exception
    return compoundStatement

def parse_localDeclarations(tokens): # <localDeclarations> := <variableDeclaration> <localDeclarations>
    global localIndex
    localDeclarations = {'type': 'localDeclarations'}
    if tokens[localIndex]['type'] == 'TYPE':
        localDeclarations['variableDeclaration'] = parse_variableDeclaration(tokens)
        if tokens[localIndex]['type'] == 'TYPE':
            localDeclarations['localDeclarations'] = parse_localDeclarations(tokens)
        else:
            localDeclarations['localDeclarations'] = None
        return localDeclarations
    else:
        return None

def parse_variableDeclaration(tokens): # <variableDeclaration> := <type> <identifier> ; | <type> <identifier> = <expression> ;
    global localIndex
    variableDeclaration = {'type': 'variableDeclaration'}
    variableDeclaration['TYPE'] = parse_type(tokens)
    variableDeclaration['ID'] = parse_Identifier(tokens)
    localIndex += 1
    return variableDeclaration

def parse_PrimaryStatement(tokens): # <primaryStatement> := <assignmentExpression> | <returnStatement> ;
    global localIndex
    primaryStatement = {'type': 'primaryStatement'}

    if tokens[localIndex]['type'] == 'ID':
        primaryStatement['assignmentExpression'] = parse_assignementExpression(tokens)
    elif tokens[localIndex]['contents'] == 'return':
        primaryStatement['returnStatement'] = parse_ReturnStatemenet(tokens)
    else:
        primaryStatement['expression'] = parse_Expression(tokens)

    if tokens[localIndex]['type'] == 'SYMBOL' and tokens[localIndex]['contents'] == ';':
        localIndex += 1
        return primaryStatement
    else:
        # print(tokens[localIndex])
        raise parse_exception

def parse_assignementExpression(tokens): # <assignementExpression> := <identifier> = <expression>
    global localIndex
    assignementExpression = {'type': 'assignementExpression'}
    assignementExpression['identifier'] = parse_Identifier(tokens)
    if tokens[localIndex]['contents'] == '=':
        localIndex += 1
        assignementExpression['expression'] = parse_Expression(tokens)
    else:
        raise parse_exception
    return assignementExpression

def parse_ReturnStatemenet(tokens): # <returnStatement> := return <expression> ;
    global localIndex
    returnStatement = {'type': 'returnStatement'}
    if tokens[localIndex]['type'] == 'KEYWORD' and tokens[localIndex]['contents'] == 'return':
        localIndex += 1
        returnStatement['contents'] = parse_Expression(tokens)
        return returnStatement
    else:
        raise parse_exception

def parse_Expression(tokens): # <expression> := <constant> | <identifier> | <expression> <op> <expression>
    global localIndex
    expression = {'type': 'expression'}
    if tokens[localIndex]['contents'].isnumeric():
        expression['constant'] = parse_Const(tokens) # This breaks set grammar, but we ran out of time for code review
        if tokens[localIndex]['type'] == 'OP' and tokens[localIndex]['contents'] != '=':
            expression['op'] = tokens[localIndex]['contents']
            localIndex += 1
            expression['expression'] = parse_Expression(tokens)
    else:
        expression['contents'] = parse_Identifier(tokens)
    return expression

def parse_Const(tokens):
    global localIndex
    constant = {'type': 'constant'}
    if tokens[localIndex]['type'] == 'NUM':
        constant['contents'] = tokens[localIndex]['contents']
        localIndex+=1
        return constant
    else:
        raise parse_exception

def print_parseTree(parseTree):
    print("Parse Tree:")
    print(parseTree)