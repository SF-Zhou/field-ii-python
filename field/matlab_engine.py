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
        self.session_name = session_name
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

    # Field II Function
    def field_init(self):
        self.e.field_init(0, nargout=0)

    def set_sampling(self, frequency: float):
        self.e.set_sampling(frequency, nargout=0)

    def xdc_linear_array(self, no_elements: int, width: float, height: float, kerf: float,
                         no_sub_x: int, no_sub_y: int, focus: np.ndarray):
        return self.e.xdc_linear_array(no_elements, width, height, kerf, no_sub_x, no_sub_y,
                                       matlab.double(np.array(focus).tolist()))

    def xdc_impulse(self, th, pulse: np.ndarray):
        self.e.xdc_impulse(th, matlab.double(pulse.tolist()), nargout=0)

    def xdc_excitation(self, th, pulse: np.ndarray):
        self.e.xdc_excitation(th, matlab.double(pulse.tolist()), nargout=0)

    def xdc_center_focus(self, th, point: np.ndarray):
        self.e.xdc_center_focus(th, matlab.double(np.array(point).tolist()), nargout=0)

    def xdc_focus(self, th, times, points: np.ndarray):
        self.e.xdc_focus(th, self.e.transpose(matlab.double(np.array(times).tolist())),
                         matlab.double(np.array(points).tolist()), nargout=0)

    def xdc_apodization(self, th, times, values: np.ndarray):
        self.e.xdc_apodization(th, self.e.transpose(matlab.double(np.array(times).tolist())),
                               matlab.double(np.array(values).tolist()), nargout=0)

    @transform_output
    def calc_scat(self, th1, th2, points: np.ndarray, amplitudes: np.ndarray):
        return self.e.calc_scat(th1, th2, matlab.double(points.tolist()),
                                self.e.transpose(matlab.double(np.array(amplitudes).tolist())), nargout=2)

    @transform_output
    def calc_scat_multi(self, th1, th2, points: np.ndarray, amplitudes: np.ndarray):
        return self.e.calc_scat_multi(th1, th2, matlab.double(points.tolist()),
                                      self.e.transpose(matlab.double(np.array(amplitudes).tolist())), nargout=2)

    @transform_output
    def calc_scat_all(self, th1, th2, points: np.ndarray, amplitudes: np.ndarray, dec_factor: int):
        return self.e.calc_scat_all(th1, th2, matlab.double(points.tolist()),
                                    self.e.transpose(matlab.double(np.array(amplitudes).tolist())),
                                    dec_factor, nargout=2)

    def scat(self, th1, th2, points: np.ndarray, amplitudes: np.ndarray, sampling_frequency: float):
        rf_data, start = self.calc_scat(th1, th2, points, amplitudes)
        _, m = rf_data.shape
        return np.r_[np.zeros((int(start * sampling_frequency + 0.5), m)), rf_data]

    def xdc_free(self, th):
        self.e.xdc_free(th, nargout=0)
