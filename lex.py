'''
Lex
'''

import ply.lex as lex

reserved_words = (
	'while',
	'print',
	'num',
	'str',
	'bool',
	'True',
	'False'
)

tokens = (
	'NUMBER',
	'STRING',
	'BOOLEAN',
	'ADD_OP',
	'MUL_OP',
	'IDENTIFIER',
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();={}'

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_MUL_OP(t):
	r'[*/]'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_STRING(t):
	r'\"[^\"]+\"'
	t.value = str(t.value)
	t.value = t.value[1:-1]
	return t

def t_BOOLEAN(t):
	r'\bTrue\b|\bFalse\b'
	if(t.value == "False"):
		t.value = False
	else:
		t.value = True
	return t

def t_NUM(t):
	r'\bnum\b'
	t.value = str(t.value)
	return t

def t_STR(t):
	r'\bstr\b'
	t.value = str(t.value)
	return t

def t_BOOL(t):
	r'\bbool\b'
	t.value = str(t.value)
	return t

def t_IDENTIFIER(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

def t_COMMENT(t):
     r'\#.*'
     pass




lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
