#!/usr/bin/env python

import re
import unittest

from mininet_functions import halve_delay, get_poisson_delay


class TestHalveDelay(unittest.TestCase):
    """Test the halve_delay function"""
    def test_simple(self):
        self.assertEqual('5.0ms', halve_delay('10ms'))
        self.assertEqual('25.0ms', halve_delay('50ms'))
        self.assertEqual('2.5ms', halve_delay('5ms'))
        self.assertEqual('50.0ms', halve_delay('100ms'))


class TestPoissonDelay(unittest.TestCase):
    """Test the get_poisson_delay function"""
    def test_simple(self):
        valid_time = re.compile('^([-+]?[0-9]*\.?[0-9]+)([PTGMkmunpf]?s)$')
        test_cases = ['10ms', '1ms', '2ms', '123ms', '0ms']
        for case in test_cases:
            match = valid_time.match(get_poisson_delay(case))
            try:
                float(match.group(1))
            except ValueError:
                self.assertEqual(True, False, 'Could not cast {} to float.'.format(match.group(1)))
            self.assertEqual(match.group(2), 'ms')


if __name__ == '__main__':
    unittest.main()

