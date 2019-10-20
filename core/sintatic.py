import codecs

import ply.yacc
from core.lexer import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('right', 'STARTTAG'),
    ('right', 'ID', 'EQUAL', 'VALUE'),
    ('left', 'GT', 'GTS'),
    ('left', 'ENDTAG'),
)

# dictionary of names (for storing variables)
names = {}


def p_xml(p):
    '''xml : STARTTAG declare GT words more ENDTAG
            | STARTTAG declare GTS'''
    print('XML')


def p_declare(p):
    '''declare : ID EQUAL VALUE declare
               | empty'''
    print('CONTENT')


def p_more(p):
    '''more : xml more
            | empty'''
    print('MORE XML')


def p_words(p):
    '''words : ID words
             | empty'''
    print('WORDS')


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    print("[Syntax error] '%s'" % p.value)


# Test
test = '/home/mackey/PycharmProjects/simpleXML/test/test1.xml'
fp = codecs.open(test, 'r', 'utf-8')
read = fp.read()
fp.close()

sintax = ply.yacc.yacc()
result = sintax.parse(read)
print(result)
