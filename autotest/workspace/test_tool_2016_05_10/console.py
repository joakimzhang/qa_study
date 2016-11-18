import serial  
import time
import re
import threading
import sys
class console():
	def connect_serial(self,console_num,baud_rate):
                time.sleep(3)
                self.thread_exit_tag = 0
                self.reference_checksum = ""
                self.checksum = ""
                self.result = 0
		self.ser = serial.Serial(int(console_num)-1,int(baud_rate))
		print self.ser.portstr
		self.print_serial_out()
	def close_serial(self):
                time.sleep(3)
                
                #self.thread_obj.exit()
		#self.sent_command("source")
		

		self.thread_exit_tag = 1
		self.ser.close()     
		
		print "close serial"
		return 1
	def compare_checksum(self,_sum_num):
		self.reference_checksum = _sum_num
		
		
		if self.reference_checksum ==  "":
			self.thread_exit_tag = 1
			#self.ser.close()
			return 1
		loop_times = 7200
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
					#self.ser.close() 
					#return 0
					return self.checksum
			else:
				print "!!!not find the check sum!!!\n"
				time.sleep(1)
				loop_times = loop_times-1    
		return 0

	def compare_checksum_bak(self,_sum_num):
                self.sent_command("help\n")
                while 1:

                        _serial_out = self.ser.readline()
                        print _serial_out
                        _result = re.search("Final Dec checksum (\w+)",_serial_out)
                        if _result != None:
                                if _result.group(1) == _sum_num:
					print "check sum Pass:",_result.group(1)
					return 1
				else:
                                        print "check sum fail:",_result.group(1)
                                        return 0
                                print _result.group(1)
                                return 1
                        time.sleep(0.01)
        def compare_result(self):
                for i in range(3000):
                        if self.result == 1:
                                return 1
                                print "QA_PASS"
                        else:
                                time.sleep(1)
                print "time out 50minute not find qa pass tag"
                return 0
        
                        
        def print_aaa(self):
                while 1:
                        if self.thread_exit_tag == 1:
                                return 0
                        #print "aaa"
                        _serial_out = self.ser.readline()
                        print _serial_out
                        _result = re.search("Final Dec checksum (\w+)",_serial_out)
                        _pass_result = re.search("QA_PASS",_serial_out)
                        if _result != None:
                                self.checksum = _result.group(1)
                                print "!!!!%s!!!"%self.checksum
                        if _pass_result != None:
                                self.result = 1
                                
                        #sys.stdout.flush()
	def print_serial_out(self):
                self.thread_obj = threading.Thread(target=self.print_aaa)
                self.thread_obj.start()
                
                #self.thread_obj.join()
		#serial_out = self.ser.readlines()
                #print serial_out
	def sent_command(self,command_char):
		print("%s\n"%command_char)
		self.ser.write("%s\n"%str(command_char))
if __name__ == "__main__":
	obj_1 = console()
	obj_1.print_serial_out()
	#obj_1.sent_command("mode1")
    
    #while 1:
    #    input_command = raw_input("please input the command:\n");
        #print "input is:",input_command
    #ser.close()             # close port 
