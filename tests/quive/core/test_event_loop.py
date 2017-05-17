import unittest
import st
import quive


class MyTestCase(unittest.TestCase):
    def test_event_loop_timeout(self):
        st.set_time_point('start')
        with quive.EventLoop(0.1):
            pass
        self.assertTrue(50 <= st.microsecond_from('start') <= 150)


if __name__ == '__main__':
    unittest.main()
