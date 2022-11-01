'''
parser.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 31 OCT 22

Parses tokens
'''

class parse_exception(Exception):
    pass

localIndex = 0

def parse(tokens):
    parseTree = parse_program(tokens)
    return parseTree

def parse_program(tokens):
    program = {'type': 'program'}
    program['declarationList'] = parse_DeclList(tokens)
    return program

def parse_DeclList(tokens):
    declarationList = {'type': 'declarationList'}
    declarationList['functionDefinition'] = parse_FuncDef(tokens)
    return declarationList

def parse_FuncDef(tokens):
    global localIndex
    functionDefinition = {'type': 'functionDefinition'}
    if tokens[localIndex]['type'] == 'TYPE':
        functionDefinition['TYPE'] = tokens[localIndex]['contents']
        localIndex += 1
        functionDefinition['ID'] = parse_Identifier(tokens)
    else:
        print(tokens[localIndex])
        raise parse_exception

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

def parse_CompoundStatement(tokens):
    compoundStatement = {'type': 'compoundStatment'}
    if tokens[localIndex]['type'] == 'RBRACE':
        return None
    elif tokens[localIndex]['contents'] == 'return':
        compoundStatement['returnStatement'] = parse_ReturnStatemenet(tokens)
    else:
        compoundStatement['primaryExpression'] = parse_PrimaryExpr(tokens)
    compoundStatement['compoundStatement'] = parse_CompoundStatement(tokens)
    if (localIndex == len(tokens)):  # Reached the end of source code without a closing brace
        raise parse_exception

    # while(tokens[localIndex]['type'] != 'RBRACE'):
    #     if tokens[localIndex]['contents'] == 'return':
    #         compoundStatement['contents'].append(parse_ReturnStatemenet(tokens))
    #     else:
    #         compoundStatement['contents'].append(parse_PrimaryExpr(tokens))
    #     if (localIndex == len(tokens)):                         # Reached the end of source code without a closing brace
    #         raise parse_exception


    return compoundStatement

def parse_ReturnStatemenet(tokens):
    global localIndex
    returnStatement = {'type': 'returnStatement'}
    if tokens[localIndex]['type'] == 'KEYWORD' and tokens[localIndex]['contents'] == 'return':
        localIndex += 1
        returnStatement['contents'] = parse_PrimaryExpr(tokens)
        if tokens[localIndex]['type'] == 'SYMBOL' and tokens[localIndex]['contents'] == ';':
            localIndex += 1
            return returnStatement
        else:
            raise parse_exception
    else:
        raise parse_exception

def parse_PrimaryExpr(tokens):
    primaryExpression = {'type': 'primaryExpr'}
    primaryExpression['contents'] = parse_Expr(tokens)
    return primaryExpression
    pass

def parse_Expr(tokens): # Will need exception later
    expression = {'type': 'expression'}
    if tokens[localIndex]['contents'].isnumeric():
        expression['contents'] = parse_Const(tokens)
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

#     parseLayers = list(parseTree.keys())
#
#     print("\n")
#     for layer in parseLayers:
#         if isinstance(parseTree[layer], str):
#             print(parseTree[layer])
#         if isinstance(parseTree[layer], dict):
#             printLayers(parseTree[layer])
#
# def printLayers(dictionary):
#     if isinstance(dictionary[layer], str):
#         print(dictionary[layer])
#     if isinstance(dictionary[layer], dict):
#
#
#
#
#
#         subDict = dictionary[layer]
#         # print(subDict)
#         subDictLayers = list(subDict.keys())
#         # print(subDictLayers)
#         for sublayer in subDictLayers:
#             if isinstance(subDict[sublayer], str):
#                 print('|' + subDict[sublayer])
#             if isinstance(subDict[sublayer], dict):
#                 print('||' + str(subDict[sublayer]))