#!/usr/bin/env python

import re
import unittest

from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost

from mininet_functions import halve_delay, get_poisson_delay, TreeTopoGeneric


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


class TestTreeTopoGeneric(unittest.TestCase):
    """Test the TreeTopoGeneric class"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=2, depth=3, bandwidth=10, delay='1ms', loss=0, fpga=None)
        # topo_1 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='1ms', loss=1, fpga=None)
        # topo_2 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='4ms', loss=2, fpga=None)
        # topo_3 = TreeTopoGeneric(spread=3, depth=2, bandwidth=1, delay='1ms', loss=50, fpga=None)
        # topo_4 = TreeTopoGeneric(spread=4, depth=4, bandwidth=100, delay='1ms', loss=0, fpga=None)
        # topo_5 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='4ms', loss=2, fpga=None)
        # topo_6 = TreeTopoGeneric(spread=1, depth=4, bandwidth=10, delay='1ms', loss=50, fpga=None)
        # topo_7 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=None)

        topologies = [topo_0]
        # topologies = [topo_0, topo_1, topo_2, topo_3, topo_4, topo_5, topo_6, topo_7]

        for topo in topologies:
            try:
                Cleanup.cleanup()
                net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
                net.start()
                self.assertEqual(True, True)
            except Exception as ex:
                self.assertEqual(True, False, 'TestTreeTopoGeneric rose an Exception of type {}.'.format(type(ex).__name__))
            finally:
                Cleanup.cleanup()


if __name__ == '__main__':
    unittest.main()

