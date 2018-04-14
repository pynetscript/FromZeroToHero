[![Build Status](https://travis-ci.org/pynetscript/FromZeroToHero.svg?branch=master)](https://travis-ci.org/pynetscript/FromZeroToHero)
[![GitHub release](https://img.shields.io/badge/version-1.2-blue.svg)](https://github.com/pynetscript/FromZeroToHero)
[![license](https://img.shields.io/github/license/pynetscript/FromZeroToHero.svg)](https://github.com/pynetscript/FromZeroToHero/blob/master/LICENSE)

# FromZeroToHero

```
Written by:           Aleks Lambreca
Creation date:        09/09/2017
Last modified date:   14/04/2018
Version:              v1.2

Script use:           Telnet into Cisco IOS devices and configure SSH.
                      Note: Supports both IPv4 and IPv6 addresses and FQDNs
                            Both Py2 and Py3 compatible
                      The script needs 2 arguments to work:
                      - 1st argument: cmdrunner.py
                      - 2nd argument: /x.json
                      Valid command looks like:
                      ./cmdrunner.py telnet/router/7200.json

Script input:         SSH Username/Password
                      Specify devices as a .json file
                      Note: See "telnet/router/7200.json" as an example
                      Prompt: "Enter domain name (example.com):"
                      Prompt: "Enter SSH key size (1024, 2048, 4096):"
                      Prompt: "Disable telnet (yes/no)?"

Script output:        Cisco IOS command output
                      Errors in screen
                      Progress bar
                      Statistics                      
                      Log erros in cmdrunner.log
                      Travis CI build notification to Slack private channel
```


# Prerequisites

0. Box with latest version of [git](https://git-scm.com/) installed.
1. Box with [netmiko 2.1.0](https://github.com/ktbyers/netmiko) installed (included in requirements.txt).
2. Box with [colorama 0.3.9](https://pypi.python.org/pypi/colorama) installed (included in requirements.txt).
3. Telnet (TCP/23) reachability to devices.    
4. Local username with privilege 15 (example: `user a.lambreca priv 15 secret cisco`).
5. Alias command to save configuration: `alias exec wr copy run start`

# Installation

```
mkdir /FromZeroToHero/ && cd /FromZeroToHero/
sudo apt-get install -y git
git clone -b https://github.com/pynetscript/FromZeroToHero.git . 
pip install -r requirements.txt
```

# .travis.yml

- [Travis CI](https://travis-ci.org/pynetscript/FromZeroToHero)
- What language: **Python**
- What versions: **2.7** , **3.4** , **3.5** , **3.6**
- What to install: **pip install -r requirements.txt**
- What to run: **python cmdrunner.py**
- Where to send notifications: **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** 
  - Install Travis CI on [Slack](https://pynetscript.slack.com) and at some point it will output a slack channel to use.
  - Replace **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** with your own channel.
  - Supports private channels.


# tools.py


- tools.py is going to be imported on our main script (cmdrunner.py).
- This way we have a cleaner main script.
- Function (get_input)
    - Get input that is both Py2 and Py3 compatible
- Function (get_credentials) 
    - Prompts for username
    - Prompts for password twice but doesn't show it on screen (getpass)
        - If passwords match each other the script will continue to run
        - If password don't match each other you will get an error message `>> Passwords do not match. Try again. ` but the script will continue to run. Use Ctrl + C to cancel the script and run it again.


# 2nd argument (.json)

Create an csv file like this example:  

```CSV
device_type,ip
cisco_ios_telnet,r1.a-corp.com
cisco_ios_telnet,192.168.1.160
cisco_ios_telnet,2001:db8:acab:a001::170
```

- Go to [Mr. Data Converter](https://shancarter.github.io/mr-data-converter/).
- Copy/paste the CSV input into the **Input CSV or tab-delimited data**.
- On the bottom, in the **Output as** choose  **JSON - Properties**.
- On the left, in the **Delimiter** and in the **Decimal Sign** choose **Comma**.
- This is what you should get from the example above.

```
[{"device_type":"cisco_ios_telnet","ip":"r1.a-corp.com"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.160"},
{"device_type":"cisco_ios_telnet","ip":"2001:db8:acab:a001::170"}]
```

- Finally i copy/pasted the output into telnet/router/7200.json which is going to be used by cmdrunner.py as the <2nd_argument>.   


# 1st argument (cmdrunner.py)

This is the main script that we will run.   
Legal examples:   
- `python2 <1st_argument> <2nd_argument>`
- `python3 <1st_argument> <2nd_argument>`

Let's use the following example to explain the script:    
- `python3 cmdrunner.py telnet/router/7200.json`

First the script will:     
- Create a log file named "cmdrunner.log".
- Prompt us for a username and a password (password required twice).
- Prompt us for the domain name.
- Prompt us for the SSH key size.
- Prompt us to disable telnet or not.

```
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Enter domain name (example.com): a-corp.com
Enter SSH key size (1024, 2048, 4096): 2048
Disable telnet (yes/no)? yes
===============================================================================
```
  
Then the script will:   
- Timestamp the date & time the script started in D/M/Y H:M:S format. 
- Telnet to the first device in the <2nd_argument> (.json).
- Run the domain name command that it prompted us earlier. 
- Generate SSH keys    
  - I added a delay factor on this command because it takes a while to generate the SSH keys.  
- Run the commands to disable telnet.   
- Disconnect the SSH session.  

Errors:
- If the is an authentication error we will get an error message `r5.a-corp.com >> Authentication error`
- If the is an connectivity (TCP/23) error we will get an error message `192.168.1.160 >> TCP/23 connectivity error`
- Errors are logged in the cmdrunner.log

Finally the script will:
- Repeat the process for all devices in <2nd_argument> (.json) 
- Timestamp the date & time the script ended in D/M/Y H:M:S format.
- Subtract start timestamp and end timstamp to get the time (in H:M:S format) of how long the script took to run.
- Print SCRIPT STATISTICS

**Note**: The script doesn't save the running-config to the startup-config. To save it, run **saver.py**.

```
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           06/04/2018 21:38:46                               |
| Script ended:             06/04/2018 21:43:08                               |
| Script duration (h:m:s):  0:04:21                                           |
+-----------------------------------------------------------------------------+
```

# 1st argument (saver.py)

This is the script that we will run to save the configuration.   
Legal examples:   
- `python2 <1st_argument> <2nd_argument>`
- `python3 <1st_argument> <2nd_argument>`

Let's use the following example to explain the script:    
- `python3 saver.py ssh/router/7200.json`

First the script will:     
- Create a log file named "saver.log".
- Prompt us for a username and a password (password required twice).

```
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
```
  
Then the script will:    
- Run `main()` function:
  - Timestamp the date & time the script started in D/M/Y H:M:S format
  - Define a queue with size of 40
  - Use multiple processors and run the ` processor(device, output_q)` function: 
    - SSH to all the devices at once in the <2nd_argument> (.json)    
    - Get devices` hostname.
    - Get devices` "ip" from .json
    - Save the running-config to startup-config - put into variable "output". 
    - Put everything from variable "output" into "output_dict" in the format "[hostname] [IP]".
    - Put "output_dict" into queue named "output_q".
    - Disconnect the SSH sessions.  
    - Errors:
      - If the is an authentication error we will get an error message `r5.a-corp.com >> Authentication error`
      - If the is an connectivity (TCP/22) error we will get an error message `192.168.1.160 >> TCP/22 connectivity error`
      - Errors are logged in saver.log
  - Makes sure all processes have finished
  - Uses a queue to pass the output back to the parent process.
  - Timestamp the date & time the script ended in D/M/Y H:M:S format.
  - Subtract start timestamp and end timstamp to get the time (in H:M:S format) of how long the script took to run.
  - Print SCRIPT STATISTICS

```
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           06/04/2018 22:12:55                               |
| Script ended:             06/04/2018 22:13:09                               |
| Script duration (h:m:s):  0:00:13                                           |
+-----------------------------------------------------------------------------+
```
  
# Successful demo (cmdrunner.py)

```
aleks@acorp:~/FromZeroToHero$ python3 cmdrunner.py telnet/router/7200.json
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Enter domain name (example.com): a-corp.com
Enter SSH key size (1024, 2048, 4096): 2048
Disable telnet (yes/no)? yes
===============================================================================
Connecting to device: r5.a-corp.com
-------------------------------------------------------------------------------
[R5] [r5.a-corp.com] >> ip domain-name a-corp.com

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#ip domain-name a-corp.com
R5(config)#end
R5#
-------------------------------------------------------------------------------
[R5] [r5.a-corp.com] >> crypto key generate rsa label SSH mod 2048

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 13 seconds)

R5(config)#end
R5#
-------------------------------------------------------------------------------
[R5] [r5.a-corp.com] >> line vty 0 4
[R5] [r5.a-corp.com] >> transport input ssh

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#line vty 0 4
R5(config-line)#transport input ssh
R5(config-line)#end
R5#
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
[R6] [192.168.1.160] >> ip domain-name a-corp.com

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#ip domain-name a-corp.com
R6(config)#end
R6#
-------------------------------------------------------------------------------
[R6] [192.168.1.160] >> crypto key generate rsa label SSH mod 2048

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 11 seconds)

R6(config)#end
R6#
-------------------------------------------------------------------------------
[R6] [192.168.1.160] >> line vty 0 4
[R6] [192.168.1.160] >> transport input ssh

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#line vty 0 4
R6(config-line)#transport input ssh
R6(config-line)#end
R6#
===============================================================================
Connecting to device: 2001:db8:acab:a001::170
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170] >> ip domain-name a-corp.com

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip domain-name a-corp.com
R7(config)#end
R7#
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170] >> crypto key generate rsa label SSH mod 2048

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#crypto key generate rsa label SSH mod 2048
The name for the keys will be: SSH

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170] >> line vty 0 4
[R7] [2001:db8:acab:a001::170] >> transport input ssh


[OK] (elapsed time was 40 seconds)

R7(config)#
line vty 0 4
R7(config-line)#transport input ssh
R7(config-line)#end
R7#
===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           06/04/2018 21:38:46                               |
| Script ended:             06/04/2018 21:43:08                               |
| Script duration (h:m:s):  0:04:21                                           |
+-----------------------------------------------------------------------------+
```

# Unsuccessful demo (cmdrunner.py)

- R5: I have misconfigured authentication.
- R6: I have no Telnet (TCP/23) reachability.
- R7: This router is configured correctly.

```
aleks@acorp:~/FromZeroToHero$ python3 cmdrunner.py telnet/router/7200.json
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Enter domain name (example.com): a-corp.com
Enter SSH key size (1024, 2048, 4096): 2048
Disable telnet (yes/no)? yes
===============================================================================
Connecting to device: r5.a-corp.com
-------------------------------------------------------------------------------
r5.a-corp.com >> Authentication error
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
192.168.1.160 >> TCP/23 connectivity error
===============================================================================
Connecting to device: 2001:db8:acab:a001::170
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170] >> ip domain-name a-corp.com

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip domain-name a-corp.com
R7(config)#end
R7#
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170] >> crypto key generate rsa label SSH mod 2048

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 17 seconds)

R7(config)#end
R7#
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170] >> line vty 0 4
[R7] [2001:db8:acab:a001::170] >> transport input ssh

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#line vty 0 4
R7(config-line)#transport input ssh
R7(config-line)#end
R7#
===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           06/04/2018 21:49:25                               |
| Script ended:             06/04/2018 21:51:14                               |
| Script duration (h:m:s):  0:01:48                                           |
+-----------------------------------------------------------------------------+
```

# cmdrunner.log

```
06/04/2018 21:49:39 - WARNING - Telnet login failed: r5.a-corp.com
06/04/2018 21:49:42 - WARNING - [Errno 113] No route to host
```


# Successful demo (saver.py)

```
aleks@acorp:~/FromZeroToHero$ ./saver.py ssh/router/7200.json 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Connecting to device: r5.a-corp.com
-------------------------------------------------------------------------------
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
===============================================================================
Connecting to device: 2001:db8:acab:a001::170
-------------------------------------------------------------------------------
[R6] [192.168.1.160]

>> write memory
Building configuration...

-------------------------------------------------------------------------------

[R7] [2001:db8:acab:a001::170]

>> write memory
Building configuration...

-------------------------------------------------------------------------------

[R5] [r5.a-corp.com]

>> write memory
Building configuration...
[OK]
-------------------------------------------------------------------------------

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           06/04/2018 22:12:55                               |
| Script ended:             06/04/2018 22:13:09                               |
| Script duration (h:m:s):  0:00:13                                           |
+-----------------------------------------------------------------------------+
```

# Unsuccessful demo (saver.py)

- R5: I have misconfigured authentication.
- R6: I have no SSH (TCP/22) reachability.
- R7: This router is configured correctly.

```
aleks@acorp:~/FromZeroToHero$ ./saver.py ssh/router/7200.json 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Connecting to device: r5.a-corp.com
-------------------------------------------------------------------------------
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
===============================================================================
Connecting to device: 2001:db8:acab:a001::170
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
r5.a-corp.com >> Authentication error
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
192.168.1.160 >> TCP/22 connectivity error
-------------------------------------------------------------------------------
[R7] [2001:db8:acab:a001::170]

>> write memory
Building configuration...

-------------------------------------------------------------------------------

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           06/04/2018 22:15:27                               |
| Script ended:             06/04/2018 22:15:46                               |
| Script duration (h:m:s):  0:00:18                                           |
+-----------------------------------------------------------------------------+
```

# saver.log

```
06/04/2018 22:15:32 - WARNING - Authentication failure: unable to connect cisco_ios r5.a-corp.com:22
Authentication failed.
06/04/2018 22:15:46 - WARNING - Connection to device timed-out: cisco_ios 192.168.1.160:22
```
