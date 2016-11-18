#!/usr/bin/python

import paramiko
import os
 
def get_file(remote, usb_dir):
    t = paramiko.Transport(("10.209.156.46",22))
    
    t.connect(username = "zhangq", password = "Avl1108")
    
    sftp = paramiko.SFTPClient.from_transport(t)
    
    remotepath=r'/media/streams/AudioTestFile/%s'%(remote.replace("\\", "/"))
    
    localpath='%s%s'%(usb_dir, remote)
    localpath_dir = os.path.split(localpath)
    try:
        sftp.get(remotepath, localpath)
    except Exception, e:
        os.makedirs(localpath_dir[0])
        sftp.get(remotepath, localpath)
    t.close()
    
get_file("FromSunplus\\AC3\\384kBps_44.1kHz\\ac3_0006-2002n_ac3_16bit.ac3", "f:\\")
