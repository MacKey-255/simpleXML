#!/usr/bin/env python
import codecs
import sys
from collections import UserString

from pip._vendor.pyparsing import unicode
from ply import lex, yacc

_VERSION = '1.0'


class XmlLexer:
    '''The XML lexer'''

    # states:
    #   default:    The default context, non-tag
    #   tag:        The document tag context
    #   attrvalue1: Single-quoted tag attribute value
    #   attrvalue2: Double-quoted tag attribute value

    states = (
        ('tag', 'exclusive'),
        ('attrvalue1', 'exclusive'),
        ('attrvalue2', 'exclusive'),
    )

    tokens = [

        # state: INITIAL
        'PCDATA',
        'OPENTAGOPEN',
        'CLOSETAGOPEN',

        # state: tag
        'TAGATTRNAME',
        'TAGCLOSE',
        'LONETAGCLOSE',
        'ATTRASSIGN',

        # state: attrvalue1
        'ATTRVALUE1OPEN',
        'ATTRVALUE1STRING',
        'ATTRVALUE1CLOSE',

        # state: attrvalue2
        'ATTRVALUE2OPEN',
        'ATTRVALUE2STRING',
        'ATTRVALUE2CLOSE',

    ]

    # Complex patterns
    re_digit = r'([0-9])'
    re_nondigit = r'([_A-Za-z])'
    re_identifier = r'(' + re_nondigit + r'(' + re_digit + r'|' + re_nondigit + r')*)'

    # ANY

    def t_ANY_error(self, t):
        t.lexer.skip(1)
        raise SyntaxError("Illegal character '%s'" % t.value[0])

    # INITIAL

    t_ignore = ''

    def t_CLOSETAGOPEN(self, t):
        r'</'
        t.lexer.push_state('tag')
        return t

    def t_OPENTAGOPEN(self, t):
        r'<'
        t.lexer.push_state('tag')
        return t

    def t_PCDATA(self, t):
        '[^<]+'
        return t

    # tag: name

    t_tag_ignore = ' \t'

    def t_tag_TAGATTRNAME(self, t):
        return t

    t_tag_TAGATTRNAME.__doc__ = re_identifier

    def t_tag_TAGCLOSE(self, t):
        r'>'
        t.lexer.pop_state()
        return t

    def t_tag_LONETAGCLOSE(self, t):
        r'/>'
        t.lexer.pop_state()
        return t

    # tag: attr

    t_tag_ATTRASSIGN = r'='

    def t_tag_ATTRVALUE1OPEN(self, t):
        r'\''
        t.lexer.push_state('attrvalue1')
        return t

    def t_tag_ATTRVALUE2OPEN(self, t):
        r'"'
        t.lexer.push_state('attrvalue2')
        return t

    # attrvalue1

    def t_attrvalue1_ATTRVALUE1STRING(self, t):
        r'[^\']+'
        t.value = unicode(t.value)
        return t

    def t_attrvalue1_ATTRVALUE1CLOSE(self, t):
        r'\''
        t.lexer.pop_state()
        return t

    t_attrvalue1_ignore = ''

    # attrvalue2

    def t_attrvalue2_ATTRVALUE2STRING(self, t):
        r'[^"]+'
        t.value = unicode(t.value)
        return t

    def t_attrvalue2_ATTRVALUE2CLOSE(self, t):
        r'"'
        t.lexer.pop_state()
        return t

    t_attrvalue2_ignore = ''

    # misc

    literals = '$%^'

    def t_ANY_newline(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)

        while 1:
            tok = self.lexer.token()
            if not tok: break
            _debug_print_('LEXER', '[%-12s] %s' % (self.lexer.lexstate, tok))


# Customization
class SyntaxError(Exception):
    pass


################################
# PARSER

tag_stack = []


# Grammer

def p_root_element(p):
    '''root : element
            | element PCDATA
    '''
    _parser_trace(p)

    p[0] = p[1]


def p_root_pcdata_element(p):
    '''root : PCDATA element
            | PCDATA element PCDATA
    '''
    _parser_trace(p)

    p[0] = p[2]


def p_element(p):
    '''element : opentag children closetag
               | lonetag
    '''
    _parser_trace(p)

    if len(p) == 4:
        p[1].children = p[2]

    p[0] = p[1]


# tag
def p_opentag(p):
    '''opentag : OPENTAGOPEN TAGATTRNAME attributes TAGCLOSE
    '''
    _parser_trace(p)

    tag_stack.append(p[2])
    p[0] = DOM.Element(p[2], p[3])


def p_closetag(p):
    '''closetag : CLOSETAGOPEN TAGATTRNAME TAGCLOSE
    '''
    _parser_trace(p)

    print(tag_stack)
    n = tag_stack.pop()
    if p[2] != n:
        raise ParserError('Close tag name ("%s") does not match the corresponding open tag ("%s").' % (p[2], n))


def p_lonetag(p):
    '''lonetag : OPENTAGOPEN TAGATTRNAME attributes LONETAGCLOSE
    '''
    _parser_trace(p)

    p[0] = DOM.Element(p[2], p[3])


# attr
def p_attributes(p):
    '''attributes : attribute attributes
                  | empty
    '''
    _parser_trace(p)

    if len(p) == 3:
        if p[2]:
            p[1].update(p[2])
            p[0] = p[1]
        else:
            p[0] = p[1]
    else:
        p[0] = {}


def p_attribute(p):
    '''attribute : TAGATTRNAME ATTRASSIGN attrvalue
    '''
    _parser_trace(p)

    p[0] = {p[1]: p[3]}


def p_attrvalue(p):
    '''attrvalue : ATTRVALUE1OPEN ATTRVALUE1STRING ATTRVALUE1CLOSE
                 | ATTRVALUE2OPEN ATTRVALUE2STRING ATTRVALUE2CLOSE
    '''
    _parser_trace(p)

    p[0] = _xml_unescape(p[2])


# child
def p_children(p):
    '''children : child children
                | empty
    '''
    _parser_trace(p)

    if len(p) > 2:
        if p[2]:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]
    else:
        p[0] = []


def p_child_element(p):
    '''child : element'''
    _parser_trace(p)

    p[0] = p[1]


def p_child_pcdata(p):
    '''child : PCDATA'''
    _parser_trace(p)

    p[0] = DOM.Pcdata(p[1])


# empty
def p_empty(p):
    '''empty :'''
    pass


# Error rule for syntax errors
class ParserError(Exception):
    pass


def p_error(p):
    raise ParserError("Parse error: %s" % (p,))
    pass


# Customization
def _parser_trace(x):
    _debug_print_('PARSER', '[%-16s] %s' % (sys._getframe(1).f_code.co_name, x))


def _yacc_production__str(p):
    # return "YaccProduction(%s, %s)" % (str(p.slice), str(p.stack))
    return "YaccP%s" % (str([i.value for i in p.slice]))


yacc.YaccProduction.__str__ = _yacc_production__str


################################
# DOM

class DOM:
    class Element:
        # Document object model
        #
        # Parser returns the root element of the XML document

        def __init__(self, name, attributes={}, children=[]):
            self.name = name
            self.attributes = attributes
            self.children = children

        def __str__(self):
            attributes_str = ''
            for attr in self.attributes:
                attributes_str += ' %s="%s"' % (attr, _xml_escape(self.attributes[attr]))

            children_str = ''
            for child in self.children:
                if isinstance(child, self.__class__):
                    children_str += str(child)
                else:
                    children_str += child

            return '<%s%s>%s</%s>' % (self.name, attributes_str, children_str, self.name)

        def __repr__(self):
            return str(self)

    class Pcdata(UserString):
        pass


################################
# ESCAPE

_xml_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def _xml_escape(text):
    L = []
    for c in text:
        L.append(_xml_escape_table.get(c, c))
    return "".join(L)


def _xml_unescape(s):
    rules = _xml_escape_table.items()

    for x, y in rules:
        s = s.replace(y, x)

    return s


################################
# INTERFACE

def xml_parse(data):
    _debug_header('INPUT')
    _debug_print_('INPUT', data)
    _debug_footer('INPUT')

    # Tokenizer
    xml_lexer = XmlLexer()
    xml_lexer.build()

    _debug_header('LEXER')
    xml_lexer.test(data)
    _debug_footer('LEXER')

    # Parser
    global tokens
    tokens = XmlLexer.tokens

    yacc.yacc(method="SLR")

    _debug_header('PARSER')
    root = yacc.parse(data, lexer=xml_lexer.lexer, debug=False)
    _debug_footer('PARSER')

    _debug_header('OUTPUT')
    _debug_print_('OUTPUT', root)
    _debug_footer('OUTPUT')

    return root


def tree(node, level=0, init_prefix=''):
    'Returns a tree view of the XML data'

    prefix = '    '
    attr_prefix = '@'
    tag_postfix = ':\t'
    attr_postfix = ':\t'

    s_node = init_prefix + node.name + tag_postfix
    s_attributes = ''
    s_children = ''

    for attr in node.attributes:
        s_attributes += init_prefix + prefix + attr_prefix + attr + attr_postfix + node.attributes[attr] + '\n'

    if len(node.children) == 1 and not isinstance(node.children[0], DOM.Element):
        s_node += node.children[0] + '\n'

    else:
        for child in node.children:
            if isinstance(child, DOM.Element):
                s_children += tree(child, level + 1, init_prefix + prefix)

        s_node += '\n'

    return s_node + s_attributes + s_children


################################
# DEBUG

_DEBUG = {
    'INPUT': False,
    'LEXER': False,
    'PARSER': False,
    'OUTPUT': False,
}


def _debug_header(part):
    if _DEBUG[part]:
        print('--------')
        print('%s:' % part)


def _debug_footer(part):
    if _DEBUG[part]:
        pass


def _debug_print_(part, s):
    if _DEBUG[part]:
        print(s)


################################
# MAIN

def main():
    # Test
    test = '/home/mackey/PycharmProjects/simpleXML/test1.xml'
    fp = codecs.open(test, 'r', 'utf-8')
    read = fp.read()
    fp.close()
    root = xml_parse(read)
    print(tree(root))


if __name__ == '__main__':
    main()
