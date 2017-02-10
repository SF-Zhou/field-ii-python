import json
import typing
import traceback
import numpy as np


class AttachAbility:
    AttachFlag = '_attach_{}'

    def getter(self):
        name = self.AttachFlag.format(self.current_name)
        obj = getattr(self, name, None)
        if not obj:
            raise ValueError("{} is NOT Set".format(self.current_name))
        return obj

    def assign(self, value, name=None):
        name = self.AttachFlag.format(name or self.current_name)
        setattr(self, name, value)

    @property
    def current_name(self):
        return traceback.extract_stack(None, 3)[0][2]


class Parameter(AttachAbility):
    def __init__(self):
        pass

    @property
    def transducer_frequency(self) -> float:  # [Hz]
        return self.getter()

    @property
    def sampling_frequency(self) -> float:  # [Hz]
        return self.getter()

    @property
    def element_width(self) -> float:  # [m]
        return self.getter()

    @property
    def element_height(self) -> float:  # [m]
        return self.getter()

    @property
    def element_count(self) -> int:  # Number of physical elements
        return self.getter()

    @property
    def active_count(self) -> int:  # Number of active elements
        return self.getter()

    @property
    def kerf(self) -> int:  # [m]
        return self.getter()

    @property
    def focus(self) -> typing.List[float]:  # Fixed focal point [m]
        return self.getter()

    @property
    def line_count(self) -> int:  # Number of lines in image
        return self.getter()

    @property
    def row_count(self) -> int:  # Number of rows in image
        return self.getter()

    @property
    def z_focus(self):  # Transmit focus
        return self.focus[2]

    @property
    def z_start(self):  # Start point on vertical direction
        return self.getter()

    @property
    def z_size(self):  # Height on vertical direction
        return self.getter()

    @property
    def point_count(self):  # Point count in phantom
        return self.getter()

    @property
    def light_points(self):  # Light points in phantom
        return self.getter()

    @property
    def dynamic_range(self):  # dB
        return self.getter()

    @property
    def data_length(self):
        return self.getter()

    @property
    def phantom(self) -> typing.Tuple[np.ndarray, np.ndarray]:
        try:
            return self.getter()
        except ValueError:
            light_points_count = len(self.light_points)
            assert light_points_count <= self.point_count

            position = np.c_[
                np.random.rand(self.point_count) * self.image_width - self.image_width / 2,
                np.zeros(self.point_count),
                np.random.rand(self.point_count) * self.z_size + self.z_start,
            ]
            amplitude = np.random.rand(self.point_count)

            position[0:light_points_count, :] = np.array(self.light_points)
            amplitude[0:light_points_count] = 20

            self.assign((position, amplitude))
            return self.getter()

    @property
    def c(self) -> float:  # Speed of Sound [m/s]
        return 1540.0

    @property
    def wave_length(self):  # [m]
        return self.c / self.transducer_frequency

    @property
    def image_width(self) -> float:  # Width of image sector
        return self.pixel_width * self.line_count

    @property
    def image_height(self) -> float:  # Height of image sector
        return self.z_size

    @property
    def pixel_width(self) -> float:
        return self.element_width + self.kerf

    @property
    def pixel_height(self) -> float:
        return self.image_height / self.row_count

    @property
    def active_count(self) -> int:
        return self.element_count - self.line_count + 1

    def load(self, filename):
        with open(filename) as f:
            paras = json.load(f)
            for key, value in paras.items():
                self.assign(value, name=key)
