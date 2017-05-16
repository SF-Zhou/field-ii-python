import os
import subprocess


class Runner:
    MethodMapper = {
        'DAS': 'delay_and_sum',
        'RDAS': 'reversed_method',
        'SA': 'synthetic_aperture',
        'RSA': 'reversed_synthetic_aperture'
    }

    def __init__(self, target='measure'):
        self.target = target

    @property
    def cpp_method_dir(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cpp_method'))

    @property
    def execution_file(self):
        return 'bin/{}'.format(self.target)

    @property
    def compile_command(self):
        return 'cd "{}" && make {}'.format(self.cpp_method_dir, self.execution_file)

    @property
    def execution_path(self):
        path_value = os.path.join(self.cpp_method_dir, self.execution_file)
        if not os.path.exists(path_value):
            raise EnvironmentError('Not Found Execution File: {}'.format(path_value))
        return path_value

    @staticmethod
    def mapper(method):
        if method in Runner.MethodMapper:
            return Runner.MethodMapper[method]
        else:
            return method

    def compile(self):
        return_code = os.system(self.compile_command)
        if return_code:
            raise EnvironmentError('Compile C++ Method Error with Return Code {}'.format(return_code))

    def run(self, config_path, method, times):
        method = self.mapper(method)
        p = subprocess.Popen([self.execution_path, '-c', config_path, '-m', method, '-t', str(times)],
                             bufsize=1,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)

        lines = []
        while True:
            line = str(p.stdout.readline().decode()).replace('\n', '')
            if line:
                print(line)
                if not line.startswith('#'):
                    lines.append(line)
            else:
                break

        if p.returncode:
            raise RuntimeError("Execution Return {}".format(p.returncode))

        result = self.Result()
        exec('\n'.join(lines), result.__dict__)
        return result

    class Result:
        def __init__(self):
            self.config_path = ''
            self.method_name = ''
            self.running_time = 0.0

        def __str__(self):
            return '{}: {} ms'.format(self.method_name, self.running_time)
