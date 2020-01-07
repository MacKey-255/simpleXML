from core.lexer import analyzer
from core.sintatic import parser, get_error
import codecs

# Config
show = False
errors = []

error = '/home/mackey/PycharmProjects/simpleXML/test.xml'
fp = codecs.open(error, 'r', 'utf-8')
text = fp.read()
fp.close()

# My Analyzer Lexical
analyzer.input(text)

while True:
    token = analyzer.token()
    if not token:
        break
    if show:
        print(token)
result = parser.parse(text, tracking=True)
errors = get_error()


def error_lineno(text, col):
    return len(text[:col].split('\n'))


if result is not None and not errors:
    print(result)
    print(result.serialize())
    print('OK')
else:
    for error in errors:
        print('{0} on line {1}'.format(error[1], error_lineno(text, error[0])))
