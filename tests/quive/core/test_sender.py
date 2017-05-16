import unittest
import quive


class MyTestCase(unittest.TestCase):
    def test_sender(self):
        signal = quive.SignalSender()
        values = []

        @quive.connect_with(signal)
        def finished(value):
            values.append(value)

        signal.emit(0)
        signal.emit(1)
        signal.emit(2)

        self.assertEqual(values, [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
