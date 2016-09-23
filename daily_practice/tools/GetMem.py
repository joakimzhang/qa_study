# coding:utf8
'''
Created on 2016��8��30��

@author: zhangq
'''
from serial import Serial
import re
from threading import Thread
import time
import datetime
import pygal
import os
class FilterMem(object):

    def __init__(self, port, baudrate):
        self.serial_obj = Serial()
        self.serial_obj.port = port-1
        self.serial_obj.baudrate = baudrate
        self.connect_uart()
    
    def connect_uart(self):
        try:
            self.serial_obj.open()
        except Exception, e:
            if self.serial_obj.isOpen():
                self.serial_obj.close()
            print e
            return 0
        
        
    def send_thread(self, _command, _period):    
        self.sent_thread = Thread(target=self.sendfunc,args=(_command, _period))
        self.sent_thread.setDaemon(True)
        self.sent_thread.start()
        #self.getmem()

    def getmem(self, keyword, file_name):
        today = datetime.date.today()
        self.file_name = r"%s_%s" % (file_name, today)
        x_list = []
        y_list = []
        with open("%s.log"%self.file_name, "w") as f:
            while 1:
                self.info = self.serial_obj.readline()
                print self.info
                current = datetime.datetime.now()
                f_time = "%s-%s-%s %s:%s:%s" % (current.year, current.month, current.day, current.hour, current.minute, current.second)
                f.write("%s:%s" % (f_time, self.info))
                match_info = re.search("%s.+?(\d+).+bytes" % keyword, self.info)
                if match_info:
                    mem_val = match_info.group(1)
                    y_list.append(int(mem_val))
                    x_list.append(current)
                    print mem_val
                if len(y_list)%10 == 0:
                    self.make_pic(x_list, y_list)
                    
                    #print match_info.group(0)
                #print "bbb"
                #time.sleep(1)



    def sendfunc(self, _char, _period):
        self.serial_obj.write("mon\n")
        while 1:
            self.serial_obj.write("%s\n" % _char)
            time.sleep(_period)
            #print _char

    # plot a sine wave from 0 to 4pi
    def make_pic(self, x_list, y_list):
        line_chart = pygal.Line()
        line_chart.title = 'Mem usage evolution (in %)'
        line_chart.x_labels = x_list
        line_chart.add('Mem', y_list)
        line_chart.render()

        f = open('%s.html' % self.file_name, 'w')
        f.write(line_chart.render())
        f.close()



if __name__ == "__main__":
    my_obj = FilterMem(9, 115200)
    my_obj.send_thread("mid", 10)
    #my_obj.connect_uart()
    my_obj.getmem("Used")
    # my_obj.sent_thread.join()
