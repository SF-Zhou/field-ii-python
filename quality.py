import os
import sys
import json
import widgets
from language import *

configs = []
show = True
output_filename = None
current_command = None

for arg in sys.argv[1:]:
    if arg == '-c':
        current_command = 'config'
    elif arg == '-o':
        current_command = 'output'
    elif arg == '-n':
        show = False
    elif current_command == 'config':
        configs.append(arg)
    elif current_command == 'output':
        output_filename = arg


results = {}
for result_config in configs:
    method_results = {}
    with open(result_config) as f:
        items = json.load(f)['results']
    filename = os.path.basename(result_config)

    device_name = '25mm'
    if device_name not in result_config:
        device_name = '45mm'
    assert device_name in result_config

    key, *_ = filename.split('.lateral')
    for method, time in items.items():
        device = '{}_{}'.format(device_name, method)

        if device not in results:
            results[device] = []
        results[device].append('{}_{}'.format(key, time))

w = widgets.QualityChart()
if 'SA' in configs[0]:
    w.method = 'SA'
    w.reversed_method = 'RSA'
else:
    w.method = 'DAS'
    w.reversed_method = 'RDAS'

for device_name, value in results.items():
    value.sort()
    l = list(map(lambda v: v.split('_'), value))
    label, nums = zip(*l)
    nums = list(map(float, nums))
    print(label, nums)

    depth, name = device_name[:4], device_name[5:]
    is_dash = name == 'NRDAS' or name == 'reversed_synthetic_aperture'

    shape = 'circle' if depth == '25mm' else 'square'
    w.add_line(label, nums, shape, is_dash)

if 'contrast' in configs[0]:
    w.label_y = language('对比度', 'Contrast')
else:
    w.label_y = language('半峰全宽 / mm', 'FWHM (mm)')
w.process()

w.export_to_image(output_filename)
if show:
    w.exec()
