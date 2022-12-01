import re
'''
lexer.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 17 NOV 22

Reads file and outputs tokens as a list of tokens
'''


formats = []
idFormat = {'type': 'ID', 'pattern': re.compile(r'[a-zA-Z][a-zA-Z0-9]*')}
numFormat = {'type': 'NUM', 'pattern': re.compile(r'[0-9]+')}
opFormat = {'type': 'OP', 'pattern': re.compile(r'[+\-*/=]')}
lparFormat = {'type': 'LPAR', 'pattern': re.compile(r'(\()')}
rparFormat = {'type': 'RPAR', 'pattern': re.compile(r'(\))')}
lbraceFormat = {'type': 'LBRACE', 'pattern': re.compile(r'({)')}
rbraceFormat = {'type': 'RBRACE', 'pattern': re.compile(r'(})')}
symFormat = {'type': 'SYMBOL', 'pattern': re.compile(r';')}

formats.append(idFormat)
formats.append(numFormat)
formats.append(opFormat)
formats.append(lparFormat)
formats.append(rparFormat)
formats.append(lbraceFormat)
formats.append(rbraceFormat)
formats.append(symFormat)

types = ['int']
keywords = ['return']
def lexer(source):
    tokens = []
    i = 0
    while (i < len(source)):
        tokensConsumed = False
        for format in formats:
            regex = format['pattern']
            if (regex.match(source[i]) != None):
                for j in range(i + 1, len(source) + 1):
                    matchBuffer = regex.match(source[i: j])
                    if (matchBuffer.group() != source[i: j] or j == len(source)):
                        match = regex.match(source[i: j])
                        tokens.append(generate_token(match, format['type']))
                        tokensConsumed = True
                        i = i + len(match.group())
                        break
                break
        if not tokensConsumed:
            i+=1

    for token in tokens:
        if token['type'] == 'ID' and token['contents'] in keywords:
            token['type'] = 'KEYWORD'
        elif token['type'] == 'ID' and token['contents'] in types:
            token['type'] = 'TYPE'
    return tokens


def generate_token(match, type):
    token = {}
    token['type'] = type
    token['span'] = match.span()
    token['contents'] = match.group()
    return token

def print_tokens(tokens):
    print("Tokens:")
    for i in range(len(tokens)):
        print('[' + str(i) + '] ' + str(tokens[i]))
    print()