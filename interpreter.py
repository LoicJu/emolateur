'''
Interprets and executes the code from the given file.
'''
from types import *
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
vars = {} # {identifier : [var_type, value]}

def valueOfToken(node):
    if not isinstance(node, AST.OpNode):
        if(isinstance(node.tok, str) and not node.is_string):
            try:
                return vars[node.tok][1]
            except KeyError:
                print ("*** Error: variable %s undefined!" % node.tok)
        return node.tok
    return node
'''def valueOfToken(t):
    if isinstance(t, AST.TokenNode):
        test= str(t)
        #test = test[1:-2]
        return vars[test][1]
    if isinstance(t, str):
        try:
            return vars[node.tok][1]
        except KeyError:
            print ("*** Error: variable %s undefined!" % node.tok)
    return t    '''   


def execute(node):
    while node:
        if node.__class__ in [AST.EntryNode, AST.ProgramNode]:
            pass
        elif node.__class__ == AST.TokenNode:
            stack.append(node)
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
            if isinstance(name, AST.TokenNode):
                name = str(name)
            if(name in vars):
                raise NameError("*** Error: variable %s not declared!" % name)
            else:
                name = name[1:-2]
                vars[name][1] = val
        elif node.__class__ == AST.DeclareNode:
            val = valueOfToken(stack.pop())
            name = stack.pop()

            if((node.var_type == 'str' and not isinstance(val, str)) or
            (node.var_type == 'num' and not isinstance(val, float)) or
            (node.var_type == 'bool' and not isinstance(val, bool))):
                raise TypeError("*** Error : %s is not a %s" %(val, node.var_type))
            name = str(name)
            name = name[1:-2]
            vars[name] = [node.var_type, val]

        elif node.__class__ == AST.PrintNode:
            val = stack.pop()
            print(valueOfToken(val))
        elif node.__class__ == AST.WhileNode:
            cond = valueOfToken(stack.pop())
            if cond:
                node = node.next[0]
            else:
                node = node.next[1]
            continue
        elif node.__class__ == AST.ForNode:
            cond = valueOfToken(stack.pop())
            if cond:
                node = node.next[0]
            else:
                node = node.next[1]
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
