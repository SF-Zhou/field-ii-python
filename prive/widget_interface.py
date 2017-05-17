from . import *


class WidgetStringItem(StringItem, StringIntItemInterface, StringFloatItemInterface):
    pass


class WidgetStringInterface(AttachAbility):
    class StringItem(WidgetStringItem):
        pass

    @property
    def string_item(self) -> StringItem:
        return self.create(type(self).StringItem, args=(self, ))

    @property
    def string(self) -> StringProperty:
        return self.string_item.string

    @property
    def int(self) -> StringIntProperty:
        return self.string_item.int

    @property
    def float(self) -> StringFloatProperty:
        return self.string_item.float


class IndexItem(IntItem):
    pass


class WidgetIndexInterface(AttachAbility):
    class IndexItem(IndexItem):
        pass

    @property
    def index_item(self) -> IndexItem:
        return self.create(type(self).IndexItem, args=(self, ))

    @property
    def index(self) -> IntProperty:
        return self.index_item.int


class StringsItem(StringListItem):
    pass


class WidgetStringListInterface(AttachAbility):
    class StringsItem(StringsItem):
        pass

    @property
    def strings_item(self) -> StringsItem:
        return self.create(type(self).StringsItem, args=(self, ))

    @property
    def string_list(self) -> StringListProperty:
        return self.strings_item.string_list
