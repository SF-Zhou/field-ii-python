import field
import warnings
import unittest


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


if __name__ == '__main__':
    unittest.main()
