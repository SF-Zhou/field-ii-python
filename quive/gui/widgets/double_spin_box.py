import prive
from .. import *


@ui_extension
class DoubleSpinBox(QDoubleSpinBox, BaseInterface, prive.WidgetStringInterface):
    class StringItem(prive.WidgetStringItem):
        def __init__(self, parent: 'DoubleSpinBox'):
            self.parent = parent

        def get_value(self):
            return str(self.parent.value())

        def set_value(self, value):
            if self.get_value() != value:
                self.parent.setValue(float(value or 0))

        def set_changed_connection(self):
            # noinspection PyUnresolvedReferences
            self.parent.valueChanged[str].connect(self.check_change)
