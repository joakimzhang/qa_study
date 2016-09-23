# coding=utf8
'''
Created on 

@author: zhangq
'''
from ConfigParser import SafeConfigParser
from tools import StringCap
from tools import FilterMem
import pygal


def get_info():
    parser = SafeConfigParser()
    parser.read("config/conf.txt")
    name = parser.get("mem_cap", "case_name")
    version = parser.get("mem_cap", "svn_version")
    keyword = parser.get("mem_cap", "keyword")
    command = parser.get("mem_cap", "command")
    period = parser.get("mem_cap", "period")
    port = parser.get("mem_cap", "port")
    baudrate = parser.get("mem_cap", "baudrate")
    new = FilterMem(int(port), int(baudrate))
    new.send_thread(command, int(period))
    file_name = r"%s_%s" % (name, version)
    new.getmem(keyword, file_name)
    # cap = StringCap.string_test()
    print 'heelo'


if __name__ == "__main__":
    get_info()