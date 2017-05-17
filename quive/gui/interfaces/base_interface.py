import prive


class BaseInterface(prive.AttachAbility):
    @property
    def name(self) -> str:
        # noinspection PyUnresolvedReferences
        return self.objectName()

    def set_focus(self):
        # noinspection PyUnresolvedReferences
        return self.setFocus()

    def set_enabled(self, status=True):
        # noinspection PyUnresolvedReferences
        return self.setEnabled(status)

    def set_disabled(self, status=True):
        # noinspection PyUnresolvedReferences
        return self.setEnabled(not status)
