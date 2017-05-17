import os
import quive
import unittest


class MyTestCase(unittest.TestCase):
    def test_double_spin_box_integer_property(self):
        with quive.EventLoop(.10):
            double_spin_box = quive.DoubleSpinBox()
            double_spin_box.show()
            times = []

            @quive.connect_with(double_spin_box.float.changed)
            def double_spin_box_double_changed(value: float):
                if len(times) == 0:
                    self.assertEqual(value, 1.1)
                elif len(times) == 1:
                    self.assertEqual(value, 10.2)
                elif len(times) == 2:
                    self.assertEqual(value, 99.3)
                elif len(times) == 3:
                    self.assertEqual(value, 0)
                times.append(len(times))

            double_spin_box.float.value = 1.1
            double_spin_box.float.value = 10.2
            double_spin_box.float.value = 99.3
            double_spin_box.float.value = -1.4
            self.assertEqual(len(times), 4)

    def test_double_spin_box_string_property(self):
        with quive.EventLoop(0.1):
            double_spin_box = quive.DoubleSpinBox()
            double_spin_box.show()
            times = []

            @quive.connect_with(double_spin_box.string.changed)
            def double_spin_box_double_changed(value: str):
                if len(times) == 0:
                    self.assertEqual(value, '1.1')
                elif len(times) == 1:
                    self.assertEqual(value, '10.2')
                elif len(times) == 2:
                    self.assertEqual(value, '99.3')
                elif len(times) == 3:
                    self.assertEqual(value, '0.0')
                times.append(len(times))

            double_spin_box.string.value = '1.1'
            double_spin_box.string.value = '10.2'
            double_spin_box.string.value = '99.3'
            double_spin_box.string.value = '-1.4'
            self.assertEqual(len(times), 4)


if __name__ == '__main__':
    unittest.main()
