import os
import field
import simulate
import unittest


class MyTestCase(unittest.TestCase):
    def test_simple_build(self):
        pool = field.MatlabPool(engine_count=1)
        para = simulate.Parameter()
        para.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'configs', 'simple.json'))
        result = pool.parallel(simulate.SimpleWorker, task=[], args=(para,))
        self.assertTrue(result)
        self.assertEqual(result[0].shape[1], 32)


if __name__ == '__main__':
    unittest.main()
