import argparse
from file_management import load_file
from lexer import lexer, print_tokens
from parser import parse, print_parseTree
from ast import astGen, print_ast
from symbol_table import generate_symbolTable, print_symbolTable
'''
main.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 17 NOV 22

Runs compiler
'''


def main():
    # Parse command-line flags
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-t', '--tokens', action='store_true')
    argparser.add_argument('-p', '--parseTree', action='store_true')
    argparser.add_argument('-a', '--ast', action='store_true')
    argparser.add_argument('-s', '--symbolTable', action='store_true')
    argparser.add_argument('filename')
    args = argparser.parse_args()
    fileContents = load_file(args.filename)

    # Perform compilation of source file
    tokens = lexer(fileContents)
    parseTree = parse(tokens)
    ast = astGen(parseTree)
    symbolTable = generate_symbolTable(parseTree)

    # Print output of components
    if args.tokens:
        print_tokens(tokens)
    if args.parseTree:
        print_parseTree(parseTree)
    if args.ast:
        print_ast(ast)
    if args.symbolTable:
        print_symbolTable(symbolTable)


if __name__ == '__main__':
    main()
