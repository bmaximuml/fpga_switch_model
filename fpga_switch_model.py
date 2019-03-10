#!/usr/bin/python

"""
Simple example of setting network and CPU parameters

NOTE: link params limit BW, add latency, and loss.
There is a high chance that pings WILL fail and that
iperf will hang indefinitely if the TCP handshake fails
to complete.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.clean import Cleanup

import os
import re
import json
import click
import logging
import logging.config

# from sys import argv

class TreeTopoGeneric(Topo):
    """"Generic Tree topology."""

    def __init__(self, spread, depth, bandwidth, delay, loss):
        """"Create tree topology according to given parameters."""

        ### Initialize topology ###
        Topo.__init__(self)

        # 10 Mbps bandwidth, 20 ms delay, 1% packet loss on each link
        linkopts = dict(bw=bandwidth, delay=delay, loss=loss, use_htb=True)

        ### Add hosts and switches ###

        # switch naming convention:
        #   s[level][switch_number]


        switches = [[None for x in range(spread ** depth)] for y in range(depth - 1)]
        hosts = [None for x in range(spread ** depth)]

        for i in range(depth):
            for j in range(spread ** i):
                if i == (depth - 1):
                    hosts[j] = self.addHost('h' + str(j))
                else:
                    sw_name = 's' + str(i) + str(j)
                    switches[i][j] = self.addSwitch(sw_name)

        ### Add links ###

        for i, row in enumerate(switches):
            for j, switch in enumerate(row):
                if switch is None:
                    break;
                if i == (depth - 2):
                    for k in range(spread):
                        # add a link between the current switch, and all hosts
                        # directly beneath it.
                        # (spread * j) + k will get all the appropriate hosts
                        self.addLink(switch, hosts[(spread * j) + k], **linkopts)

                else:
                    for k in range(spread):
                        # add a link between the current switch, and all
                        # switches directly beneath it.
                        # i + 1 refers to 1 level deeper in the tree, and
                        # (spread * j) + k will get all the appropriate child
                        # switches on that level.
                        self.addLink(switch, switches[i + 1][(spread * j) + k], **linkopts)


def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def validate_delay(ctx, param, value):
    valid_time = re.compile("^[0-9]+[PTGMkmunpf]?s$")
    # This will allow any valid time, such as '10ms', '23s', '1Gs', etc.
    # Naturally 1 Ps is both an absurd unit and not a very useful delay, but it should technically be valid.
    if not valid_time.match(value):
        raise click.BadParameter("delay must be in the format <time><unit>s. E.g. '10ms', '23s', '200ns'.")


@click.command()
@click.option('-s', '--spread', default=3, show_default=True, help='Number of children each node will have')
@click.option('-d', '--depth', default=4, show_default=True, help='Number of levels in the tree')
@click.option('-b', '--bandwidth', default=10, show_default=True, help='Max bandwidth of all links in Mbps')
@click.option('-e', '--delay', default='1ms', show_default=True, help='delay of all links',
              callback=validate_delay)
@click.option('-l', '--loss', default=0, show_default=True, help='% chance of packet loss for all links')

@click.option('-p', '--ping_all', is_flag=True, help='Run a ping test between all hosts')
@click.option('-i', '--iperf', is_flag=True, help='Test bandwidth between first and last host')

@click.option('-q', '--quick', is_flag=True, help='For testing purposes')

@click.option('--log', default='info', show_default=True,
              type=click.Choice(['debug', 'info', 'output', 'warning', 'error', 'critical']), help='Set the log level')
def performance_test(spread, depth, bandwidth, delay, loss, ping_all, iperf, quick, log):
    if quick:
        spread = 3
        depth = 3
        bandwidth = 500
        delay = '0ms'
        loss = 0
        ping_all = True
        iperf = True
        log = 'info'


    Cleanup.cleanup()
    setLogLevel(log)
    logger = logging.getLogger(__name__)

    if log == 'debug':
        logger.setLevel(logging.DEBUG)
        setup_logging(default_level=logging.DEBUG)
    elif log == 'warning':
        logger.setLevel(logging.WARNING)
        setup_logging(default_level=logging.WARNING)
    elif log == 'error':
        logger.setLevel(logging.ERROR)
        setup_logging(default_level=logging.ERROR)
    elif log == 'critical':
        logger.setLevel(logging.CRITICAL)
        setup_logging(default_level=logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)
        setup_logging(default_level=logging.INFO)



    "Create network and run simple performance test"
    topo = TreeTopoGeneric(spread, depth, bandwidth, delay, loss)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
    net.start()
    logger.info("Dumping host connections")
    dumpNodeConnections(net.hosts)

    if ping_all:
        logger.info("Running ping test between all hosts")
        net.pingAll()

    if iperf:
        logger.info("Testing bandwidth between first and last hosts")
        net.iperf()
        
    net.stop()

if __name__ == '__main__':
    performance_test()
