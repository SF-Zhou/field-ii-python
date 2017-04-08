import os
import sys
import colored
import functools

os.system('cd cpp_method && make && cd ..')

execution_path = 'cpp_method/bin/measure'
times = int(sys.argv[1]) if len(sys.argv) > 1 else 1
methods = ['delay_and_sum', 'reversed_method']
print('times = {}'.format(times))
config_folders = [
    'configs/1.reversed.delay.and.sum/1.change.sampling.frequency',
    'configs/1.reversed.delay.and.sum/2.change.element.count',
    'configs/1.reversed.delay.and.sum/3.change.row.count'
]

def success(*args):
    print(colored.fg(2), end='')
    print(*args, end='')
    print(colored.attr(0))
    sys.stdout.flush()

def listdir(folder):
    files = os.listdir(folder)
    return list(map(os.path.join, [folder] * len(files), files))

config_paths = functools.reduce(lambda a, b: a + b, map(listdir, config_folders), [])

for config_path in config_paths:
    success('config = {}'.format(config_path))
    for method in methods:
        os.system('{} -c {} -m {} -t {}'.format(execution_path, config_path, method, times))
    success('\n')

success('Finished!')
