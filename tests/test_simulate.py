import os
import field
import param
import simulate
import unittest


class MyTestCase(unittest.TestCase):
    def test_simple_build(self):
        pool = field.MatlabPool(engine_count=1)
        para = param.Parameter()
        para.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'configs', '0.base.config', 'simple.json'))
        result = pool.parallel(simulate.SimpleWorker, task=[], args=(para,))
        self.assertTrue(result)
        self.assertEqual(result[0].shape[1], 32)

    def test_linear_array_imaging_build(self):
        pool = field.MatlabPool(engine_count=2)
        para = param.Parameter()
        para.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'configs', '0.base.config', 'linear_array_imaging.json'))
        task = list(range(para.line_count // 2 - 2, para.line_count // 2 + 2 + 1))
        result = pool.parallel(simulate.LinearArrayImagingWorker, task=task, args=(para,))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), len(task))


if __name__ == '__main__':
    unittest.main()
