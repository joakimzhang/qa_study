# coding:utf8
'''
Created on 2016��8��30��

@author: zhangq
'''
from serial import Serial
import re
from threading import Thread
import time


class FilterMem(object):

    def __init__(self, port, baudrate):
        self.serial_obj = Serial()
        self.serial_obj.port = port
        self.serial_obj.baudrate = baudrate
    
    def connect_uart(self):
        try:
            self.serial_obj.open()
        except Exception, e:
            if self.serial_obj.isOpen():
                print "11111111111"
                self.serial_obj.close()
            print e
            return 0
        self.sent_thread = Thread(target=self.sendmid,args=("mid",))
        self.sent_thread.setDaemon(True)
        self.sent_thread.start()
        #self.get_thread_2 = Thread(target=self.getmem)
        
        
        #self.sent_thread_2.setDaemon(True)
        
        #self.sent_thread_2.start()
        
        
        #print "start get"
        self.getmem()

    def getmem(self):
        while 1:
            self.info = self.serial_obj.readline()
            match_info = re.search("Max malloc    :.*bytes", self.info)
            #if match_info:
                #print match_info.group[1]
            print self.info
            print match_info
            #print "bbb"
            #time.sleep(1)

    def sendmid(self, _char):
        self.serial_obj.write("mon\n")
        while 1:
            self.serial_obj.write("%s\n" % _char)
            time.sleep(1)
            #print _char

if __name__ == "__main__":
    my_obj = FilterMem(8, 115200)
    my_obj.connect_uart()
    # my_obj.getmem()
    # my_obj.sent_thread.join()
