import os
import sys
import functools

os.system('echo off && cd cpp_method && make && cd ..')

execution_path = 'cpp_method/bin/measure'
times = int(sys.argv[1]) if len(sys.argv) > 1 else 1
methods = ['synthetic_aperture', 'reversed_synthetic_aperture']
print('times = {}'.format(times))
config_folders = [
    'configs/1.change.sampling.frequency',
    'configs/2.change.line.count',
    'configs/3.change.row.count'
]


def listdir(folder):
    files = os.listdir(folder)
    return list(map(os.path.join, [folder] * len(files), files))

config_paths = functools.reduce(lambda a, b: a + b, map(listdir, config_folders), [])

for config_path in config_paths:
    print('config = {}'.format(config_path))
    for method in methods:
        os.system('{} -c {} -m {} -t {}'.format(execution_path, config_path, method, times))
