import ply.lex as lex
import codecs

# List Tokens
tokens = (
    'STARTTAG',  # <TABLE
    'ENDTAG',  # TABLE>
    'ID',  # align
    'VALUE',  # "text"
    'EQUAL',  # =
    # 'LT',  # <
    # 'LTS',  # </
    'GTS',  # />
    'GT',  # >
)

# Ignored characters
t_ignore = ' \t'

# Tokens
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUAL = r'='
# t_LTS = r'</'
# t_LT = r'<'
t_GTS = r'/>'
t_GT = r'>'


def t_STARTTAG(t):
    r'<[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value[1:]
    return t


def t_ENDTAG(t):
    r'</[a-zA-Z_][a-zA-Z0-9_]*>'
    return t


def t_VALUE(t):
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
"""
# Test
test = '/home/mackey/PycharmProjects/simpleXML/test/test1.xml'
fp = codecs.open(test, 'r', 'utf-8')
read = fp.read()
fp.close()

# My Analyzer Lexical
analyzer = lex.lex()
analyzer.input(read)

while True:
    token = analyzer.token()
    if not token:
        break
    print(token)
"""
