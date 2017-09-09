# FromZeroToHero

Written by:             Aleks Lambreca   
Creation date:          09/09/2017      
Last modified date:     10/09/2017      
  
Script use:	            Telnet into cisco devices (with Netmiko) and configure SSH.    
Script input:           Username/Password   
Script output:          IOS command output  
      
# Notes

This isn't the best python script out there.  
I would highly suggest to go over [this](https://www.youtube.com/user/GPM365/playlists) youtube playlist.  

# tools.py

Getpass function asks for password but doesn't show it in screen.
Custom function to get input that is compatible with both Python 2 and 3.
Prompts for, and returns a username and password.
This is going to be imported on our python script (telnet-cmdrunner.py)

# cisco_ios_telnet_devices.json

Create an csv file like this example:

```
device_type,ip
cisco_ios_telnet,192.168.1.150
cisco_ios_telnet,192.168.1.160
cisco_ios_telnet,192.168.1.170
```

Copy paste into everything on the csv file to [Mr. Data Converter](https://shancarter.github.io/mr-data-converter/#)
From the bottom, choose **Output as JSON - Properties**.
From the left (SETTINGS) choose **Delimiter Comma** and **Decimal Sign Commad**.
Now this is what i should get from the example above.

```
[{"device_type":"cisco_ios_telnet","ip":"192.168.1.150"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.160"},
{"device_type":"cisco_ios_telnet","ip":"192.168.1.170"}]
```

This is how i generated my list of devices that netmiko will telnet on them
