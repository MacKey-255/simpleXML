import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from core.lexer import analyzer
from core.sintatic import parser


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainApp(App):
    title = 'Parser Simple XML'
    icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
    kv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.kv')
    errors = []

    @staticmethod
    def get_example():
        """
        import codecs
        error = '/home/mackey/PycharmProjects/simpleXML/test/error.xml'
        ok = '/home/mackey/PycharmProjects/simpleXML/test/ok.xml'
        fp = codecs.open(error, 'r', 'utf-8')
        text = fp.read()
        fp.close()
        """
        return '''<x main="True">
    </b>asdasd
    <xml data="single">
        </b>
        <p>
        <k></k>
        <aps />
        <a>Hola
    </xml>
</x>'''

    def token(self, show=False):
        # My Analyzer Lexical
        analyzer.input(self.root.ids.text_input.text)

        while True:
            token = analyzer.token()
            if not token:
                break
            if show:
                self.errors.append(token)

    def error_lineno(self, col):
        return len(self.root.ids.text_input.text[:col].split('\n'))

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Cargar Simple XML", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.root.ids.text_input.text = stream.read()
        self.dismiss_popup()

    def compile(self):
        from core.sintatic import alternative_error
        self.token()
        result = parser.parse(self.root.ids.text_input.text, tracking=True)
        errors = alternative_error()
        if result is not None and not errors:
            self.root.ids.error_output.text = '[color=00ff00]OK[/color]'
        else:
            text = ''
            for error in errors:
                text += '[color=ff0000] {0} on line {1} [/color]\n\n'.format(error[1], self.error_lineno(error[0]))
            errors.clear()
            self.root.ids.error_output.text = text

    def on_start(self):
        # Get Data & Assign in text_input
        text = self.get_example()
        self.root.ids.text_input.text = text
