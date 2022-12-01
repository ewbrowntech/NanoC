import re
'''
ir.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 30 NOV 22

Generates 3-Address Code Intermediate Representation (IR) from AST
'''

ir = ""

def generate_ir(ast):
    for function in ast:
        unpack_function(ast, function)
    return ir

def unpack_function(ast, function):
    global ir
    ops = ['*', '+', '-']
    instructions = ast[function]
    for instruction in instructions:
        instructionOps = []
        for character in instruction:
            if character in ops:
                instructionOps.append(character)
        if "(" in instruction and ")" in instruction:
            ir += acknowledge_parentheses(instruction)
        elif len(instructionOps) > 1: # IR is 3-address, so instructions with more than one op must be split
            ir += split_instruction(instruction)
        else:
            ir += instruction + "\n"

def split_instruction(instruction): # No proper order of operations for now
    primaryOps = ['*']
    secondaryOps = ['+', '-']
    identifier = instruction.split("=")[0].strip()      # Keep the identifier for use in any added lines
    instructionOps = []
    for character in instruction:
        if character in primaryOps or character in secondaryOps:
            instructionOps.append(character)            # Get every op in the instruction
    expression = instruction.split("=")[1].strip()      # Get the expression being split
    expressionH1 = expression.rsplit(instructionOps[1], 1)[0].strip()
    expressionH2 = expression.rsplit(instructionOps[1], 1)[1].strip()
    instructionH1 = identifier + " = " + expressionH1
    instructionH2 = identifier + " = " + identifier + " " + instructionOps[1] + " " + \
                    expressionH2
    modifiedInstruction = instructionH1 + "\n" + instructionH2 + "\n"
    return modifiedInstruction

def acknowledge_parentheses(instruction):
    identifier = instruction.split("=")[0].strip()      # Keep the identifier for use in any added lines
    expression = instruction.split("=")[1].strip()
    containedExpression = re.search('\((.*)\)', expression).group(1)

    # For situations like val = (1 + 1)
    if expression[0] == "(" and expression[-1] == ")" and \
            not any(character in ["(", ")"] for character in containedExpression): # For (1 + 1) but not (1) + (1)
        return identifier + " = " + containedExpression + "\n"      # val = (1 + 1) becomes val = 1 + 1

    ops = ['*', '+', '-']
    instructionOps = []
    if expression[0] != "(":
        for character in instruction.split("(")[0]:
            if character in ops: instructionOps.append(character)
        instructionH1 = identifier + " = " + containedExpression
        instructionH2 = identifier + " = " + expression.split(instructionOps[-1])[0].strip() \
                        + " " + instructionOps[-1] + " " + identifier
    else:
        for character in instruction.split(")")[1]:
            if character in ops: instructionOps.append(character)
        instructionH1 = identifier + " = " + containedExpression
        instructionH2 = identifier + " = " + identifier + " " + instructionOps[-1] + " " \
                        + instruction.split(")")[1].split(instructionOps[-1])[1].strip()
    return instructionH1 + "\n" + instructionH2 + "\n"

class irException(Exception):
    pass

def print_ir(ir):
    print("Intermediate Representation:")
    print(str(ir))