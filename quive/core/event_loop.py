from . import *


class EventLoop:
    def __init__(self, timeout=None, *args):
        self.event = QEventLoop(None, *args)
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

later_times = dict()
later_times_cnt = 0


def later(second=0.01, func=None, *args, **kwargs):
    global later_times_cnt

    assert func
    t = Timer()
    t.setSingleShot(True)
    t.timeout.connect(func, *args, **kwargs)

    later_times_cnt += 1
    later_times[later_times_cnt] = t

    def del_current_timer(cnt):
        del later_times[cnt]
    t.timeout.connect(del_current_timer, later_times_cnt)

    t.start(int(second * 1000))


def run_until(func):
    class Thread(QThread):
        def run(self):
            func()

    with EventLoop() as loop:
        thread = Thread()
        # noinspection PyUnresolvedReferences
        thread.finished.connect(loop.quit)
        thread.start()
