from .. import *
from . import BaseInterface


class ChangedSignalInterface(BaseInterface):
    @property
    def changed(self) -> SignalSender:
        if getattr(self, 'changed_', None) is None:
            setattr(self, 'changed_', SignalSender())
        return getattr(self, 'changed_')
