from .. import *


class WidgetController:
    def __init__(self, parent=None, constructor=None):
        assert constructor is not None

        if isinstance(parent, WidgetController):
            parent = parent.w

        self.w = self.__trick__(constructor, parent)

    def warning(self, text, title='警告'):
        # noinspection PyCallByClass
        QMessageBox.warning(self.w, title, text)

    def information(self, text, title='提示'):
        # noinspection PyCallByClass
        QMessageBox.information(self.w, title, text)

    def message(self, ok=True, ok_msg='成功', bad_msg='失败'):
        if ok:
            self.information(ok_msg)
        else:
            self.warning(bad_msg)

    @staticmethod
    def __trick__(constructor, parent) -> Widget:
        return constructor(parent)

    # actions
    def close(self):
        self.w.close()

    def show(self):
        self.w.show()

    def hide(self):
        self.w.hide()
