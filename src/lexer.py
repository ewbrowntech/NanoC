import re

'''
lexer.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 30 AUG 22

Reads file and outputs tokens as a list of dictionaries
'''


symbolPattern = re.compile(r'(?:[\\(){}[\]=&|^+<>/*%;.\'"?!~-])')
idPattern = re.compile(r'(?:\w+|\d+)')

# Scans through string of file contents to build a list of tokens.
# Arguments:
# - fileContents (string) - full contents of the source code file
# Returns:
# - tokens (list of dictionaries) - tokens from source code
def lexer(fileContents):
    matches = []
    symbolMatches = symbolPattern.finditer(fileContents)
    matches.append(symbolMatches)
    textMatches = idPattern.finditer(fileContents)
    matches.append(textMatches)
    tokens = []
    for matchList in matches:
        for match in matchList:
            span = match.span()
            token = {}
            token['type'] = 'ID'
            token['pos'] = span[0]
            token['contents'] = match.group()
            tokens.append(token)
    tokens = sorted(tokens, key=lambda d: d['pos'])
    for token in tokens:
        print(token)



