'''
Lex
'''

import ply.lex as lex

reserved_words = (
	'while',
	'print',
	'for',
	'in',
	'if',
	'else',
)

tokens = (
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'CMP_OP',
	'IDENTIFIER',
	'NEWLINE',
	# EMOJIS
	'EMO_CREEPYSMILE',
	# END OF EMOJIS
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '()={},'

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_MUL_OP(t):
	r'[*/]'
	return t

def t_CMP_OP(t):
	r'={2}|!=|<=|>=|[<>]'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_IDENTIFIER(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

# this define a new line
def t_NEWLINE(t):
	r'\n+'
	# line below not necessary, need to understand what it does and what's its use, maybe useless
	#t.lexer.lineno += len(t.value)
	return t

t_ignore  = ' \t'

# EMOJIS
# Unicode must be 8 chars long !

def t_EMO_CREEPYSMILE(t):
	r'\U0001F642'
	return t

# END OF EMOJIS

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

def t_COMMENT(t):
     r'\#.*'
     pass

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
