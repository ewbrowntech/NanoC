import argparse
from file_management import load_file
from compilation.lexer import lexer, print_tokens
from compilation.parser import parse, print_parseTree
from compilation.ast import astGen, print_ast
from compilation.symbol_table import generate_symbolTable, print_symbolTable
from compilation.ir import generate_ir, print_ir
from compilation.optimize import optimize, print_optimizedIR
from compilation.nasm import generate_asm, print_asm


'''
main.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 01 DEC 22

Runs compiler
'''


def main():
    # Parse command-line flags
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-t', '--tokens', action='store_true')
    argparser.add_argument('-p', '--parseTree', action='store_true')
    argparser.add_argument('-a', '--ast', action='store_true')
    argparser.add_argument('-s', '--symbolTable', action='store_true')
    argparser.add_argument('-i', '--ir', action='store_true')
    argparser.add_argument('-o', '--optimize', action='store_true')
    argparser.add_argument('-asm', '--assemblyCode', action='store_true')

    argparser.add_argument('filename')
    args = argparser.parse_args()
    fileContents = load_file(args.filename)

    # Perform compilation of source file
    tokens = lexer(fileContents)  # Scan in source code as list of tokens
    if args.tokens:
        print_tokens(tokens)
    parseTree = parse(tokens)  # Parse tokens into a grammatical parse tree
    if args.parseTree:
        print_parseTree(parseTree)
    ast = astGen(parseTree)  # Transform parse tree into an abstract syntax tree
    if args.ast:
       print_ast(ast)
    symbolTable = generate_symbolTable(parseTree)  # Traverse parse tree to build a symbol table
    if symbolTable and args.symbolTable:
        print_symbolTable(symbolTable)
    ir = generate_ir(ast)
    if args.ir:
       print_ir(ir)
    if args.optimize:
        ir = optimize(ir, symbolTable)
        print_optimizedIR(ir)
    if args.assemblyCode:
        assembly_code = generate_asm(ir)
        print_asm(assembly_code)
    # query_symbolTable('val2', symbolTable)


if __name__ == '__main__':
    main()
