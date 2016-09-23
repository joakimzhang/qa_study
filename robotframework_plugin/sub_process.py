#coding=utf-8
import subprocess
import time
import threading
import re
class sub_process():
    #def __init__(self):
        #self.p = subprocess.Popen(r"D:\similator_test\Debug\test_audio.exe",stdin=subprocess.PIPE)
    def connect_command_sim(self,_exe_path):
        """用于连接串口"""
        #self.handle = open(r'stdout.txt','w',0)
        #self.handle2 = open(r'stderr.txt','w',0)
        #self.p = subprocess.Popen(str(_exe_path),bufsize=0,stdin=subprocess.PIPE,stdout=self.handle,stderr=self.handle2)
        self.p = subprocess.Popen(str(_exe_path),bufsize=0,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.pid = self.p.pid
        print self.pid
        self.thread_exit_tag = 0
        self.check_result = 0
        self.threading_obj = threading.Thread(target=self.print_all_out)
        self.threading_obj.start()
        
    def clear_out(self):
        """断开串口连接"""
        i = 1
        returncode = self.p.poll()
        while 1:
            #sys.stdout.flush()
            get_read = self.p.stdout.readline()
            returncode = self.p.poll()
            i = i+1
            print i,returncode
            print get_read
            time.sleep(0.01)
            if get_read == "":
                break
        print "complete"
    def get_checksum(self,_reference_sum):
        """判断是否解析出checksum值，如果没有就等待"""
        for i in range(3000):
            time.sleep(1)
            if i%10 == 0:
                self.sent_command_sim("help")
            if self._check_num == _reference_sum:
                print "checksum:%s==%s"%(self._check_num,_reference_sum)            
                #return 1
                return self._check_num
            elif self._check_num == "":
                #print "can not find check sum:^_^"
                #return 0
                pass
            else:
                print "checksum is:%s!=reference:%s"%(self._check_num,_reference_sum)
                #return 0
                return self._check_num
        print "50 minute time out,can not find checksum"
        return 0
    def get_result(self):
        """判断是否解析出QA_PASS这个字符串，如果没有就等待"""
        for i in range(3000):
            if self.check_result == 1:
                print "QA_PASS"
                return 1
            else:
                time.sleep(1)
        print "time out 50minute not find qa pass tag"
        return 0
        
    def print_all_out(self):
        """解析串口输出的字符串，Final Dec checksum和QA_PASS"""
        self._check_num = ""
        while 1:
            if self.thread_exit_tag == 1:
                return 0
            #final_txt = self.handle.read()
            final_txt = self.p.stdout.readline()
            print final_txt
            check_obj = re.search("Final Dec checksum (\w+)",final_txt)
            _check_result = re.search("QA_PASS",final_txt)
            if check_obj != None:
                self._check_num = check_obj.group(1)
            if _check_result != None:
                self.check_result = 1
            time.sleep(0.01)
    def sent_command_sim(self,_command):
        """发送串口命令"""
        self.p.stdin.write("%s\n"%_command)
        print _command
        #self.p.stdout.flush()
        self.p.stdin.flush()
    def print_checksum(self):
        for i in range(1200):
            #print "repeat:",i,"!!!!!!!!!!!!"
            time.sleep(0.01)
            self.sent_command_sim("help")    
        #self.handle.close()
        time.sleep(1)
        #self.handle = open(r'stdout.txt','r',0)
        self.print_all_out()
            
    def kill_subprocess(self):
        self.thread_exit_tag = 1
        time.sleep(2)
        #self.p.terminate()
        self.p.kill()
        print "kill the process"
        #self.handle.close()
        #self.handle = open(r'stdout.txt','w+',0)
        #self.print_all_out()
        #self.handle.close()

if __name__ == "__main__":
    new_sub_process = sub_process()
    new_sub_process.connect_command_sim(r"D:\Debug\test_audio.exe")
    #new_sub_process.print_stdout(1000)
    new_sub_process.clear_out()
    print "b" 
    new_sub_process.sent_command_sim(r"configfile test.mp3")
    #new_sub_process.sent_command_sim(r"play 8 0 1")
 
    new_sub_process.sent_command_sim(r"source")
    new_sub_process.sent_command_sim(r"stop 1")
    new_sub_process.sent_command_sim(r"source")
    new_sub_process.sent_command_sim(r"source")
    new_sub_process.print_stdout(2)
    #new_sub_process.sent_command_sim(r"play 8 1 1")


    time.sleep(1)
    #new_sub_process.sent_command_sim(r"stop 1")
    new_sub_process.kill_subprocess
    #time.sleep(5)
    #handle = open(r'1.txt','r')
    #_file = handle.read()
    #print _file
    #print re.search("Final Dec checksum (\w+)",_file).group(1)

    
