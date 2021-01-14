#!/usr/bin/env python
from netmiko import ConnectHandler
import sys
import json
import netmiko

# Defines Netmiko exceptions
netmiko_exceptions = (netmiko.ssh_exception.NetmikoTimeoutException,
                      netmiko.ssh_exception.NetmikoAuthenticationException)

# Defines the command you must run, otherwise code exits
if len(sys.argv) < 2:
    print('Usage: bgp.py routers.json')
    exit()

# Load routers from routers.json file
with open(sys.argv[1]) as dev_file:
    routers = json.load(dev_file)

# Create a txt file and open
filename = 'bgp.txt'
with open(filename, 'w') as output_file:
    # Work through each device
    for routers in routers:
        try:
            net_connect = ConnectHandler(**routers)
            # Print tilde 39 times, then print the hostname then print tilde another 39 times
            output_file.write('~' * 39 + net_connect.base_prompt + '~' * 39 + '\n\n')
            s = net_connect.send_command('show bgp summary | grep esta')

            for line in s.splitlines():
                try:
                    peer_ip = line.split()[0]
                    peer_as = line.split()[1]
                    output_file.write('Peer {} ASN {}'.format(peer_ip, peer_as) + (' Rejected Prefixes ' + net_connect.send_command('show route receive-protocol bgp {} | count | exc "iso|inet|mast"'.format(peer_ip))))
                except IndexError:
                    continue
        except netmiko_exceptions as e:
            output_file.write('~' * 37 + 'Failed to connect to: ' + '~' * 37 + '\n\n'.format(str(routers), str(e)))
        finally:
            pass
