import os
import simulate
import subprocess
import numpy as np


def cpp_method(image_data: np.ndarray, para: simulate.Parameter, config_path: str, method: str):
    cpp_method_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cpp_method')
    return_code = os.system('cd "{}" && make'.format(cpp_method_dir))
    if return_code:
        raise EnvironmentError('Compile C++ Method Error with Return Code {}'.format(return_code))

    execution_path = os.path.join(cpp_method_dir, 'bin/beamforming')
    if not os.path.exists(execution_path):
        raise EnvironmentError('Not Found Execution File')

    p = subprocess.Popen([execution_path, '-c', config_path, '-m', method],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)

    if p.returncode:
        raise "Execution Return {}".format(p.returncode)
