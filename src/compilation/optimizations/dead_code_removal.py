'''
dead_code_removal.py

@Author - Shanti Upadhyay - spu0004@auburn.edu

@Version - 01 DEC 22

Remove unused code within function from IR
'''
programVariables = []
utilizedVariables = []
dependencies = {}

def perform_dead_code_removal(ir, symbolTable):
    global programVariables
    global utilizedVariables
    global dependencies
    ir = ir.splitlines()
    programVariables = get_program_variables(symbolTable, programVariables)
    utilizedVariables, dependencies = get_utilized_variables(ir, programVariables, utilizedVariables, dependencies)
    ir = remove_lines(ir, utilizedVariables, dependencies)
    return ir

def get_program_variables(symbolTable, programVariables):
    for function in symbolTable:
        for item in symbolTable[function]:
            if item != "returnType":
                programVariables.append(item)
    return programVariables            

def get_utilized_variables(ir, programVariables, utilizedVariables, dependencies):
    for i in range(len(ir) - 1, -1, -1):
        if "return" in ir[i]:
            expression = ir[i].split(" ", 1)[1]
            for variable in programVariables:
                if variable in expression:
                    utilizedVariables.append(variable)
                    dependencies[variable] = 1
        else:
            (identifier, expression) = ir[i].split(" = ")
            if identifier in utilizedVariables:
                for variable in programVariables:
                    if variable in expression:
                        utilizedVariables.append(variable)
                        if variable in dependencies:
                            dependencies[variable] += 1
                        else:
                            dependencies[variable] = 1
    return utilizedVariables, dependencies

def remove_lines(ir, utilizedVariables, dependencies):
    for i in range(len(ir) - 1, -1, -1):
        line = ir[i]
        if not any(variable in line for variable in utilizedVariables):
            ir.remove(line)
        
        for variable in utilizedVariables:
            if variable in line: 
                if 'return' not in line:
                    identifier = line.split(" = ")[0]
                    if variable == identifier and dependencies[identifier] == 0:
                        ir.remove(line)
                    elif variable == identifier and dependencies[identifier] > 0:
                        dependencies[identifier] -= 1     
    return ir
    