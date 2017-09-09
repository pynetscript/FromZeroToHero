# FromZeroToHero

```
Written by:             Aleks Lambreca   
Creation date:          09/09/2017      
Last modified date:     10/09/2017      
  
Script use:             Telnet into cisco devices (with Netmiko) and configure SSH.    
Script input:           Username/Password   
Script output:          IOS command output  
```

# Notes

This isn't the best python script out there.  
I would highly suggest to go over [this](https://www.youtube.com/user/GPM365/playlists) youtube playlist first.  

# Prerequisites

Telnet reachability.   
Username/secret/privilege 15 preconfigured (example: `user a.lambreca priv 15 secret cisco`).  

# tools.py

Getpass function asks for password but doesn't show it in screen.  
Custom function to get input that is compatible with both Python 2 and 3.  
Prompts for, and returns a username and password.  
This is going to be imported on our python script (telnet-cmdrunner.py).

# cisco_ios_telnet_devices.json

Create an csv file like this example:  

```
device_type,ip
cisco_ios_telnet,192.168.1.150
cisco_ios_telnet,192.168.1.160
cisco_ios_telnet,192.168.1.170
```

Copy paste into everything on the csv file to [Mr. Data Converter](https://shancarter.github.io/mr-data-converter/#).  
From the bottom, choose **Output as JSON - Properties**.  
From the left (SETTINGS) choose **Delimiter Comma** and **Decimal Sign Commad**.  
Now this is what i should get from the example above.  

```
[{"device_type":"cisco_ios_telnet","ip":"192.168.1.150"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.160"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.170"}]
```

This is how i generated my list of devices that netmiko will telnet on them.  

# telnet-cmdrunner.py

This is the main script that we will run.  
It will prompt us like this and you will input your username and your password x 2.

```
Username:
Password: 
Retype password: 
```

Then the script will connect to each device in **cisco_ios_telnet_devices.json** and run the commands in `domain_name`, `crypto_key_gen` and `ssh_commands`. I have also added a delay factor on the `crypto key generate rsa label SSH mod 2048` command because it takes a while.

After all commands are sent to a device, it will disconnect, and repeat this process for the next device.

Here is a demo:

```
aleks@acorp:~/pyscript$ ./telnet-cmdrunner.py 
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
[OK] (elapsed time was 8 seconds)

R5(config)#end
R5#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R5(config)#ip ssh rsa keypair-name SSH
R5(config)#ip ssh version 2
R5(config)#end
R5#
-------------------------------------------------------------------------------

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
[OK] (elapsed time was 12 seconds)

R6(config)#end
R6#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R6(config)#ip ssh rsa keypair-name SSH
R6(config)#ip ssh version 2
R6(config)#end
R6#
-------------------------------------------------------------------------------

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
[OK] (elapsed time was 7 seconds)

R7(config)#end
R7#
-------------------------------------------------------------------------------
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R7(config)#ip ssh rsa keypair-name SSH
R7(config)#ip ssh version 2
R7(config)#end
R7#
-------------------------------------------------------------------------------
```
