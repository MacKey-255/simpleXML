import codecs
from core.lexer import analyzer
from core.sintatic import parser, names, alternative_error


def main():
    # Test
    test = '/home/mackey/PycharmProjects/simpleXML/test/error.xml'
    fp = codecs.open(test, 'r', 'utf-8')
    read = fp.read()
    fp.close()

    # My Analyzer Lexical
    analyzer.input(read)

    while True:
        token = analyzer.token()
        if not token:
            break
        # print(token)

    result = parser.parse(read, tracking=True)
    alternative_error()
    print(result)
    print('RESULT', 'OK' if result else 'ERROR')
    # print('LINE', len(read[:44].split('\n')))
    # print(names)


if __name__ == '__main__':
    main()
