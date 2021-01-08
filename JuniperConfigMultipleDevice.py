#!/usr/bin/env python
from netmiko import ConnectHandler
import sys

# Defines the command you must run, otherwise code exits
if len(sys.argv) < 2:
    print('Usage: JuniperConfigMultipleDevice.py configBGP.txt ')
    exit()

# Load  commands from configBGP.txt file
with open(sys.argv[1]) as cli_file:
    configBGP = cli_file.readlines()

# Device details
device = ['172.16.0.188', '172.16.0.187', '172.16.0.186', '172.16.0.185', '172.16.0.184']
device_type = 'juniper'
username = 'evansk'
password = 'wiocc1234'

# Login to each router using provided credentials
for device in device:
    print('~' * 79)
    print('Connecting to ', device)
    net_connect = ConnectHandler(host=device, device_type=device_type, username=username, password=password)

    # Runs every line on the txt file
    for command in configBGP:
        output = (net_connect.send_config_set(command, exit_config_mode=False))
        print(output)
    # Commit config
    output = net_connect.commit()
    print(output)
