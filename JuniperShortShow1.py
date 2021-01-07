#!/usr/bin/env python
from netmiko import ConnectHandler
import credentials

# Router details
router = {"device_type": "juniper", "host": "172.16.0.184", "username": "evansk", "password": "wiocc1234"}

# Router Credentials from user
username, password = credentials.get_credentials()
router['username'] = username
router['password'] = password

# Login to the router using provided credentials
net_connect = ConnectHandler(**router)

# Create a txt file and open
filename = 'show_bgp_summary.txt'
with open(filename, 'w') as output_file:
    # Print tilde 39 times, then print the hostname then print tilde another 39 times
    output_file.write('~' * 39 + net_connect.base_prompt + '~' * 39 + '\n\n')

    # Runs the command provided and store output on the created file
    output_file.write('## Output of: ' 'show bgp summary | grep 37000' '\n')
    output_file.write(net_connect.send_command('show bgp summary | grep 37000') + '\n')
