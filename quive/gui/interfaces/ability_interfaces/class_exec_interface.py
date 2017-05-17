from .. import BaseInterface


class ClassExecInterface(BaseInterface):
    def exec(self, *args):
        pass

    @classmethod
    def class_exec(cls, *args):
        cls(*args).exec()
