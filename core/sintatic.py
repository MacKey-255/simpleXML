from ply import yacc
from core.lexer import tokens

# Precedence rules for the arithmetic operators
precedence = ()

# dictionary of names (for storing variables)
names = {}

# Stack of the Tags
start_tag_stack = []
end_tag_stack = []

# Stack Error
errors = []


def log_get(p):
    if p[1] is not None:
        result = ()
        for o in p:
            result += (o,)
        return result
    else:
        return None


def p_xml(p):
    #  p[0    p[1]    p[2]   p[3]     p[4]
    '''xml : opentag words children closetag
           | opentag children words closetag
           | alonetag words'''
    if len(p) == 5:
        p[0] = {p[4]: p[1]}
        if p[3] is not None:
            p[0].update(p[3])
        names[p[4]] = p[1]
        if p[2] is not None:
            if names[p[4]] is not None:
                names[p[4]].update({'@text': p[2]})
            else:
                names[p[4]] = {'@text': p[2]}


def p_opentag(p):
    '''opentag : START attributes GT'''
    # Tag Start
    start_tag_stack.append({p[1]: p.lexpos(1)})
    p[0] = p[2]


def p_closetag(p):
    '''closetag : END'''
    n = start_tag_stack.pop()
    p[0] = p[1]
    if not p[1] in n:
        # Add actual closetag
        start_tag_stack.append(n)
        # Search start_tag for close_tag
        correct = False
        for i in reversed(range(0, len(start_tag_stack))):
            if p[1] in start_tag_stack[i]:
                correct = True
                # Remove Tag Start
                start_tag_stack.remove(start_tag_stack[i])
                break
        if not correct:
            # Add Tag Close
            end_tag_stack.append({p[1]: p.lexpos(1)})


def p_alonetag(p):
    '''alonetag : START attributes GTS'''
    p[0] = {p[1]: p[2]}
    names[p[1]] = p[2]


def p_attributes(p):
    '''attributes : ID EQUAL VALUE attributes
               | empty'''
    if len(p) == 5:
        p[0] = {p[1]: p[3]}
        if p[4] is not None:
            p[0].append(p[4])


def p_children(p):
    '''children : xml children
            | empty'''
    p[0] = p[1]


def p_words(p):
    '''words : ID words
             | empty'''
    p[0] = p[1]


def p_empty(p):
    '''empty :'''
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
            errors.append([p.lexpos, "Wrong closing <{0}>".format(p.value)])
        else:
            errors.append([p.lexpos, "Syntax Error at {0} with token: '{1}'".format(p.value, p.type)])


def alternative_error(error=None):
    if error is None:
        error = errors
    # Extract Error
    print(start_tag_stack, end_tag_stack)
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
