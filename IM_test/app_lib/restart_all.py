import os
import time
import re
import switchStream
import utils

def restart_board():
    ir_cmd_tool = os.path.join(os.path.dirname(os.getcwd()),'tool','IR_Auto.exe')
    #execute reboot by power 0x000A
    cmd_str = '%s %d %d %s' %(ir_cmd_tool, 0, 64, 10)
    utils.execCLI_wait(cmd_str)
    time.sleep(3)
    utils.execCLI_wait(cmd_str)
#     print "restart board success!"
    return True

def replay_stream(main_dir, hostname, port, type1 = 'BKS'):
    if type1 == 'BKS':
        #execute replay by BKS
        #Connect remote server
        try:
            socket_con = switchStream.ConnectSocket(hostname, int(port))
        except:
            return -99
        res=socket_con.recevieResult()
        #print "res=",res
        if re.search('Welcome', res):
            pass
        else:
            return -99
        #Stop ts 
        socket_con.sendCmd('stop')
        res1 = socket_con.recevieResult()
        #print "res1=", res1
        re1 = -1
        if re.search('Success', res1) or re.search('Already Stopped!', res1):
            re1 = 0
                
        #Play ts 
        socket_con.sendCmd('play')
        res2 = socket_con.recevieResult()
        #print "res2=", res2
        re2 = -1
        if re.search('Success', res2) or re.search('Already Played!', res2):
            re2 = 0
    
        socket_con.closeSocket()
        if re1==0 and re2==0:
            #print "replay stream success!" 
            return 0
        elif re1==-1 and re2==0:
            return -1
        elif re1==0 and re2==-1:
            return -2
        elif re1==-1 and re2==-1:
            return -3
    elif type1 == 'DEKTEC':
        dek_cmd_tool = os.path.join(main_dir,'tool','switch_stream.exe')
        cmd_str = '%s -H %s -P %d -D replay' %(dek_cmd_tool, hostname, int(port))
        (return_code,
         output,
         strout) = utils.execCLI_wait(cmd_str)
        
        return return_code
    
def play_stream(main_dir, hostname, port, type1 = 'BKS'):
    if type1 == 'BKS':
        #execute replay by BKS
        #Connect remote server
        try:
            socket_con = switchStream.ConnectSocket(hostname, int(port))
        except:
            return -99
        res=socket_con.recevieResult()
        if re.search('Welcome', res):
            pass
        else:
            return -99
    
        #Play ts 
        socket_con.sendCmd('play')
        res = socket_con.recevieResult()
        re1 = -1
        if re.search('Success', res):
            re1 = 0
        elif re.search('Already Playing!', res):
            re1 = 0
        else:
            re1 = -1
        
        socket_con.closeSocket()
        
        return re1
    elif type1 == 'DEKTEC':
        dek_cmd_tool = os.path.join(main_dir,'tool','switch_stream.exe')
        cmd_str = '%s -H %s -P %d -D play' %(dek_cmd_tool, hostname, int(port))
        (return_code,
         output,
         strout) = utils.execCLI_wait(cmd_str)
        
        return return_code
    
def stop_stream(main_dir, hostname, port, type1 = 'BKS'):
    if type1 == 'BKS':
        #execute replay by BKS
        #Connect remote server
        try:
            socket_con = switchStream.ConnectSocket(hostname, int(port))
        except:
            return -99
        res=socket_con.recevieResult()
        if re.search('Welcome', res):
            pass
        else:
            return -99
        #Stop ts 
        socket_con.sendCmd('stop')
        res = socket_con.recevieResult()
        re1 = -1
        if re.search('Success', res):
            re1 = 0
        elif re.search('Already Stopped!', res):
            re1 = 0
        else:
            re1 = -1 
    
        socket_con.closeSocket()

        return re1
    elif type1 == 'DEKTEC':
        dek_cmd_tool = os.path.join(main_dir,'tool','switch_stream.exe')
        cmd_str = '%s -H %s -P %d -D stop' %(dek_cmd_tool, hostname, int(port))
        print cmd_str
        (return_code,
         output,
         strout) = utils.execCLI_wait(cmd_str)
        
        return return_code
    
if __name__ == "__main__":
    pass
    host = '10.209.157.54'
    port = 7777
#    stop_stream(host, port)
    if 0:
        card_type='DEKTEC'
    else:
        card_type='BKS'
    main='E:\\Auto_code\\Auto_APP'
    res=replay_stream(main, host, port,card_type)
    print "res=",res
    