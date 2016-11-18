import os

import math
from struct import *

def sine(_fc,_fs,_db,_bit,_second):
	list = []
	pi = math.pi
	fc = float(_fc)
	fs = float(_fs)

	A = 10**(_db/20.0)*(2**(_bit-1)-1)
	print "the A is:",A
	#*32767*20
	#x = [i for i in range(1000)]
	print math.sin(0)
	#for x in range(int(fs)*_second):
	for x in range(96000):
		#print (x*fc)/48000.0
		#print fc*x%fs
		result = int(round(((math.sin(2*pi*fc*x/fs))*A),0))
		#print hex(result)
		#pack_result = pack('i',result)
		pack_result = pack('h',result)
		#print int(pack_result)
		list.append(pack_result)
	#print list
	return list
	print "conplete"
def write_file(_list,_file_name):
	file_name = open(_file_name,'wb')
	for i in _list:
		file_name.write(i)
		file_name.write(i)
	file_name.close()


def ch8_to_stero():
    os.system('ffmpeg -i front_left.wav -i front_right.wav -i front_center.wav -i lfe.wav -i back_left.wav -i back_right.wav -i side_left.wav -i side_right.wav -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a][6:a][7:a]amerge=inputs=8[aout]" -map "[aout]" output_8ch1.wav')
    print "aaa"
def ch7_to_stero():
    os.system('ffmpeg -i front_left.wav -i front_right.wav -i front_center.wav -i lfe.wav -i back_left.wav -i back_right.wav -i side_left.wav -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a][6:a]amerge=inputs=7[aout]" -map "[aout]" output_7ch.wav')
    print "aaa"

def ch4_to_stero():
    os.system('ffmpeg -i front_left.wav -i front_right.wav -i back_left.wav -i back_right.wav -filter_complex "[0:a][1:a][2:a][3:a]amerge=inputs=4[aout]" -map "[aout]" output_4ch.wav')
    
def ch6_to_stero():
    os.system('ffmpeg -i front_left.wav -i front_right.wav -i front_center.wav -i lfe.wav -i back_left.wav -i back_right.wav -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a]amerge=inputs=6[aout]" -map "[aout]" output_6ch.wav')

def ch5_to_stero():
    os.system('ffmpeg -i front_left.wav -i front_right.wav -i front_center.wav -i lfe.wav -i back_left.wav -filter_complex "[0:a][1:a][2:a][3:a][4:a]amerge=inputs=5[aout]" -map "[aout]" output_5ch.wav')

    
def ch5_to_stero_2():
    os.system('ffmpeg -i lfe.wav -i back_left.wav -i back_right.wav -i side_left.wav -i side_right.wav -filter_complex "[0:a][1:a][2:a][3:a][4:a]amerge=inputs=5[aout]" -map "[aout]" output_5ch_2.wav')


def ch5_to_stero_0db():
    os.system('ffmpeg -i front_left_0db.wav -i front_right_0db.wav -i front_center_0db.wav -i lfe_0db.wav -i back_left_0db.wav -filter_complex "[0:a][1:a][2:a][3:a][4:a]amerge=inputs=5[aout]" -map "[aout]" output_5ch_0db.wav')

def ch3_to_stero():
    os.system('ffmpeg -i front_left.wav -i front_right.wav -i front_center.wav -filter_complex "[0:a][1:a][2:a]amerge=inputs=3[aout]" -map "[aout]" output_3ch.wav')

    
def wav_to_mp3(input, output):
    os.system('ffmpeg -i %s -acodec mp3 %s'%(input, output))

	
	
#sine_list = sine(1000,882000,0,16,1)
#write_file(sine_list,r'front_left.wav')	

#ch8_to_stero() 
ch8_to_stero()
ch7_to_stero()
ch6_to_stero()
ch5_to_stero()
ch4_to_stero()
ch3_to_stero()
#ch3_to_stero()
#ch5_to_stero_0db()
#wav_to_mp3("output_8ch1.wav", "output_8ch1.mp3")
