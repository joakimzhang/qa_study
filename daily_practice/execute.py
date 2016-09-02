# coding=utf8
'''
Created on 2016��9��2��

@author: zhangq
'''
from ConfigParser import SafeConfigParser
from tools import StringCap
from tools import GetMem


def get_config():
    parser = SafeConfigParser()
    parser.read("config/conf.txt")
    print parser.get("mem_cap", "name", "time")
    cap = StringCap.string_test()
    print 'heelo'
    
if __name__ == "__main__":
    get_config()


