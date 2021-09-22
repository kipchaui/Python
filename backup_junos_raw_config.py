#!/usr/bin/env python
from netmiko import ConnectHandler
import datetime
import netmiko
import json
import os


with open('routers.json') as devices:
        r = json.load(devices)
        for router in r:
                try:
                        net_connect = ConnectHandler(**router)
                        filename = (str(datetime.date.today()) + '_' + net_connect.base_prompt).replace('admin@', '')
                        with open(os.path.join('/usr/local/bin/python/backup_config',filename), 'w') as r_conf:
                                r_conf.write(net_connect.send_command('show configuration | display set | no-more'))
                except Exception as e:
                        r_conf.write('Failed to connect to: ' + '\n\n'.format(str(router), str(e)))
                finally:
                        pass
