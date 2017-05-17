from ..core import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

__save__ = []
# noinspection PyArgumentList
if not QApplication.instance():
    __save__.append(QApplication([]))
Signal = pyqtSignal
assert QPainter == QPainter
