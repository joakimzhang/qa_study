#coding=utf-8
import subprocess
import time

class strip_ogg():
    def get_ogg_packet_file(self,_vorbis_exe_path,_ogg_file_path,_pcm_path,packet_file_path):
        self.p2 = subprocess.Popen([_vorbis_exe_path,_ogg_file_path,_pcm_path,packet_file_path],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print self.p2.stdout.readlines()
        self.pid = self.p2.pid
        print self.pid
        print _vorbis_exe_path
        print _ogg_file_path
        print _pcm_path
        print packet_file_path
        time.sleep(2)
        self.p2.kill()
if __name__ == "__main__":
	new_obj = strip_ogg()
	new_obj.get_ogg_packet_file("E:\\test\\Yangtze_HD_Audio\\vorbis\\vorbis.exe","D:\\Breathless_MPEG1_LAYER2_64kbps_32khz_Stereo.ogg","D:\\Breathless_MPEG1_LAYER2_64kbps_32khz_Stereo.pcm","D:\\Breathless_MPEG1_LAYER2_64kbps_32khz_Stereo.packet")
        new_obj.kill_get_ogg_packet_file()
