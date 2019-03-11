#!/usr/bin/python

"""
Simple example of setting network and CPU parameters

NOTE: link params limit BW, add latency, and loss.
There is a high chance that pings WILL fail and that
iperf will hang indefinitely if the TCP handshake fails
to complete.
"""

import json
import logging
import logging.config
import os
import re

import click
from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.util import dumpNodeConnections


# from sys import argv


class TreeTopoGeneric(Topo):
    """"Generic Tree topology."""

    def __init__(self, spread, depth, bandwidth, delay, loss, fpga, fpga_bandwidth, fpga_delay, fpga_loss):
        """"Create tree topology according to given parameters."""
        logger = logging.getLogger(__name__)

        # Initialize topology #
        Topo.__init__(self)

        # Setup parameters
        fpga_bandwidth = bandwidth if fpga_bandwidth is None else fpga_bandwidth
        fpga_delay = delay if fpga_delay is None else halve_delay(fpga_delay)
        fpga_loss = loss * 2 if fpga_loss is None else fpga_loss

        link_opts = dict(bw=bandwidth, delay=delay, loss=loss, use_htb=True)
        fpga_link_opts = dict(bw=fpga_bandwidth, delay=fpga_delay, loss=fpga_loss, use_htb=True)
        cloud_link_opts = dict(bw=1000, delay='0ms', loss=0, use_htb=True)

        # Add hosts and switches #

        # switch naming convention:
        #   s[level][switch_number]

        switches = [[None for _ in range(spread ** (depth - 1))] for _ in range(depth - 1)]
        hosts = [None for _ in range(spread ** (depth - 1))]

        for i in range(depth):
            for j in range(spread ** i):
                if i == (depth - 1):
                    hosts[j] = self.addHost('h' + str(j))
                else:
                    sw_name = 's' + str(i) + str(j)
                    switches[i][j] = self.addSwitch(sw_name)
                    if fpga is not None and fpga == i:
                        # Create host to serve as FPGA in switch
                        # Will have one link to the relevant FPGA
                        # The link will have the bandwidth and loss specified by the user, and half the delay
                        # These parameters are as if they were caused by the FPGA, rather than a link
                        # As a result, latency is halved since it will essentially be doubled by the packet flowing in
                        # and out of the host
                        self.addHost('f{}'.format(j))
                        self.addLink(sw_name, 'f{}'.format(j), **fpga_link_opts)

        # Add host to serve as cloud
        # Will have one high bandwidth, 0 latency link to root switch
        self.addHost('cloud')
        self.addLink(switches[0][0], 'cloud', **cloud_link_opts)

        # Add links #

        for i, row in enumerate(switches):
            for j, switch in enumerate(row):
                if switch is None:
                    break
                if i == (depth - 2):
                    for k in range(spread):
                        # add a link between the current switch, and all hosts
                        # directly beneath it.
                        # (spread * j) + k will get all the appropriate hosts
                        logger.debug("Adding standard link from switch[{}][{}] to "
                                     "host[{}]".format(i, j, (spread * j) + k))
                        self.addLink(switch, hosts[(spread * j) + k], **link_opts)

                else:
                    for k in range(spread):
                        # add a link between the current switch, and all
                        # switches directly beneath it.
                        # i + 1 refers to 1 level deeper in the tree, and
                        # (spread * j) + k will get all the appropriate child
                        # switches on that level.
                        logger.debug("Adding standard link from switch[{}][{}] to "
                                     "switch[{}][{}]".format(i, j, i + 1, (spread * j) + k))
                        self.addLink(switch, switches[i + 1][(spread * j) + k], **link_opts)


def halve_delay(delay):
    valid_time = re.compile('^([-+]?[0-9]*\.?[0-9]+)([PTGMkmunpf]?s)$')
    match = valid_time.match(delay)
    half = float(match.group(1)) / 2
    return "{}{}".format(half, match.group(2))


def setup_logging(
        default_path='logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration"""
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
    valid_time = re.compile('^([-+]?[0-9]*\.?[0-9]+)([PTGMkmunpf]?s)$')
    # This will allow any valid time, such as '10ms', '2.3s', '1Gs', etc.
    # Naturally 1Ps is both an absurd unit and not a very useful delay, but it is technically valid.
    if not valid_time.match(str(value)):
        raise click.BadParameter("delay must be in the format <time><unit>s. E.g. '10ms', '23s', '200ns'.")

    return str(value)


def validate_fpga_delay(ctx, param, value):
    return None if value is None else validate_delay(ctx, param, value)


@click.command()
@click.option('-s', '--spread', type=click.IntRange(min=1), default=2, show_default=True,
              help='Number of children each node will have.')
@click.option('-d', '--depth', type=click.IntRange(min=1), default=4, show_default=True,
              help='Number of levels in the tree.')
@click.option('-b', '--bandwidth', type=click.IntRange(min=0), default=10, show_default=True,
              help='Max bandwidth of all links in Mbps.')
@click.option('-e', '--delay', type=str, default='1ms', show_default=True, callback=validate_delay,
              help='Delay of all links.')
@click.option('-l', '--loss', default=0, show_default=True, type=click.IntRange(0, 100),
              help='% chance of packet loss for all links.')
@click.option('-f', '--fpga', type=click.IntRange(min=0),
              help='Level of the tree which should be modelled as FPGA switches (root is 0).')
@click.option('--fpga-bandwidth', type=click.IntRange(min=0), help='Max bandwidth of FPGA switch links in Mbps. ' +
                                                                   'Defaults to bandwidth of all links if unset.')
@click.option('--fpga-delay', type=str, callback=validate_fpga_delay, help='Delay of FPGA switch links. ' +
                                                                           'Defaults to delay of all links if unset.')
@click.option('--fpga-loss', type=click.IntRange(0, 100), help='% chance of packet loss for FPGA switch links.' +
                                                               'Defaults to 2 * loss of all links if unset.')
@click.option('-p', '--ping-all', is_flag=True, help='Run a ping test between all hosts.')
@click.option('-i', '--iperf', is_flag=True, help='Test bandwidth between first and last host.')
@click.option('-q', '--quick', is_flag=True, help='For testing purposes.')
@click.option('--log', default='info', show_default=True,
              type=click.Choice(['debug', 'info', 'output', 'warning', 'error', 'critical']), help='Set the log level.')
def performance_test(spread,
                     depth,
                     bandwidth,
                     delay,
                     loss,
                     fpga,
                     fpga_bandwidth,
                     fpga_delay,
                     fpga_loss,
                     ping_all,
                     iperf,
                     quick,
                     log
                     ):
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
    topo = TreeTopoGeneric(spread, depth, bandwidth, delay, loss, fpga, fpga_bandwidth, fpga_delay, fpga_loss)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
    net.start()
    logger.info("Dumping host connections")
    dumpNodeConnections(net.hosts)

    number_of_hosts = 0
    for node in net.keys():
        if node[0] == 'h':
            number_of_hosts += 1

    if ping_all:
        if number_of_hosts > 1:
            logger.info("Running ping test between all hosts")
            net.pingAll()
        else:
            logger.warning(str(number_of_hosts) + " host(s). Unable to run ping test.")

    if iperf:
        if number_of_hosts > 1:
            logger.info("Testing bandwidth between first and last hosts")
            net.iperf()
        else:
            logger.warning(str(number_of_hosts) + " host(s). Unable to run bandwidth test.")

    net.stop()


if __name__ == '__main__':
    performance_test()
