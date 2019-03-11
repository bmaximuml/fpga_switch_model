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
import numpy as np

import click

from performance_tests import test_cloud_fpga
try:
    from mininet_functions import setup_mininet
except ImportError:
    os.symlink("mn/mininet", "mininet")
    from mininet_functions import setup_mininet
from mininet.util import dumpNodeConnections


def get_poisson_delay(delay):
    """Returns a Poisson distributed delay of the given delay."""
    valid_time = re.compile('^([-+]?[0-9]*\.?[0-9]+)([PTGMkmunpf]?s)$')
    match = valid_time.match(delay)
    poisson = np.random.poisson(float(match.group(1)))
    return "{}{}".format(poisson, match.group(2))


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
@click.option('-c', '--cloud-fpga', type=bool, default=True, show_default=True,
              help='Test performance between leaf and root or leaf and FPGA switch')
@click.option('--dump-node-connections', is_flag=True, help='Dump all node connections.')
@click.option('--poisson', is_flag=True, help="Use a poisson distribution for link delay.")
@click.option('-q', '--quick', is_flag=True, help='For testing purposes.')
@click.option('--log', default='info', show_default=True,
              type=click.Choice(['debug', 'info', 'output', 'warning', 'error', 'critical']), help='Set the log level.')
def main(spread,
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
         dump_node_connections,
         poisson,
         quick,
         log,
         cloud_fpga
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

    net = setup_mininet(log, spread, depth, bandwidth, delay, loss, fpga, fpga_bandwidth,
                        fpga_delay, fpga_loss, poisson)
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

    if dump_node_connections:
        logger.info("Dumping host connections")
        dumpNodeConnections(net.hosts)

    number_of_hosts = 0
    for node in net.keys():
        if node[0] == 'h':
            number_of_hosts += 1

    if cloud_fpga:
        test_cloud_fpga(net, fpga)

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
    main()
