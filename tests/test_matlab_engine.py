import field
import warnings
import unittest
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_start_matlab_engine(self):
        import matlab.engine
        session_names = matlab.engine.find_matlab()
        if not session_names:
            matlab = field.MatlabEngine()
            self.assertIsNotNone(matlab.engine)

    def test_connect_matlab_engine(self):
        import matlab.engine
        session_names = matlab.engine.find_matlab()
        if session_names:
            matlab = field.MatlabEngine(session_names[0])
            self.assertIsNotNone(matlab.engine)
        else:
            with warnings.catch_warnings():
                warnings.warn("Not Found Shared MATLAB Session")

    def test_matlab_function(self):
        import matlab.engine
        session_names = matlab.engine.find_matlab()
        if session_names:
            matlab = field.MatlabEngine(session_names[0])

            res = matlab.linspace(0.0, 6.28, 10)
            self.assertTrue(isinstance(res, np.ndarray))
            self.assertEqual(res.shape, (1, 10))

            res = matlab.magic(4)
            self.assertEqual(res.shape, (4, 4))
        else:
            self.fail("Not Found Shared MATLAB Session")

    def test_matlab_pool(self):
        matlab_pool = field.MatlabPool(engine_count=2)
        for session_name in matlab_pool.session_names:
            self.assertTrue(isinstance(session_name, str))

        class FieldIIInitWorker(field.MatlabWorker):
            def run(self, *args):
                self.e.field_init()
                return self.e.session_name

        result = matlab_pool.parallel(FieldIIInitWorker, list(range(10)))
        self.assertEqual(result, matlab_pool.session_names)


if __name__ == '__main__':
    unittest.main()
