from . import QTimer, SignalSender


class Timer(QTimer):
    def __init__(self, *args):
        super().__init__(*args)

        self.triggered = SignalSender()
        self.timeout.connect(self.triggered.emit)
        self.timeout = self.triggered
