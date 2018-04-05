import os
import sys
import json
import widgets

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
    for item in items:
        if item['name'] != 'reversed_method':
            method_results[item['name']] = item['time']
    filename = os.path.basename(result_config)

    key = ''
    device_name = 'i5'
    for d in ['i5', 'i7', 'TX1']:
        if d in filename:
            device_name = d
            key, *_ = filename.split('.' + d)

    for method, time in method_results.items():
        device = '{}_{}'.format(device_name, method)
        if device not in results:
            results[device] = []
        results[device].append('{}_{}'.format(key, time))

w = widgets.LineChart()
if 'synthetic' in configs[0]:
    w.method = '合成孔径算法'
    w.reversed_method = '反向合成孔径算法'
else:
    w.method = '延迟叠加算法'
    w.reversed_method = '反向延迟叠加算法'

for name, value in results.items():
    value.sort()
    l = list(map(lambda v: v.split('_'), value))
    label, nums = zip(*l)
    nums = list(map(float, nums))
    print(label, nums)

    if 'i5' in name:
        shape = 'triangle'
    elif 'i7' in name:
        shape = 'square'
    else:
        shape = 'circle'

    is_dash = 'reversed' in name

    w.add_line(label, nums, shape, is_dash)
w.process()

w.export_to_image(output_filename)
wmf_name = output_filename.replace('pdf', 'wmf')
os.system("inkscape --without-gui -f {} -m {}".format(output_filename, wmf_name))

if show:
    w.exec()
