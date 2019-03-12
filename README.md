# FPGA Switch Model

This is a Python application for modelling networking topologies containing some FPGA-based switches which will perform 
compute.

These switches will not be able to perform as fast as the cloud servers they are stepping in for, however they prevent
packets from needing to be sent all the way into datacenters.

This application can be used to model the performance of networks containing these switches.


## Usage 
Requires root.

`fpga_switch_model.py [OPTIONS]`

Options:

| Short Tag | Long Tag | Default | Description | 
|---|---|---|---
| -s | --spread | 2 | Number of children each node will have. | 
| -d | --depth | 4 | Number of levels in the tree. |
| -b | --bandwidth | 10 | Max bandwidth of all links in Mbps. |
| -e | --delay | '1ms' | Delay of all links. |
| -l | --loss | 0 | Percentage chance of packet loss for all links. |
| -f | --fpga | | Level of the tree which should be modelled as FPGA switches (root is 0). |
| | --fpga-bandwidth | <--bandwidth value> | Max bandwidth of FPGA switches in Mbps. Defaults to bandwidth of all links if unset. |
| | --fpga-delay | <--delay value * 2> | Delay of FPGA switches. Defaults to 2 * delay of all links if unset.|
| | --fpga-loss | <--loss value * 2> | Percentage chance of packet loss for FPGA switches. Defaults to 2 * loss of all links if unset.|
| -p | --ping-all | | Run a ping test between all hosts. |
| -i | --iperf | | Test bandwidth between first and last host. |
| -c | --cloud-fpga | True | Test performance between leaf and root or leaf and FPGA switch. |
| | --dump-node-connections | | Dump all node connections before running tests. |
| | --poisson | | Use a poisson distribution for link delay. |
| | --log | 'info' | Set the log level. |
| | --help | | Show this message and exit. |
