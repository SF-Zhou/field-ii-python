from . import *


class EventLoop:
    def __init__(self, timeout=None, *args):
        self.event = QEventLoop()
        self.timeout = timeout

    def quit(self):
        self.event.quit()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.timeout is not None:
            t = Timer()
            t.timeout.connect(self.quit)
            t.start(int(self.timeout * 1000))
        self.event.exec_()


def wait(second=0.01):
    second = max(0.01, second)
    with EventLoop(second):
        pass
