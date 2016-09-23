import os, sys
import ConfigParser

import globalVariable

_config = None

class UITestError(Exception):
    """The test script had an unrecoverable error."""
    pass

class ConfigurationError(UITestError):
    pass

def _xdg_config_dir():
#     return os.environ.get('XDG_CONFIG_HOME', '%s/.config' % os.environ['HOME'])
    return os.path.dirname(os.getcwd())


def _config_init(force=False):
    global _config
    if force or not _config:
        config = ConfigParser.SafeConfigParser()
        config.readfp(
            open(os.path.join(os.getcwd(), 'appConfig.cfg')))
        config.read([
            '%s/appConfig.cfg' % _xdg_config_dir(),
            # Config files specific to the test suite / test run:
            os.environ.get('STBT_CONFIG_FILE', ''),
        ])
        _config = config
    return _config

def get_config(section, key, default=None, type_=str):
    """Read the value of `key` from `section` of the IM config file.

    Raises `ConfigurationError` if the specified `section` or `key` is not
    found, unless `default` is specified (in which case `default` is returned).
    """

    config = _config_init()

    try:
        return type_(config.get(section, key))
    except ConfigParser.Error as e:
        if default is None:
            raise ConfigurationError(e.message)
        else:
            return default
    except ValueError:
        raise ConfigurationError("'%s.%s' invalid type (must be %s)" % (
            section, key, type_.__name__))

class MatchParameters(object):
    '''
    parse image match configure
    '''
    def __init__(self, match_method=None, match_threshold=None,
                 confirm_method=None, confirm_threshold=None,
                 erode_passes=None):
        if match_method is None:
            match_method = get_config('match', 'match_method')
        if match_threshold is None:
            match_threshold = get_config(
                'match', 'match_threshold', type_=float)
        if confirm_method is None:
            confirm_method = get_config('match', 'confirm_method')
        if confirm_threshold is None:
            confirm_threshold = get_config(
                'match', 'confirm_threshold', type_=float)
        if erode_passes is None:
            erode_passes = get_config('match', 'erode_passes', type_=int)

        if match_method not in (
                "sqdiff-normed", "ccorr-normed", "ccoeff-normed"):
            raise ValueError("Invalid match_method '%s'" % match_method)
        if confirm_method not in ("none", "absdiff", "normed-absdiff"):
            raise ValueError("Invalid confirm_method '%s'" % confirm_method)

        self.match_method = match_method
        self.match_threshold = match_threshold
        self.confirm_method = confirm_method
        self.confirm_threshold = confirm_threshold
        self.erode_passes = erode_passes

class ParseConfigFile(object):

    def __init__(self, prj_dir, file_name = 'appConfig.cfg', capture_conf = 'system.ini'):
        self.prj_dir = prj_dir
        self.cfg_file_name = file_name
        self.capture_conf = os.path.join(prj_dir, 'videoCapture', capture_conf)
        cfg_file_abspath = os.path.join(self.prj_dir, self.cfg_file_name)
        self.config = ConfigParser.ConfigParser()
        try:
            self.cfg_fp = open(cfg_file_abspath,"r")
            self.config.readfp(self.cfg_fp)
        except Exception,e:
            print e
            sys.exit(-1)
        self.chgConfig()
            
    def chgConfig(self):
        kwargs = {}
        if self.config.has_section('video_capture'):
            if self.config.has_option('video_capture', 'bSnapJpg'):
                kwargs['bSnapJpg'] = self.config.get('video_capture', 'bSnapJpg')
            if self.config.has_option('video_capture', 'bMultiPic'):
                kwargs['bMultiPic'] = self.config.get('video_capture', 'bMultiPic')
            if self.config.has_option('video_capture', 'strSnapDur'):
                kwargs['strSnapDur'] = self.config.get('video_capture', 'strSnapDur')
            if self.config.has_option('video_capture', 'nMultiPicNum'):
                kwargs['nMultiPicNum'] = self.config.get('video_capture', 'nMultiPicNum')
        with open(self.capture_conf, 'r') as f:
            lines = f.readlines()
        try:
            with open(self.capture_conf, 'w') as f:
                for key in kwargs:
                    lines[:] = map(lambda l: l.replace(l, '%s=%s\r\n'%(key,kwargs[key]) if key in l else l),lines)
                for line in lines:
                    f.write(line)
        except Exception, e:
            print e
            sys.stderr('modify video capture config file error!')
            
    def parseConfigItem(self, section, item, item_type='get'):
        if self.self.config.has_section(section):
            if self.self.config.has_option(section, item):
                    return getattr(self.config, item_type)('platform', 
                                                           'target_type')
            else:
                return False
        else:
            False

    def readConfigFile(self):
        '''Parse configure file
        Get global user-defined argument through parsing configure file,
        configure file absolute path C:\TL_AUTO\AutoSDKself.config.cfg
        Content of configure file:
        -- [serial] : All variables about serial connection.
        -- [connection] : Connection times
        -- [prompt] : Prompt characters of OS, (bootloader is "Libra>", 
                      testshell is "###>", linux is "/.*#").
        -- [test_case] : All variables about test case running.
        -- [log_info] : Log path. (system log path is C:\SDKAT_sys_log.txt
                                   case log path is C:\TL_AUTO\CASE_LOG)
        '''

        if self.config.has_section('platform'):
            if self.config.has_option('platform', 'target_type'):
                globalVariable.serial_config['target_type'] = \
                self.config.get('platform', 'target_type')
            else:
                globalVariable.serial_config['df_exec_times'] = 1
        if self.config.has_section('serial'):
            if self.config.has_option('serial', 'serial_port'):
                globalVariable.serial_config['serial_port'] = \
                self.config.get('serial','serial_port')
            else:
                raise RuntimeError("Argument serial_port is missing")

            if self.config.has_option('serial', 'baudrate'):
                globalVariable.serial_config['baudrate'] = \
                self.config.getint('serial', 'baudrate')
            else:
                raise RuntimeError("Argument baudrate is missing")

            if self.config.has_option('serial', 'xonxoff'):
                globalVariable.serial_config['xonxoff'] = \
                self.config.getint('serial', 'xonxoff')
            else:
                raise RuntimeError("Argument xonxoff is missing")

            if self.config.has_option('serial', 'timeout'):
                globalVariable.serial_config['timeout'] = \
                self.config.getint('serial', 'timeout')
            else:
                raise RuntimeError("[Exception] : Argument timeout is missing")
            
            if self.config.has_option('serial', 'reboot_delay'):
                globalVariable.serial_config['reboot_delay'] = \
                self.config.getint('serial', 'reboot_delay')
            else:
                raise RuntimeError("[Exception] : Argument reboot_delay is missing")

        if self.config.has_section('testcase'):
            if self.config.has_option('testcase', 'testcase_list'):
                globalVariable.TC_LIST_FILE = \
                self.config.get('testcase', 'testcase_list')
            else:
                globalVariable.TC_LIST_FILE = ''

        if self.config.has_section('connection'):
            if self.config.has_option('connection', 'conn_times'):
                globalVariable.serial_config['conn_times'] = \
                self.config.getint('connection', 'conn_times')
            else:
                globalVariable.serial_config['conn_times'] = 3

            if self.config.has_option('connection', 'reboot_switch'):
                globalVariable.REBOOT_SWITCH = \
                self.config.getboolean('connection', 'reboot_switch')
            else:
                globalVariable.REBOOT_SWITCH = True

        if self.config.has_section('prompt'):
                globalVariable.serial_config['bl_prompt'] = \
                self.config.get('prompt', 'bl_prompt')
                globalVariable.serial_config['ts_prompt'] = \
                self.config.get('prompt', 'ts_prompt')
                globalVariable.serial_config['lx_prompt'] = \
                self.config.get('prompt', 'lx_prompt')
        else:
            raise RuntimeError("[Exception] : Section prompt is missing")

        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'df_exec_times'):
                globalVariable.serial_config['df_exec_times'] = \
                self.config.getint('test_case', 'df_exec_times')
            else:
                globalVariable.serial_config['df_exec_times'] = 1

        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'testcase_list'):
                globalVariable.TC_LIST_FILE = \
                self.config.get('test_case', 'testcase_list')
            else:
                globalVariable.TC_LIST_FILE = ''
        
        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'tp_lock_cmd'):
                globalVariable.TP_LOCK_CMD = \
                self.config.get('test_case', 'tp_lock_cmd')
            else:
                globalVariable.TP_LOCK_CMD = ''
        
        
        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'ignore_failed_case'):
                globalVariable.serial_config['flag_ifc'] = \
                self.config.getboolean('test_case', 'ignore_failed_case')
        
        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'failed_case_exec_times'):
                globalVariable.FAILED_CASE_EXEC_TIMES =  \
                self.config.getint('test_case', 'failed_case_exec_times')
            else:
                globalVariable.FAILED_CASE_EXEC_TIMES = 0
        else:
            globalVariable.FAILED_CASE_EXEC_TIMES = 0

        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'reboot_during_case'):
                globalVariable.CASE_REBOOT_SWITCH = \
                self.config.getboolean('test_case', 'reboot_during_case')

        if self.config.has_section('test_case'):
            if self.config.has_option('test_case', 'max_execute_time'):
                globalVariable.MAX_EXEC_TIME = \
                self.config.getint('test_case', 'max_execute_time')

        #Parse section [loadfile]
        if self.config.has_section('loadfile'):
            if self.config.has_option('loadfile', 'load_bootloader'):
                globalVariable.LOAD_BOOT = \
                self.config.get('loadfile', 'load_bootloader')

        if self.config.has_section('loadfile'):
            if self.config.has_option('loadfile', 'load_kernel'):
                globalVariable.LOAD_KERNEL = \
                self.config.get('loadfile', 'load_kernel')

        if self.config.has_section('loadfile'):
            if self.config.has_option('loadfile', 'load_rootfs'):
                globalVariable.LOAD_ROOTFS = \
                self.config.get('loadfile', 'load_rootfs')
        #Parse section [svn_account]
        if self.config.has_section('svn_info'):
            if self.config.has_option('svn_info', 'svn_server'):
                globalVariable.SVN_SERVER = \
                self.config.get('svn_info', 'svn_server')
        if self.config.has_section('svn_info'):
            if self.config.has_option('svn_info', 'svn_user'):
                globalVariable.SVN_USER = \
                self.config.get('svn_info', 'svn_user')

        if self.config.has_section('svn_info'):
            if self.config.has_option('svn_info', 'svn_passwd'):
                globalVariable.SVN_PASSWD = \
                self.config.get('svn_info', 'svn_passwd')
        if self.config.has_section('svn_info'):
            if self.config.has_option('svn_info', 'svn_path'):
                globalVariable.SVN_PATH = \
                self.config.get('svn_info', 'svn_path')
        
        if self.config.has_section('mail_pool'):
            if self.config.has_option('mail_pool', 'mail_list'):
                mails = self.config.get('mail_pool', 'mail_list')
                globalVariable.USER_MAIL_LIST.extend(mails.split(','))
                
            if self.config.has_option('mail_pool', 'cc_list'):
                cc = self.config.get('mail_pool', 'cc_list')
                globalVariable.USER_CC_LIST.extend(cc.split(','))
        
        if self.config.has_section('stream_card'):
            if self.config.has_option('stream_card', 'card_type'):
                globalVariable.CARD_TYPE = \
                self.config.get('stream_card', 'card_type')
            if self.config.has_option('stream_card', 'stream_host'):
                globalVariable.STREAM_HOST = \
                self.config.get('stream_card', 'stream_host')
            if self.config.has_option('stream_card', 'stream_port'):
                globalVariable.STREAM_PORT = \
                self.config.get('stream_card', 'stream_port')
        if self.config.has_section('match_control'):
            if self.config.has_option('match_control', 'duration'):
                globalVariable.DURARION = self.config.getint('match_control', 'duration')
                
        if self.config.has_section('apache'):
            if self.config.has_option('apache', 'server'):
                globalVariable.APACHE_SERVER = self.config.get('apache', 'server')

        return globalVariable.serial_config
