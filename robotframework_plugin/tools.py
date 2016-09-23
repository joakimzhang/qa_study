#coding=utf-8
import subprocess
import os
import re
import paramiko
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
        
    def download_file(self, remote_list, usb_dir):
        t = paramiko.Transport(("10.209.156.46",22))
        t.connect(username = "zhangq", password = "Avl1108")
        sftp = paramiko.SFTPClient.from_transport(t)
        for remote in remote_list:
            print remote
            remotepath=r'/media/streams/AudioTestFile/%s'%(remote.replace("\\", "/"))
            localpath='%s%s'%(usb_dir, remote)
            localpath_dir = os.path.split(localpath)
            try:
                sftp.get(remotepath, localpath)
            except Exception, e:
                os.makedirs(localpath_dir[0])
                sftp.get(remotepath, localpath)
        t.close()
    def creat_pe_case(self):
        stream_list = []
        #os.chdir(r"D:\autotest\workspace")
        #suite_file = open(r"Decoder_PE\__init__.txt", "r")
        suite_file = open(r"Decoder_PE\sample.txt", "r")
        suite_param = suite_file.read()
        print suite_param
        suite_file.close()
        list =  [i for i in os.listdir(os.getcwd()) if re.search("Decoder_.*\.txt", i)]
        print list
        for j in list:
            file_ = open(j, "r")
            file_new_ = open("Decoder_PE\\%s"%j, "w")
            file_new_.write(suite_param)
            file_new_.write("*** Test Cases ***\n")
            file_read = file_.read()
            #sub_list = re.findall("[\s\S]*?设置音频[\s\S]*?检查checksum    \w*?\s", file_read)
            sub_list = re.findall("[\s\S]*?设置音频[\s\S]*?断开串口\s", file_read)
            sub_list_0= re.search("Test Cases *\*\*\S([\s\S]*)",sub_list[0] )
            #print len(sub_list)
            sub_list[0] = sub_list_0.group(1)
            #print "~~~~~~~~~~~~~~~\n"
            for k in sub_list:
                #stream_ = re.search("设置音频    .*?    ", i)
                name_ = re.search("(\S.*\S)", k)
                stream_ = re.search("设置音频    (\S*)    ", k)
                check_sum_ = re.search("检查checksum    (\S*)", k)
                if name_:
                    #print "!!!!!!!!!!!!!!!!!\n"
                    print name_.group(1)
                    #print stream_.group(1)
                    #print check_sum_.group(1)
                    file_new_.write("%s\n"%name_.group(1))
                    file_new_.write("    [Template]    PE_DEC_CASE\n")
                    file_new_.write("    %s    %s\n"%(stream_.group(1), check_sum_.group(1)))
                    stream_list.append(stream_.group(1))
        return stream_list
        #self._get_file(stream_list,usb_dir)

if __name__ == "__main__":
    new_tools = tools()
    #new_tools.ffmpeg_eac3_to_spdif("D:\\48K_8ch.eac3","D:\\out_8.spdif")
    #new_tools.pcm24_to_16("D:\\AudioOut_A6.pcm","D:\\AudioOut_A6_18.pcm")
    #print "hello"

    new_tools.creat_pe_case()
        
 
        
        
        
        
        






    
    
