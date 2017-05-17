from .. import *


class SquareLayout(QLayout):
    def __init__(self, parent: QWidget=None,
                 default_item: QWidget=None):
        super().__init__(parent)

        self.item = default_item
        self.last_received_rect = QRect(0, 0, 0, 0)
        self.geometry_rect = QRect(0, 0, 0, 0)

        self.setSpacing(0)

    def addItem(self, item: QLayoutItem):
        if self.item is None:
            self.replace_item(item)

    def addWidget(self, w: QWidget):
        self.addItem(QWidgetItem(w))

    def take(self):
        item, self.item = self.item, None
        return item

    def takeAt(self, index: int):
        return self.take() if index == 0 else None

    def itemAt(self, index: int):
        return self.item if index == 0 else None

    def count(self):
        return 1 if self.item is not None else 0

    def replace_item(self, item):
        old_item, self.item = self.item, item
        self.setGeometry(self.geometry_rect)
        return old_item

    def expandingDirections(self):
        return Qt.Horizontal | Qt.Vertical

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        return self.item.minimumSize() if self.item is not None else QSize()

    def hasHeightForWidth(self):
        return False

    def geometry(self):
        return QRect(self.geometry_rect)

    def setGeometry(self, rect: QRect):
        if self.item is None or self.are_rects_equal(self.last_received_rect, rect):
            return

        self.last_received_rect = rect

        proper_size = self.calculate_proper_size(rect.size())
        proper_location = self.calculate_center_location(rect.size(), proper_size)

        self.geometry_rect = QRect(proper_location, proper_size)
        self.item.setGeometry(self.geometry_rect)
        super().setGeometry(self.geometry_rect)

    def calculate_proper_size(self, from_size: QSize):
        minimum_length = min(from_size.width(), from_size.height())
        return QSize(minimum_length - self.spacing(), minimum_length - self.spacing())

    @staticmethod
    def calculate_center_location(from_size: QSize, item_size: QSize):
        x = max(from_size.width() // 2 - item_size.width() // 2, 0)
        y = max(from_size.height() // 2 - item_size.height() // 2, 0)
        return QPoint(x, y)

    @staticmethod
    def are_rects_equal(a: QRect, b: QRect):
        if a.x() == b.x() and a.y() == b.y() and a.height() == b.height() and a.width() == b.width():
            return True
        return False

    def update(self):
        self.setGeometry(self.geometry())
