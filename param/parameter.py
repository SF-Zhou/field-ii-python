import os
import json
import typing
import traceback
import numpy as np


class AttachAbility:
    AttachFlag = '_attach_{}'

    def getter(self):
        name = self.AttachFlag.format(self.current_name)
        obj = getattr(self, name, None)
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
    def save_path(self):
        value = self.getter()
        if not os.path.exists(value):
            os.system('mkdir -p {}'.format(value))
        return value

    @property
    def signal_path(self):
        return os.path.join(self.save_path, 'signal')

    @property
    def image_path(self):
        return os.path.join(self.save_path, 'image')

    @property
    def worker(self):
        return self.getter()

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
    def kerf(self) -> int:  # [m]
        return self.getter()

    @property
    def focus(self) -> typing.List[float]:  # Fixed focal point [m]
        return self.getter()

    @property
    def line_count(self) -> int:  # Number of lines in image
        return self.getter()

    @property
    def total_element_count(self) -> int:
        return self.element_count + self.line_count - 1

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
    def light_cysts(self):  # Light cysts in phantom
        return self.getter()

    @property
    def dark_cysts(self):  # Dark cysts in phantom
        return self.getter()

    @property
    def just_light_cysts(self):
        return self.getter()

    @property
    def dynamic_range(self):  # dB
        return self.getter()

    @property
    def data_length(self):
        return self.getter()

    @property
    def from_image(self):
        return self.getter()

    @property
    def phantom(self) -> typing.Tuple[np.ndarray, np.ndarray]:
        phantom = self.getter()

        if phantom is None:
            x0 = np.random.rand(self.point_count)
            y0 = np.random.rand(self.point_count)
            z0 = np.random.rand(self.point_count)

            x = (x0 - 0.5) * self.scatter_width
            y = (y0 - 0.5) * self.image_thickness
            z = z0 * self.z_size + self.z_start
            amplitude = np.random.rand(self.point_count)

            if self.from_image:
                from PIL import Image
                im = Image.open(os.path.join(os.path.dirname(self.config_path), self.from_image))
                im_arr = np.array(im.convert('L'))
                h, w = im_arr.shape
                ph = np.array(z0 * h, dtype=np.int)
                pw = np.array(x0 * w, dtype=np.int)
                brightness = im_arr[ph, pw]
                amplitude *= brightness
                amplitude[brightness >= 250] *= 4

            total = np.ones(self.point_count, dtype=bool)
            for light_cyst in self.light_cysts or []:
                px, r, pz = light_cyst
                inside = (x - px) ** 2 + (z - pz) ** 2 < r ** 2
                amplitude[inside] *= 10
                total[inside] = False

            for dark_cyst in self.dark_cysts or []:
                px, r, pz = dark_cyst
                inside = (x - px) ** 2 + (z - pz) ** 2 < r ** 2
                amplitude[inside] = 0

            position = np.c_[x, y, z]
            if self.light_points:
                light_points_count = len(self.light_points)
                assert light_points_count <= self.point_count

                position[0:light_points_count, :] = np.array(self.light_points)
                amplitude[0:light_points_count] = 20

            if self.just_light_cysts:
                amplitude[total] = 0
            position = position[amplitude > 0]
            amplitude = amplitude[amplitude > 0]
            phantom = (position, amplitude)
            self.assign(phantom)
        return phantom

    @property
    def c(self) -> float:  # Speed of Sound [m/s]
        return 1540.0

    @property
    def wave_length(self):  # [m]
        return self.c / self.transducer_frequency

    @property
    def scatter_width(self):
        return self.getter() or self.image_width

    @property
    def image_width(self) -> float:  # Width of image sector
        return self.pixel_width * self.line_count

    @property
    def image_height(self) -> float:  # Height of image sector
        return self.z_size

    @property
    def image_thickness(self) -> float:  # Thickness of image sector
        return 1e-3

    @property
    def image_size(self) -> typing.Tuple[float, float]:  # image size, mm
        return self.image_width * 1000, self.image_height * 1000

    @property
    def pixel_width(self) -> float:
        return self.element_width + self.kerf

    @property
    def pixel_height(self) -> float:
        return self.image_height / self.row_count

    @property
    def active_count(self) -> int:
        return self.element_count - self.line_count + 1

    @property
    def config_path(self):
        return self.getter()

    @property
    def methods(self):
        return self.getter()

    @property
    def speed_test(self):
        return self.getter()

    @property
    def lateral_test(self):
        return self.getter()

    @property
    def contrast_test(self):
        return self.getter()

    def load(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError("Not Found {}".format(filename))

        self.assign(filename, 'config_path')
        with open(filename) as f:
            paras = json.load(f)
            if 'save_path' not in paras and filename[:8] == 'configs/':
                paras['save_path'] = 'data/' + filename[8:-5]
            if 'line_count' not in paras and 'element_count' in paras:
                paras['line_count'] = paras['element_count']
            for key, value in paras.items():
                self.assign(value, name=key)
