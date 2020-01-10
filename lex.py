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
	'False',
	'for',
	'in',
	'if',
	'else',
)

tokens = (
	'NUMBER',
	'STRING',
	'BOOLEAN',
	'ADD_OP',
	'MUL_OP',
	'CMP_OP',
	'IDENTIFIER',
	'NEWLINE',
	# EMOJIS
	'EMO_NUM',
	'EMO_STR',
	'EMO_BOOL',
	'EMO_PENCIL',
	'EMO_CREEPY_SMILE',
	'EMO_CREEPY_SMILE_REVERSED',
	'EMO_PLEADING',
	'EMO_EYES',
	'EMO_CHECK',
	'EMO_CROSS',
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

# this define a new line
def t_NEWLINE(t):
	r'\n+'
	# line below not necessary, need to understand what it does and what's its use, maybe useless
	#t.lexer.lineno += len(t.value)
	return t

t_ignore  = ' \t'

# EMOJIS
# Unicode must be 8 chars long !

def t_EMO_NUM(t):
	r'\U0001F522'
	return t

def t_EMO_STR(t):
	r'\U0001F4D6'
	return t

def t_EMO_BOOL(t):
	r'\U00002049'
	return t

def t_EMO_PENCIL(t):
	r'\U0000270F'
	return t

def t_EMO_CREEPY_SMILE(t):
	r'\U0001F642'
	return t

def t_EMO_CREEPY_SMILE_REVERSED(t):
	r'\U0001F643'
	return t

def t_EMO_PLEADING(t):
	r'\U0001F97A'
	return t

def t_EMO_EYES(t):
	r'\U0001F440'
	return t

def t_EMO_CHECK(t):
	r'\U00002705'
	return t

def t_EMO_CROSS(t):
	r'\U0000274C'
	return t

# END OF EMOJIS

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

def t_COMMENT(t):
     r'(\#|\U0001F4AC).*'
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
