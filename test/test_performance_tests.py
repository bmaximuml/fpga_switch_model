#!/usr/bin/env python

import unittest
from mininet_functions import TreeTopoGeneric
from performance_tests import test_cloud_fpga
from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.topolib import TreeTopo

class TestTestCloudFpga(unittest.TestCase):
    """Test the test_cloud_fpga function"""
    def test_simple(self):
        topo_0 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=None)
        topo_1 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=1)
        topo_2 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=2)
        topo_3 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=3)
        topo_4 = TreeTopoGeneric(spread=2, depth=7, bandwidth=10, delay='1ms', loss=0, fpga=4)

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
