import os
import re
import ConfigParser
import tempfile
import time

import globalVariable

class CaseInfo():
    _values = []
    def __init__(self, ts = None, case_name = None, exit_status = None, duration = None, note = ''):
        self._values.append((ts, case_name, exit_status, duration, note))


class ParseCase(object):
    def __init__(self, main_path = '', logger = None):
        self.main_path = main_path
        self.caseInfo_dir = os.path.join(self.main_path, 'caseInfo')
        self.case_list_file = os.path.join(self.main_path,'caseInfo', self.chose_caselist())
        self.case_dir = os.path.join(self.main_path,'caseInfo', 'Case')
        self.logger = logger
        cases = self.extract_case(self.case_list_file)
        print cases
        if cases:
            self.iter_case = iter(cases)
    
    def chose_caselist(self):
        caselist_files = []
        for f in os.listdir(self.caseInfo_dir):
            f_abs = os.path.join(self.caseInfo_dir, f)
            if os.path.isfile(f_abs):
                caselist_files.append(f)
        print '#'*80
        for cf in caselist_files:
            print cf
        print '#'*80
        caselist_file = raw_input('please chose the caselist file to run:')
        print 'your choice is: ', caselist_file
        return caselist_file.strip()
    
    def extract_case(self, file_name = 'caselist.txt'):
        def find_comment(cases):
            comm = [idx for idx, l in enumerate(cases) if l.startswith('/*') or l.startswith('*/')]
            if comm:
                del_indexs = []
                for item in zip(comm[::2],comm[1::2]):
                    del_indexs.extend(range(item[0],item[1]+1))
                
                filter_cases = [l for idx,l in enumerate(cases) if idx not in del_indexs ]
            else:
                filter_cases = cases
            return filter_cases
        
        with open(file_name,'r') as cl:
            lines = cl.readlines()
            cases = filter(lambda l: l.strip(), lines)
            cases[:] = filter(lambda l: not l.startswith('#'), cases)
            filter_cases = find_comment(cases)
            filter_cases[:] = map(lambda l: os.path.join(self.case_dir, l.strip()), filter_cases)
            
        return filter_cases
    
    def get_group(self):
        casefile = self.iterForCaseList() 
        if casefile is not None:
            case_name = os.path.basename(casefile)
            casefile = casefile.replace('\n','')
            tf =tempfile.mktemp()
            try: 
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
            except IOError:
                globalVariable.serial_config['case_num']['failed'] += 1
                return 'NonExist', case_name
        
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


if __name__ == '__main__':
    main_dir = os.path.dirname(os.getcwd())
    
    case_inst = ParseCase(main_dir)
    print case_inst.iterForCaseList()
    print case_inst.iterForCaseList()

#   prinprint case_inst.get_group(main_dir,'D:\IM\ImageMatch\Case_Info\Case\CTA-1235.conf')
        
        
    