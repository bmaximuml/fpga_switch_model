#!/usr/bin/env python

import unittest
from mininet_functions import TreeTopoGeneric
from performance_tests import test_cloud_fpga

from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost


class TestTreeTopoGenericPoisson(unittest.TestCase):
    """Test the TreeTopoGeneric class with the get_poisson_delay function"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=None,
                                 poisson=True)
        topo_1 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='1ms', loss=1, fpga=None,
                                 poisson=True)
        topo_2 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='4ms', loss=2, fpga=None,
                                 poisson=True)
        topo_3 = TreeTopoGeneric(spread=3, depth=2, bandwidth=1, delay='1ms', loss=50, fpga=None,
                                 poisson=True)
        topo_4 = TreeTopoGeneric(spread=4, depth=4, bandwidth=100, delay='1ms', loss=0, fpga=None,
                                 poisson=True)
        topo_5 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='4ms', loss=2, fpga=None,
                                 poisson=True)
        topo_6 = TreeTopoGeneric(spread=1, depth=4, bandwidth=10, delay='1ms', loss=50, fpga=None,
                                 poisson=True)
        topo_7 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=None,
                                 poisson=True)
        topo_8 = TreeTopoGeneric(spread=4, depth=6, bandwidth=10, delay='1ms', loss=0, fpga=1,
                                 poisson=True)
        topo_9 = TreeTopoGeneric(spread=3, depth=4, bandwidth=10, delay='1ms', loss=0, fpga=2,
                                 poisson=True)
        topo_10 = TreeTopoGeneric(spread=5, depth=2, bandwidth=10, delay='1ms', loss=0, fpga=3,
                                 poisson=True)
        topo_11 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=4,
                                 poisson=True)

        topologies = [topo_0, topo_1, topo_2, topo_3, topo_4, topo_5, topo_6, topo_7, topo_8, topo_9, topo_10, topo_11]

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

class TestTreeTopoGenericHalveDelay(unittest.TestCase):
    """Test the TreeTopoGeneric class with the halve_delay function"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='3ms', loss=0, fpga=1)
        topo_1 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='10ms', loss=1, fpga=2)
        topo_2 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='4ms', loss=2, fpga=3)
        topo_3 = TreeTopoGeneric(spread=3, depth=3, bandwidth=1, delay='2ms', loss=50, fpga=3)
        topo_4 = TreeTopoGeneric(spread=4, depth=4, bandwidth=100, delay='1ms', loss=0, fpga=1)
        topo_5 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='4ms', loss=2, fpga=2)
        topo_6 = TreeTopoGeneric(spread=1, depth=4, bandwidth=10, delay='20ms', loss=50, fpga=2)
        topo_7 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=5)

        topologies = [topo_0, topo_1, topo_2, topo_3, topo_4, topo_5, topo_6, topo_7]

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


class TestTreeTopoGenericHalveDelayPoisson(unittest.TestCase):
    """Test the TreeTopoGeneric class with the get_poisson_delay and halve_delay functions"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='7ms', loss=0, fpga=4,
                                 poisson=True)
        topo_1 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='32ms', loss=1, fpga=2,
                                 poisson=True)
        topo_2 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='4ms', loss=2, fpga=6,
                                 poisson=True)
        topo_3 = TreeTopoGeneric(spread=3, depth=3, bandwidth=1, delay='19ms', loss=50, fpga=2,
                                 poisson=True)
        topo_4 = TreeTopoGeneric(spread=4, depth=4, bandwidth=100, delay='14ms', loss=0, fpga=2,
                                 poisson=True)
        topo_5 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='4ms', loss=2, fpga=4,
                                 poisson=True)
        topo_6 = TreeTopoGeneric(spread=1, depth=4, bandwidth=10, delay='12ms', loss=50, fpga=2,
                                 poisson=True)
        topo_7 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='31ms', loss=0, fpga=5,
                                 poisson=True)
        topo_8 = TreeTopoGeneric(spread=4, depth=6, bandwidth=10, delay='1ms', loss=0, fpga=1,
                                 poisson=True)
        topo_9 = TreeTopoGeneric(spread=3, depth=4, bandwidth=10, delay='1ms', loss=0, fpga=2,
                                 poisson=True)
        topo_10 = TreeTopoGeneric(spread=5, depth=2, bandwidth=10, delay='11ms', loss=0, fpga=3,
                                 poisson=True)
        topo_11 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='7ms', loss=0, fpga=4,
                                 poisson=True)

        topologies = [topo_0, topo_1, topo_2, topo_3, topo_4, topo_5, topo_6, topo_7, topo_8, topo_9, topo_10, topo_11]

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


class TestTestCloudFpgaTestCloud(unittest.TestCase):
    """Test the test_cloud_fpga with the halve_delay function and the TreeTopoGeneric class"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=3, depth=4, bandwidth=10, delay='1ms', loss=0, fpga=2)
        topo_1 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=1, fpga=3)
        topo_2 = TreeTopoGeneric(spread=2, depth=6, bandwidth=1, delay='1ms', loss=0, fpga=5)
        topo_3 = TreeTopoGeneric(spread=5, depth=3, bandwidth=10, delay='10ms', loss=1, fpga=2)
        topo_4 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='1ms', loss=0, fpga=3)

        topologies = [topo_0, topo_1, topo_2, topo_3, topo_4]

        for i, topo in enumerate(topologies):
            Cleanup.cleanup()
            net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
            net.start()
            try:
                test_cloud_fpga(net, None if i == 0 else i)
                self.assertEqual(True, True)
            except Exception as ex:
                self.assertEqual(True, False, 'test_cloud_fpga rose an Exception of type {}.'.format(type(ex).__name__))
            finally:
                Cleanup.cleanup()


class TestTestCloudFpgaHalveDelayPoisson(unittest.TestCase):
    """Test the test_cloud_fpga function with the halve_delay and the get_poisson_delay functions
    and the TreeTopoGeneric class"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=3, depth=4, bandwidth=10, delay='1ms', loss=0, fpga=2
                                 , poisson=True)
        topo_1 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=1, fpga=3
                                 , poisson=True)
        topo_2 = TreeTopoGeneric(spread=2, depth=6, bandwidth=1, delay='1ms', loss=0, fpga=5
                                 , poisson=True)
        topo_3 = TreeTopoGeneric(spread=5, depth=3, bandwidth=10, delay='10ms', loss=1, fpga=2
                                 , poisson=True)
        topo_4 = TreeTopoGeneric(spread=3, depth=5, bandwidth=10, delay='1ms', loss=0, fpga=3
                                 , poisson=True)

        topologies = [topo_0, topo_1, topo_2, topo_3, topo_4]

        for i, topo in enumerate(topologies):
            Cleanup.cleanup()
            net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
            net.start()
            try:
                test_cloud_fpga(net, None if i == 0 else i)
                self.assertEqual(True, True)
            except Exception as ex:
                self.assertEqual(True, False, 'test_cloud_fpga rose an Exception of type {}.'.format(type(ex).__name__))
            finally:
                Cleanup.cleanup()

if __name__ == '__main__':
    unittest.main()
