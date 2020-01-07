from core.utils import _xml_escape


class DOM:
    class Element:
        # Document object model
        #
        # Parser returns the root element of the XML document

        def __init__(self, name, attributes={}, children=[], text=''):
            self.name = name
            self.attributes = attributes
            self.children = children
            self.text = text

        def serialize(self):
            return {
                'name': self.name,
                'attributes': self.attributes,
                'children': [children.serialize() for children in self.children],
                'text': self.text
            }

        def __str__(self):
            attributes_str = ''
            for attr in self.attributes:
                attributes_str += ' %s="%s"' % (attr, _xml_escape(self.attributes[attr]))

            children_str = ''
            for child in self.children:
                children_str += self.text
                if isinstance(child, self.__class__):
                    children_str += str(child)
                else:
                    children_str += child

            if not self.children:
                children_str = self.text
            return '<%s%s>%s</%s>' % (self.name, attributes_str, children_str, self.name)

        def __repr__(self):
            return str(self)
