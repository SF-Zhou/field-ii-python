from . import *
import typing


class StringValueModel(ValueModel):
    @property
    def value(self) -> str:
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)


class StringProperty(AbstractProperty, StringValueModel):
    pass


class StringItemInterface(AbstractItem):
    @property
    def string(self) -> StringProperty:
        return self.create(StringProperty, args=(self, ))


class StringItem(StringItemInterface):
    pass


class IntValueModel(ValueModel):
    @property
    def value(self) -> int:
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)


class IntProperty(AbstractProperty, IntValueModel):
    pass


class IntItemInterface(AbstractItem):
    @property
    def int(self) -> IntProperty:
        return self.create(IntProperty, args=(self, ))


class IntItem(IntItemInterface):
    pass


class FloatValueModel(ValueModel):
    @property
    def value(self) -> float:
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)


class FloatProperty(AbstractProperty, FloatValueModel):
    pass


class FloatItemInterface(AbstractItem):
    @property
    def float(self) -> FloatProperty:
        return self.create(FloatProperty, args=(self, ))


class FloatItem(FloatItemInterface):
    pass


class DictValueModel(ValueModel):
    @property
    def value(self) -> dict:
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)


class DictProperty(AbstractProperty, DictValueModel):
    pass


class DictItemInterface(AbstractItem):
    @property
    def dict(self) -> DictProperty:
        return self.create(DictProperty, args=(self, ))


class DictItem(DictItemInterface):
    pass


class ListValueModel(ValueModel):
    @property
    def value(self) -> list:
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)


class ListProperty(AbstractProperty, ListValueModel):
    pass


class ListItemInterface(AbstractItem):
    @property
    def list(self) -> ListProperty:
        return self.create(ListProperty, args=(self, ))


class ListItem(ListItemInterface):
    pass


class StringListValueModel(ValueModel):
    @property
    def value(self) -> typing.List[str]:
        return self.get_value()

    @value.setter
    def value(self, value):
        self.set_value(value)

    @property
    def count(self):
        return len(self.value)


class StringListProperty(AbstractProperty, StringListValueModel):
    pass


class StringListItemInterface(AbstractItem):
    @property
    def string_list(self) -> StringListProperty:
        return self.create(StringListProperty, args=(self, ))


class StringListItem(StringListItemInterface):
    pass


class StringIntProperty(IntProperty):
    def get_value(self):
        return int(self.parent.get_value())

    def set_value(self, value):
        self.parent.set_value(str(value))


class StringIntItemInterface(StringItemInterface):
    @property
    def int(self) -> StringIntProperty:
        return self.create(StringIntProperty, args=(self, ))


class StringFloatProperty(FloatProperty):
    def get_value(self):
        return float(self.parent.get_value())

    def set_value(self, value):
        self.parent.set_value(str(value))


class StringFloatItemInterface(StringItemInterface):
    @property
    def float(self) -> StringFloatProperty:
        return self.create(StringFloatProperty, args=(self, ))
