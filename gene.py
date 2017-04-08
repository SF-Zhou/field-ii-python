import os
import sys
import param
import field
import simulate
import numpy as np

if len(sys.argv) < 2:
    raise EnvironmentError("""Run this program like this:\n    python3 simu.py configs/multi_scat.json""")

for config_path in sys.argv[1:]:
    if not os.path.exists(config_path):
        raise FileNotFoundError("Not Found {}".format(config_path))

    para = param.Parameter()
    para.load(config_path)

    worker = getattr(simulate, para.worker + 'Worker', None)
    if worker is None:
        raise FileNotFoundError("Not Found {}Worker in simulate module".format(para.worker))

    engine_count = 1 if para.worker.endswith("SyntheticAperture") else 4
    pool = field.MatlabPool(engine_count=engine_count)
    task = list(range(para.line_count))

    lines = pool.parallel(worker, task=task, args=(para,))

    with open(para.signal_path, 'wb') as f:
        for line in lines:
            f.write(np.array(line, dtype=np.float32).tobytes())
