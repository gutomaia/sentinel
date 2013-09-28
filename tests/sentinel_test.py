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

from sentinel.weapon_x import WeaponX
from sentinel.util import find_genes
import sys

class WeaponXTest(unittest.TestCase):

    def setUp(self):
        if 'hello.hello' in sys.modules:
            del sys.modules['hello.hello']

    def test_xweapon_find_module_hello(self):
        wx = WeaponX()
        wx.claws = True
        loader = wx.find_module('hello')
        self.assertIsNone(loader)

    def test_xweapon_find_module_hello_hello(self):
        wx = WeaponX()
        wx.claws = True
        loader = wx.find_module('hello.hello')
        self.assertIsNotNone(loader)

    def test_xweapon_load_module_hello_hello(self):
        wx = WeaponX()
        self.assertTrue('hello.hello' not in sys.modules)
        module = wx.load_module('hello.hello')
        self.assertIsNotNone(module)
        self.assertTrue('hello.hello' in sys.modules)
        from hello.hello import world
        self.assertEquals('Hello', world())
        self.assertEquals('Hello', world(False))
        self.assertEquals('Foo', world(True))

    def test_xweapon_load_module_hello_hello_with_mutation_true(self):
        genes = find_genes('hello.hello', 'example/hello/')
        wx = WeaponX()
        wx.gene = genes[0]
        self.assertTrue('hello.hello' not in sys.modules)
        module = wx.load_module('hello.hello')
        self.assertIsNotNone(module)
        self.assertTrue('hello.hello' in sys.modules)
        from hello.hello import world
        self.assertEquals('Foo', world())
        self.assertEquals('Foo', world(False))
        self.assertEquals('Foo', world(True))

    def test_xweapon_load_module_hello_hello_with_mutation_false(self):
        genes = find_genes('hello.hello', 'example/hello/')
        wx = WeaponX()
        wx.gene = genes[1]
        self.assertTrue('hello.hello' not in sys.modules)
        module = wx.load_module('hello.hello')
        self.assertIsNotNone(module)
        self.assertTrue('hello.hello' in sys.modules)
        from hello.hello import world
        self.assertEquals('Hello', world())
        self.assertEquals('Hello', world(False))
        self.assertEquals('Hello', world(True))


if __name__ == '__main__':
    unittest.main()