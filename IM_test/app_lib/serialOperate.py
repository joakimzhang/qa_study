import serial
import sys

import globalVariable


class SerialOperation(object):
    def __init__(self):
        self.com = globalVariable.serial_config['serial_port']
        self.xonxoff = globalVariable.serial_config['xonxoff']
        self.baudrate = globalVariable.serial_config['baudrate']
        self.timeout = globalVariable.serial_config['timeout']
    def connectSerial(self):
        try:
            self.inst = serial.Serial(self.com,
                                      baudrate = self.baudrate,
                                      xonxoff = self.xonxoff,
                                      timeout = self.timeout)
        except Exception ,e:
            print 'Exception is ' ,e
            return False
        if self.inst.isOpen():
            return True
        else:
            return False
    
    def is_open(self):
        return self.inst.isOpen() 
    
    def readable(self):
        try:
            return self.inst.readable()
        except Exception:
            return False

    def write_msg(self,msg):
        self.inst.flushInput()
        self.inst.write(msg)
        
    def read_msg(self):
        return self.inst.readline()
    
    def closeSerial(self):
        self.inst.close()



