#coding=UTF-8
import os
import sys
import datetime
import hashlib
import time
"""
这个脚本用来一直运行，以便把scancp命令拷贝到server上的文件考到我们的rommter目录，这样就不用手动拷贝了
原理是检测server上rom.bin文件的MD5值，如果有变化就考呗文件到roomter目录
"""
class sync_bin():
    def __init__(self):
        _format = "%y-%m-%d_%H.%M.%S"
        _today = datetime.datetime.today()
        self.save_time = _today.strftime(_format)
        #self.rom 是源bin文件，也就是/home/scannedfiles/zhangq 下面的bin文件
        self.rom = r"\\10.209.156.47\scannedfiles\zhangq\rom.bin"
        #self.roomter_dir是目的目录，这里是roomter的目录
        self.roomter_dir = r"D:\roomter"
        self.roomter_bak_dir = r"%s\bin_dir" % self.roomter_dir
        if os.path.isfile(self.rom) == False:
            print "can not find %s"%self.rom
            sys.exit(1)
        elif os.path.isdir(self.roomter_dir) == False:
            print "can not find %s"%self.roomter_dir
            sys.exit(1)
        elif os.path.isdir(self.roomter_bak_dir) == False:
            os.mkdir(self.roomter_bak_dir) 
            print "can not find %s,will make a new one" %self.roomter_bak_dir
    def detect_change(self):
        _old_md5 = ''
        while 1:
            _rom = open(self.rom,"rb")
            h = hashlib.sha1()
            h.update(_rom.read())
            _new_md5 = h.hexdigest()
            _rom.close()
            if _new_md5 == _old_md5:
                print "new MD5:",_new_md5,'\nold MD5:',_old_md5
                pass
            else:
                print "find diff,copying"
                _old_md5 = _new_md5
                self.copy_rom_file()
            time.sleep(2)
    def copy_rom_file(self):
    
        bak_bin = r"%s\%s.bin" % (self.roomter_bak_dir,self.save_time)
        print bak_bin
        if os.path.isfile(self.rom) == True and os.path.isdir(self.roomter_dir) == True:
            print "oo"
            os.system("copy %s %s" % (self.rom,self.roomter_dir))
            os.system("copy %s %s" % (self.rom,bak_bin))
        print os.listdir(self.roomter_dir)

if __name__ == "__main__":
    
    new_case = sync_bin()
    new_case.detect_change()
    #copy_rom_file(rom,roomter_dir)
