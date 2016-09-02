# coding:utf8
import string
'''
@author: zhangq
'''

def string_test():
    s = "this is just a practice"
    # 首字母大写
    print s.capitalize()
    # capword用法
    print string.capwords(s)
    # capword的实现方法
    print ' '.join(x.capitalize() for x in s.split(' '))

