from .. import *
from . import PointF


class SizeF(QSizeF):
    @property
    def w(self):
        return self.width()

    @property
    def h(self):
        return self.height()

    @property
    def size(self):
        return self.width(), self.height()

    def __add__(self, other):
        return super().__add__(other)

    def half_width(self):
        return SizeF(self.width() / 2, self.height())

    def half_height(self):
        return SizeF(self.width(), self.height() / 2)

    def width_add(self, v):
        return SizeF(self.width() + v, self.height())

    def width_sub(self, v):
        return SizeF(self.width() - v, self.height())

    def width_set(self, v):
        return SizeF(v, self.height())

    def height_add(self, v):
        return SizeF(self.width(), self.height() + v)

    def height_sub(self, v):
        return SizeF(self.width(), self.height() - v)

    def height_set(self, v):
        return SizeF(self.width(), v)

    def to_rect(self, p: PointF):
        return QRectF(p, self)

    @staticmethod
    def text_size(text, font: QFont=None):
        font_metrics = QFontMetrics(font)

        lines = text.split('\n')
        width = max(map(font_metrics.width, lines))
        height = font_metrics.height() * len(lines)
        return SizeF(width, height)
