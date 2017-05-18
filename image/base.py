import numpy as np
from . import UImage
from PIL import Image
from scipy import signal


def convert_to_decibel(raw_data: np.ndarray) -> np.ndarray:
    data = np.abs(signal.hilbert(raw_data)).T
    env = np.multiply(np.log10(data), 20)
    env = env - env.max()
    return env


def convert_to_pixel(decibel: np.ndarray, dynamic_range) -> np.ndarray:
    float_pixel = 255 * (decibel / dynamic_range + 1)
    float_pixel[float_pixel < 0] = 0
    return np.array(float_pixel, dtype=np.uint8)


def convert_to_image(u_image: UImage) -> Image:
    width, height = u_image.size
    im = Image.fromarray(u_image.pixel)
    return im.resize((int(width * 10), int(height * 10))).convert('RGB')
