import prive
from .. import *


@ui_extension
class Label(QLabel, BaseInterface, prive.WidgetStringInterface):
    class StringItem(prive.WidgetStringItem):
        def __init__(self, parent: 'Label'):
            self.parent = parent

        def get_value(self):
            return self.parent.text()

        def set_value(self, value):
            self.parent.setText(value or '')
