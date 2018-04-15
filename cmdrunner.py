#!/usr/bin/python

###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        09/09/2017
# Last modified date:   15/04/2018
# Version:              v1.2
#
# Script use:           Telnet into Cisco IOS devices and configure SSH.
#                       Note: Supports both IPv4 and IPv6 addresses and FQDNs
#                             Both Py2 and Py3 compatible
#                       The script needs 2 arguments to work:
#                       - 1st argument: cmdrunner.py
#                       - 2nd argument: /x.json
#                       Valid command looks like:
#                       ./cmdrunner.py telnet/router/7200.json
#
# Script input:         Username/Password
#                       Specify devices as a .json file
#                       Note: See "telnet/router/7200.json" as an example
#                       Prompt: "Enter domain name (example.com):"
#                       Prompt: "Enter SSH key size (1024, 2048, 4096):"
#                       Prompt: "Disable telnet (yes/no)?"
#
# Script output:        Cisco IOS command output
#                       Errors in screen
#                       Progress bar
#                       Statistics
#                       Log erros in cmdrunner.log
#                       Travis CI build notification to Slack private channel
###############################################################################


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from colorama import init
from colorama import Fore
from colorama import Style
from progressbar import *

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


# Logs on the working directory on the file named cmdrunner.log
logger = logging.getLogger('__name__')
hdlr = logging.FileHandler('cmdrunner.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   # KeyboardInterrupt: Ctrl-C


# If connection times out, the script will continue to run.
# If authentication fails, the script will continue to run.
netmiko_ex_time = (netmiko.ssh_exception.NetMikoTimeoutException, socket.error)
netmiko_ex_auth = (netmiko.ssh_exception.NetMikoAuthenticationException)


# If arguments not equal to 2 we get an error.
if len(sys.argv) != 2:
    print('>> Usage: cmdrunner.py /x.json')
    exit()


with open(sys.argv[1]) as dev_file:
    devices = json.load(dev_file)

    
# Prompt for username and password
username, password = tools.get_credentials()


# Prompt for domain name
print(Fore.WHITE + '='*79 + Style.RESET_ALL)
get_domain_name = tools.get_input('Enter domain name (example.com): ')
domain_name = ('ip domain-name ' + get_domain_name)

# Prompt for SSH key size
get_keygen = tools.get_input('Enter SSH key size (1024, 2048, 4096): ')
keygen = ('crypto key generate rsa label SSH mod ' + get_keygen)

ssh = ['ip ssh rsa keypair-name SSH',
       'ip ssh version 2']

# Prompt for disable telnet
disable_telnet = []
get_telnet = tools.get_input('Disable telnet (yes/no)? ')
if 'yes' in get_telnet:
    disable_telnet = ['line vty 0 4', 
                      'transport input ssh']
else:
    pass


# Script start timestamp and formatting
start_timestamp = datetime.datetime.now()
start_time = start_timestamp.strftime('%d/%m/%Y %H:%M:%S')


# Progress Bar
widgets = ['\n',
           Percentage(), ' ', Bar(marker='#', left='[', right=']'),
           ' ', '[',SimpleProgress(),']',' ' '[', ETA(),']', '\n']

pbar = ProgressBar(widgets=widgets)


for device in pbar(devices):
    device['username'] = username
    device['password'] = password
    try:
        print(Fore.WHITE + '='*79 + Style.RESET_ALL)
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(current_time, '- Connecting to device:', device['ip'])

        # SSH into each device from "x.json" (2nd argument).
        connection = netmiko.ConnectHandler(**device)

        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(current_time, '- Successfully connected -', device['ip'])
        print('-'*79)

        # Get device's "hostname" from netmiko, and "ip" from .json
        hostname = connection.base_prompt
        ip = (device['ip'])

        # Configure domain-name.
        print('[{0}] [{1}] >> {2}'.format(hostname, ip, domain_name) + '\n')
        print(connection.send_config_set(domain_name))
        print('-'*79)

        # Generate SSH keys (add some delay).
        print('[{0}] [{1}] >> {2}'.format(hostname, ip, keygen) + '\n')   
        print(connection.send_config_set(keygen, delay_factor=10))
        print('-'*79)

        # If "disable_telnet" list empty (we chose "no") skip it.
        # If "disable_telnet" list not empty (we chose "yes") disable telnet.
        if not disable_telnet:
            pass
        else:
            for cmd in disable_telnet:
                print('[{0}] [{1}] >> '.format(hostname, ip) + cmd)
            print()
            print(connection.send_config_set(disable_telnet))
        
        # Disconnect SSH session.
        connection.disconnect()


    except netmiko_ex_auth as ex_auth:
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(Fore.RED + current_time, '- Authentication error -', device['ip'] + Style.RESET_ALL)
        # Log the error on the working directory in cmdrunner.log
        logger.warning(ex_auth)

    except netmiko_ex_time as ex_time:
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(Fore.RED + current_time, '- TCP/23 connectivity error -', device['ip'] + Style.RESET_ALL)
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
