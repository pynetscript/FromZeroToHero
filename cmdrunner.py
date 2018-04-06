#!/usr/bin/python

###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        09/09/2017
# Last modified date:   06/04/2018
# Version:              v1.1
#
# Script use:           Tlnet into Cisco IOS devices and configure SSH.
#                       Note: Commands are send all at once (not one by one)
#                             Supports both IPv4 and IPv6 addresses and FQDNs
#                             Both Py2 and Py3 compatible
#                       The script needs 3 arguments to work:
#                       - 1st argument: cmdrunner.py
#                       - 2nd argument: /x.json
#                       - 3rd argument: /x.txt
#                       Note: A full command looks like:
#                       ./cmdrunner.py router/7200.json router/cmd.txt
#
# Script input:         SSH Username/Password
#                       Specify devices as a .json file
#                       Note: See "router/7200.json" as an example
#                       Specify SSH config commands as a .txt file
#                       Note: Show commands need "do" in the front
#                            See "router/cmd.txt" as an example
#
# Script output:        Cisco IOS command output
#                       Statistics
#                       Erros in cmdrunner.log
#                       Travis CI build notification to Slack private channel
###############################################################################


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from colorama import init
from colorama import Fore
from colorama import Style


# Standard library modules
import netmiko
import json
import sys                      
import signal                   # Capture and handle signals past from the OS.
import datetime
import time
import logging
import socket
import os

# Local modules
import tools


# Logs on the working directory on the file named fromzerotohero.log
logger = logging.getLogger('__name__')
hdlr = logging.FileHandler('cmdrunner.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   # KeyboardInterrupt: Ctrl-C


#netmiko_ex_time = (netmiko.ssh_exception.NetMikoTimeoutException, socket.error)
#netmiko_ex_auth = (netmiko.ssh_exception.NetMikoAuthenticationException)


# If connection times out, the script will continue to run.
# If authentication fails, the script will continue to run.
netmiko_ex_time = (netmiko.ssh_exception.NetMikoTimeoutException)
netmiko_ex_auth = (netmiko.ssh_exception.NetMikoAuthenticationException)


username, password = tools.get_credentials()


# If less than 3 arguments we get an error.
# If more than 3 arguments we get an error.
if len(sys.argv) < 3:
    print('>> Usage: cmdrunner.py /x.json /x.txt')
    exit()

if len(sys.argv) > 3:
    print('>> Usage: cmdrunner.py /x.json /x.txt')
    exit()


with open(sys.argv[1]) as dev_file:
    devices = json.load(dev_file)

with open(sys.argv[2]) as cmd_file:
commands = cmd_file.readlines()


# Script start timestamp and formatting
start_timestamp = datetime.datetime.now()
start_time = start_timestamp.strftime('%d/%m/%Y %H:%M:%S')


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


for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print(Fore.WHITE + '='*79 + Style.RESET_ALL)
        print('Connecting to device:', device['ip'])
        print('-'*79)

        # SSH into each device from "x.json" (2nd argument).
        connection = netmiko.ConnectHandler(**device)

        # Send each command from "x.txt" to device (3rd argument).
        for command in commands:
            print(Fore.RED + '>> ' + command + Style.RESET_ALL)
            print(connection.send_config_set(command))
            
            # If only whitespace in line do nothing and continue.
            if command in ['\n', '\r\n']:
                pass
            else:
                print(connection.send_config_set(command))
                print('-'*79)

        """
        # Enable SSH commands
        print(connection.send_config_set(domain_name))
        print('-'*79)
        print(connection.send_config_set(crypto_key_gen, delay_factor=10))
        print('-'*79)
        print(connection.send_config_set(ssh_commands))
        """

        # Any needed cleanup before closing sessions.
        #connection.cleanup()
        # Disconnect SSH session.
        connection.disconnect()

        # Connect again and disable Telnet.
        print(Fore.WHITE + '='*79 + Style.RESET_ALL)
        print('Connecting to device:', device['ip'])
        print('-'*79)

        connection = netmiko.ConnectHandler(**device)

        print(connection.send_config_set(disable_telnet))
        print('-'*79)

        # Save running-config to startup-config.
        save_conf = connection.send_command_timing('write memory')
        if 'Overwrite the previous NVRAM configuration?[confirm]' in save_conf:
            save_conf = connection.send_command_timing('')
        if 'Destination filename [startup-config]' in save_conf:
            save_conf = connection.send_command_timing('')
        print(Fore.RED + '>> write memory' + "\n" + Style.RESET_ALL)
        print(save_conf)

        #connection.cleanup()
        connection.disconnect()

    except netmiko_ex_auth as ex_auth:
        print(Fore.RED + device['ip'], '>> Authentication error')
        # Log the error on the working directory in cmdrunner.log
        logger.warning(ex_auth)

    except netmiko_ex_time as ex_time:
        print(Fore.RED + device['ip'], '>> TCP/22 connectivity error')
        # Log the error on the working directory in cmdrunner.log
        logger.warning(ex_time)


# Script end timestamp and formatting
end_timestamp = datetime.datetime.now()
end_time = end_timestamp.strftime('%d/%m/%Y %H:%M:%S')

# Script duration and formatting
total_time = end_timestamp - start_timestamp
total_time = str(total_time).split(".")[0]


# SCRIPT STATISTICS
print(Fore.WHITE + '='*79 + Style.RESET_ALL)
print("+" + "-"*77 + "+")
print("|" + " "*30 + "SCRIPT STATISTICS" +       " "*30 + "|")
print("|" + "-"*77 + "|")
print("| Script started:          ", start_time, " "*30 + "|")
print("| Script ended:            ", end_time,   " "*30 + "|")
print("| Script duration (h:m:s): ", total_time, " "*42 + "|")
print("+" + "-"*77 + "+")
