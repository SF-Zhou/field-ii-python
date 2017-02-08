from . import MatlabEngine


class MatlabWorker:
    def __init__(self, e: MatlabEngine, task: list):
        self.e = e
        self.task = task
        self.value = None

    def run(self, *args):
        pass

    def start(self):
        self.value = self.run()
