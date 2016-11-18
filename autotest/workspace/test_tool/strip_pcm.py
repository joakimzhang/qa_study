import time
import os
import binascii
def strip_pcm(_file_name):
	print _file_name
	if os.path.exists(r"%s"%_file_name) == False:
		print r"can not find the file:%s"%_file_name
		return 0
	resource_obj = open(r"%s"%_file_name,'rb')
	new_obj = open("%s"%_file_name.replace(".","_new."),'wb')
	
	L_16BIT = resource_obj.read(2)
	R_16BIT = resource_obj.read(2)
	new_obj.write(L_16BIT)
	new_obj.write(R_16BIT)
	i = 0
	while 1:
		
		L_16BIT_NEW = resource_obj.read(2)
		R_16BIT_NEW = resource_obj.read(2)
		#print "R:%s\n"% binascii.b2a_hex(L_16BIT_NEW)
		if L_16BIT_NEW == "":
			print "strip complete!!!!!"
			break
		elif L_16BIT_NEW == L_16BIT and binascii.b2a_hex(L_16BIT_NEW) != "0000":
			continue
		elif R_16BIT_NEW == R_16BIT and binascii.b2a_hex(R_16BIT_NEW) != "0000":
			continue
		else:
			new_obj.write(L_16BIT_NEW)
			L_16BIT = L_16BIT_NEW
			new_obj.write(R_16BIT_NEW)
			R_16BIT = R_16BIT_NEW
			i = i+1

		#time.sleep(0.01)
		
		if i%8192 == 0 and i != 0:
			print "%skbit"%(i/8192)
	resource_obj.close()
	new_obj.close()
def user_input():
	while 1:
		print "please input the file name:"
		file_name = raw_input()
		if file_name == "exit":
			break
		else:
			strip_pcm(file_name)
		print "press exit to quit,file name to continue"
		time.sleep(0.1)
user_input()
#strip_pcm("AUDIO_IO_HDMI_48K_FS.pcm")