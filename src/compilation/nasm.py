'''This file geenrates the assembly code from optimized IR (3 address code)
    Assembly code targets the x86_64 architecture. A subset the ISA is supported.
    input: Optimized IR
    output: Assembly code

    @Author: Paul Atilola
    @version: December 05, 2022
'''

def generate_asm(ir):
    assembly_code = build_asm(ir)

    return assembly_code




#print assembly code
def print_asm(assembly_code):
    print('\n x86 Assembly Code:')
    for asm_code in assembly_code:
        if type(asm_code) == list:
            for sub_asm in asm_code:
                print(sub_asm)
        else:
            print(asm_code)



#convert C program to asm
def build_asm(ir):
    assembly_code = list()
    assigned_vars = list()

    for code in ir:
        code_elements = list(code.split())
        if code_elements:
            assignedVar = code_elements[0]
            if assignedVar not in assigned_vars and assignedVar != 'return':
                assigned_vars.append(assignedVar)
                if len(code_elements) > 3:
                    asm_code = build_asm_expression(code_elements, assigned_vars)
                    assembly_code.append(asm_code)
                else:
                    asm_code = build_asm_assignment(code_elements, assigned_vars)
                    assembly_code.append(asm_code)

            elif assignedVar == 'return':
                asm_code = build_asm_return(code_elements, assigned_vars)
                assembly_code.append(asm_code)

    return assembly_code



#generates expressions
def build_asm_expression(code_elements, assigned_vars):
    assignedvar = code_elements[0]
    stringCode = list()

    if '+' in code_elements:
        idx = code_elements.index('+')
        op1 = code_elements[idx - 1]
        op2 = code_elements[idx + 1]

        op1string = ''
        op2string = ''
        exprstring = ''
        finExprstring = ''

        if op1 and op2 in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op1)+']'+'                   ;move the value of '+str(op1)+' into the eax register'
            op2string += 'mov'+' '+'ebx'+', '+'['+str(op2)+']'+'                   ;move the value of '+str(op2)+' into the ebx register'
            stringCode.append(op1string)
            stringCode.append(op2string)

            exprstring += 'add'+' '+'eax'+', '+'ebx'+'                     ;Add the value in ebx to the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                     ;move result into memory location pointed by '+str(assignedvar)
            stringCode.append(finExprstring)


        elif op1 in assigned_vars and op2 not in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op1)+']'+'                    ;move the value of '+str(op1)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'add'+' '+'eax'+', '+str(op2)+'                    ;Add '+str(op2)+' to the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


        elif op2 in assigned_vars and op1 not in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op2)+']'+'                     ;move the value of '+str(op2)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'add'+' '+'eax'+', '+str(op1)+'                    ;Add '+str(op1)+' to the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


        else:
            op1string += 'mov'+' '+'eax'+', '+str(op1)+'                    ;move the value  '+str(op1)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'add'+' '+'eax'+', '+str(op2)+'                    ;Add '+str(op2)+' to the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)



    elif '-' in code_elements:
        idx = code_elements.index('-')
        op1 = code_elements[idx - 1]
        op2 = code_elements[idx + 1]

        op1string = ''
        op2string = ''
        exprstring = ''
        finExprstring = ''

        if op1 and op2 in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op1)+']'+'                    ;move the value of '+str(op1)+' into the eax register'
            op2string += 'mov'+' '+'ebx'+', '+'['+str(op2)+']'+'                    ;move the value of '+str(op2)+' into the ebx register'
            stringCode.append(op1string)
            stringCode.append(op2string)

            exprstring += 'sub'+' '+'eax'+', '+'ebx'+'                     ;subtract the value in ebx from the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                     ;move result into memory location pointed by '+str(assignedvar)
            stringCode.append(finExprstring)


        elif op1 in assigned_vars and op2 not in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op1)+']'+'                     ;move the value of '+str(op1)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'sub'+' '+'eax'+', '+str(op2)+'                     ;subtract '+str(op2)+' to the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                     ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


        elif op2 in assigned_vars and op1 not in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+str(op1)+'                     ;move  value '+str(op1)+' into the eax register'
            op2string += 'mov'+' '+'ebx'+', '+'['+str(op2)+']'+'                      ;move the value of '+str(op2)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'sub'+' '+'eax'+', '+'ebx'+'                    ;subtract value in ebx from the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                     ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


        else:
            op1string += 'mov'+' '+'eax'+', '+str(op1)+'                    ;move the value  '+str(op1)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'sub'+' '+'eax'+', '+str(op2)+'                     ;sub '+str(op2)+' from the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                     ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)



    elif '*' in code_elements:
        idx = code_elements.index('*')
        op1 = code_elements[idx - 1]
        op2 = code_elements[idx + 1]

        op1string = ''
        op2string = ''
        exprstring = ''
        finExprstring = ''

        if op1 and op2 in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op1)+']'+'                    ;move the value of '+str(op1)+' into the eax register'
            op2string += 'mov'+' '+'ebx'+', '+'['+str(op2)+']'+'                    ;move the value of '+str(op2)+' into the ebx register'
            stringCode.append(op1string)
            stringCode.append(op2string)

            exprstring += 'mul'+' '+'eax'+', '+'ebx'+'                     ;multiply the value in ebx and the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                     ;move result into memory location pointed by '+str(assignedvar)
            stringCode.append(finExprstring)


        elif op1 in assigned_vars and op2 not in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op1)+']'+'                     ;move the value of '+str(op1)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'mul'+' '+'eax'+', '+str(op2)+'                    ;multiply '+str(op2)+' and the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


        elif op2 in assigned_vars and op1 not in assigned_vars:
            op1string += 'mov'+' '+'eax'+', '+'['+str(op2)+']'+'                    ;move the value of '+str(op2)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'mul'+' '+'eax'+', '+str(op1)+'                    ;multiply '+str(op1)+' and the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


        else:
            op1string += 'mov'+' '+'eax'+', '+str(op1)+'                    ;move the value  '+str(op1)+' into the eax register'
            stringCode.append(op1string)

            exprstring += 'mul'+' '+'eax'+', '+str(op2)+'                    ; multiply '+str(op2)+' and the value in eax'
            stringCode.append(exprstring)

            finExprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move result into memory location pointed by '+str(assignedvar)

            stringCode.append(finExprstring)


    return stringCode

 

#generate assignment asm
def build_asm_assignment(code_elements, assigned_vars):
    assignedvar = code_elements[0]
    operand = code_elements[-1]
    stringCode = list()

    if operand in assigned_vars:
        opstring = ''
        exprstring = ''
        opstring += 'mov'+' '+'eax'+', '+'['+str(operand)+']'+'                     ;load the value of '+str(operand)+' into the eax register'
        stringCode.append(opstring)

        exprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+'eax'+'                    ;move the value in eax into the memory location pointed to by '+str(assignedvar)
        stringCode.append(exprstring)

    else:
        exprstring = ''
        exprstring += 'mov'+' '+'dword'+' '+'['+str(assignedvar)+']'+', '+str(operand)+'                    ;move the value '+str(operand)+' into the memory location pointed to by '+str(assignedvar)
        stringCode.append(exprstring)

    return stringCode


#generate asm for return 
def build_asm_return(code_elements, assigned_vars):
    returnVar = code_elements[-1]
    opstring = ''
    stringCode = list()

    if code_elements[0] == 'return':
        if returnVar in assigned_vars:
            returnstring = ''
            opstring += 'mov'+' '+'eax'+', '+'['+str(returnVar)+']'+'                     ;load the value of '+str(returnVar)+' into the eax register'
            stringCode.append(opstring)

            returnstring += 'ret'+'                    ;return the value in eax'
            stringCode.append(returnstring)

        else:
            returnstring = ''
            opstring += 'mov'+' '+'eax'+', '+str(returnVar)+'                    ;load the value '+str(returnVar)+' into the eax register'
            stringCode.append(opstring)

            returnstring += 'ret'+'                   ;return the value in eax'
            stringCode.append(returnstring)


    return stringCode

























            





    




