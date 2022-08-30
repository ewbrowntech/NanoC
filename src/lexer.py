'''
lexer.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 AUG 22

Reads file and outputs tokens as a list of dictionaries
'''

# Scans through string of file contents to build a list of tokens.
# Arguments:
# - fileContents (string) - full contents of the source code file
# Returns:
# - tokens (list of dictionaries) - tokens from source code
# Idea of calling separate functions from replit.com/talk/Make-a-Full-Lexer-in-Python/111397
def lexer(fileContents):
    operators = ['+', '-', '*', '=', '>', '>=']
    tokens = []
    i = 0
    while (i < len(fileContents)):
        lexeme = fileContents[i]
        if lexeme.isalpha():
            token = {}
            token['type'], token['content'], pos = id(fileContents[i:])
            token['position'] = i
            tokens.append(token)
            i += pos
        elif lexeme.isdigit():
            token = {}
            token['type'], token['content'], pos = val(fileContents[i:])
            token['position'] = i
            tokens.append(token)
            i += pos
        elif lexeme in operators:
            token = {}
            token['type'], token['content'], pos = op(fileContents[i:], operators)
            token['position'] = i
            tokens.append(token)
            i += pos
        else:
            i += 1
    print(tokens)
    return tokens

def id(fileContents):
    id = ''
    idKeys = ['int', 'string', 'char']
    for char in fileContents:
        if not char.isalpha() and not char.isdigit() and char != "_":
            break
        id += char
    if id in idKeys:
        print("Keyword match!")
        return 'keyword', id, len(id)
    return 'id', id, len(id)

def val(fileContents):
    val = ''
    for char in fileContents:
        if not char.isdigit():
            break
        val += char
        return 'val', val, len(val)

def op(fileContents, operators):
    op = ''
    for char in fileContents:
        if char not in operators:
            break
        if (op + char) not in operators:
            break
        op += char
    return 'operator', op, len(op)




