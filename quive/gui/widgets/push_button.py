import prive
from .. import *


@ui_extension
class PushButton(QPushButton, ExcitedSignalInterface, prive.WidgetStringInterface):
    def set_excited_signal_connection(self):
        # noinspection PyUnresolvedReferences
        self.clicked.connect(self.excited.emit)

    class StringItem(prive.WidgetStringItem):
        def __init__(self, parent: 'PushButton'):
            self.parent = parent

        def get_value(self):
            return self.parent.text()

        def set_value(self, value):
            self.parent.setText(value or '')
            self.check_change()
