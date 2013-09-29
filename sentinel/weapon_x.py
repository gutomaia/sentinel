import sys
import imp
import ast

from mutator import Mutator

from re import match

class WeaponX(object):
    claws = False
    regex = r'^hello\.[a-z]*$'
    gene = None

    @classmethod
    def deploy(cls):
        sys.meta_path = [cls]
        #sys.path_hooks.append(cls)

    @classmethod
    def set_claws(cls, state, gene):
        #print 'claws %s' % state
        cls.claws = state
        cls.gene = gene
        #ms = []
        for m in sys.modules:
            if match(cls.regex, m):
                if sys.modules[m]:
                    reload(sys.modules[m])
                    #print 'reload %s' % m
                #ms.append(m)
        if 'hello.hello_test' in sys.modules:
            reload(sys.modules['hello.hello_test'])

    @classmethod
    def find_module(cls, fullname, path=None):
        #TODO use path
        #print 'find_module %s' % fullname
        if cls.claws and match(cls.regex, fullname):
            #print 'FOUND %s' % fullname
            return cls
        return None

    @classmethod
    def load_module(cls, name):
        #print 'load_module %s' % name
        if name == 'hello.hello':
            with open('example/hello/hello.py') as f:
                tree = ast.parse(f.read())
            Mutator(cls.gene).visit(tree)
            tree = ast.fix_missing_locations(tree)
            mymodule = imp.new_module(name)
            code = compile(tree, '<string>', 'exec')
            exec code in mymodule.__dict__
            sys.modules[name] = mymodule
            return mymodule