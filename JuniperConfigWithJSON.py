#!/usr/bin/env python
from netmiko import ConnectHandler
import json
import credentials
import sys

# Defines the command you must run, otherwise code exits
if len(sys.argv) < 3:
    print('Usage: JuniperConfig.py configBGP.txt routers.json')
    exit()

# Get logins from credentials.py file
username, password = credentials.get_credentials()

# Load  commands from configBGP.txt file
with open(sys.argv[1]) as cli_file:
    configBGP = cli_file.readlines()

# Load routers from routers.json file
with open(sys.argv[2]) as dev_file:
    routers = json.load(dev_file)

# Login to each router using provided credentials
for routers in routers:
    routers['username'] = username
    routers['password'] = password
    print('~' * 79)
    print('Connecting to ', routers['host'])
    net_connect = ConnectHandler(**routers)
    # Executes each command on the txt file
    for command in configBGP:
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
