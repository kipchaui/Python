#!/usr/bin/env python
from netmiko import ConnectHandler
import json
import sys
import netmiko

# Defines Netmiko exceptions
netmiko_exceptions = (netmiko.ssh_exception.NetmikoTimeoutException,
                      netmiko.ssh_exception.NetmikoAuthenticationException)

# Defines the command you must run, otherwise code exits
if len(sys.argv) < 3:
    print('Usage: JuniperShowWithJSON1.py ShowCommands.txt routers.json')
    exit()

# Load  commands from ShowCommands.txt file
with open(sys.argv[1]) as cli_file:
    ShowCommands = cli_file.readlines()

# Load routers from routers.json file
with open(sys.argv[2]) as dev_file:
    routers = json.load(dev_file)

# Create a txt file and open
filename = 'show_bgp_summary_1.txt'
with open(filename, 'w') as output_file:
    # Login to each device with provided logins
    for routers in routers:
        try:
            net_connect = ConnectHandler(**routers)

            # Print tilde 39 times, then print the hostname then print tilde another 39 times
            output_file.write('~' * 39 + net_connect.base_prompt + '~' * 39 + '\n\n')

            # Runs every command on the txt file provided and store output on the created file
            for command in ShowCommands:
                output_file.write('## Output of: ' + command + '\n')
                output_file.write(net_connect.send_command(command) + '\n')
        except netmiko_exceptions as e:
            output_file.write('~' * 37 + 'Failed to connect to: ' + '~' * 37 + '\n\n'.format(str(routers), str(e)))
        finally:
            pass
