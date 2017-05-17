from .. import *


class PointF(QPointF):
    def __add__(self, other):
        if isinstance(other, QSizeF):
            return PointF(self.x() + other.width(), self.y() + other.height())
        else:
            return PointF(self.x() + other.x(), self.y() + other.y())

    def __sub__(self, other):
        if isinstance(other, QSizeF):
            return PointF(self.x() - other.width(), self.y() - other.height())
        else:
            return PointF(self.x() - other.x(), self.y() - other.y())

    def __mul__(self, other):
        return PointF(self.x() * other, self.y() * other)

    def x_add(self, v):
        return PointF(self.x() + v, self.y())

    def x_sub(self, v):
        return PointF(self.x() - v, self.y())

    def y_add(self, v):
        return PointF(self.x(), self.y() + v)

    def y_sub(self, v):
        return PointF(self.x(), self.y() - v)
