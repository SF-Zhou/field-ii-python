import unittest
import quive


class MyTestCase(unittest.TestCase):
    def test_dialog_closed_signal(self):
        dialog = quive.Dialog()
        executed = [False]

        @quive.connect_with(dialog.closed)
        def is_closed():
            executed[0] = True

        quive.later(0.1, dialog.close)
        dialog.exec()
        self.assertTrue(all(executed))


if __name__ == '__main__':
    unittest.main()
