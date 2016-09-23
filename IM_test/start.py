import os
import app_lib


def main():
    
    main_dir = os.getcwd()
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
    app_lib.pKill(logger_obj, process = "ttermpro.exe")
    while case_info is not None:
        if case_info[0] == 'NonExist':
            case_name = case_info[1]
            logger_obj.info("run case: <%s>" % case_name)
            log_folder = statis_ins.log_folder
            case_inst = app_lib.CaseLog(case_name, log_folder)
            ret = ('FAIL', 'case file is not existed')
            statis_ins.add_case_result(case_name, ret)
            app_lib.CaseFactory(timestamp = case_inst.curr_time, test_name = case_name, 
                            exit_status = ret[0], failure_reason = ret[1], duration = 0, notes = '')
        else:
            case_name = case_info[0]
            case_items = case_info[1]
            case_content = case_info[2]
              
            logger_obj.info("run case: <%s>" % case_name)
            log_folder = statis_ins.log_folder
            case_inst = app_lib.CaseLog(case_name, log_folder)        
            case_exec = app_lib.ExecCase(main_dir, logger_obj, case_inst, log_folder)
            duration, ret = case_exec.exec_case_group(case_items, case_content)
            statis_ins.add_case_result(case_name, ret)
            app_lib.CaseFactory(timestamp = case_inst.curr_time, test_name = case_name, 
                                exit_status = ret[0], failure_reason = ret[1], duration = duration, notes = '')
        case_info = parse_tc_ins.get_group()
        
    statis_ins.add_statistics_result()
    app_lib.CaseFactory.send_report(statis_ins.curr_time)
          
    logger_obj.info('all case done!')
    logging_ins.closeHnadler()
    
if __name__ == '__main__':
    main()