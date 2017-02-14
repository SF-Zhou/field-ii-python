import param
import numpy as np
from PIL import Image
from scipy import signal


def show(image: np.ndarray, para: param.Parameter):
    data = np.abs(signal.hilbert(image)).transpose()
    data[data == 0] = 1e-100
    env = np.multiply(np.log10(data), 20)
    env = env - env.max()
    gray = 255 * (env / para.dynamic_range + 1)
    im = Image.fromarray(gray)
    im = im.resize((int(para.image_width * 1e3 * 10),
                    int(para.image_height * 1e3 * 10)))
    im.show()
