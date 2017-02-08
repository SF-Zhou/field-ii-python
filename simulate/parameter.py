import json
import typing
import traceback


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
    def image_width(self) -> int:  # Size of image sector
        return self.getter()

    @property
    def z_focus(self):  # Transmit focus
        return self.getter()

    @property
    def c(self) -> float:  # Speed of Sound [m/s]
        return 1540.0

    @property
    def wave_length(self):  # [m]
        return self.c / self.transducer_frequency

    @property
    def pixel_width(self):  # [m]
        return self.element_width + self.kerf

    def load(self, filename):
        with open(filename) as f:
            paras = json.load(f)
            for key, value in paras.items():
                self.assign(value, name=key)
