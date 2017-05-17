from .. import QPen
from . import scaling


class Pen(QPen):
    def __init__(self, *args):
        if len(args) >= 2:
            assert isinstance(args[1], int) or isinstance(args[1], float)
            super().__init__(args[0], args[1] * scaling.ratio, *args[2:])
        else:
            super().__init__(*args)

    def setWidth(self, width):
        super().setWidth(int(width * scaling.ratio + 0.5))

    def setWidthF(self, width):
        super().setWidthF(width * scaling.ratio)
