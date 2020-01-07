import codecs
import eel

###############
# Global vars #
###############
dom = None

########################
# Functions Expose eel #
########################
@eel.expose
def parser_coding(code=None, show_lexer=False):
    print(code)
    if code is None or code == '':
        return 'Not Code :('
    # Load Data
    analyzer = result_parser = None
    from core.lexer import analyzer
    from core.sintatic import parser, get_error
    # Lexer
    analyzer.input(code)
    result = ''
    while True:
        token = analyzer.token()
        if not token:
            break
        print(token)
        if show_lexer:
            result += '{0} \n'.format(token)
    # Parser
    result_parser = parser.parse(code, tracking=True)
    errors = get_error()
    # Return result
    if not errors and result_parser is not None:
        result += 'OK'
        global dom  # Use global var
        dom = result_parser
    else:
        # Merge errors with result
        for error in errors:
            result += '{0} on line {1} \n'.format(error[1], error_lineno(code, error[0]))
        if not errors:
            result += 'Multiple root tags'
    # Delete data
    errors.clear()
    return result


@eel.expose
def get_dom():
    if dom is None:
        return []   # No Compile)
    # Serializer DOM to JSON
    return [dom.serialize()]


#####################
# Functions Statics #
#####################
def test():
    error = '/home/mackey/PycharmProjects/simpleXML/test.xml'
    fp = codecs.open(error, 'r', 'utf-8')
    text = fp.read()
    fp.close()
    return text


def error_lineno(text, col):
    return len(text[:col].split('\n'))
