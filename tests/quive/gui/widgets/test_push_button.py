import unittest
import quive


class MyTestCase(unittest.TestCase):
    def test_push_button_text(self):
        with quive.EventLoop(0.1):
            push_button = quive.PushButton()
            push_button.show()
            times = []

            @quive.connect_with(push_button.string.changed)
            def text_changed(text):
                if len(times) == 0:
                    self.assertEqual(text, 'first')
                elif len(times) == 1:
                    self.assertEqual(text, 'second')
                times.append(len(times))

            push_button.string.value = 'first'
            push_button.string.value = 'second'
            self.assertEqual(len(times), 2)


if __name__ == '__main__':
    unittest.main()
