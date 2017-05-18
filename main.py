import os
import st
import sys
import json
import param
import colored
import hashlib
import datetime
import numpy as np
from runner import Runner


def success(*args):
    print(colored.fg(2), end='')
    print(*args, end='')
    print(colored.attr(0))


def fail(*args):
    print(colored.fg(1), end='')
    print(*args, end='')
    print(colored.attr(0))


class Option:
    MethodMapper = {
        'DAS': 'delay_and_sum',
        'RDAS': 'reversed_method',
        'ORDAS': 'optimized_reversed_method',
        'SA': 'synthetic_aperture',
        'RSA': 'reversed_synthetic_aperture'
    }

    class Mode(st.Enum):
        Initial = ()
        Config = ()
        Method = ()
        Times = ()

    def __init__(self, *args):
        self.configs = []
        self.command = []
        self.methods = []
        self.times = 1

        self.args = args if args else sys.argv[1:]
        self.process_args()

        self.device = ''

        if os.path.exists('device.json'):
            with open('device.json', 'r') as f:
                j = json.load(f)
                self.device = j['name']

    @property
    def is_simulation(self):
        return 's' in self.command

    @property
    def is_calculation(self):
        return 'c' in self.command

    @property
    def is_measure(self):
        return 'm' in self.command

    @property
    def is_view(self):
        return 'v' in self.command

    def process_args(self):
        assert len(self.args), 'Args has to be set'

        self.command, *args = self.args
        current_mode = self.Mode.Initial
        for arg in args:
            if arg == '-c':
                current_mode = self.Mode.Config
            elif arg == '-m':
                current_mode = self.Mode.Method
            elif arg == '-t':
                current_mode = self.Mode.Times
            else:
                if current_mode == self.Mode.Config:
                    self.configs.append(arg)
                elif current_mode == self.Mode.Method:
                    if arg in self.MethodMapper:
                        arg = self.MethodMapper[arg]
                    self.methods.append(arg)
                elif current_mode == self.Mode.Times:
                    self.times = int(arg)
                else:
                    raise SyntaxError('Command Error: {}'.format(args))
        if not self.configs:
            raise SyntaxError('Configs Not Found')

    def process(self):
        if self.is_calculation:
            Runner(is_measure=False).compile()
        if self.is_measure:
            Runner(is_measure=True).compile()

        for config_path in self.configs:
            if config_path.endswith('res.json'):
                continue

            self.output_tip('Current Config: {}'.format(config_path))

            para = param.Parameter()
            para.load(config_path)

            if self.is_simulation:
                self.simulation(para)

            if self.is_calculation:
                self.calculation(para, self.methods, self.times, self.is_measure)

            if self.is_measure:
                if not self.device:
                    raise EnvironmentError('Device Info Not Set')

                with open(config_path, 'r') as f:
                    current_version = hashlib.md5(f.read().encode()).hexdigest()

                need_calculation = True
                result_path = '{}.{}.res.json'.format(config_path[:-5], self.device)
                if os.path.exists(result_path):
                    with open(result_path, 'r') as f:
                        j = json.load(f)
                        if 'version' in j and j['version'] == current_version:
                            if 'times' in j and j['times'] == self.times:
                                need_calculation = False

                if need_calculation:
                    results = self.calculation(para, self.methods, self.times, self.is_measure)

                    final = {
                        "version": current_version,
                        "time": str(datetime.datetime.now()),
                        "times": self.times,
                        "results": results
                    }

                    with open(result_path, 'w') as f:
                        json.dump(final, f, indent=2)

            if self.is_view:
                self.view(para, self.methods)

            print()

    @staticmethod
    def simulation(para: param.Parameter):
        import field
        import simulate

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

    @staticmethod
    def calculation(para: param.Parameter, methods: list, times: int, is_measure: bool):
        if not methods:
            raise SyntaxError('Methods Not Found')

        results = []
        for method in methods:
            Option.output_tip('Current Method: {}'.format(method))

            runner = Runner(is_measure=is_measure)
            result = runner.run(para.config_path, method, times)

            results.append({
                "name": result.method_name,
                "time": result.running_time
            })
        return results

    @staticmethod
    def view(para: param.Parameter, methods: list):
        import image
        import quive
        import widgets

        if not methods:
            raise SyntaxError('Methods Not Found')

        with quive.EventLoop() as loop:
            for method in methods:
                image_path = para.image_path + '.' + method

                if not os.path.exists(image_path):
                    raise FileNotFoundError("Not Found {}".format(image_path))

                raw_image = np.fromfile(image_path, dtype=np.float32)
                if method == 'reversed_synthetic_aperture':
                    raw_image.shape = para.row_count, para.line_count
                    raw_image = raw_image.T
                else:
                    raw_image.shape = para.line_count, para.row_count

                decibel = image.convert_to_decibel(raw_image)
                pixel = image.convert_to_pixel(decibel, para.dynamic_range)
                u_image = image.UImage(pixel, para.image_size, para.z_start * 1000)

                w = widgets.ImageWidget()
                w.u_image = u_image
                w.setWindowTitle('{} {}'.format(para.config_path, method))
                w.show()
                w.closed.connect(loop.quit)

    @staticmethod
    def output_tip(tip):
        success('=' * len(tip))
        success(tip)


if __name__ == '__main__':
    option = Option()
    option.process()
