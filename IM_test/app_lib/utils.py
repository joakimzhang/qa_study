import os
import time
import shlex
import subprocess
import datetime
import psutil

def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        ret = func(*args, **kwargs)
        end = datetime.datetime.now()
        return end - start, ret
    return wrapper

def execCLI_wait(cmd_line, shell=True):
        cmd_args = shlex.split(cmd_line, posix=False)
        cmd_exec =  subprocess.Popen(cmd_args,bufsize=0,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=shell)
        output,strrout= cmd_exec.communicate()
        cmd_exec.wait()
        return (cmd_exec.returncode, output, strrout)

def execCLI(cmd_line, shell=True):
    cmd_args = shlex.split(cmd_line, posix=False)
    subprocess.Popen(cmd_args,bufsize=0,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=shell)
#     output,strrout= cmd_exec.communicate()
#     return output, strrout

# def pKill(name = 'VideoCapture.exe'):
#     cmd_line = 'taskkill /F /IM %s' % name
#     cmd_args = shlex.split(cmd_line, posix = False)
#     subprocess.call(cmd_args)

def pKill(log_obj, process = "VideoCapture.exe"):
    pidList = psutil.get_pid_list()
    for eachPid in pidList:
        eachProcess = psutil.Process(eachPid)
        try:
            processName = eachProcess.name()
        except:
            pass
        if(processName == process):
            try:
                log_obj.info('kill process: <%s>' % process)
                eachProcess.terminate()
            except:
                pass

def Time2ISOString( s ):
    return time.strftime("%H:%M:%S", time.localtime( float(s) ) )

if __name__ == "__main__":
    cmd_str = os.path.join(os.path.dirname(os.getcwd()),'videoCapture','VideoCapture.exe')
    for i in range(100):
        try:
            output, strrout = execCLI(cmd_str)
            print 'output:',output
            print 'strrout:',strrout 
        except Exception,e:
            print e
        time.sleep(2)    
        pKill()
        print i

