#!/usr/bin/env python

import click
import os

from unittest import TextTestRunner, TestLoader


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='verbose output')
@click.option('-t', '--test-dir', default=os.path.dirname(os.path.realpath(__file__)), type=str,
              help='The directory to look for tests in')
def runTests(test_dir, verbose):
    """discover and run all tests in test_dir"""
    testSuite = TestLoader().discover(test_dir)
    verbosity = 2 if verbose else 1
    # run tests
    TextTestRunner(verbosity=verbosity).run(testSuite)

if __name__ == '__main__':
    # get the directory containing tests
    runTests()
