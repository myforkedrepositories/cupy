import threading
import unittest

import cupy
from cupy.cuda import driver


class TestDriver(unittest.TestCase):
    def test_ctxGetCurrent(self):
        # Make sure to create context.
        cupy.arange(1)
        self.assertNotEqual(0, driver.ctxGetCurrent())

    def test_ctxGetCurrent_thread(self):
        # Make sure to create context in main thread.
        cupy.arange(1)

        def f(self):
            self._result0 = driver.ctxGetCurrent()
            cupy.arange(1)
            self._result1 = driver.ctxGetCurrent()

        self._result0 = None
        self._result1 = None
        t = threading.Thread(target=f, args=(self,))
        t.daemon = True
        t.start()
        t.join()

        # The returned context pointer must be NULL on sub thread
        # without valid context.
        self.assertEqual(0, self._result0)

        # After the context is created, it should return the valid
        # context pointer.
        self.assertNotEqual(0, self._result1)
