# FPGA Switch Model

This is a Python application for modelling networking topologies containing some FPGA-based switches which will perform 
compute.

These switches will not be able to perform as fast as the cloud servers they are stepping in for, however they prevent
packets from needing to be sent all the way into datacenters.

This application can be used to model the performance of networks containing these switches.

## Installation

The application is currently only supported on Ubuntu 16.04 LTS, since this is the only version of Ubuntu which a stable release of mininet is supported on. Once mininet 2.2.3 is release, Ubuntu 18.04 LTS will also be supported.

To install the application you will first need to install git (to clone the repository) and python (to run the application).
1. `sudo apt install git python-pip` Install git and python
2. `git clone --recursive https://github.com/benjilev08/fpga_switch_model` Clone the repository
3. `cd fpga_switch_model` Enter the clone directory
4. `sudo -H pip install .` Install the application and its dependencies. This must be run as root in order to correctly install mininet.
5. Run the application as shown below

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
| | --fpga-bandwidth | 504 | Max bandwidth of FPGA switches in Mbps. Defaults to max bandwidth of PCIe. |
| | --fpga-delay | <--delay value * 2> | Delay of FPGA switches. Defaults to 2 * delay of all links if unset.|
| | --fpga-loss | <--loss value * 2> | Percentage chance of packet loss for FPGA switches. Defaults to 2 * loss of all links if unset.|
| -p | --ping-all | | Run a ping test between all hosts. |
| -i | --iperf | | Test bandwidth between first and last host. |
| -c | --cloud-fpga | True | Test performance between leaf and root or leaf and FPGA switch. |
| | --dump-node-connections | | Dump all node connections before running tests. |
| | --poisson | | Use a poisson distribution for link delay. |
| | --log | 'info' | Set the log level. |
| | --help | | Show this message and exit. |
