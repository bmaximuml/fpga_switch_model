#!/usr/bin/env python

import os
from unittest import TextTestRunner, TestLoader
import click


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='verbose output')
@click.option('-t', '--test-dir', default=os.path.dirname(os.path.realpath(__file__)), type=str,
              help='The directory to look for tests in')
def run_tests(test_dir, verbose):
    """discover and run all tests in test_dir"""
    test_suite = TestLoader().discover(test_dir)
    verbosity = 2 if verbose else 1
    # run tests
    result = TextTestRunner(verbosity=verbosity).run(test_suite)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    # get the directory containing tests
    run_tests()
