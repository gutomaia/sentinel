import unittest

from hello import world

class HelloTest(unittest.TestCase):

    def test_hello(self):
        self.assertEquals('Hello', world())