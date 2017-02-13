import os
import sys
import simulate
import subprocess


if len(sys.argv) < 3:
    raise EnvironmentError("""Run this program like this:
    python3 calc.py configs/multi_scat.json delay_and_sum""")

config_path = sys.argv[1]
if not os.path.exists(config_path):
    raise FileNotFoundError("Not Found {}".format(config_path))
method = sys.argv[2]
times = int(sys.argv[3]) if len(sys.argv) > 3 else 1

para = simulate.Parameter()
para.load(config_path)

cpp_method_dir = os.path.join(os.path.dirname(__file__), 'cpp_method')
execution_file = 'bin/{}'.format('beamforming' if times == 1 else 'measure')
return_code = os.system('cd "{}" && make {}'.format(cpp_method_dir, execution_file))
if return_code:
    raise EnvironmentError('Compile C++ Method Error with Return Code {}'.format(return_code))

execution_path = os.path.join(cpp_method_dir, execution_file)
if not os.path.exists(execution_path):
    raise EnvironmentError('Not Found Execution File')

return_code = os.system('{} -c {} -m {} -t {}'.format(execution_path, config_path, method, str(times)))
if return_code:
    raise "Execution Return {}".format(return_code)
