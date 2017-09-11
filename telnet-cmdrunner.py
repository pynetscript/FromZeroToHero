#!/usr/bin/python


from __future__ import absolute_import, division, print_function
# "sudo pip install colorama" is required to download the Python2 package.
# "sudo pip3 install colorama" is required to download the PYthon3 package.
from colorama import init, Fore, Style


import netmiko  # "sudo pip3 install netmiko" required for Python3.
import json
import tools
import sys      # Capture and handle signals past from the Operating System.
import signal


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   # KeyboardInterrupt: Ctrl-C


# If authentication fails, the script will continue to run.
# If connection times out, the script will continue to run.
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)


username, password = tools.get_credentials()


with open('cisco_ios_telnet_devices.json') as dev_file:
    cisco_ios_telnet_devices = json.load(dev_file)


domain_name = ['ip domain-name a-corp.com']

crypto_key_gen = ['crypto key generate rsa label SSH mod 2048']

ssh_commands = ['ip ssh rsa keypair-name SSH',
                'ip ssh version 2',
                'line vty 0 4',
                'transport input ssh telnet']


for device in cisco_ios_telnet_devices:
    device['username'] = username
    device['password'] = password
    try:
        print(Fore.YELLOW + '='*79 + Style.RESET_ALL)
        print('Connecting to device:', device['ip'])
        print('-'*79)
        # Establish session to each device in "cisco_ios_telnet_devices.json"
        # ** is used to unpack the dictonary for Netmiko
        connection = netmiko.ConnectHandler(**device)
        print(connection.send_config_set(domain_name))
        print('-'*79)
        print(connection.send_config_set(crypto_key_gen, delay_factor=10))
        print('-'*79)
        print(connection.send_config_set(ssh_commands))
        print('-'*79)
        output = connection.send_command_timing('write memory')
        print(output)
        if 'Overwrite the previous NVRAM configuration?[confirm]' in output:
            output = connection.send_command_timing('')

        # Disconnect sessions.
        connection.disconnect()


    except netmiko_exceptions as e:
        print('Failed to:', device['ip'])
        print(e)
