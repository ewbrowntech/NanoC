import sys
from file_management import load_file
from lexer import lexer
'''
main.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 AUG 22

Runs compiler
'''

def main(args):
    fileContents = load_file(args[1])
    tokens = lexer(fileContents)

if __name__ == '__main__':
    main(sys.argv)