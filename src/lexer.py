import re

'''
lexer.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 16 OCT 22

Reads file and outputs tokens as a list of dictionaries
'''

testLine = "int i = 5 * (3 + 4);"

formats = []
idFormat = {'type': 'ID', 'pattern': re.compile(r'[a-zA-Z][a-zA-Z0-9]*')}
numFormat = {'type': 'NUM', 'pattern': re.compile(r'[0-9]+')}
opFormat = {'type': 'OP', 'pattern': re.compile(r'[+\-*/=]')}
lparFormat = {'type': 'LPAR', 'pattern': re.compile(r'(\()')}
rparFormat = {'type': 'RPAR', 'pattern': re.compile(r'(\))')}
symFormat = {'type': 'SYMBOL', 'pattern': re.compile(r';')}

formats.append(idFormat)
formats.append(numFormat)
formats.append(opFormat)
formats.append(lparFormat)
formats.append(rparFormat)
formats.append(symFormat)


def lexer(source):
    tokens = []
    i = 0
    while (i < len(source)):
        tokensConsumed = False
        print("i = " + str(i))
        print("Char: " + source[i])
        for format in formats:
            regex = format['pattern']
            print(str(regex))
            if (regex.match(source[i]) != None):
                print(regex.match(source[i]))
                for j in range(i + 1, len(source) + 1):
                    print("j = " + str(j))
                    matchBuffer = regex.match(source[i: j])
                    if (matchBuffer.group() != source[i: j] or j == len(source)):
                        match = regex.match(source[i: j])
                        tokens.append(generate_token(match, format['type']))
                        tokensConsumed = True
                        i = i + len(match.group())
                        break
                break
        if not tokensConsumed:
            print("No token generated")
            i+=1
    return tokens

def generate_token(match, type):
    print("Generating token...")
    token = {}
    token['type'] = type
    token['span'] = match.span()
    token['contents'] = match.group()
    print("Token: " + str(token))
    return token

def print_tokens(tokens):
    print("Tokens:")
    for token in tokens:
        print('[' + str(tokens.index(token)) + '] ' + str(token))

print_tokens(lexer(testLine))