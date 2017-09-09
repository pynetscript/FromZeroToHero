#!/usr/bin/python


from __future__ import absolute_import, division, print_function

import netmiko
import json
import tools
import sys      ### Capture and handle signals past from the Operating System.
import signal


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  ### IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   ### KeyboardInterrupt: Ctrl-C


### If authentication fails, the script will continue to run.
### If connection times out, the script will continue to run.
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)


username, password = tools.get_credentials()


with open('cisco_ios_telnet_devices.json') as dev_file:
    cisco_ios_telnet_devices = json.load(dev_file)


domain_name = [ 'ip domain-name a-corp.com']

crypto_key_gen = [ 'crypto key generate rsa label SSH mod 2048']

ssh_commands = [ 'ip ssh rsa keypair-name SSH',
                 'ip ssh version 2',]


for device in cisco_ios_telnet_devices:
    device['username'] = username
    device['password'] = password
    try:
        print()
        print('='*79)
        print('Connecting to device:', device['ip'])
        print('-'*79)
        ### Establish session to each device in "cisco_ios_telnet_devices.json"
        ### ** is used to unpack the dictonary for Netmiko
        connection = netmiko.ConnectHandler(**device)

        print(connection.send_config_set(domain_name))
        print('-'*79)
        print(connection.send_config_set(crypto_key_gen, delay_factor=10))
        print('-'*79)
        print(connection.send_config_set(ssh_commands))
        print('-'*79)

        ### Disconnect sessions.
        connection.disconnect()

    except netmiko_exceptions as e:
        print('Failed to:', device['ip'])
        print(e)
