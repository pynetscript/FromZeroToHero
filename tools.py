from __future__ import absolute_import, division, print_function


### Getpass function asks for password but doesn't show it in screen.
from getpass import getpass


### Custom function to get input that is compatible with Python 2 and 3.
def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line


### Prompts for, and returns a username and password.
def get_credentials():
    print('='*79)
    username = get_input('Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype password: ')
        if password != password_verify:
            print('>> Passwords do not match. Try again. ')
            password = None
        return username, password
