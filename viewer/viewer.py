import numpy as np
from PIL import Image
from scipy import signal


def viewer(image_data: list, width, height, dynamic_range: int=20):
    l = max(map(len, image_data))

    data = np.zeros((l, len(image_data)))
    for i, line in enumerate(image_data):
        line.shape = -1
        data[0:len(line), i] = line

    data = np.abs(signal.hilbert(data))

    data[data == 0] = 1e-100
    env = np.multiply(np.log10(data), 20)
    env = env - env.max()
    gray = 255 * (env / dynamic_range + 1)
    im = Image.fromarray(gray)

    im = im.resize((int(width * 10), int(height * 10)))
    im.show()
