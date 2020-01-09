'''
Parser
'''

import ply.yacc as yacc

from lex import tokens
import AST
import copy

vars = {}

def p_programme_statement(p):
    ''' programme : statement
        | statement line '''
    p[0] = AST.ProgramNode(p[1])

# enlever ca ?
def p_programme_recursive(p):
    ''' programme : statement line programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_programme_recursive_line(p):
    ''' programme : line programme '''
    p[0] = AST.ProgramNode(p[2])

def p_statement(p):
    ''' statement : assignation
        | structure '''
    p[0] = p[1]

def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])

def p_structure(p):
    ''' structure : WHILE expression '{' programme '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_cond_if(p):
    ''' structure : IF expression '{' programme '}' '''
    p[0] = AST.CondIfNode([p[2],p[4]])

def p_cond_if_else(p):
    ''' structure : IF expression '{' programme '}' ELSE '{' programme '}' '''
    p[0] = AST.CondIfElseNode([p[2],p[4],p[8]])

# identifiant et nombre sont peut-etre provisoires
def p_for(p):
    ''' structure : FOR identifiant IN nombre ',' nombre ',' nombre '{' programme '}' '''
    assign = AST.AssignNode([AST.TokenNode(p[2]),p[4]])
    cond = AST.OpNode('<',[AST.TokenNode(p[2]),p[6]])#ici AST token node
    increment = AST.AssignNode([AST.TokenNode(p[2]),AST.OpNode('+', [AST.TokenNode(p[2]) , p[8]])])# ici ast token node
    programme = p[10]
    p[0] = AST.ForNode([assign,cond,increment,programme])

# PEUT-ETRE PROVISOIRE
def p_nombre(p):
    ''' nombre : NUMBER '''
    p[0] = AST.TokenNode(p[1])

# PEUT-ETRE PROVISOIRE
def p_identifiant(p):
    ''' identifiant : IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_newline(p):
    ''' line : NEWLINE '''
    p[0] = AST.NewLineNode(p[1])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression
            | expression CMP_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

# EMOJIS

def p_emo_pencil(p):
    ''' statement : EMO_PENCIL expression '''
    p[0] = AST.PrintNode(p[2])

# END OF EMOJIS

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1) #to see more
    #result = yacc.parse(prog, debug = 0)
    if result:
        print (result)

        '''
        import os
        os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
        '''
    else:
        print ("Parsing returned no result!")
