from typing import Protocol
import paramiko
from getpass import getpass
import time
import re


"""
Function to send commands to CLI 
return the output of the executed CLI    
"""
def send_command(remote_conn,command):
    remote_conn.send(command)
    time.sleep(5)
    output = (remote_conn.recv(65535)).decode('ascii')
    return output
    

"""
Function to Upgrade the NFVIS via CIMC MGMT
++ It sets the boot order - CDROM:CIMC-VDVD,CDROM:Virtual-CD,HDD:SSD
++ Checks if the image - 'Cisco_NFVIS-4.6.1-FC1.iso' is present.
++ if not download the image
++ map the image 
++ powercycle 

No return value    
"""

def CIMC_Upgrade(ip, username, password, image, download_cmd, ftp_user,ftp_pass,map_cmd,hsh):
    
    
    try:
        
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(ip, port=22, username=username,
                                password=password,look_for_keys=False, 
                                allow_agent=False)
        
        
        
        print(f"connection Established and invoking the shell \n{hsh}")

        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(5)
        
        print(f"ivoked shell succefully \n{hsh}")
        
        print(f"setting the bios boot order CDROM:CIMC-VDVD,CDROM:Virtual-CD,HDD:SSD \n{hsh}")
        
        output = send_command(remote_conn,"scope bios\n")
        print(f"{output} \n{hsh}")
        
        output = send_command(remote_conn,"set boot-order CDROM:CIMC-VDVD,CDROM:Virtual-CD,HDD:SSD\n")
        print(f"{output} \n{hsh}")
        
        output = send_command(remote_conn,"commit\n")
        print(f"{output} \n{hsh}")
        
        output = send_command(remote_conn,"show actual-boot-order\n")
        print(f"boot order set successfully \n{output} \n{hsh}")
        
        output = send_command(remote_conn,"top\n")
        print(f"{output} \n{hsh}")
        

        output = send_command(remote_conn,"scope host-image-mapping\n")

        if '/host-image-mapping #' in re.findall("/.*#", output):
            
            print(f"successfully navigated to host-image-mapping \n{hsh}")
        
                
            output = send_command(remote_conn, "show filelist\n")
            lst_images = re.findall("C.*NFVIS.*iso", output)
            print(f"list of images present {lst_images} \n{hsh}")
            
    
        if image not in lst_images:
            
            for command in [download_cmd, ftp_user,ftp_pass]:
                
                output = send_command(remote_conn, command)
                print(f"{output} \n{hsh}")
            
        
            while (True):
                
                output = send_command(remote_conn,"show detail\n")
                time.sleep(3)
                host_image_mapping = (re.findall("Host Image Status.*",output))
                print(f"status check {host_image_mapping} \n{hsh}")
                
                output = send_command(remote_conn, "show filelist\n")
                time.sleep(3)
                lst_images = re.findall("C.*NFVIS.*iso", output)
                
                time.sleep(70)
            
                if image in lst_images:
                    print(f" image downloaded succesfully {lst_images} \n{hsh}")
                    break
        
        output = send_command(remote_conn, map_cmd)
        print(f"{output} \n{hsh}")
        time.sleep(3)
        output = send_command(remote_conn, "show detail\n")
        print(f"{output} \n{hsh}")
            
        Current_image_mapping = (re.findall("Current Mapped Image.*iso",output))
        print(Current_image_mapping)
        host_image_mapping = (re.findall("Host Image Status.*",output))
            
            
            
        if "Current Mapped Image : "+image in Current_image_mapping:
            
            output = send_command(remote_conn, "top\n")
            print(f"{output} \n{hsh}")
                
            output = send_command(remote_conn, "scope chassis\n")
            print(f"{output} \n{hsh}")
            
            output = send_command(remote_conn, "power cycle\n")
            print(f"{output} \n{hsh}")
            
            output = send_command(remote_conn, "y\n")
            print(f"{output} \n{hsh}")
            print(f"NFVIS will be power cycled and boot up with {image}")
                     
        
        remote_conn_pre.close()
    
    except:
        print("******ERROR********")
        print("please check the pointers")
        

if __name__=='__main__':
    hsh = '#'*40
    ip = '10.0.101.50'
    username = 'admin'
    password = 'password'
    image = 'Cisco_NFVIS-4.6.1-FC1.iso'
    ftp = '10.0.101.35'
    ftp_path = 'ftp/files/'
    ftp_user = 'ftpuser\n'
    ftp_pass = 'ftpuser\n'
    Prot = 'FTP'
    download_cmd = f"download-image {Prot} {ftp} {ftp_path}{image}\n"
    map_cmd = f"map-image {image}\n"
    CIMC_Upgrade(ip, username, password, image, download_cmd, ftp_user,ftp_pass,map_cmd,hsh)
