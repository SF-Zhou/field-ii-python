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
    filename = os.path.basename(result_config)

    key, *_ = filename.split('.lateral')
    for method, time in items.items():
        if method not in results:
            results[method] = []
        results[method].append('{}_{}'.format(key, time))

w = widgets.QualityChart()
if 'SA' in configs[0]:
    w.method = 'SA'
    w.reversed_method = 'RSA'
else:
    w.method = 'DAS'
    w.reversed_method = 'RDAS'

for name, value in results.items():
    value.sort()
    l = list(map(lambda v: v.split('_'), value))
    label, nums = zip(*l)
    nums = list(map(float, nums))
    print(label, nums)

    is_dash = name == 'NRDAS' or name == 'reversed_synthetic_aperture'
    w.add_line(label, nums, 'none', is_dash)

if 'contrast' in configs[0]:
    w.label_y = 'Contrast (%)'
else:
    w.label_y = 'Lateral Resolution (mm)'
w.process()

w.export_to_image(output_filename)
if show:
    w.exec()
