import sys, os
import ast

from StringIO import StringIO

import unittest

from cerebro import Cerebro

def list_python_files(path):
    pfiles = []
    for r,d,f in os.walk(path):
        for files in f:
            if files.endswith('.py'):
                 pfiles.append(os.path.join(r,files))
    return pfiles

def get_suite(path):
    sys.path.append(path)
    tests = unittest.TestLoader()
    return tests.discover(path, pattern='*_test.py')

def run_tests(target_module, path=None):
    loader = unittest.TestLoader()
    #TODO suite = loader.loadTestsFromModule('hello')
    suite = loader.discover('example/', pattern='*_test.py')

    #TODO reload test package
    st = StringIO()
    result = unittest.TextTestRunner(stream=st ,verbosity=3, failfast=True).run(suite)
    return result

def tests_are_green(target_module, path=None):
    result = run_tests(target_module)
    assert result.testsRun > 0
    return result.wasSuccessful()

def find_genes(target, path):
    ps = list_python_files(path)
    g = []
    for p in ps:
        with open(p) as f:
            tree = ast.parse(f.read())
        c = Cerebro()
        c.visit(tree)
        tree = ast.fix_missing_locations(tree)
        g += c.genes
    return g
