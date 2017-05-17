from . import *
from .. import QFont


class Scaling:
    def __init__(self):
        base = 800.0  # the width of a character when dpi = 96
        width = SizeF.text_size('Q', QFont('Courier New', 1000)).w
        self.ratio = width / base

scaling = Scaling()
