#!/usr/bin/python

###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        09/09/2017
# Last modified date:   11/03/2018
# Github:               https://github.com/pynetscript/FromZeroToHero
#
# Script use:           Telnet into cisco_ios_telnet_devices.json and configure
#                       SSH. The script is both Python2/3 compatible.
#
# Script input:         Username/Password
#
# Script output:        Cisco IOS command output
#                       Statistics
#                       Errors in fromzerotohero.log
###############################################################################


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from colorama import init, Fore, Style


# Standard library modules
import netmiko
import json
import sys                      # Capture and handle signals past from the OS.
import signal
import datetime
import time
import logging
import socket

# Local modules
import tools


# Logs on the working directory on the file named fromzerotohero.log
logger = logging.getLogger('__name__')
hdlr = logging.FileHandler('fromzerotohero.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   # KeyboardInterrupt: Ctrl-C


netmiko_ex_time = (netmiko.ssh_exception.NetMikoTimeoutException, socket.error)
netmiko_ex_auth = (netmiko.ssh_exception.NetMikoAuthenticationException)


username, password = tools.get_credentials()


print(Fore.WHITE + '='*79 + Style.RESET_ALL)
start_time = datetime.datetime.today()
print("Script started:      ", start_time)


with open('cisco_ios_telnet_devices.json') as dev_file:
    cisco_ios_telnet_devices = json.load(dev_file)


# Enable SSH commands
domain_name = ['ip domain-name a-corp.com']

crypto_key_gen = ['crypto key generate rsa label SSH mod 2048']

ssh_commands = ['ip ssh rsa keypair-name SSH',
                'ip ssh version 2',
                'line vty 0 4',
                'transport input ssh telnet']

# Disable Telnet commands
disable_telnet = ['line vty 0 4',
                  'transport input ssh']


for device in cisco_ios_telnet_devices:
    device['username'] = username
    device['password'] = password
    try:
        print(Fore.WHITE + '='*79 + Style.RESET_ALL)
        print('Connecting to device:', device['ip'])
        print('-'*79)

        # Establish session to each device in "cisco_ios_telnet_devices.json"
        # ** is used to unpack the dictonary for Netmiko
        connection = netmiko.ConnectHandler(**device)

        # Enable SSH commands
        print(connection.send_config_set(domain_name))
        print('-'*79)
        print(connection.send_config_set(crypto_key_gen, delay_factor=10))
        print('-'*79)
        print(connection.send_config_set(ssh_commands))


        # Any needed cleanup before closing sessions.
        # Disconnect sessions.
        connection.cleanup()
        connection.disconnect()


        print(Fore.WHITE + '='*79 + Style.RESET_ALL)
        print('Connecting to device:', device['ip'])
        print('-'*79)

        connection = netmiko.ConnectHandler(**device)

        # Disable Telnet commands.
        print(connection.send_config_set(disable_telnet))
        print('-'*79)

        save_conf = connection.send_command_timing('write memory')
        print(save_conf)
        if 'Overwrite the previous NVRAM configuration?[confirm]' in save_conf:
            save_conf = connection.send_command_timing('')
        if 'Destination filename [startup-config]' in save_conf:
            save_conf = connection.send_command_timing('')

        connection.cleanup()
        connection.disconnect()


    except netmiko_ex_auth as ex_auth:
        print(Fore.RED + device['ip'], '>> Authentication error')
        # Log the error on the working directory @ fromzerotohero.log
        logger.warning(ex_auth)

    except netmiko_ex_time as ex_time:
        print(Fore.RED + device['ip'], '>> TCP/22 connectivity error')
        # Log the error on the working directory @ fromzerotohero.log
        logger.warning(ex_time)


end_time = datetime.datetime.today()
total_time = end_time - start_time


### SCRIPT STATISTICS
print(Fore.WHITE + '='*79 + Style.RESET_ALL)
print("+" + "-"*77 + "+")
print("|" + " "*30 + "SCRIPT STATISTICS" +       " "*30 + "|")
print("|" + "-"*77 + "|")
print("| Script started:          ", start_time, " "*23 + "|")
print("| Script ended:            ", end_time,   " "*23 + "|")
print("| Script duration (h/m/s): ", total_time, " "*35 + "|")
print("+" + "-"*77 + "+")
