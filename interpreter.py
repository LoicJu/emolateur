'''
Interprets and executes the code from the given file.
'''

import AST

operations = {
    '+'  : lambda x,y: x+y,
    '-'  : lambda x,y: x-y,
    '*'  : lambda x,y: x*y,
    '/'  : lambda x,y: x/y,
    '==' : lambda x,y: x==y,
    '!=' : lambda x,y: x!=y,
    '<=' : lambda x,y: x<=y,
    '>=' : lambda x,y: x>=y,
    '<'  : lambda x,y: x<y,
    '>'  : lambda x,y: x>y,
}

stack = []
vars = {}

def valueOfToken(t):
    if isinstance(t, str):
        try:
            return vars[t]
        except KeyError:
            print ("*** Error: variable %s undefined!" % t)
    return t

def execute(node):
    while node:
        if node.__class__ in [AST.EntryNode, AST.ProgramNode]:
            pass
        elif node.__class__ == AST.TokenNode:
            stack.append(node.tok)
        elif node.__class__ == AST.OpNode:
            arg2 = valueOfToken(stack.pop())
            if node.nbargs == 2:
                arg1 = valueOfToken(stack.pop())
            else:
                arg1 = 0
            stack.append(operations[node.op](arg1,arg2))
        elif node.__class__ == AST.AssignNode:
            val = valueOfToken(stack.pop())
            name = stack.pop()
            vars[name] = val
        elif node.__class__ == AST.PrintNode:
            val = stack.pop()
            print (valueOfToken(val))
        elif node.__class__ == AST.WhileNode:
            cond = valueOfToken(stack.pop())
            if cond:
                node = node.next[0]
            else:
                node = node.next[1]
            continue
        elif node.__class__ == AST.CondIfNode:
            # Condition not evaluated yet
            if not node.evaluated:
                # Avoids evaluating the same condition twice
                node.evaluated = True
                cond = valueOfToken(stack.pop())
                # The condition is True
                if cond:
                    node = node.next[0]
                    continue
            # The condition has already been evaluated OR the condition is False
            node = node.next[1]
            continue
        elif node.__class__ == AST.CondIfElseNode:
            # Condition not evaluated yet
            if not node.evaluated:
                # Avoids evaluating the same condition twice
                node.evaluated = True
                cond = valueOfToken(stack.pop())
                # The condition is True
                if cond:
                    node = node.next[0]
                # Else
                else:
                    node = node.next[1]
                continue
            # The condition has already been evaluated
            node = node.next[2]
            continue
        if node.next:
            node = node.next[0]
        else:
            node = None


if __name__ == "__main__":
    from parserEmo import parse
    from threader import thread
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)

    execute(entry)
