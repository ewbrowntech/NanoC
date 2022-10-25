# tokens = [{'type': 'keyword', 'contents': 'int'}, {'type': 'ID', 'contents': 'i'}, {'type': 'op', 'contents': '='},
#          {'type': 'val', 'contents': '5'}, {'type': 'op', 'contents': '*'}, {'type': 'lparen', 'contents': '('},
#          {'type': 'val', 'contents': '5'}, {'type': 'op', 'contents': '+'}, {'type': 'val', 'contents': '5'},
#          {'type': 'rparen', 'contents': ')'}]

# Decl: assgnDecl
# assgnDecl: key id = expr | id = expr
# expr = num | expr op expr | (expr)



class parse_exception:
    pass

keywords = ["int"]
localIndex = 0
def parse(tokens):
    parseTree = []
    parseTree.append("Decl")
    for token in tokens:
        if token['type'] == 'keyword':
            parseTree.append("assignDecl")
            parseTree.append(parseAssgn(tokens, tokens.index(token)))
    return parseTree

def parse_program(tokens, index):
    pass

def parse_DeclList():
    pass

def parse_FuncDef():
    pass

def parse_Identifier():
    pass

def parse_ParamList():
    pass

def parse_CompoundStatement():
    pass

def parse_ReturnStatemenet(tokens):
    global localIndex
    returnStatement = {'type': 'returnStatement'}
    if tokens(localIndex)['type'] == 'KEYWORD' and tokens(localIndex)['contents'] == 'return':
        localIndex += 1
        returnStatement['contents'] = parse_PrimaryExpr(tokens)
        if tokens(localIndex)['type'] == 'SYMBOL' and tokens(localIndex)['contents'] == ';':
            localIndex += 1
            return returnStatement
        else:
            raise parse_exception
    else:
        raise parse_exception

def parse_PrimaryExpr(tokens):
    primaryExpression = {'type': 'expression'}
    primaryExpression['contents'] = parse_Expr(tokens)
    return primaryExpression
    pass

def parse_Expr(tokens): # Will need exception later
    expression = {'type': 'expression'}
    expression['contents'] = parse_Const(tokens)
    return expression

def parse_Const(tokens):
    global localIndex
    constant = {'type': 'constant'}
    if tokens(localIndex)['type'] == 'NUM':
        constant['contents'] = tokens(localIndex)['contents']
        localIndex+=1
        return constant
    else:
        raise parse_exception
def parseAssgn(tokens, index):
    assgnExpr = {}
    for i in range(index, len(tokens)):
        if tokens[i]['type'] == 'keyword':
            assgnExpr['key'] = tokens[i]['contents']
        pass
    return assgnExpr

# for token in tokens:
#     print(token)
# print("\n" + str(parse(tokens)))