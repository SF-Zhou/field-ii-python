import typing
import numpy as np


class UImage:
    def __init__(self, pixel: np.ndarray, size: typing.Tuple[float, float], z_start: float):
        self.pixel = pixel
        self.size = size
        self.z_start = z_start
