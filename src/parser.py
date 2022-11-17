"""
parser.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 17 NOV 22

Parses tokens
"""


def parse(tokens):
    parseTree = parse_program(tokens)
    return parseTree

class parseException(Exception):
    pass

localIndex = 0

# <program> := <declarationList>
def parse_program(tokens):
    program = {'type': 'program', 'declarationList': parse_declarationList(tokens)}
    return program

# <declarationList> := <functionDefinition> FOR NOW
def parse_declarationList(tokens):  # <declarationList> := <functionDefinition>
    declarationList = {'type': 'declarationList', 'functionDefinition': parse_functionDefinition(tokens)}
    return declarationList

# <functionDefinition> := <type> <id> ( <parameterList> ) { <compoundStatement> }
def parse_functionDefinition(tokens):
    global localIndex
    functionDefinition = {'type': 'functionDefinition', 'TYPE': parse_type(tokens), 'ID': parse_identifier(tokens)}

    if tokens[localIndex]['type'] == 'LPAR' and tokens[localIndex]['contents'] == '(':
        localIndex += 1
        functionDefinition['parameterList'] = None
    else:
        raise parseException

    if tokens[localIndex]['type'] == 'RPAR' and tokens[localIndex]['contents'] == ')':
        localIndex += 1
    else:
        raise parseException

    if tokens[localIndex]['type'] == 'LBRACE' and tokens[localIndex]['contents'] == '{':
        localIndex += 1
        functionDefinition['compoundStatement'] = parse_CompoundStatement(tokens)
    else:
        raise parseException

    if tokens[localIndex]['type'] == 'RBRACE' and tokens[localIndex]['contents'] == '}':
        localIndex += 1
        return functionDefinition
    else:
        raise parseException

# <type> = int
def parse_type(tokens):
    global localIndex
    type = {'type': 'type'}
    if tokens[localIndex]['type'] == 'TYPE':
        type['contents'] = tokens[localIndex]['contents']
        localIndex += 1
    else:
        print(tokens[localIndex])
        raise parseException
    return type

# <identifier> := string
def parse_identifier(tokens):
    global localIndex
    identifier = {'type': 'identifier'}
    if tokens[localIndex]['type'] == 'ID':
        identifier['contents'] = tokens[localIndex]['contents']
        localIndex += 1
        return identifier
    else:
        raise parseException

# <parameterList> = <identifier> <parameterList> | <variableDeclaration> <parameterList> | None
def parse_parameterList():
    return None

# <compoundStatement> := <localDeclarations> <compoundStatement> | <primaryStatement> <compoundStatement> | None
def parse_CompoundStatement(tokens):
    global localIndex
    compoundStatement = {'type': 'compoundStatement'}
    if tokens[localIndex]['type'] == 'RBRACE':
        return None
    if tokens[localIndex]['type'] == 'TYPE':
        compoundStatement['localDeclarations'] = parse_localDeclarations(tokens)
    else:
        compoundStatement['primaryStatement'] = parse_primaryStatement(tokens)
    compoundStatement['compoundStatement'] = parse_CompoundStatement(tokens)
    if localIndex == len(tokens):  # Reached the end of source code without a closing brace
        raise parseException
    return compoundStatement

# <localDeclarations> := <variableDeclaration> <localDeclarations>
def parse_localDeclarations(tokens):
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

# <variableDeclaration> := <type> <identifier> ; | <type> <identifier> = <expression> ;
def parse_variableDeclaration(tokens):
    global localIndex
    variableDeclaration = {'type': 'variableDeclaration', 'TYPE': parse_type(tokens), 'ID': parse_identifier(tokens)}
    localIndex += 1
    return variableDeclaration

# <primaryStatement> := <assignmentExpression> | <returnStatement> ;
def parse_primaryStatement(tokens):
    global localIndex
    primaryStatement = {'type': 'primaryStatement'}

    if tokens[localIndex]['type'] == 'ID':
        primaryStatement['assignmentExpression'] = parse_assignmentExpression(tokens)
    elif tokens[localIndex]['contents'] == 'return':
        primaryStatement['returnStatement'] = parse_returnStatement(tokens)
    else:
        primaryStatement['expression'] = parse_expression(tokens)

    if tokens[localIndex]['type'] == 'SYMBOL' and tokens[localIndex]['contents'] == ';':
        localIndex += 1
        return primaryStatement
    else:
        # print(tokens[localIndex])
        raise parseException

# <assignmentExpression> := <identifier> = <expression>
def parse_assignmentExpression(tokens):
    global localIndex
    assignmentExpression = {'type': 'assignmentExpression', 'identifier': parse_identifier(tokens)}
    if tokens[localIndex]['contents'] == '=':
        localIndex += 1
        assignmentExpression['expression'] = parse_expression(tokens)
    else:
        raise parseException
    return assignmentExpression

# <returnStatement> := return <expression> ;
def parse_returnStatement(tokens):
    global localIndex
    returnStatement = {'type': 'returnStatement'}
    if tokens[localIndex]['type'] == 'KEYWORD' and tokens[localIndex]['contents'] == 'return':
        localIndex += 1
        returnStatement['contents'] = parse_expression(tokens)
        return returnStatement
    else:
        raise parseException

# <expression> := <constant> | <identifier> | <expression> <op> <expression>
def parse_expression(tokens):
    global localIndex
    expression = {'type': 'expression'}
    if tokens[localIndex]['contents'].isnumeric():
        expression['constant'] = parse_constant(tokens)    # This breaks set grammar
        if tokens[localIndex]['type'] == 'OP' and tokens[localIndex]['contents'] != '=':
            expression['op'] = tokens[localIndex]['contents']
            localIndex += 1
            expression['expression'] = parse_expression(tokens)
    else:
        expression['contents'] = parse_identifier(tokens)
    return expression

# <constant> := num
def parse_constant(tokens):
    global localIndex
    constant = {'type': 'constant'}
    if tokens[localIndex]['type'] == 'NUM':
        constant['contents'] = tokens[localIndex]['contents']
        localIndex += 1
        return constant
    else:
        raise parseException

def print_parseTree(parseTree):
    print("Parse Tree:")
    print(parseTree)
