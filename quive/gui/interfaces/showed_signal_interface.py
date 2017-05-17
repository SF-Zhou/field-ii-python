from .. import *
from . import BaseInterface


class ShowedSignalInterface(BaseInterface):
    @property
    def showed(self) -> SignalSender:
        if getattr(self, 'showed_', None) is None:
            setattr(self, 'showed_', SignalSender())
        return getattr(self, 'showed_')
