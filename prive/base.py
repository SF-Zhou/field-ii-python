import typing
import traceback
from . import *


class ValueModel:
    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)

    def get_value(self):
        pass

    def set_value(self, value):
        pass

    def get_string(self) -> typing.Optional[str]:
        return self.get_value()


class AttachAbility(ValueModel):
    AttachFlag = '_attach_{}'

    def create(self, creator, args: tuple=(),
               finished_with: typing.Callable[[], object]=None):
        name = self.AttachFlag.format(self.current_name)

        obj = getattr(self, name, None)
        if obj is None:
            obj = creator(*args)
            setattr(self, name, obj)
            if finished_with:
                finished_with()
        return obj

    def assign(self, value):
        name = self.AttachFlag.format(self.current_name)
        setattr(self, name, value)

    @property
    def current_name(self):
        return traceback.extract_stack(None, 3)[0][2]


class ValueInterface(ValueModel):
    pass


class ChangedInterface(AttachAbility):
    @property
    def changed(self) -> SignalSender:
        return self.create(SignalSender, finished_with=self.set_changed_connection)

    # noinspection PyUnresolvedReferences
    def check_change(self, *_):
        if self.value != self.changed.last_value:
            self.changed.emit(self.value)

    def emit_changed(self):
        self.changed.emit(self.value)

    def set_changed_connection(self):
        pass


class AbstractItem(ValueInterface, ChangedInterface):
    pass


class Item(AbstractItem):
    pass


class AbstractProperty(ValueInterface, ChangedInterface):
    def __init__(self, parent: AbstractItem):
        self.parent = parent

    def set_changed_connection(self):
        self.parent.changed.connect(self.check_change)

    def get_value(self):
        return self.parent.get_value()

    def set_value(self, value):
        self.parent.set_value(value)

    def connect(self, other: 'AbstractProperty'):
        self.changed.connect(other.set_value)
        other.changed.connect(self.set_value)
        other.value = self.value
