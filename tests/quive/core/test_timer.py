import unittest
import quive
import time


class MyTestCase(unittest.TestCase):
    def test_timer(self):
        start = time.time()
        quive.wait(0.1)
        end = time.time()

        elapsed_time = end - start
        self.assertTrue(0.05 <= elapsed_time)
        self.assertTrue(elapsed_time <= 0.15)


if __name__ == '__main__':
    unittest.main()