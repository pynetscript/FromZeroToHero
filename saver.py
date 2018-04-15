#!/usr/bin/python

###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        06/04/2018
# Last modified date:   15/04/2018
# Version:              v1.1
#
# Script use:           Telnet into Cisco IOS devices and configure SSH.
#                       Note: Supports both IPv4 and IPv6 addresses and FQDNs
#                             Both Py2 and Py3 compatible
#                       The script needs 2 arguments to work:
#                       - 1st argument: saver.py
#                       - 2nd argument: /x.json
#                       Valid command looks like:
#                       ./saver.py ssh/router/7200.json
#
# Script input:         Username/Password
#                       Specify devices as a .json file
#                       Note: See "ssh/router/7200.json" as an example
#
# Script output:        Cisco IOS command output
#                       Errors in screen
#                       Progress bar
#                       Statistics
#                       Log erros in saver.log
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
from multiprocessing import Process, Queue

# Local modules
import tools


# Logs on the working directory on the file named saver.log
logger = logging.getLogger('__name__')
hdlr = logging.FileHandler('saver.log')
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


def processor(device, output_q):
    device['username'] = username
    device['password'] = password
    try:
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(current_time, '- Connecting to device:', device['ip'])

        output_dict = {}

        # SSH into each device from "x.json" (2nd argument).
        connection = netmiko.ConnectHandler(**device)

        print()
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(current_time, '- Successfully connected -', device['ip'])

        # Get device's "hostname" from netmiko, and "ip" from .json
        hostname = connection.base_prompt
        ip = (device['ip'])

        # Save running-config to startup-config.
        # Put into "output". 
        save_conf = connection.send_command_timing('write memory')
        if 'Overwrite the previous NVRAM configuration?[confirm]' in save_conf:
            save_conf = connection.send_command_timing('')
        if 'Destination filename [startup-config]' in save_conf:
            save_conf = connection.send_command_timing('')

        output = ('') + "\n"
        output += (save_conf)

        # Put everything from "output" into "output_dict".
        output_dict[Fore.WHITE + '='*79 + Style.RESET_ALL + '\n' + '[{0}] [{1}] >> write memory'.format(hostname, ip)] = output

        # Put "output_dict" into queue named "output_q".
        output_q.put(output_dict)

        # Disconnect SSH session.
        connection.disconnect()


    except netmiko_ex_auth as ex_auth:
        print()
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(Fore.RED + current_time, '- Authentication error -', device['ip'] + Style.RESET_ALL)
        # Log the error on the working directory in cmdrunner.log
        logger.warning(ex_auth)
        print()

    except netmiko_ex_time as ex_time:
        print()
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(Fore.RED + current_time, '- TCP/22 connectivity error -', device['ip'] + Style.RESET_ALL)
        # Log the error on the working directory in cmdrunner.log
        logger.warning(ex_time)
        print()


def main():
    # Script start timestamp and formatting
    start_timestamp = datetime.datetime.now()
    start_time = start_timestamp.strftime('%d/%m/%Y %H:%M:%S')
    
    # Queue used in line 121.
    output_q = Queue(maxsize=40)

    # Use processes and run the "processor" function. 
    procs = []
    for device in devices:
        my_proc = Process(target=processor, args=(device, output_q))
        my_proc.start()
        procs.append(my_proc)

    # Make sure all processes have finished
    for a_proc in procs:
        a_proc.join()

    # Use a queue to pass the output back to the parent process.
    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.items():
            print(k)
            print(val)


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


if __name__ == "__main__":
    main()
