import sys
import os
import datetime
import globalVariable

def sys_exitfunc(error_no,logger_obj):
    '''sys_exitfunc(error num, system logger)
    Input error number and error information to system log after exit.
    '''
    exit_msg = 'Abort system with exited number (%d)' %error_no
    logger_obj.error(LogMsgFormat.setSysLogFmt('[System]',exit_msg))
    sys.exit(error_no)

class LogMsgFormat():
    '''
    This functions:
    -- setSysLogFmt(title, message) : Set format for system log.
    '''

    @staticmethod
    def setSysLogFmt(title,msg):
        return title.ljust(17) + ' -- %s' %msg

class CaseLog(object):
    
    def __init__(self, case_name,case_folder):
        self.curr_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.case_log_name = case_name + '_' + self.curr_time + '.log'
        self.case_dir = os.path.join(case_folder,case_name)
        if not os.path.exists(self.case_dir):
            os.mkdir(self.case_dir)
        self.abs_case_log = os.path.join(self.case_dir, self.case_log_name)
        self.case_handler = open(self.abs_case_log, 'a+')
        globalVariable.serial_config['case_name'] = case_name

    def closeFile(self):
        self.case_handler.close()

class StatisticsCaseCount():
    '''Statistics report operations.
    This functions:
    -- writeDataToFile() : Add statistics info to file SDKAT_stats_report.txt
    '''
    
    def __init__(self):
        self.curr_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.log_folder = os.path.join(os.getcwd(), 'CASE_LOG', self.curr_time)
        if not os.path.exists(self.log_folder):
            os.mkdir(self.log_folder)
        case_statistics = 'case_statistics.log'
        abs_case_statistics = os.path.join(self.log_folder, case_statistics)
        self.case_statis_handler = open(abs_case_statistics, 'a+') 
        self.line_format = '{0:<40}{1:<40}{2:<40}'
        self.add_title()
    
    def add_title(self):
        self.case_statis_handler.write(self.line_format.format('Case Name', 'Result', 'Reason') + '\n')
        
    def add_case_result(self, case_name, result):
        self.case_statis_handler.write(self.line_format.format(case_name, result[0], result[1] if result[1] != 'success' else '') + '\n')
        self.case_statis_handler.flush()
        
    def add_statistics_title(self):
        self.case_statis_handler.write(self.line_format.format('Total', 'PASS[%]', 'FAIL[%]') + '\n')
    
    def add_statistics_result(self):
        self.case_statis_handler.write('\n\n')
        self.case_statis_handler.write('='*110 + '\n')
        self.add_statistics_title()
        Pass = globalVariable.serial_config['case_num']['passed']
        Fail = globalVariable.serial_config['case_num']['failed']
        Total = Pass + Fail
        if Total != 0:
            pass_rate = float(Pass)/Total
            fail_rate = float(Fail)/Total
        else:
            pass_rate = 0
            fail_rate = 0
        self.case_statis_handler.write(self.line_format.format(Total, '%s[%s]'%(Pass,float('%.2f'%(pass_rate))*100), '%s[%s]'%(Fail,float('%.2f'%(fail_rate))*100)))
        self.case_statis_handler.close()