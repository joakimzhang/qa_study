#coding=utf-8
import os
class roomter():
    """重置roomter"""
    def reset_roomter(self,_command):
        os.system(u'%s'%_command) 
        #ret = os.system('downbinfile_32M rom.bin') 
if __name__ == "__main__":
	new_obj = roomter()
	new_obj.reset_roomter("D:\\roomter\\downbinfile_32M rom.bin")
