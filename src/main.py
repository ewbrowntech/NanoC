import sys
from file_management import load_file
from lexer import lexer, print_tokens
from parser import parse, print_parseTree
from ast import astGen, print_ast
'''
main.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 25 OCT 22

Runs compiler
'''

def main(args):
    fileContents = load_file(args[1])
    tokens = lexer(fileContents)
    # Tokens
    print_tokens(tokens)

    parseTree = parse(tokens)
    # Parse Tree
    print_parseTree(parseTree)

    ast = astGen(parseTree)
    print_ast(ast)

if __name__ == '__main__':
    main(sys.argv)