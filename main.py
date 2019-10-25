import codecs
from core.lexer import analyzer
from core.sintatic import parser, names


def main():
    # Test
    test = '/home/mackey/PycharmProjects/simpleXML/test1.xml'
    fp = codecs.open(test, 'r', 'utf-8')
    read = fp.read()
    fp.close()

    # My Analyzer Lexical
    analyzer.input(read)

    while True:
        token = analyzer.token()
        if not token:
            break
        print(token)

    result = parser.parse(read,tracking=True)
    print('RESULT', result)
    print(names)


if __name__ == '__main__':
    main()
