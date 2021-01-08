#!/usr/bin/env python
from getpass import getpass


# prompt user to enter credentials & masks the password
def get_credentials():
    username = input('Enter Username: ')
    password = getpass()
    return username, password
