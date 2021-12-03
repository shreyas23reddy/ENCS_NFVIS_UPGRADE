# ENCS_NFVIS_UPGRADE

Upgrade NFVIS using CIMC MGMT port

++ Script helps in Fresh install of NFVIS version.
++ Migrating to SD-Branch feature - which requires a fresh install.
++ We support SD-Branch feature from 4.2 and above. 


CLI VIEW

ENCS5412-FGL214381Z5# scope bios

ENCS5412-FGL214381Z5 /bios # set boot-order CDROM:CIMC-VDVD,CDROM:Virtual-CD,HDD:SSD
To manage boot-order:
- Reboot server to have your boot-order settings take place
- Do not disable boot options via BIOS screens
- If a specified device type is not seen by the BIOS, it will be removed
from the boot order configured on the BMC
- Your boot order sequence will be applied subject to the previous rule.
The configured list will be appended by the additional device types
seen by the BIOS
ENCS5412-FGL214381Z5 /bios *# commit

Install NFVIS Cisco_NFVIS-4.6.1-FC1.iso from Cisco Software Download Site
Method 1.1 : Using CIMC CLI, Image upload from FTP location. Power cycle x86 : Start installation with the mapped .iso

Spoiler
ENCS5412-FGL214381Z5# scope host-image-mapping
ENCS5412-FGL214381Z5 /host-image-mapping # show detail
Current Mapped Image : None
Host Image Status: None
ENCS5412-FGL214381Z5 /host-image-mapping # download-image FTP 10.29.43.4 Cisco_NFVIS-4.6.1-FC1.iso
Username: anonymous
Password: Image download has started.
Please check the status using "show detail".
ENCS5412-FGL214381Z5 /host-image-mapping # show detail
Current Mapped Image : None
Host Image Status: "Downloading ..Please wait: 28.3%"
ENCS5412-FGL214381Z5 /host-image-mapping # show detail
Current Mapped Image : None
Host Image Status: Processing Image.....please wait
ENCS5412-FGL214381Z5 /host-image-mapping # show detail
Current Mapped Image : None
Host Image Status: Image Downloaded and Processed Successfully
ENCS5412-FGL214381Z5 /host-image-mapping # show filelist
Index Name
----- ---------------------------------------------
1 Cisco_NFVIS-4.6.1-FC1.iso
ENCS5412-FGL214381Z5 /host-image-mapping # map-image Cisco_NFVIS-4.6.1-FC1.iso
Please check the status using "show detail".
ENCS5412-FGL214381Z5 /host-image-mapping # show detail
Current Mapped Image : Cisco_NFVIS-4.6.1-FC1.iso
Host Image Status: Image mapped successfully, set CDROM as the Boot device.
ENCS5412-FGL214381Z5 /host-image-mapping # show filelist detail
File:
Index: 1
Name: Cisco_NFVIS-4.6.1-FC1.iso
Date: Wed, 18 Aug 2021 13:02:37 GMT
MD5: 56c81d560a39d2cdd4edb922ae21d3ab
Size: 1773289472
ENCS5412-FGL214381Z5 /host-image-mapping #
ENCS5412-FGL214381Z5 /bios # top
ENCS5412-FGL214381Z5# scope chassis
ENCS5412-FGL214381Z5 /chassis # power cycle
This operation will change the server's power state.
Do you want to continue?[y|N]y
ENCS5412-FGL214381Z5 /chassis # top
ENCS5412-FGL214381Z5# scope sol
ENCS5412-FGL214381Z5 /sol # set enabled yes
ENCS5412-FGL214381Z5 /sol *# commit
ENCS5412-FGL214381Z5 /sol # connect host
CISCO Serial Over LAN:
Press Ctrl+x to Exit the session

