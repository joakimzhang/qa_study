#!usr/bin/python#coding=utf-8
import os
import subprocess
import sys

class tools():
	#os.system("..\\tools\\ffmpeg -i D:\\48K_8ch.eac3 -acodec copy -f spdif D:\\out.spdif")
	#p = subprocess.Popen("..\\tools\\ffmpeg -i D:\\48K_8ch.eac3 -acodec copy -f spdif D:\\out.spdif",stdin=subprocess.PIPE,stdout=subprocess.sys.stdout)
	def ffmpeg_convert_to_spdif(self,_input_file,_output_file):
		"""用ffmpeg将源文件转换为spdif的raw格式\r\n
		用法：ffmpeg_convert_to_spdif 绝对路径1 绝对路径2 \r\n
		ffmpeg_convert_to_spdif  D:\\AudioTestFile\\AudioIO\\48K_8ch.eac3 d:\\result\\FFMPEG_16bit.pcm"""
		#p = subprocess.Popen(r"ffmpeg.exe -i %s -acodec copy -f spdif %s"%(str(_input_file),str(_output_file)),stdin=subprocess.PIPE,stdout=subprocess.sys.stdout)
		#p.stdin.write("y")
		p = subprocess.Popen("tools\\ffmpeg.exe -i %s -acodec copy -f spdif %s"%(_input_file,_output_file),stdin=subprocess.PIPE)
		p.communicate("y")
		pass
	def ffmpeg_convert_to_pcm(self,_sample_rate,_input_file,_output_file):
		"""用ffmpeg将源文件转换为pcm格式\r\n
		用法：ffmpeg_convert_to_pcm 采样率 绝对路径1 绝对路径2\r\n
		ffmpeg_convert_to_pcm  48000 D:\\AudioTestFile\\AudioIO\\48K_8ch.eac3 d:\\result\\FFMPEG_16bit.pcm"""
		#p = subprocess.Popen(r"ffmpeg.exe -i %s -acodec copy -f spdif %s"%(str(_input_file),str(_output_file)),stdin=subprocess.PIPE,stdout=subprocess.sys.stdout)
		#p.stdin.write("y")
		p = subprocess.Popen("tools\\ffmpeg.exe -i %s -ar %s -acodec copy -f s16le %s"%(_input_file,_sample_rate,_output_file),stdin=subprocess.PIPE)
		p.communicate("y")
		pass
	def pcm24_to_16(self,_input_file,_output_file):
		"""用于将24bit的pcm转换为16bit\r\n
		用法：
		Pcm24 To 16 绝对路径1 绝对路径2\r\n
		Pcm24 To 16  D:\\A4.pcm d:\\result\\ A4_16bit.pcm
		"""
		p = subprocess.Popen("tools\\pcm24to16 %s %s"%(_input_file,_output_file),stdin=subprocess.PIPE)
		#p.stdin.write("y")
		p.communicate("y")
		pass
if __name__ == "__main__":
	#new_tools = tools()
	#new_tools.ffmpeg_eac3_to_spdif("D:\\48K_8ch.eac3","D:\\out_8.spdif")
	#new_tools.pcm24_to_16("D:\\AudioOut_A6.pcm","D:\\AudioOut_A6_18.pcm")
	print "hello"