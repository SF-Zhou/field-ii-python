import sys
import param
from runner import Runner


if len(sys.argv) < 3:
    raise EnvironmentError("""Run this program like this:
    python3 calc.py configs/multi_scat.json delay_and_sum""")

config_path = sys.argv[1]
method = sys.argv[2]
times = int(sys.argv[3]) if len(sys.argv) > 3 else 1
target = 'beamforming' if times == 1 else 'measure'

para = param.Parameter()
para.load(config_path)

Runner(target).run(config_path, method, times)
