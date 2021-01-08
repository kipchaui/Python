#!/usr/bin/env python
from netmiko import ConnectHandler
import sys

# Defines the command you must run, otherwise code exits
if len(sys.argv) < 2:
    print('Usage: JuniperConfigSingleDevice.py Juniper5.txt ')
    exit()

# Load  commands from RouterXX.txt file
with open(sys.argv[1]) as cli_file:
    Juniper5 = cli_file.readlines()

# Device details
router = {"device_type": "juniper", "host": "192.168.216.10", "username": "evans.kipchaui", "password": "evans.123"}

# Login to the each router using provided credentials
print('~' * 79)
print('Connecting to ', router['host'])
net_connect = ConnectHandler(**router)

# Executes each commands on txt file
for command in Juniper5:
    output = (net_connect.send_config_set(command, exit_config_mode=False))
    print(output)

# Asks user to confirm commit of the changes
output = input('Are you sure you want to commit?: Y/N   ', )
if output in ['Y', 'y', 'Yes', 'yes']:
    # Commit config
    output = net_connect.commit()
    print(output)
else:
    # Rolls back the changes and exit config mode
    rollback = ['rollback']
    output = (net_connect.send_config_set(rollback, exit_config_mode=True))
    print(output)
