import sys

""" SVM - Simple Virtual Machine (or Stupid Virtual Machine)
Very simplistic virtual machine aimed to illustrate some compilers' concepts.
It probably has no other use whatsoever.

usage: svm.py <filename> 
This reads and execute the "bytecode" file given in <filename>.
It does so quite slowly and implements almost no error checking :-(

SVM implements a very simplistic stack machine. It has a stack (containing only numbers) 
and a "central memory" that is adressable by names instead of adresses (think "variables"...)

The format of svm's "bytecode" is the following:
    
    each line in is the form
    tag: opcode parameter?
    
    the tag is optional; parameters depend on the opcode.
    
    Valid opcodes are:
        
        PUSHC <val>: pushes the constant value <val> on the execution stack
        PUSHV <id>: pushes the value of the identifier <id> on the execution stack
        SET <id>: pops a value from the stack and sets <id> accordingly
        PRINT: pops a value from the stack and prints it.
        ADD, SUB, MUL, DIV: pops two values from the stack and pushes their 
                    sum, difference, product, quotient respectively.
        USUB: Changes the sign of the number on the top of the stack.
        JMP <tag>: jumps to <tag>
        JIZ, JINZ <tag>: if the top of the stack is (not) zero, jumps to <tag>
        
    Example: this would be a valid "bytecode" file to print the numbers from 0 to 9:
                    PUSHC 0.0
                    SET a
                    JMP cond1
        body1: PUSHV a
                    PRINT
                    PUSHV a
                    PUSHC 1.0
                    ADD
                    SET a
        cond1: PUSHV a
                    PUSHC 10.0
                    SUB
                    JINZ body1        
                    
    NB: whitespace is not significant in bytecode files. The identation above is for readability only.
    
    Have fun!
    
    SVM v0.1 - Matthieu Amiguet/HE-Arc, 2008
"""

def parse(filename):
    code = [line.split(':') for line in open(filename)]
    adresses = {}

    for num, line in enumerate(code):
        if len(line) == 2:
            adresses[line[0]] = num
            del line[0]

    code = [line[0].split() for line in code]
    
    return code, adresses

def execute(code, adresses):
    ip = 0 # instruction pointer
    stack = [] # execution stack
    vars = {} # "central memory"

    # this is for speed optimization
    spop = stack.pop
    sappend = stack.append

    nb_instr = len(code)
    while ip < nb_instr:
        mnemo = code[ip][0]
        
        # Stack and memory manipulation
        if mnemo == "PUSHC":
            sappend(float(code[ip][1]))
        elif mnemo == "PUSHV":
                sappend(vars[code[ip][1]])    
        elif mnemo == "SET":
            val = spop()
            vars[code[ip][1]] = val
            
        # Printing
        elif mnemo == "PRINT":
            print (spop())
            
        # Arithmetics
        elif mnemo == "ADD":
            val2 = spop()
            val1 = spop()
            sappend(val1+val2)
        elif mnemo == "SUB":
            val2 = spop()
            val1 = spop()
            sappend(val1-val2)
        elif mnemo == "MUL":
            val2 = spop()
            val1 = spop()
            sappend(val1*val2)    
        elif mnemo == "DIV":
            val2 = spop()
            val1 = spop()
            sappend(val1/val2)    
        elif mnemo =="USUB":
            stack[-1] = -stack[-1]
            
        # (un)conditional jumps
        elif mnemo == "JMP":
            ip = adresses[code[ip][1]]
            continue
        elif mnemo == "JINZ":
            cond = spop()
            if cond != 0:
                ip = adresses[code[ip][1]]
                continue    
        elif mnemo == "JIZ":
            cond = spop()
            if cond == 0:
                ip = adresses[code[ip][1]]
                continue     
            
        # Fallback
        else:
            print ("Uknown opcode %r. Stopping here." % mnemo)
            break
        

        ip += 1
    
if __name__ == '__main__':
    code, adresses = parse(sys.argv[1])
    execute(code, adresses)