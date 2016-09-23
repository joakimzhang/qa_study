import threading
import Queue
import shutil
import os
import sys
import re
import time
import matplotlib.pylab as plt

import imageMatch 
import collectLogs
import parseCase
import parseIrkey
import globalVariable 
import utils
from serialOperate import SerialOperation
from restart_all import play_stream, stop_stream, replay_stream

error_map = {'-1':'Play stream failed',
             '-2':'Change STD failed!',
             '-3':'Load file failed!',
             '-4':'Set frequency failed!',
             '-5':'Set BandWidth failed!',
             '-6':'Set Modulation failed!',
             '-8':'Set FrameMode failed!',
             '-7':'Set CodeRate failed!',
             '-99':'socket connected failed'}

def switchStream(logger_obj,stream_map,main_dir):
    global error_map
    switch_stream_tool = {'BKS':os.path.join(main_dir,'app_lib','switchStream.py'),
                          'DEKTEC':os.path.join(main_dir,'tool','switch_stream.exe')}
    
    action_list = {'play':play_stream,
                   'stop':stop_stream,
                   'replay':replay_stream}
    
    logger_obj.info("stream_map['stream_std']: %s"%stream_map['stream_std'])
    
    if stream_map['stream_std'] == 'DVB-S':
        if stream_map['stream_symbol']:
            switch_stream_cmd = 'python %s -H %s -P %s -f %s --std %s -F %s -S %s ' \
                        %(switch_stream_tool,
                          stream_map['stream_serverip'],
                          stream_map['stream_serverport'],
                          stream_map['stream_file'],
                          stream_map['stream_std'],
                          stream_map['stream_freq'],
                          stream_map['stream_symbol'])
        else:
            switch_stream_cmd = 'python %s -H %s -P %s -f %s --std %s -F %s' \
                        %(switch_stream_tool,
                          stream_map['stream_serverip'],
                          stream_map['stream_serverport'],
                          stream_map['stream_file'],
                          stream_map['stream_std'],
                          stream_map['stream_freq'])
    elif stream_map['stream_std'] == 'DTMB':
        if stream_map.has_key('match_delay'):
            match_delay = int(stream_map['match_delay'])
        else:
            match_delay = 0
        if stream_map.has_key('stream_action'):
            if stream_map['stream_action']:
                try:
                    result = action_list[stream_map['stream_action']](main_dir, stream_map['stream_serverip'],
                                        stream_map['stream_serverport'],stream_map['card_type'])
                except IndexError:
                    logger_obj.error('your action:%s not existed!'%stream_map['stream_action'])
                    return (False,)
                if result == 0:
                    logger_obj.info('%s stream card success!'%stream_map['stream_action'])
                    return True, match_delay
                elif result == -99:
                    logger_obj.error('connect to stream card server failed,please check ip,port and if remote control is opened')
                    return (False,)
                else:
                    logger_obj.error('%s stream card failed!'%stream_map['stream_action'])
                    return (False,)
        if stream_map['card_type'] == 'BKS':
            switch_stream_cmd = 'python %s -H %s -P %s -f %s --std %s -F %s ' \
                        %(switch_stream_tool['BKS'],
                          stream_map['stream_serverip'],
                          stream_map['stream_serverport'],
                          stream_map['stream_file'],
                          stream_map['stream_std'],
                          stream_map['stream_freq'])
        elif stream_map['card_type'] == 'DEKTEC':
            switch_stream_cmd = '%s -H %s -P %s -f %s --std %s -F %s ' \
                        %(switch_stream_tool['DEKTEC'],
                          stream_map['stream_serverip'],
                          stream_map['stream_serverport'],
                          stream_map['stream_file'],
                          stream_map['stream_std'],
                          stream_map['stream_freq'])
        if stream_map.has_key('stream_bandwidth'):
            if stream_map['stream_bandwidth'] != 'None':
                switch_stream_cmd += '--BW %d '%(int(stream_map['stream_bandwidth']))
        if stream_map.has_key('stream_modulation'):
            if stream_map['stream_modulation'] != 'None':
                switch_stream_cmd += '-M %d '%(int(stream_map['stream_modulation']))
        if stream_map.has_key('stream_framemode'):
            if stream_map['stream_framemode'] != 'None':
                switch_stream_cmd += '--FM %d '%(int(stream_map['stream_framemode']))
        if stream_map.has_key('stream_coderate'):
            if stream_map['stream_coderate'] != 'None':
                switch_stream_cmd += '--CR %d '%(int(stream_map['stream_coderate']))
        if stream_map.has_key('stream_carriermode'):
            if stream_map['stream_carriermode'] != 'None':
                switch_stream_cmd += '--CM %d '%(int(stream_map['stream_carriermode']))
    
    logger_obj.warning('switch stream......,During this period, please do not press any key!')
    if stream_map.has_key('no_wait'):
        if stream_map['no_wait'] == 'True':
            utils.execCLI(switch_stream_cmd, shell=False)
            output = ''
        else:
            _, output, _ = utils.execCLI_wait(switch_stream_cmd, shell=False)
    else:
        _, output, _ = utils.execCLI_wait(switch_stream_cmd, shell=False)
    err_re = re.search('(-\d+)', output, re.I)
    if err_re:
        logger_obj.error(error_map[str(err_re.groups()[0])])
        return (False,)
    else:
        logger_obj.info('switch stream success!')
        return True, match_delay
    
class ExecCase(object):
    def __init__(self, main_dir, logger, case_log_inst, log_folder):
        self.logger = logger
        self.dest = log_folder
        self.case_inst = case_log_inst
        self.irk_map = globalVariable.IRK_MAP
        self.ir_cmd_tool=os.path.join(os.getcwd(),'tool','IR_Auto.exe')
        self.main_dir = main_dir
        self.img_dir = 'videoCapture\SnapPictures'
        self.template_dir = 'caseInfo\Case_pic'
        self.reset_tool = os.path.join(self.main_dir, 'tool', 'Board_Reset.exe')
        self.line_style = ['r','g','b','c','k','y','m']
        self.pos = 0
        self.memory_flag = False
        self.fig = plt.figure()
        
    def get_ir_cmd(self, irstr):   
        tc_opts = []         
        cmd = irstr.split(',')[0].strip()
        times = int(irstr.split(',')[-1].strip())
        interval = irstr.split(',')[1].strip()
        
        for _ in range(times):
            if cmd in self.irk_map:
                tc_opts.append((cmd,self.irk_map[cmd],interval))
            else:
                self.logger.error('CMD : %s does not exist on map %s' %(cmd, self.irk_map))
                return None     
        return tc_opts
    
    def run_cmds(self, cmd_list):  
        for cmd_item in cmd_list:
            if globalVariable.serial_config['target_type'] == 'libra2' or globalVariable.serial_config['target_type'] == 'Sunplus':
                cmd_str = '%s %d %d %d' %(self.ir_cmd_tool, 0, 255, cmd_item[0][1])
            elif globalVariable.serial_config['target_type'] == 'librasd':
                cmd_str = '%s %d %d %d' %(self.ir_cmd_tool, 0, 64, cmd_item[0][1])
            elif globalVariable.serial_config['target_type'] == 'SaiKeDa':
                cmd_str = '%s %d %d %d' %(self.ir_cmd_tool, 0, 255, cmd_item[0][1])
            
               
            return_code, output, _ = utils.execCLI_wait(cmd_str)
            
            interval = float(cmd_item[0][2])
            if interval < 0:
                interval = 0
            self.logger.info('{0:<8},{1:<6}'.format(cmd_item[0][0], cmd_item[0][2]))
            time.sleep(interval/1000)
                 
            if return_code == 0:
                pass
            else:
                self.logger.info('IRKEY {%s} is not successful, output is {%s}'%(cmd_str, output))
                return False
        
        self.logger.info('send all the commands done!')
        return True

    def get_input(self, content, step, tp):
        if tp == 'group':
            input_info = dict(content.get(step.replace('GROUP','Input')))
            if input_info.has_key('irlist'):
                ir_list = input_info.get('irlist').split('\n')
                input_info.pop('irlist')
            elif input_info.has_key('irfile'):
                ir_list = input_info.get('irfile').split('\n')
                input_info.pop('irfile')
            if not input_info.has_key('command'):
                return ir_list, {}
            else:    
                return ir_list if ir_list else [], input_info
        elif tp == 'stream':
            return dict(content.get(step))
        else:
            raise IndexError
    
    def get_output(self, content, step, tp):
        if tp == 'group':
            bmp_info = dict(content.get(step.replace('GROUP','Output')))  
        elif tp == 'stream':
            bmp_info = dict(content.get(step.replace('Stream','SOutput')))
        else:
            raise IndexError
        cmdfile = []
        if bmp_info.has_key('bmpfile'):
            bmps = bmp_info.get('bmpfile').split('\n')
            return bmps
        elif bmp_info.has_key('cmdfile') and not bmp_info.has_key('epgfile'):
            cmdfile.append(bmp_info.get('cmdfile'))
            return cmdfile
        elif bmp_info.has_key('cmdfile') and bmp_info.has_key('epgfile'):
            cmdfile.append(bmp_info.get('cmdfile'))
            cmdfile.append(bmp_info.get('epgfile'))
            return cmdfile
        else:
            return ['']
    def get_images(self):
        cmd_str = os.path.join(self.main_dir, 'videoCapture', 'VideoCapture.exe')
        try:
            utils.execCLI(cmd_str)  
        except Exception,e:
            print e
    
    def wait_create(self):
        return os.path.exists(os.path.join(self.main_dir,self.img_dir))
    
    def clear_images(self):
        pic_dir = os.path.join(self.main_dir, self.img_dir)
        for f in os.listdir(pic_dir):
            full_path = os.path.join(pic_dir, f)
            if os.path.exists(full_path):
                os.remove(full_path)
    
    def reset(self):
        cmd_str = '%s %d %d' % (self.reset_tool, 1000, 1)
        return_code, _, _ = utils.execCLI_wait(cmd_str)
        
        if return_code != 0:
            self.logger.error('reset board failed!')
        
    def draw_chart(self, locatation, fig, files_name = []):
        with open(files_name[0], 'r+') as f:
            lines = f.readlines()
            mvalues = []
            for line in lines:
                if 'COMMON' in line:
                    try:
                        mvalues.append(line.split()[4])
                    except IndexError:
                        continue

        img_path = os.path.join(locatation, 'memory_chart.png')
        globalVariable.IMAGE_DICT[globalVariable.serial_config['case_name']] = img_path[img_path.index('CASE_LOG') + 9:]
                
        base_file = os.path.basename(files_name[0])
        m_chart = base_file.split('.')[0] if '.' in base_file else base_file
        m_x = range(1,len(mvalues) + 1)
        m_y = [int(val) for val in mvalues]
        if len(files_name) == 1:     
            plt.plot(m_x,m_y,self.line_style[self.pos], label = m_chart)
            self.pos = self.pos + 1
            plt.xlabel('times')
            plt.ylabel('memory size')
            plt.title('Memory Size Tendency Chart')
            plt.legend(loc = 'best')
            fig.savefig(img_path)
        elif len(files_name) == 2:
            with open(files_name[1], 'r+') as f:
                lines = f.readlines()
                evalues = []
                for line in lines:
                    if 'm_nCurAllocSize' in line:
                        try:
                            evalues.append(line.split()[2])
                        except IndexError:
                            continue
                    
            ax1 = fig.add_subplot(2,1,1)
            ax2 = fig.add_subplot(2,1,2)
            
            base_file = os.path.basename(files_name[1])
            e_chart = base_file.split('.')[0] if '.' in base_file else base_file
            e_x = range(1,len(evalues) + 1)
            e_y = [int(val) for val in evalues]
            ax1.plot(m_x,m_y,self.line_style[self.pos], label = m_chart)
    #         ax1.set_xlabel('times')
            ax1.set_ylabel('memory size')
            ax1.set_title('Memory Size Tendency Chart')
            ax1.legend(loc = 'best')
            
            ax2.plot(e_x,e_y,self.line_style[self.pos], label = e_chart)
    #         ax2.set_xlabel('times')
            ax2.set_ylabel('m_nCurAllocSize')
            ax2.set_title('epginfo memory Tendency Chart')
            ax2.legend(loc = 'best')
            self.pos = self.pos + 1
            fig.savefig(img_path)
        else:
            self.logger.error('something is error!')
            
                  
    def mem_monitor(self, serial_inst, w_event, log_q, content, step, ir_list, cmds, tp = 'group', func = None): 
        def find_lines(expect_string):
            tmp_output = []
            start = time.time()
            while time.time() - start <= 2:
                line = serial_inst.read_msg()
                line = self.ts_format(line)
                log_q.put(line)
                if expect_string in line:
                    l = serial_inst.read_msg()
                    log_q.put(l)
                    tmp_output.append(l)
                    w_event.clear()
                    break
            else:
                w_event.clear()
                self.logger.error('can not find expect_string: %s'%expect_string)
            return tmp_output
        epginfo = False
           
        cmdfiles = self.get_output(content, step, tp)

        files_abs = map(lambda f: os.path.join(self.case_inst.case_dir,f),cmdfiles)
        for f in files_abs:
            if os.path.exists(f):
                os.remove(f)

        mf = open(files_abs[0], 'a+')
        if len(files_abs) == 2:
            epginfo = True
            ef = open(files_abs[1], 'a+')
        
        cms = [cmd.strip() for cmd in cmds['command'].split(',')]

        if cmds.has_key('times') and cmds.has_key('duration'):
            self.logger.error('times and duration should not exists at the same time')
            
        if cmds.has_key('times') and cmds.has_key('duration'):
            self.logger.error('times and duration should not exists at the same time')
        
        if cmds.has_key('times'):
            for _ in range(0, int(cmds.get('times'))):
                w_event.set()
                serial_inst.write_msg(cms[0] + '\n')
                map(lambda line:mf.write(line), find_lines('HeapName'))
                if epginfo:
                    if not w_event.isSet():
                        w_event.set()
                    serial_inst.write_msg(cms[1] + '\n')
                    map(lambda line:ef.write(line), find_lines('m_nMaxAllocNum'))    
                func(ir_list)
                
        if cmds.has_key('duration'):
            start = time.time()
            duration = cmds.get('duration')
            sec = int(duration.strip())*60
            while time.time() - start <= sec:
                w_event.set()
                serial_inst.write_msg(cms[0] + '\n')
                map(lambda line:mf.write(line), find_lines('HeapName'))
                if epginfo:
                    if not w_event.isSet():
                        w_event.set()
                    serial_inst.write_msg(cms[1] + '\n')
                    map(lambda line:ef.write(line), find_lines('m_nMaxAllocNum'))
                func(ir_list)
        
        mf.close()
        if epginfo:
            ef.close()         
        self.draw_chart(self.case_inst.case_dir, self.fig, files_abs)
    
    def ts_format(self, line):
        ts = time.strftime('[%y-%m-%d %H:%M:%S]')
        return ts + ' ' + line
       
    def exit_clean(self, serial_inst, s_event):
        globalVariable.serial_config['case_num']['failed'] += 1
        if serial_inst.is_open():
            serial_inst.closeSerial()
        if not s_event.isSet():
            s_event.set()
    
    @utils.timeit
    def exec_case_group(self, case_steps, case_content):
        stream_info = ''    
        serial_inst = SerialOperation()
        if not serial_inst.connectSerial():
            self.logger.error('Connect to COM failed!')
            sys.exit()
        w_event = threading.Event()
        s_event = threading.Event()
        log_q = Queue.Queue()
#         self.reset()
        log_t = SerialLog(serial_inst, self.case_inst, self.logger, w_event, s_event, log_q, name = 'log_record') 
        log_t.start()
#         time.sleep(20)
        for step in case_steps:
            match = Queue.Queue()
            queue = Queue.Queue()
            if step.find('Stream')==0:
                content = case_content.get(step)
                if isinstance(content, list):
                    stream_info = dict(content)
                    ret_value = switchStream(self.logger, stream_info, self.main_dir)
                    if not ret_value[0]:
                        self.logger.error('switch stream failed')
                        self.exit_clean(serial_inst, s_event)
                        return 'FAIL', 'switch stream failed'
                    else:
                        time.sleep(ret_value[1])
                elif isinstance(content, dict):
                    stream_info = self.get_input(content, step, tp = 'stream')
                    ret = switchStream(self.logger, stream_info, self.main_dir)
                    if not ret[0]:
                        self.logger.error('switch stream failed')
                        #sys.exit()
                        self.exit_clean(serial_inst, s_event)
                        ret = 'FAIL', 'switch stream failed'
                        return ret
                    else:
                        time.sleep(ret[1])
                    ret = self.start_match(match, queue, step, content, tp = 'stream')
                    if ret[0] == 'FAIL':
                        self.exit_clean(serial_inst, s_event)
                        return ret
                else:
                    raise TypeError
            elif step.find('GROUP') == 0:
                content = case_content.get(step)
                ir_list, cmds = self.get_input(content, step, tp = 'group')
                
                def exec_ir_cmd(ir_list):
                    ir_cmd_list = []
                    for str_ir in ir_list:
                        if str_ir=='':
                            break
                        ir_cmd = self.get_ir_cmd(str_ir)
                        ir_cmd_list.append(ir_cmd)
                    self.run_cmds(ir_cmd_list)
                
                if not cmds:     
                    exec_ir_cmd(ir_list)
                    templates = self.get_output(content, step, tp = 'group')
                    if templates[0]:
                        ret = self.start_match(match, queue, step, content, tp = 'group')
                        if ret[0] == 'FAIL':
                            self.exit_clean(serial_inst, s_event)
                            return ret
                        if self.memory_flag:
                            ret = 'PASS(memory check)', 'success'
                    else:
                        ret = 'PASS', 'success'
                else:
                    self.mem_monitor(serial_inst, w_event, log_q, content, step, ir_list, cmds, tp = 'group', func = exec_ir_cmd)
                    ret = 'PASS(memory check)', 'success'
                    self.memory_flag = True
        globalVariable.serial_config['case_num']['passed'] += 1
        time.sleep(2)
        s_event.set()
        serial_inst.closeSerial()
        return ret
             
    def start_match(self, match, queue, step, content, tp):
        self.clear_images()
        self.logger.debug('start to capture video!')
        self.get_images()
        while not self.wait_create():
            pass
        else:
            self.logger.debug('%s has been created successfully'%self.img_dir)
        
        templates = self.get_output(content, step, tp)
              
        templates[:] = map(lambda t: os.path.join(self.main_dir, self.template_dir, t), templates)
        if _match_thread(self.case_inst, self.logger, match, queue, self.dest, self.main_dir, self.img_dir, templates):
            self.logger.info('%s match success!'%templates)
        else:
            failed_info = '%s match failed!'%os.path.basename(templates[0])
            self.logger.info(failed_info)
            return 'FAIL', failed_info
        time.sleep(4)
                      
        return 'PASS', 'success'
                
def _match_thread(case_inst, log_obj, match, queue, dest, main_dir, img_dir, templates, thread_num = 1):
    event = threading.Event()
    threads = []
    generator = _ImageGenerator(log_obj, event = event, name = 'generator_thread', queue = queue,  match = match, main_dir = main_dir, 
                 img_dir = img_dir)
    threads.append(generator)
    generator.start()
    for i in range(thread_num):
        t = _ImageMatch(case_inst, log_obj, match, queue, event = event, name = 'match_thread_%s'%i, main_dir = main_dir, img_dir = img_dir, templates = templates)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
        log_obj.debug('joining %s', t.getName())
    
    log_obj.debug('clear the event signal')
    event.clear()
    
    pic_dir = os.path.join(main_dir, img_dir)
    for f in os.listdir(pic_dir):
        full_path = os.path.join(pic_dir, f)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except:
                print 'delete image failed'
    if not match.empty():
        return True
    else:
        return False

def match_process(image, template):
    return imageMatch.detect_match(image, template)

class SerialLog(threading.Thread):
    def __init__(self, serial_inst, case_inst, log_obj, write_event, stop_event, log_q, name, target = None):
        threading.Thread.__init__(self, target = target, name = name)
        self.serial_inst = serial_inst
        self.log_obj = log_obj
        self.write_event = write_event
        self.stop_event = stop_event
        self.log_q = log_q
        self.case_inst = case_inst
        
    def run(self):
        self.log_obj.info('serial log threading enter')
        while True:
            if not self.stop_event.isSet():
                if not self.write_event.isSet():
                    if self.serial_inst.readable():
                        line = self.serial_inst.read_msg()
                        line = self.ts_format(line)
                        self.log_q.put(line)
                    if self.log_q.qsize() > 20:
                        for _ in range(0, 20):
                            self.case_inst.case_handler.write(self.log_q.get())
                        self.case_inst.case_handler.flush() 
            else:
                self.write_log()
                self.log_obj.info('serial log threading exit')
                break
    
    def write_log(self):
        while not self.log_q.empty():
            self.case_inst.case_handler.write(self.log_q.get())
        self.case_inst.case_handler.close()
    
    def ts_format(self, line):
        ts = time.strftime('[%y-%m-%d %H:%M:%S]')
        return ts + ' ' + line
        
class _ImageGenerator(threading.Thread):
    seen = set()
    def __init__(self, log_obj, event = None, target = None, name = None, queue = None,  match = None, main_dir = None, 
                 img_dir = None, scan_freq = 0.5):
        threading.Thread.__init__(self, target = target, name = name)
        self.log_obj = log_obj
        self.q = queue
        self.match = match
        self.img_dir = os.path.join(main_dir, img_dir)
        self.scan_freq = scan_freq
        self.event = event
    
    def run(self):
        start = time.time()
        while time.time() - start <= globalVariable.DURARION:
            if not self.match.empty():
                self.log_obj.debug('have matched, stop to capture pictures!')
                utils.pKill(self.log_obj)
                break
            files = os.listdir(self.img_dir)
            if not files:
                self.log_obj.debug('directory is empty')
            else:
                for name in os.listdir(self.img_dir):
                    if name not in self.seen:
                        full_path = os.path.join(self.img_dir, name)
                        self.seen.add(name)
                        self.q.put(full_path)
                        if not self.event.isSet():
                            self.event.set() 
            time.sleep(self.scan_freq)
        else:
            self.event.set()
            self.log_obj.debug('match timeout!, stop to capture pictures!')
            utils.pKill(self.log_obj)

class _ImageMatch(threading.Thread):
    def __init__(self, case_inst, log_obj, match = None, queue = None, event = None, target = None, 
                 name = None, main_dir = None, img_dir = None, templates = None):
        threading.Thread.__init__(self, target = target, name = name)
        self.case_inst = case_inst
        self.match = match
        self.queue = queue
        self.main_dir = main_dir
        self.img_dir = os.path.join(main_dir, img_dir)
        self.templates = templates
        self.log_obj = log_obj
        self.event = event
        
    def run(self):
        self.log_obj.debug('waiting signal from generator thread...')
        self.event.wait()
        self.log_obj.debug('catch the signal from generator thread')
#         self.event.clear()
        start = time.time()
        failed_template = ''
        while time.time() - start <= globalVariable.DURARION:
            if self.match.qsize():
                self.log_obj.debug("have matched, won't match other images")
                break
            if not self.queue.empty():
                
                img = self.queue.get()
                for template in self.templates:
                    if match_process(img, template):
                        self.log_obj.debug('%s match found in %s'%(template, img))
                        continue         
                    else:
                        self.log_obj.debug('%s not match in %s'%(template, img))
                        failed_template = template
                        break
                else:
                    self.match.put(img)
        else:
            
            failed_match_dir = os.path.join(self.case_inst.case_dir, os.path.basename(failed_template))
            if not os.path.exists(failed_match_dir):
                os.mkdir(failed_match_dir)
            for name in os.listdir(self.img_dir):
                shutil.copy(os.path.join(self.img_dir, name), failed_match_dir)
                shutil.copy(os.path.join(self.main_dir, 'match_debug.py'), self.case_inst.case_dir)
            self.log_obj.debug('image match timeout, exiting from %s!'%self.name)
        
if __name__ == '__main__':
    templates = ['channel_match.bmp']
    
    logging_ins = collectLogs.CollectSysLoging()
    logging_ins.addSysLog(os.path.join(os.path.dirname(os.getcwd()),  
                                       'temp_log.txt'))  
    logger_obj = logging_ins.getLogger()  
    globalVariable.serial_config['target_type'] = 'Sunplus'  
    parse_irk_ins = parseIrkey.ParseIrkey()
       
    case_inst = parseCase.ParseCase(os.path.dirname(os.getcwd()), 'caselist.txt')
    case_file = os.path.join(os.path.dirname(os.getcwd()), 'caseInfo', 'Case', 'APP-2031.conf')
    case_step, case_content = case_inst.get_group(os.path.dirname(os.getcwd()),case_file)
    
    newExec = ExecCase()
    newExec.exec_stream_ir(logger_obj, case_step, case_content)
