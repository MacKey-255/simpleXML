from ply import yacc
from core.dom import DOM
from core.lexer import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'WORDS'),
    ('right', 'ID', 'EQUAL', 'VALUE'),
    ('left', 'LT', 'LTS', 'GT', 'GTS'),
)

# Stack of the Tags
start_tag_stack = []
end_tag_stack = []

# Stack Error
errors = []


def p_xml(p):
    #  p[0    p[1]    p[2]   p[3]     p[4]
    """xml : opentag children words closetag
           | opentag words children closetag
           | alonetag words"""
    if len(p) == 5:
        if type(p[2]) == list:
            p[1].children = p[2]
            p[1].text = p[3]
        else:
            p[1].children = p[3]
            p[1].text = p[2]
    else:
        p[1].text = p[2]
    p[0] = p[1]


def p_opentag(p):
    """opentag : LT ID attributes GT"""
    # Tag Start
    start_tag_stack.append({p[2]: p.lexpos(1)})
    p[0] = DOM.Element(p[2], p[3])


def p_closetag(p):
    """closetag : LTS ID GT"""
    n = start_tag_stack.pop()
    p[0] = p[2]
    if not p[2] in n:
        start_tag_stack.append(n)  # Add actual closetag
        # Search start_tag for close_tag
        correct = False
        for i in reversed(range(0, len(start_tag_stack))):
            if p[2] in start_tag_stack[i]:
                correct = True
                # Remove Tag Start
                start_tag_stack.remove(start_tag_stack[i])
                break
        if not correct:
            # Add Tag Close
            end_tag_stack.append({p[2]: p.lexpos(1)})


def p_alonetag(p):
    """alonetag : LT ID attributes GTS"""
    p[0] = DOM.Element(p[2], p[3])


def p_attributes(p):
    """attributes : ID EQUAL VALUE attributes
               | empty"""
    if len(p) == 5:
        p[0] = {p[1]: p[3]}
        if p[4] is not None:
            p[0].update(p[4])
    else:
        p[0] = {}


def p_children(p):
    """children : xml children
            | empty"""
    if len(p) == 3:
        if p[2]:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]
    else:
        p[0] = []


def p_words(p):
    """words : WORDS words
             | empty"""
    if len(p) == 3:
        if p[2]:
            p[1] += ' ' + p[2]
        p[0] = p[1]
    else:
        p[0] = ''


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if p:
        if p.type == 'START':
            for k in start_tag_stack:
                if p.value in [o for o in k]:
                    errors.append([p.lexpos, "Start tag has wrong close tag </{0}>".format(p.value)])
                    break
        elif p.type == 'ID':
            errors.append([p.lexpos, "Unexpected token '{0}'".format(p.value)])
        elif p.type == 'END':
            errors.append([p.lexpos, "Wrong closing </{0}>".format(p.value)])
        elif p.type == 'LT':
            errors.append([p.lexpos, "Multiple root tags"])
        else:
            errors.append([p.lexpos, "Syntax Error at {0} with token: '{1}'".format(p.value, p.type)])


def get_error(error=None):
    if error is None:
        error = errors
    # Extract Error
    if start_tag_stack:
        for tag in start_tag_stack:
            error.append([tag[[o for o in tag][0]], "Syntax error at starting <{0}>".format([o for o in tag][0])])
    if end_tag_stack:
        for tag in end_tag_stack:
            error.append([tag[[o for o in tag][0]], "Syntax error at closing </{0}>".format([o for o in tag][0])])
    # Clear old End and Start Tag Stack
    end_tag_stack.clear()
    start_tag_stack.clear()
    return error


parser = yacc.yacc()
