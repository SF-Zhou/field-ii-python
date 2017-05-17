from .. import *


@ui_extension
class Widget(QWidget, ClosedSignalInterface, ClassExecInterface, ContainerAbilityInterface):
    def __init__(self, parent=None, *args):
        if getattr(parent, 'w', None) is not None:
            parent = parent.w
        super().__init__(parent, *args)

    def closeEvent(self, event: QCloseEvent):
        self.closed.emit()
        event.accept()

    def exec(self):
        with EventLoop() as loop:
            self.closed.connect(loop.quit)
            self.show()

    @property
    def background_color(self):
        return self.attach(lambda: None)

    @background_color.setter
    def background_color(self, value):
        self.assign(value)
        self.update()

    @property
    def size(self) -> (int, int):
        return self.width(), self.height()

    def paintEvent(self, *args, **kwargs):
        painter = Painter(self)

        if self.background_color is not None:
            painter.fillRect(self.rect(), self.background_color)
        self.paint(painter)

    def paint(self, painter: Painter):
        pass
