import caseExec
import globalVariable 
import parseIrkey
import utils
import os
import tempfile
import re
import ConfigParser

import os
import app_lib
import time

class send_key():
    def __init__(self):
        IRK_MAP = {}
        IRK_MAP=int("0x0044", 16)
        #aaa=parseIrkey.ParseIrkey()
        #aaa.insertIrk2Map('Gospell')
        
#        N=globalVariable.IRK_MAP
#        for i in N:
#            print i
        
    def send_one_key(self,key_value):
        cmd_aaa=globalVariable.IRK_MAP[key_value] 
        print cmd_aaa
        print globalVariable.IRK_MAP[key_value] 
        ir_cmd_tool=os.path.join(os.getcwd(),'tool','IR_Auto.exe')

        cmd_str = '%s %d %d %d' %(ir_cmd_tool, 0, 255, cmd_aaa)
        print cmd_str
        utils.execCLI_wait(cmd_str) 
        

        
class ParseCase(object):
    def __init__(self, main_path = '', logger = None):
        self.main_path = main_path
        self.case_list_file = os.path.join(self.main_path,'caseInfo', 'caselist.txt')
        self.case_dir = os.path.join(self.main_path)
        self.logger = logger
         
        with open(self.case_list_file,'r') as cl:
            cases = filter(lambda l: l.strip(), cl.readlines())     
            cases[:] = map(lambda l: os.path.join(self.case_dir, l), cases)
        if cases:
            self.iter_case = iter(cases)
    
    def get_group(self):
        casefile = "a.txt"
        if casefile is not None:
            casefile = casefile.replace('\n','')
            tf =tempfile.mktemp() 
            with open (tf,'w') as tmf:
                with open(casefile,'r') as fff:
                    for line in fff.readlines():
                        if re.search(r' , ',line) and not re.search(r'=', line):
                            lines=' '+line
                        elif re.search(r'.bmp',line) and not re.search(r'=',line):
                            lines=' '+line
                        else:
                            lines=line
                        tmf.write('%s' %lines)
                tmf.seek(0)         
        
            case_name = os.path.basename(casefile)
            cf = ConfigParser.ConfigParser()
            cf.read(tf)
            case_io={}
            List_sections=[]
            for sections in cf.sections():
                List_sections.append(sections)
            sorted_section_list=[]
    
            for i in List_sections:
                if re.match(r'Stream_\d+',i):
                    try:
                        next_item = List_sections[List_sections.index(i)+1]
                    except IndexError:
                        pass
                    if re.match(r'SOutput_\d', next_item):
                        ID = i.split('_')
                        group = 'Stream_%s' % ID[-1]
    
                        sorted_section_list.append(group)
                        List_io = {'%s' % next_item:cf.items(next_item),'%s' % i:cf.items(i)}
                        case_io[group] = List_io
                    else:
                        sorted_section_list.append(i)
                        case_io[i]=cf.items(i)
                    
                elif re.match(r'Input_\d+',i):
                    if 'irfile' in cf.options(i):
                        irfile = os.path.join(self.main_path,'caseInfo','Case_irfile',cf.get(i, 'IRFile'))
                        with open(irfile, 'r') as f:
                            key_list = f.read()
                            cf.set(i, 'IRFile', key_list)
                    next_item = List_sections[List_sections.index(i)+1]
                    ID = i.split('_')
                    group = 'GROUP_%s' % ID[-1]
                    sorted_section_list.append(group)
                    List_io = {'%s' % next_item:cf.items(next_item),'%s' % i:cf.items(i)}
                    case_io[group] = List_io
                elif re.match(r'.*Output_\d',i):
                    pass
                else:
                    raise Exception('invalid input:%s' %i)
            
            return case_name, sorted_section_list, case_io
        else:
            return None
    
    def iterForCaseList(self):
        try:
            case_file = self.iter_case.next()
        except StopIteration:
            return None
        
        return case_file
       
class main():
    def main(self):
    
        main_dir = os.getcwd()
        #main_dir=os.path.join(os.getcwd(), 'TMP')
        print main_dir
        logging_ins = app_lib.CollectSysLoging()
        logging_ins.addSysLog(os.path.join(os.getcwd(), 'SYS_LOG', 'APP_sys_log.txt'))
        logger_obj = logging_ins.getLogger()
        
        config_ins = app_lib.ParseConfigFile(main_dir)
        config_ins.readConfigFile()
        
        statis_ins = app_lib.StatisticsCaseCount()
        app_lib.ParseIrkey()
        parse_tc_ins = app_lib.parseCase.ParseCase(main_dir, logger_obj)
        case_info = parse_tc_ins.get_group()
        
        app_lib.pKill(logger_obj)
    #     print case_info
        while case_info is not None:
            case_name = case_info[0]
            case_items= case_info[1]
            case_content = case_info[2]
              
            logger_obj.info("run case: <%s>" % case_name)
            log_folder = statis_ins.log_folder
            case_inst = app_lib.CaseLog(case_name, log_folder)        
            case_exec = app_lib.ExecCase(main_dir, logger_obj, case_inst, log_folder)
            duration, ret = case_exec.exec_case_group(case_items, case_content)
            app_lib.CaseFactory(timestamp = case_inst.curr_time, test_name = case_name, 
                                exit_status = ret[0], failure_reason = ret[1], duration = duration, notes = '')
            case_info = parse_tc_ins.get_group()
          
        app_lib.CaseFactory.send_report(statis_ins.curr_time)
          
        logger_obj.info('all case done!')
        logging_ins.closeHnadler()
        
if __name__ == '__main__':
    test=send_key()
    test.send_one_key('MENU')
    test.send_one_key('EXIT')
    main().main()
    