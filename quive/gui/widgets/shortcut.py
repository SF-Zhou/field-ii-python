from .. import *


@ui_extension
class Shortcut(QShortcut, ExcitedSignalInterface):
    def __init__(self, key, parent):
        if isinstance(key, str):
            key = QKeySequence(key)
        if not isinstance(parent, QWidget):
            parent = parent.w
        super().__init__(key, parent)

    def set_excited_signal_connection(self):
        # noinspection PyUnresolvedReferences
        self.activated.connect(self.excited.emit)
