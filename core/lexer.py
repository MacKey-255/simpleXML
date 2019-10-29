import ply.lex as lex

# List Tokens
tokens = (
    'TAG',
    'START',
    'END',
    'ID',
    'WORDS',
    'VALUE',
    'EQUAL',
    'GTS',
    'GT',
)

states = (
    ('TAG', 'exclusive'),
)

# Ignored characters
t_ignore = ' \t\n'

# Tokens
t_WORDS = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_TAG_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_TAG_EQUAL = r'='
t_TAG_GTS = r'/>'
t_TAG_GT = r'>'
t_TAG_ignore = " \t\n"


def t_TAG(t):
    r'<[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    t.type = 'START'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin('TAG')
    return t


def t_TAG_START(t):
    r'<[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    t.lexer.level += 1
    return t


def t_TAG_END(t):
    r'</[a-zA-Z_][a-zA-Z0-9_]*>'
    t.value = t.value[2:-1]
    t.lexer.level -= 1
    # Closing Condition
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')
    return t


def t_TAG_error(t):
    t.lexer.skip(1)


def t_TAG_VALUE(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # dropping off the double quotes
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("[ILLEGAL_CHARACTER] '%s'" % t.value[0])
    t.lexer.skip(1)


analyzer = lex.lex()
