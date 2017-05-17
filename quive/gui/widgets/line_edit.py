from .. import *
import prive


@ui_extension
class LineEdit(QLineEdit, BaseInterface, prive.WidgetStringInterface):
    class StringItem(prive.WidgetStringItem):
        def __init__(self, parent: 'LineEdit'):
            self.parent = parent

        def get_value(self):
            return self.parent.text()

        def set_value(self, value):
            value = value or ''
            if value != self.get_value():
                self.parent.setText(value)

        def set_changed_connection(self):
            # noinspection PyUnresolvedReferences
            self.parent.textChanged.connect(self.string.check_change)
