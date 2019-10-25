from ply import yacc
from core.lexer import tokens

# Precedence rules for the arithmetic operators
precedence = ()

# dictionary of names (for storing variables)
names = {}


def p_get(p):
    if p[1] is not None:
        result = ()
        for o in p:
            result += (o,)
        return result
    else:
        return None


def p_program(p):
    #  p[0    p[1]    p[2]  p[3] p[4] p[5]  p[6]
    '''program : TAG declare GT words more END
               | TAG declare GTS'''
    p[0] = p_get(p)
    error = False
    if p[3] != '/>':
        if p[1] != p[6]:
            error = True
            print('XML ERROR', p[0])
            print('line', p.lineno(1))
            print('col', p.lexpos(1))
            #p_error(p)
    if p[0] is not None and not error:
        print('XML', p[0])


def p_xml(p):
    '''xml : START declare GT words more END
           | START declare GTS'''
    p[0] = p_get(p)


def p_declare(p):
    '''declare : ID EQUAL VALUE declare
               | empty'''
    p[0] = p_get(p)
    # Save Values
    if len(p) == 5:
        names[p[1]] = p[3]


def p_more(p):
    '''more : xml more
            | empty'''
    p[0] = p_get(p)


def p_words(p):
    '''words : ID words
             | empty'''
    p[0] = p_get(p)
    if p[0] is not None:
        print('WORDS', p[0])


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        print("Syntax error at '%s'" % p.value)
        print("line : '%s'" % p.lineno)
        print("column: '%s'" % p.lexpos)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
