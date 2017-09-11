from __future__ import absolute_import, division, print_function
# "sudo pip install colorama" is required to download the Py2 package.
# "sudo pip3 install colorama" is required to download the Py3 package.
from colorama import init, Fore, Style


# Getpass function asks for password but doesn't show it in screen.
from getpass import getpass


# Custom function to get input that is compatible with Py2 & 3.
def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line


# Prompts for, and returns a username and password.
def get_credentials():
    print(Fore.YELLOW + '='*79 + Style.RESET_ALL)
    username = get_input('Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype password: ')
        if password != password_verify:
            print('>> Passwords do not match. Try again. ')
            password = None
        return username, password
