import sys
import imp
import ast

from mutator import Mutator

from re import match

class WeaponX(object):
    claws = False
    regex = r'hello.*'
    gene = False

    @classmethod
    def set_claws(cls, state, gene):
        cls.claws = state
        cls.gene = gene
        ms = []
        for m in sys.modules:
            if match(cls.regex, m):
                ms.append(m)
        for m in ms:
            del sys.modules[m]

    def __init__(self, *args):
        pass


    def find_module(self, fullname, path=None):
        if self.claws and fullname == 'hello.hello':
            return self
        return None
 
    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        if name == 'hello.hello':
            with open('example/hello/hello.py') as f:
                tree = ast.parse(f.read())
            Mutator(self.gene).visit(tree)
            tree = ast.fix_missing_locations(tree)
            mymodule = imp.new_module('hello.hello')
            code = compile(tree, '<string>', 'exec')
            exec code in mymodule.__dict__
            sys.modules[name] = mymodule
            return mymodule

sys.meta_path = [WeaponX()]