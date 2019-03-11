def test_cloud_fpga(net, fpga):
    """Test how long it takes a packet to travel between the leaf and the root (or FPGA switch).

    If the fpga flag is set, this will test how long it takes a packet to travel between the leaf
    and the first FPGA switch.
    If it is unset, this will test how long it takes a packet to travel between the leaf and the
    root.

    The tests are conducted using the ping protocol, which uses ICMP packets."""
    logger = logging.getLogger(__name__)
    h0 = net.get('h0')
    if fpga:
        logger.info('Testing performance between leaf (h0) and FPGA switch (f0)')
        f0 = net.get('f0')
        ping = h0.cmd('ping -c 10 {}'.format(f0.IP()))
    else:
        logger.info('Testing performance between leaf (h0) and cloud (cloud)')
        cloud = net.get('cloud')
        ping = h0.cmd('ping -c 10 {}'.format(cloud.IP()))

    rtt_results = re.compile('rtt.*')
    search = rtt_results.search(ping)
    rtt = search.group(0)
    logger.info('Ping results: %s', rtt)
