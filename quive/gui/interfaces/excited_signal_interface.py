from .. import *
from . import BaseInterface


class ExcitedSignalInterface(BaseInterface):
    @property
    def excited(self) -> SignalSender:
        return self.attach(SignalSender, finished_with=self.set_excited_signal_connection)

    def set_excited_signal_connection(self):
        pass
