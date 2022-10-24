tokens = [{'type': 'keyword', 'contents': 'int'}, {'type': 'ID', 'contents': 'i'}, {'type': 'op', 'contents': '='},
         {'type': 'val', 'contents': '5'}, {'type': 'op', 'contents': '*'}, {'type': 'lparen', 'contents': '('},
         {'type': 'val', 'contents': '5'}, {'type': 'op', 'contents': '+'}, {'type': 'val', 'contents': '5'},
         {'type': 'rparen', 'contents': ')'}]

# Decl: assgnDecl
# assgnDecl: key id = expr | id = expr
# expr = num | expr op expr | (expr)

keywords = ["int"]

def parse(tokens):
    parseTree = []
    parseTree.append("Decl")
    for token in tokens:
        if token['type'] == 'keyword':
            parseTree.append("assignDecl")
            parseTree.append(parseAssgn(tokens, tokens.index(token)))
    return parseTree

def parseAssgn(tokens, index):
    assgnExpr = {}
    for i in range(index, len(tokens)):
        if tokens[i]['type'] == 'keyword':
            assgnExpr['key'] = tokens[i]['contents']
        pass
    return assgnExpr

for token in tokens:
    print(token)
print("\n" + str(parse(tokens)))