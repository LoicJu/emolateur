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

def p_programme_recursive(p):
    ''' programme : statement line programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_programme_recursive_line(p):
    ''' programme : line programme '''
    p[0] = AST.ProgramNode(p[2])

def p_statement(p):
    ''' statement : assignation
        | structure
        | declaration'''
    p[0] = p[1]

def p_statement_print(p):
    ''' statement : PRINT expression
        | EMO_PENCIL expression '''
    p[0] = AST.PrintNode(p[2])

def p_structure(p):
    ''' structure : WHILE expression '{' programme '}'
        | EMO_EYES expression '{' programme '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_cond_if(p):
    ''' structure : IF expression '{' programme '}'
        | EMO_CHECK expression '{' programme '}' '''
    p[0] = AST.CondIfNode([p[2],p[4]])

def p_cond_if_else(p):
    ''' structure : IF expression '{' programme '}' ELSE '{' programme '}'
        | EMO_CHECK expression '{' programme '}' EMO_CROSS '{' programme '}' '''
    p[0] = AST.CondIfElseNode([p[2],p[4],p[8]])

# the for structure, we need to send in the assign, cond or increment an AST.TokenNode because we take always the same (p[2])
# so it needs to be AST.TokenNode to be handle separately
def p_for(p):
    ''' structure : FOR identifiant IN expression ',' expression ',' expression '{' programme '}'
        | EMO_CREEPY_SMILE identifiant IN expression ',' expression ',' expression '{' programme '}' '''
    assign = AST.AssignNode([AST.TokenNode(p[2]),p[4]])
    cond = AST.OpNode('<',[AST.TokenNode(p[2]),p[6]])
    increment = AST.AssignNode([AST.TokenNode(p[2]),AST.OpNode('+', [AST.TokenNode(p[2]) , p[8]])])
    programme = p[10]
    p[0] = AST.ForNode([assign,cond,increment,programme])

# for the for_decl structure, we need to send in the declare, cond or increment an AST.TokenNode because we take always the same (p[3])
# so it needs to be AST.TokenNode to be handle separately
def p_for_decl(p):
    ''' structure : FOR NUM identifiant IN expression ',' expression ',' expression '{' programme '}'
        | EMO_CREEPY_SMILE_REVERSED EMO_NUM identifiant IN expression ',' expression ',' expression '{' programme '}' '''
    declare = AST.DeclareNode(p[2], [AST.TokenNode(p[3]), p[5]])
    cond = AST.OpNode('<',[AST.TokenNode(p[3]),p[7]])
    increment = AST.AssignNode([AST.TokenNode(p[3]),AST.OpNode('+', [AST.TokenNode(p[3]) , p[9]])])
    programme = p[11]
    p[0] = AST.ForNode([declare,cond,increment,programme])

# for with shortcut (start = 0 ; step = 1)
def p_for_pleading(p):
    ''' structure : EMO_PLEADING EMO_NUM identifiant expression '{' programme '}' '''
    declare = AST.DeclareNode(p[2], [AST.TokenNode(p[3]), AST.TokenNode(0)])
    cond = AST.OpNode('<',[AST.TokenNode(p[3]),p[4]])
    increment = AST.AssignNode([AST.TokenNode(p[3]),AST.OpNode('+', [AST.TokenNode(p[3]) , AST.TokenNode(1)])])
    programme = p[6]
    p[0] = AST.ForNode([declare,cond,increment,programme])

# for with shortcut (start = 0 ; step = 10)
def p_for_devil(p):
    ''' structure : EMO_DEVIL EMO_NUM identifiant expression '{' programme '}' '''
    declare = AST.DeclareNode(p[2], [AST.TokenNode(p[3]), AST.TokenNode(0)])
    cond = AST.OpNode('<',[AST.TokenNode(p[3]),p[4]])
    increment = AST.AssignNode([AST.TokenNode(p[3]),AST.OpNode('+', [AST.TokenNode(p[3]) , AST.TokenNode(10)])])
    programme = p[6]
    p[0] = AST.ForNode([declare,cond,increment,programme])

# identifier (variable)
def p_identifiant(p):
    ''' identifiant : IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

# declare the new line
def p_newline(p):
    ''' line : NEWLINE '''
    p[0] = AST.NewLineNode(p[1])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression
            | expression CMP_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var_or_bool(p):
    '''expression : NUMBER
        | IDENTIFIER
        | BOOLEAN '''
    p[0] = AST.TokenNode(p[1])

def p_expression_string(p):
    '''expression : STRING '''
    p[0] = AST.TokenNode(p[1], True)

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_assign(p):
    ''' assignation : identifiant '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_declaration(p):
    ''' declaration : NUM identifiant '=' expression
        | STR identifiant '=' expression
        | BOOL identifiant '=' expression
        | EMO_NUM identifiant '=' expression
        | EMO_STR identifiant '=' expression
        | EMO_BOOL identifiant '=' expression '''
    p[0] = AST.DeclareNode(p[1], [AST.TokenNode(p[2]), p[4]])

# EMOJIS


# END OF EMOJIS

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Syntax error: unexpected end of file!")


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
