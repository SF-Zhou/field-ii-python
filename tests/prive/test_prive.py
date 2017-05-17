import prive
import pickle
import unittest


class MyTestCase(unittest.TestCase):
    def test_project_storage_tree(self):
        class ItemDemo(prive.IntProjectItem):
            pass

        class ProjectDemo(prive.AbstractProject):
            def __init__(self):
                self.width = ItemDemo(self)
                self.height = ItemDemo(self)

        p = ProjectDemo()
        p.width.int.value = 16
        p.height.int.value = 20
        self.assertEqual(p.value, {'width': '16', 'height': '20'})
        pickled_p = pickle.dumps(p.value)

        p.value = {'height': 17}
        self.assertEqual(p.height.int.value, 17)
        self.assertEqual(p.width.value, None)

        p.value = pickle.loads(pickled_p)
        self.assertEqual(p.width.string.value, '16')
        self.assertEqual(p.height.string.value, '20')

    def test_value_changed(self):
        class ItemDemo(prive.IntProjectItem):
            pass

        class ProjectDemo(prive.AbstractProject):
            def __init__(self):
                self.width = ItemDemo(self)
                self.height = ItemDemo(self)

        p = ProjectDemo()
        times = []

        @prive.connect_with(p.width.int.changed)
        def width_changed(value: int):
            times.append(len(times))

            if len(times) == 1:
                self.assertEqual(value, 16)
            elif len(times) == 2:
                self.assertEqual(value, 20)
            elif len(times) == 3:
                self.assertEqual(value, 0)
            else:
                pass

        p.width.string.value = '16'
        p.width.value = '20'
        p.width.int.value = 0

        self.assertEqual(len(times), 3)

    def test_setting_value(self):
        class SettingItemDemo(prive.IntSettingItem):
            pass

        class SettingDemo(prive.AbstractSetting):
            def __init__(self):
                self.margin = SettingItemDemo(self, 5)

        s = SettingDemo()
        self.assertEqual(s.margin.int.value, 5)
        self.assertEqual(s.value, {})

        s.margin.int.value = 20
        self.assertEqual(s.margin.int.value, 20)
        self.assertEqual(s.value, {'margin': '20'})

if __name__ == '__main__':
    unittest.main()
