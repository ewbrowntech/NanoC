'''
ir.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 NOV 22

Generates 3-Address Code Intermediate Representation (IR) from AST
'''

ir = ""

def generate_ir(ast):
    for function in ast:
        unpack_function(ast, function)
    return ir

def unpack_function(ast, function):
    global ir
    ops = ['+', '-']
    instructions = ast[function]
    for instruction in instructions:
        instructionOps = []
        for character in instruction:
            if character in ops:
                instructionOps.append(character)
        if len(instructionOps) > 1: # IR is 3-address, so instructions with more than one op must be split
            ir += split_instruction(instruction)
        else:
            ir += instruction + "\n"

def split_instruction(instruction):
    ops = ['+', '-']
    identifier = instruction.split("=")[0].strip()
    instructionOps = []
    for character in instruction:
        if character in ops:
            instructionOps.append(character)  # Get every op in the instruction

    expression = instruction.split("=")[1].strip()
    instructionH1 = identifier + " = " + expression.split(instructionOps[1])[0].strip()
    instructionH2 = identifier + " = " + identifier + " " + instructionOps[1] + " " + \
                    expression.split(instructionOps[1])[1].strip()
    modifiedInstruction = instructionH1 + "\n" + instructionH2 + "\n"
    return modifiedInstruction

class irException(Exception):
    pass

def print_ir(ir):
    print("Intermediate Representation:")
    print(str(ir))