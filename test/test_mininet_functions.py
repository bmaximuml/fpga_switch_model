#!/usr/bin/env python

import unittest

from mininet_functions import halve_delay

class TestHalveDelay(unittest.TestCase):
    """Test the halve_delay function"""
    def testSimple(self):
        self.assertEqual('5.0ms', halve_delay('10ms'))

if __name__ == '__main__':
    unittest.main()

