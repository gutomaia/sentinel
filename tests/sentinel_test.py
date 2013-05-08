import unittest

from sentinel.sentinel import Sentinel

from sentinel.util import list_python_files, get_unittest_files, get_unittests

class SentinelTest(unittest.TestCase):

    def test_list_python_files(self):
        f = list_python_files('example/hello')
        self.assertEquals(
            ['example/hello/__init__.py', 'example/hello/hello.py', 'example/hello/hello_test.py'], f)
        t = get_unittest_files(f)
        self.assertEquals(
            ['example.hello.hello_test'], t)

    def test_get_unittests(self):
        suite = get_unittests('example/hello')
        self.assertEquals(1, len(suite._tests))

    def test_sentinel(self):
        s = Sentinel(r'hello.*','example/hello')

if __name__ == '__main__':
    unittest.main()