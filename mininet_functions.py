import logging

from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.topo import Topo


class TreeTopoGeneric(Topo):
    """"Generic Tree topology."""

    def __init__(self, spread, depth, bandwidth, delay, loss, fpga, fpga_bandwidth, fpga_delay,
                 fpga_loss, poisson):
        """"Create tree topology according to given parameters."""
        logger = logging.getLogger(__name__)

        # Initialize topology #
        Topo.__init__(self)

        # Setup parameters
        fpga_bandwidth = bandwidth if fpga_bandwidth is None else fpga_bandwidth
        fpga_delay = delay if fpga_delay is None else halve_delay(fpga_delay)
        fpga_loss = loss * 2 if fpga_loss is None else fpga_loss

        if poisson:
            link_opts = dict(bw=bandwidth, delay=get_poisson_delay(delay), loss=loss, use_htb=True)
            fpga_link_opts = dict(bw=fpga_bandwidth, delay=get_poisson_delay(fpga_delay),
                                  loss=fpga_loss, use_htb=True)
        else:
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
                        # The link will have the bandwidth and loss specified by the user, and half
                        # the delay
                        # These parameters are as if they were caused by the FPGA, rather than a
                        # link
                        # As a result, latency is halved since it will essentially be doubled by the
                        # packet flowing in
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


def setup_mininet(log, spread, depth, bandwidth, delay, loss, fpga, fpga_bandwidth, fpga_delay,
                  fpga_loss, poisson):
    """Run tasks to setup and start the mininet environment."""
    Cleanup.cleanup()

    setLogLevel(log)

    # Create network
    topo = TreeTopoGeneric(spread, depth, bandwidth, delay, loss, fpga, fpga_bandwidth, fpga_delay,
                           fpga_loss, poisson)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
    net.start()

    return net
