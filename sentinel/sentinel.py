import os
import sys
import re
import logging
import argparse
from ConfigParser import ConfigParser

from util import list_python_files, get_unittest_files, tests_are_green, find_genes
import weapon_x

class Sentinel(object):

    def __init__(self, target, path):
        self.target = target
        f = list_python_files(path)
        t = get_unittest_files(f)
        mutants = dict()
        if tests_are_green(t):
            for gene in find_genes(target, path):
                wolverine = weapon_x.WeaponX()
                wolverine.target = target
                wolverine.set_claws(True, gene)
                if tests_are_green(t):
                    g = gene.split('|')[0]
                    m = gene.split('|')[1]
                    d = gene.split('|')[2]
                    if g not in mutants:
                        mutants[g] = dict()
                    mutants[g][m] = d
            for m in mutants:
                print 'you found the mutant %s with the powers:' % (m)
                for p in mutants[m]:
                    print '\t-%s with mutation %s' % (mutants[m][p], p)
        else:
            print 'tests must be green'

def main(argv = None):
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description='Sentinel program will track and kill mutants',
        epilog='')

    subparsers = parser.add_subparsers(
        title="subcommands", description="utilities", help="aditional help")

    py_cmd = subparsers.add_parser('dojo') #, aliases=['py'])
    py_cmd.add_argument('-v', '--verbose', default='False', action='store_true', help="verbose output")
    py_cmd.add_argument('-p', '--path', default='False', metavar='PATH', help="path application")

    py_cmd.add_argument('target', nargs='?', metavar='TARGET', help="python module to inspect")
    py_cmd.set_defaults(func=exec_dojo)

    args = parser.parse_args(argv[1:])
    kargs = vars(args)
    args.func(**kargs)

def exec_dojo(target, path, verbose, func):
    s = Sentinel(target, path)