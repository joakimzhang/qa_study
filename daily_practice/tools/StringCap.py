# coding:utf8
import string
import binascii
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

def string_templete():
    s = "this is just a prictice"
    # 生成转换表
    pattern = string.maketrans("abcd", "1234")
    pattern2 = string.maketrans("1234", "abcd")
    # 完成替换
    s1 = s.translate(pattern)
    s2 = s1.translate(pattern2)
    print s1
    print s2


def format_string():
    s = 1234
    print "%x" % s


def str_newline():
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\
             " aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
def bytearray_test():
    str = "aaaaaaaaaa"
    with open("1x_tx.bin", "rb") as f:
        tag = f.read(4)
        print bytearray(tag)[0]
        print binascii.hexlify(tag)[0]
    with open("1x_rx.bin", "rb") as f:
        tag = f.read(4)
        print bytearray(tag)[0]
        print binascii.hexlify(tag)[0]
    print bytearray(str)
