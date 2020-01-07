import os
from gui.server import *

if __name__ == '__main__':
    # Setup eels root folder
    web_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gui'), 'web')
    eel.init(web_path, allowed_extensions=['.js', '.html'])
    # Start eel
    eel.start('main.html', size=(480, 520))
