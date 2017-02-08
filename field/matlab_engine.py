import numpy as np
import matlab.engine


def n_array(cell_array):
    return np.array(getattr(cell_array, '_data')).reshape(cell_array.size, order='F')


def to_n_array(v):
    return n_array(v) if getattr(v, '_data', None) else v


def transform_output(func):
    def new_func(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            return [to_n_array(v) for v in result]
        elif isinstance(result, tuple):
            return tuple(to_n_array(v) for v in result)
        else:
            return to_n_array(result)
    return new_func


class MatlabEngine:
    def __init__(self, session_name: str=None):
        if session_name:
            self.engine = matlab.engine.connect_matlab(session_name)
        else:
            self.engine = matlab.engine.start_matlab()

    @property
    def e(self) -> matlab.engine.MatlabEngine:
        return self.engine

    # MATLAB function
    @transform_output
    def linspace(self, start, end, count):
        return self.e.linspace(start, end, count)

    @transform_output
    def magic(self, size: int):
        return self.e.magic(size)
