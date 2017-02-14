import os
import sys
import param
import viewer
import numpy as np


if len(sys.argv) != 3:
    raise EnvironmentError("""Run this program like this:
    python3 show.py configs/multi_scat.json delay_and_sum""")

config_path = sys.argv[1]
if not os.path.exists(config_path):
    raise FileNotFoundError("Not Found {}".format(config_path))
method = sys.argv[2]

para = param.Parameter()
para.load(config_path)

image_path = para.image_path + '.' + method

if not os.path.exists(image_path):
    raise FileNotFoundError("Not Found {}".format(image_path))

image = np.fromfile(image_path, dtype=np.float32)
image.shape = para.line_count, para.row_count
viewer.show(image, para)
