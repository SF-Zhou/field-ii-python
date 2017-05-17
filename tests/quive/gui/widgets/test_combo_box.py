import unittest
import st
import quive


class MyTestCase(unittest.TestCase):
    def test_combo_box_row(self):
        with quive.EventLoop(0.1):
            combo_box = quive.ComboBox()
            combo_box.show()

            combo_box.string_list.value = st.foreach(str, range(10))
            self.assertEqual(combo_box.string_list.value, st.foreach(str, range(10)))

            combo_box.string_list.value = st.foreach(str, range(9))
            self.assertEqual(combo_box.string_list.value, st.foreach(str, range(9)))

    def test_combo_box_string_list(self):
        with quive.EventLoop(0.1):
            combo_box = quive.ComboBox()
            combo_box.show()
            executed = [False]

            string_list = st.foreach(str, range(10))

            @quive.connect_with(combo_box.string_list.changed)
            def string_list_changed(string_list_now):
                self.assertEqual(string_list, string_list_now)
                executed[0] = True

            combo_box.string_list.value = string_list
            self.assertTrue(executed[0])

    def test_combo_box_set_text(self):
        with quive.EventLoop(0.1):
            combo_box = quive.ComboBox()
            combo_box.show()
            times = []

            @quive.connect_with(combo_box.string.changed)
            def text_changed(text):
                if len(times) == 0:
                    self.assertEqual(text, 'first')
                elif len(times) == 1:
                    self.assertEqual(text, 'second')
                elif len(times) == 2:
                    self.assertEqual(text, 'first')
                elif len(times) == 3:
                    self.assertEqual(text, '')
                times.append(len(times))

            combo_box.string.set_value('first')
            combo_box.string.set_value('second')
            combo_box.string.set_value('first')
            self.assertEqual(len(times), 3)
            self.assertEqual(combo_box.string_list.count, 2)

            combo_box.clear()
            self.assertEqual(len(times), 4)
            self.assertEqual(combo_box.string_list.count, 0)


if __name__ == '__main__':
    unittest.main()
