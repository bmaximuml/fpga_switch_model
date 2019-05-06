#!/usr/bin/env python

import unittest

from mininet_functions import halve_delay


class TestHalveDelay(unittest.TestCase):
    """Test the halve_delay function"""
    def test_simple(self):
        self.assertEqual('5.0ms', halve_delay('10ms'))
        self.assertEqual('25.0ms', halve_delay('50ms'))
        self.assertEqual('2.5ms', halve_delay('5ms'))
        self.assertEqual('50.0ms', halve_delay('100ms'))


if __name__ == '__main__':
    unittest.main()

