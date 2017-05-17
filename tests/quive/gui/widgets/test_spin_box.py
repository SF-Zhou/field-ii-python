import unittest
import quive


class MyTestCase(unittest.TestCase):
    def test_spin_box_integer_property(self):
        with quive.EventLoop(0.1):
            spin_box = quive.SpinBox()
            spin_box.show()
            times = []

            @quive.connect_with(spin_box.int.changed)
            def spin_box_integer_changed(value: int):
                if len(times) == 0:
                    self.assertEqual(value, 1)
                elif len(times) == 1:
                    self.assertEqual(value, 10)
                elif len(times) == 2:
                    self.assertEqual(value, 99)
                elif len(times) == 3:
                    self.assertEqual(value, 0)
                times.append(len(times))

            spin_box.int.value = 1
            spin_box.int.value = 10
            spin_box.int.value = 99
            spin_box.int.value = -1
            self.assertEqual(len(times), 4)

    def test_spin_box_string_property(self):
        with quive.EventLoop(0.1):
            spin_box = quive.SpinBox()
            spin_box.show()
            times = []

            @quive.connect_with(spin_box.string.changed)
            def spin_box_integer_changed(value: str):
                if len(times) == 0:
                    self.assertEqual(value, '1')
                elif len(times) == 1:
                    self.assertEqual(value, '10')
                elif len(times) == 2:
                    self.assertEqual(value, '99')
                elif len(times) == 3:
                    self.assertEqual(value, '0')
                times.append(len(times))

            spin_box.string.value = '1'
            spin_box.string.value = '10'
            spin_box.string.value = '99'
            spin_box.string.value = '-1'
            self.assertEqual(len(times), 4)

if __name__ == '__main__':
    unittest.main()
