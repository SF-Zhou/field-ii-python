from . import *


class AbstractSetting(AbstractProject):
    pass


class AbstractSettingItem(AbstractProjectItem):
    def __init__(self, parent: AbstractSetting, default_value=None):
        super().__init__(parent)

        if default_value is not None:
            self.self_storage = str(default_value)

    def get_value(self):
        if self.parent is not None:
            ret = self.parent.get_property(self.name)
            if ret is not None:
                return ret
        return self.self_storage


class StringSettingItem(AbstractSettingItem, StringItemInterface):
    pass


class StringListSettingItem(AbstractSettingItem, StringListItemInterface):
    pass


class IntSettingItem(AbstractSettingItem, StringIntItemInterface):
    pass


class FloatSettingItem(AbstractSettingItem, StringFloatItemInterface):
    pass
