import ply.lex as lex

# List Tokens
tokens = (
    'WORDS',
    'ID',
    'VALUE',
    'EQUAL',
    'GTS',
    'GT',
    'LTS',
    'LT',
)

states = (
    ('TAG', 'exclusive'),
)

# Ignored characters
t_ignore = ' \t\n'

# Tokens
t_WORDS = r'[a-zA-Z0-9_]+'
t_TAG_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_TAG_EQUAL = r'='
t_TAG_ignore = " \t\n"


def t_LTS(t):
    r'</'
    t.lexer.push_state('TAG')
    return t


def t_LT(t):
    r'<'
    t.lexer.push_state('TAG')
    return t


def t_TAG_GT(t):
    r'>'
    t.lexer.pop_state()
    return t


def t_TAG_GTS(t):
    r'/>'
    t.lexer.pop_state()
    return t


def t_TAG_error(t):
    t.lexer.skip(1)


def t_TAG_VALUE(t):
    r'"[^"]*"|\'[^"]*\''
    t.value = t.value[1:-1]  # dropping off the double quotes
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("[ILLEGAL_CHARACTER] '%s'" % t.value[0])
    t.lexer.skip(1)


analyzer = lex.lex()
