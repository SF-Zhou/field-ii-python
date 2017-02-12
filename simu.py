import os
import sys
import field
import simulate
import numpy as np

if len(sys.argv) != 3:
    raise EnvironmentError("""Run this program like this:
    python3 zombie.py MultiScat configs/multi_scat.json""")

_, worker_name, config_path = sys.argv

worker = getattr(simulate, worker_name + 'Worker', None)
if worker is None:
    raise FileNotFoundError("Not Found {}Worker in simulate module".format(worker_name))

if not os.path.exists(config_path):
    raise FileNotFoundError("Not Found {}".format(config_path))

para = simulate.Parameter()
para.load(config_path)
pool = field.MatlabPool(engine_count=4)
task = list(range(para.line_count))

lines = pool.parallel(worker, task=task, args=(para,))

with open(para.signal_path, 'wb') as f:
    for line in lines:
        f.write(np.array(line, dtype=np.float32).tobytes())
