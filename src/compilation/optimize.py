from .optimizations.dead_code_removal import perform_dead_code_removal

'''
optimize.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 08 DEC 22

Perform optimization passes upon the IR
'''

def optimize(ir, symbolTable):
    ir = perform_dead_code_removal(ir, symbolTable)
    return ir

def print_optimizedIR(ir):
    print("Optimized IR:")
    for code in ir:
        print(code)
    print()