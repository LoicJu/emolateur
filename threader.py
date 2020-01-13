import AST
from AST import addToClass

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

@addToClass(AST.WhileNode)
def thread(self, lastNode):
    beforeCond = lastNode
    exitCond = self.children[0].thread(lastNode)
    exitCond.addNext(self)
    exitBody = self.children[1].thread(self)
    exitBody.addNext(beforeCond.next[-1])
    return self

# Define the AST ForNode
@addToClass(AST.ForNode)
def thread(self, lastNode):
    beforeCond = self.children[0] # the before cond will be the first children, so the delaration or the assignation.
    assignOrDeclare = self.children[0].thread(lastNode) # define the begining of the for node, that will be the assign (or declare)
    exitCond = self.children[1].thread(self.children[0]) # define the exit condition, that will follow the assign or declare, it's the condition of the for
    exitCond.addNext(self) # add the next of the programme after the condition
    programme = self.children[3].thread(self) # define the programme in the for loop
    # increment après
    increment = self.children[2].thread(self.children[3]) # define the increment
    increment.addNext(beforeCond.next[-1]) #after the increment, go back to the condition
    return self

@addToClass(AST.CondIfNode)
def thread(self, lastNode):
    cond = self.children[0].thread(lastNode)
    cond.addNext(self)
    prog = self.children[1].thread(self)
    prog.addNext(self)
    return self

@addToClass(AST.CondIfElseNode)
def thread(self, lastNode):
    cond = self.children[0].thread(lastNode)
    cond.addNext(self)
    prog_if = self.children[1].thread(self)
    prog_if.addNext(self)
    prog_else = self.children[2].thread(self)
    prog_else.addNext(self)
    return self

def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry

if __name__ == "__main__":
    from parserEmo import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)

    graph = ast.makegraphicaltree()
    entry.threadTree(graph)

    name = os.path.splitext(sys.argv[1])[0]+'-ast-threaded.pdf'
    graph.write_pdf(name)
    print ("wrote threaded ast to", name)
