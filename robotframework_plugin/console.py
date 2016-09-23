#coding=utf-8
import serial  
import time
import re
import threading
class console():
    def connect_serial(self,console_num,baud_rate):
        """用于连接串口"""
        time.sleep(3)
        self.thread_exit_tag = 0
        self.reference_checksum = ""
        self.checksum = ""
        self.result = 0
        self.ser = serial.Serial(int(console_num)-1,int(baud_rate))
        print self.ser.portstr
        self.serial_thread()
    def close_serial(self):
        """断开串口连接"""
        time.sleep(3)
        #self.thread_obj.exit()
        #self.sent_command("source")
        self.thread_exit_tag = 1
        self.ser.close()     
        print "close serial"
        return 1
    def compare_checksum(self,_sum_num):
        """判断是否解析出checksum值，如果没有就等待"""
        self.reference_checksum = _sum_num
        
        if self.reference_checksum ==  "":
            self.thread_exit_tag = 1
            return 1
        loop_times = 72000
        while loop_times:
            if self.checksum != "":
                if self.checksum == self.reference_checksum:
                    print "!!!checksum(%s) == reference(%s)!!!\n"%(self.checksum,self.reference_checksum)
                    self.thread_exit_tag = 1
                    #self.ser.close() 
                    #return 1
                    return self.checksum
                else:
                    print "!!!checksum(%s) != reference(%s)!!!\n"%(self.checksum,self.reference_checksum)
                    self.thread_exit_tag = 1
                    return self.checksum
            else:
                print "!!!not find the check sum!!!\n"
                time.sleep(1)
                loop_times = loop_times-1    
        return 0
    def compare_result(self):
        """判断是否解析出QA_PASS这个字符串，如果没有就等待"""
        for i in range(3000):
            if self.result == 1:
                    return 1
                    print "QA_PASS"
            else:
                    time.sleep(1)
        print "time out 50minute not find qa pass tag"
        return 0
        
                        
    def parse_string(self):
        """解析串口输出的字符串，Final Dec checksum和QA_PASS"""
        while 1:
            if self.thread_exit_tag == 1:
                return 0    
            _serial_out = self.ser.readline()
            print _serial_out
            _result = re.search("Final Dec checksum (\w+)",_serial_out)
            _pass_result = re.search("QA_PASS",_serial_out)
            if _result != None:
                self.checksum = _result.group(1)
                print "!!!!%s!!!"%self.checksum
            if _pass_result != None:
                self.result = 1
    def serial_thread(self):
        """起一个线程运行parse_string"""
        self.thread_obj = threading.Thread(target=self.parse_string)
        self.thread_obj.start()
        #self.thread_obj.join()
        #serial_out = self.ser.readlines()
        #print serial_out
    def sent_command(self,command_char):
        """发送串口命令"""
        print("%s\n"%command_char)
        self.ser.write("%s\n"%str(command_char))
if __name__ == "__main__":
	obj_1 = console()
	obj_1.serial_thread()

