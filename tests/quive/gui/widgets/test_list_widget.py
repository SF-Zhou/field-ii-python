import unittest
import st
import quive


class MyTestCase(unittest.TestCase):
    def test_list_widget_row(self):
        with quive.EventLoop(0.1) as event:
            list_widget = quive.ListWidget()
            list_widget.show()
            executed = [False]

            @quive.connect_with(list_widget.string.changed)
            def text_changed(text):
                self.assertEqual(text, '1')
                executed[0] = True

            list_widget.string_list.value = st.foreach(str, range(10))
            list_widget.index.value = 1
            self.assertTrue(executed[0])

    def test_list_widget_string_list(self):
        with quive.EventLoop(0.1) as event:
            list_widget = quive.ListWidget()
            list_widget.show()
            executed = [False]
            string_list = st.foreach(str, range(10))

            @quive.connect_with(list_widget.string_list.changed)
            def string_list_changed(string_list_now):
                self.assertEqual(string_list, string_list_now)
                executed[0] = True

            list_widget.string_list.value = string_list
            self.assertTrue(executed[0])

    def test_list_widget_set_text(self):
        with quive.EventLoop(0.1):
            list_widget = quive.ListWidget()
            list_widget.show()
            times = []

            @quive.connect_with(list_widget.string.changed)
            def text_changed(string):
                if len(times) == 0:
                    self.assertEqual(string, 'first')
                elif len(times) == 1:
                    self.assertEqual(string, 'second')
                elif len(times) == 2:
                    self.assertEqual(string, 'first')
                elif len(times) == 3:
                    self.assertEqual(string, '')
                times.append(len(times))

            list_widget.string.set_value('first')
            list_widget.string.set_value('second')
            list_widget.string.set_value('first')
            self.assertEqual(len(times), 3)
            self.assertEqual(list_widget.string_list.count, 2)


if __name__ == '__main__':
    unittest.main()
