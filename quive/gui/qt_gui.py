from PyQt5.QtWidgets import *


__saved__ = []
# noinspection PyArgumentList
if not QApplication.instance():
    __saved__.append(QApplication([]))
