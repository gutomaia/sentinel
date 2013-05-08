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

def get_unittest_files(files):
    #return [f for f in files if f.endswith('_test.py') ]
    return ['example.hello.hello_test']

def get_unittests(path):
    sys.path.append(path)
    tests = unittest.TestLoader()
    return tests.discover(path, pattern='*_test.py')

def run_tests(tests):
    loader = unittest.TestLoader()
    suite = loader.discover('example/', pattern='*_test.py')
    st = StringIO()
    result = unittest.TextTestRunner(stream=st ,verbosity=3).run(suite)
    return result

def tests_are_green(tests):
    result = run_tests(tests)
    assert result.testsRun > 0
    #if not result.wasSuccessful():
    #    print result.errors
    #    print result.failures
    #print result.wasSuccessful()
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
