# FromZeroToHero

```
Written by:             Aleks Lambreca   
Creation date:          09/09/2017      
Last modified date:     17/01/2018      
  
Script use:             Telnet into cisco devices (with Netmiko) and configure SSH. 
                        Script is both Python2 & 3 compatible.
Script input:           Username/Password   
Script output:          IOS command output  
```

# Note

This isn't the best python script out there :)  

# Prerequisites

1. Box with [netmiko](https://github.com/ktbyers/netmiko) installed.  
2. Telnet reachability to devices.    
3. Username/secret/privilege 15 preconfigured (example: `user a.lambreca priv 15 secret cisco`).  

# tools.py

- Colorama (optional).  

```
sudo pip install colorama
sudo pip3 install colorama
```

- Getpass function asks for password but hides the input.  
- Custom function (get_input) to get input that is compatible with both Python 2 and 3.  
- Custom function (get_credentials) that prompts for, and returns a username and password (password is asked twice, and if they don't match you get an error message `>> Passwords do not match. Try again. `. The script though will continue to run, but you should use Ctrl + C to cancel the script and try again.  
- tools.py is going to be imported on our main python script (telnet-cmdrunner.py). This way we have a cleaner script to work with.  

# cisco_ios_telnet_devices.json

Create an csv file like this example:  

```
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

Then i copy/pasted the output into cisco_ios_telnet_devices.json which is going to be used on our main python script.

# telnet-cmdrunner.py

This is the main script that we will run.  
It will prompt us for a username and a password (password required twice).

```
Username:
Password: 
Retype password: 
```

Then the script will connect to each device in **cisco_ios_telnet_devices.json** and run the commands in `domain_name`, `crypto_key_gen` and `ssh_commands`.  

Commands:  
```
ip domain-name a-corp.com
crypto key generate rsa label SSH mod 2048
ip ssh rsa keypair-name SSH
ip ssh version 2
line vty 0 4
transport input ssh telnet
```

I have also added a delay factor on the `crypto key generate rsa label SSH mod 2048` command because it takes a while to generate the SSH keys.  

Then i run `write memory` and if i get the output:   
`Overwrite the previous NVRAM configuration?[confirm]` or `Destination filename [startup-config]`  
i send blank line (like enter) which is the `output = connection.send_command_timing('')` line.  

After all commands are sent to a device, the script will repeat the process for tall devices in cisco_ios_telnet_devices.json. When it finishes it will clean and disconnect the sessions from all devices. 
  
# Successful demo:  

```
aleks@acorp:~/FromZeroToHero$ ./telnet-cmdrunner.py 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
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
[OK] (elapsed time was 11 seconds)

R5(config)#end
R5#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#ip ssh rsa keypair-name SSH
R5(config)#ip ssh version 2
R5(config)#line vty 0 4
R5(config-line)#transport input ssh
R5(config-line)#end
R5#
-------------------------------------------------------------------------------
Building configuration...
[OK]
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
% Generating 2048 bit RSA keys, keys will be non-exportable...end
R6#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#ip ssh rsa keypair-name SSH
R6(config)#ip ssh version 2
R6(config)#line vty 0 4
R6(config-line)#transport input ssh
R6(config-line)#end
R6#
-------------------------------------------------------------------------------
Building configuration...
[OK]
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
% Generating 2048 bit RSA keys, keys will be non-exportable...end
R7#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip ssh rsa keypair-name SSH
R7(config)#ip ssh version 2
R7(config)#line vty 0 4
R7(config-line)#transport input ssh
R7(config-line)#end
R7#
-------------------------------------------------------------------------------
Building configuration...
[OK]
```

# Unsuccessful demo:

- R5: I have misconfigured authentication.
- R6: I have no TCP/23 (Telnet) reachability.
- R7: This router is configured correctly.

```1C Enterprise
aleks@acorp:~/FromZeroToHero$ ./telnet-cmdrunner.py 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
Connecting to device: 192.168.1.150
-------------------------------------------------------------------------------
Failed to: 192.168.1.150
Telnet login failed: 192.168.1.150
===============================================================================
Connecting to device: 192.168.1.160
-------------------------------------------------------------------------------
Failed to: 192.168.1.160
[Errno 113] No route to host
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
The name for the keys will be: SSH

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 20 seconds)

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
-------------------------------------------------------------------------------
Building configuration...
[OK]
```
