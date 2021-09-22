#!/usr/bin/env python
import os
import shutil

dir = 'backup_config'
for file in os.listdir(dir):
    dir_name = file[:10]
    dir_path = dir + '/' + dir_name
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if os.path.exists(dir_path):
        shutil.move(dir +'/'+ file, dir_path)
