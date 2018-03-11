# FromZeroToHero

```
Written by:           Aleks Lambreca
Creation date:        09/09/2017
Last modified date:   11/03/2018

Script use:           Telnet into cisco_ios_telnet_devices.json and configure SSH.
                      Disable telnet (optional).

Script input:         Username/Password

Script output:        Cisco IOS command output
                      Statistics
                      Errors in fromzerotohero.log
```

# Disclaimer

This isn't the best python script out there :)  

# Prerequisites

1. Box with [netmiko](https://github.com/ktbyers/netmiko) installed.  
2. Telnet (TCP/23) reachability to devices.    
3. Local username with privilege 15 (example: `user a.lambreca priv 15 secret cisco`).  

# tools.py

- Colorama (optional).  

```Cython
sudo pip install colorama
sudo pip3 install colorama
```

- Getpass function asks for password but hides the input.  
- Custom function (get_input) to get input that is compatible with both Python 2 and 3.  
- Custom function (get_credentials) that prompts for, and returns a username and password (password is asked twice, and if they don't match you get an error message `>> Passwords do not match. Try again. `. The script though will continue to run, but you should use Ctrl + C to cancel the script and try again.  
- tools.py is going to be imported on our main script (telnet-cmdrunner.py). This way we have a cleaner script to work with.  

# cisco_ios_telnet_devices.json

Create an csv file like this example:  

```CSV
device_type,ip
cisco_ios_telnet,192.168.1.150
cisco_ios_telnet,192.168.1.160
cisco_ios_telnet,192.168.1.170
```

Copy paste everything from the csv file to [Mr. Data Converter](https://shancarter.github.io/mr-data-converter/#).  
From the bottom, choose **Output as JSON - Properties**.  
From the left, choose **Delimiter Comma** and **Decimal Sign Commad**.  
This is what you should get from the example above.  

```
[{"device_type":"cisco_ios_telnet","ip":"192.168.1.150"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.160"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.170"}]
```

Then i copy/pasted the output into cisco_ios_telnet_devices.json which is going to be used on our main script.

# telnet-cmdrunner.py

This is the main script that we will run.   

First the script will:  
- Prompt us for a username and a password (password required twice).
- Print date & time the script started.

```
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Script started:       2018-03-11 16:42:07.337380
===============================================================================
```
  
Then the script will:    
- Connect to the first device in **cisco_ios_telnet_devices.json**.    
- Run the commands in `domain_name`.  
- Run the commands in `crypto_key_gen`.   
- Run the commands in `ssh_commands`.   
- Clean and disconnect the session.
- Connect to the first device in **cisco_ios_telnet_devices.json**.    
- Run the commands in `disable_telnet`.  
- Save the running-config to startup-config.  
- Clean and disconnect the session.

Finally the script will:
- Repeat the process for all devices in **cisco_ios_telnet_devices.json**.  

I added a delay factor on the `crypto key generate rsa label SSH mod 2048` command because it takes a while to generate the SSH keys.  

# Disable Telnet

If you don't want to disable telnet access to the devices, comment line 82 up to line 98 in **telnet-cmdrunner.py**.  
  
# Successful demo:  

```Cython
aleks@acorp:~/FromZeroToHero$ ./telnet-cmdrunner.py 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Script started:       2018-03-11 16:42:07.337380
===============================================================================
Connecting to device: 192.168.1.150
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#ip domain-name a-corp.com
R5(config)#end
R5#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 26 seconds)

R5(config)#end
R5#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#ip ssh rsa keypair-name SSH
R5(config)#ip ssh version 2
R5(config)#line vty 0 4
R5(config-line)#transport input ssh telnet
R5(config-line)#end
R5#
===============================================================================
Connecting to device: 192.168.1.150
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#line vty 0 4
R5(config-line)#transport input ssh
R5(config-line)#end
R5#
-------------------------------------------------------------------------------
Warning: Attempting to overwrite an NVRAM configuration previously written
by a different version of the system image.
Overwrite the previous NVRAM configuration?[confirm]
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#ip domain-name a-corp.com
R6(config)#end
R6#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 18 seconds)

R6(config)#end
R6#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#ip ssh rsa keypair-name SSH
R6(config)#ip ssh version 2
R6(config)#line vty 0 4
R6(config-line)#transport input ssh telnet
R6(config-line)#end
R6#
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#line vty 0 4
R6(config-line)#transport input ssh
R6(config-line)#end
R6#
-------------------------------------------------------------------------------
Warning: Attempting to overwrite an NVRAM configuration previously written
by a different version of the system image.
Overwrite the previous NVRAM configuration?[confirm]
===============================================================================
Connecting to device: 192.168.1.170
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip domain-name a-corp.com
R7(config)#end
R7#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 9 seconds)

R7(config)#end
R7#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip ssh rsa keypair-name SSH
R7(config)#ip ssh version 2
R7(config)#line vty 0 4
R7(config-line)#transport input ssh telnet
R7(config-line)#end
R7#
===============================================================================
Connecting to device: 192.168.1.170
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#line vty 0 4
R7(config-line)#transport input ssh
R7(config-line)#end
R7#
-------------------------------------------------------------------------------
Warning: Attempting to overwrite an NVRAM configuration previously written
by a different version of the system image.
Overwrite the previous NVRAM configuration?[confirm]
===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           2018-03-11 16:42:07.337380                        |
| Script ended:             2018-03-11 16:48:23.320913                        |
| Script duration (h/m/s):  0:06:15.983533                                    |
+-----------------------------------------------------------------------------+
```

# Unsuccessful demo:

- R5: I have misconfigured authentication.
- R6: I have no Telnet (TCP/23) reachability.
- R7: This router is configured correctly.

```Cython
aleks@acorp:~/FromZeroToHero$ ./telnet-cmdrunner.py
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Script started:       2018-03-11 17:09:13.531507
===============================================================================
Connecting to device: 192.168.1.150
-------------------------------------------------------------------------------
192.168.1.150 >> Authentication error
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
192.168.1.160 >> TCP/22 connectivity error
===============================================================================
Connecting to device: 192.168.1.170
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip domain-name a-corp.com
R7(config)#end
R7#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#crypto key generate rsa label SSH mod 2048
% You already have RSA keys defined named SSH.
% They will be replaced.

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 8 seconds)

R7(config)#end
R7#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip ssh rsa keypair-name SSH
R7(config)#ip ssh version 2
R7(config)#line vty 0 4
R7(config-line)#transport input ssh telnet
R7(config-line)#end
R7#
===============================================================================
Connecting to device: 192.168.1.170
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#line vty 0 4
R7(config-line)#transport input ssh
R7(config-line)#end
R7#
-------------------------------------------------------------------------------
Building configuration...
[OK]
===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           2018-03-11 17:09:13.531507                        |
| Script ended:             2018-03-11 17:11:31.171253                        |
| Script duration (h/m/s):  0:02:17.639746                                    |
+-----------------------------------------------------------------------------+
```
