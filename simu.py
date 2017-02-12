import os
import sys
import field
import simulate
import numpy as np

if len(sys.argv) != 2:
    raise EnvironmentError("""Run this program like this:\n    python3 simu.py configs/multi_scat.json""")

config_path = sys.argv[1]
if not os.path.exists(config_path):
    raise FileNotFoundError("Not Found {}".format(config_path))

para = simulate.Parameter()
para.load(config_path)

worker = getattr(simulate, para.worker + 'Worker', None)
if worker is None:
    raise FileNotFoundError("Not Found {}Worker in simulate module".format(para.worker))

pool = field.MatlabPool(engine_count=4)
task = list(range(para.line_count))

lines = pool.parallel(worker, task=task, args=(para,))

with open(para.signal_path, 'wb') as f:
    for line in lines:
        f.write(np.array(line, dtype=np.float32).tobytes())
