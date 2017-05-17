from PyQt5.QtCore import QObject, pyqtSignal as Signal

__all__ = ('SignalSender', 'connect_with')


class SignalWrapper(QObject):
    signal = Signal(object)


class SignalSender:
    def __init__(self):
        self.signal = SignalWrapper()
        self.last_emit = None
        self.last_error = []

    def emit(self, *args, **kwargs):
        self.last_emit = args, kwargs
        self.last_error.clear()

        self.signal.signal.emit((args, kwargs))

        if self.last_error:
            raise self.last_error[0]

    def connect(self, func, *args, **kwargs):
        def slot_func(data, *_):
            try:

                if len(kwargs):
                    k = data[1].copy()
                    k.updata(kwargs)
                else:
                    k = data[1]

                return func(*(args + data[0]), **k)
            except BaseException as e:
                self.last_error.append(e)
        slot_func.__name__ = getattr(func, '__name__', '<Lambda>')

        self.signal.signal.connect(slot_func)

    @property
    def has_emitted(self):
        return self.last_emit is not None

    @property
    def last_value(self):
        if self.last_emit is None:
            return None
        else:
            args, kwargs = self.last_emit

            if len(kwargs) == 0:
                if len(args) == 0:
                    return None
                elif len(args) == 1:
                    return args[0]
                else:
                    return args
            else:
                return self.last_emit


def connect_with(signal: SignalSender, *args, **kwargs):
    def pack_func(func):
        signal.connect(func, *args, **kwargs)
        return func
    return pack_func
