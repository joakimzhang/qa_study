# coding:utf8
'''
Created on 2016年9月7日

@author: zhangq
'''
import re
import MySQLdb
from __builtin__ import file
import struct
import binascii
import os
import hashlib
import xlrd


class MysqlTool(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1",
                                    user="root",
                                    passwd="Avl1108",
                                    db="hdcp_new")
        self.cursor = self.conn.cursor()
        self.table_exist()

    def table_exist(self):
        sql_table_num = (
            "select count(*) from information_schema.tables"
            " where table_schema='hdcp_new'")
        self.cursor.execute(sql_table_num)
        table_num = self.cursor.fetchone()[0]
        if not table_num:
            self.create_table()

    def create_table(self):
        _sql_1x_tx = "create table if not exists 1x_tx(\
            id int not null auto_increment, value varchar(2000),\
            is_use enum('yes', 'no'), primary key(id))"
        _sql_1x_rx = "create table if not exists 1x_rx(\
            id int not null auto_increment, value varchar(2000),\
            is_use enum('yes', 'no'), primary key(id))"
        _sql_2x_rx = "create table if not exists 2x_rx(\
            id int not null auto_increment, value varchar(2000),\
            is_use enum('yes', 'no'), primary key (id))"
        _sql_2x_tx = "create table if not exists 2x_tx(\
            id int not null auto_increment, value varchar(2000),\
            is_use enum('yes', 'no'), primary key (id))"
        _sql_statistics = "create table if not exists statistics(\
            type enum('1x_tx', '1x_rx', '2x_tx', '2x_rx'),\
            total int, left_num int, start_id int)"
        _sql_insert_statistics = (
            "insert into statistics values('1x_tx',0,0,0),\
            ('1x_rx',0,0,0),('2x_tx',0,0,0),('2x_rx',0,0,0)")
        _sql_mac = "create table if not exists mac_addr(\
            id int not null auto_increment, mac_value varchar(16),\
            primary key (id))"
        _sql_file_md5 = "create table if not exists file_md5(\
            md5_value varchar(2000),file_name varchar(2000))"

        self.cursor.execute(_sql_file_md5)
        self.cursor.execute(_sql_1x_tx)
        self.cursor.execute(_sql_1x_rx)
        self.cursor.execute(_sql_2x_rx)
        self.cursor.execute(_sql_2x_tx)
        self.cursor.execute(_sql_statistics)
        self.cursor.execute(_sql_insert_statistics)
        self.cursor.execute(_sql_mac)
        self.conn.commit()

    def insert_key(self, table, value):
        _sql = "insert into %s(value, is_use) values('%s', 'no')" % (
            table, str(value))
        # print _sql
        self.cursor.execute(_sql)
        self.conn.commit()

    def update_statistic(self, table, left_num):
        _sql = ("update statistics set left_num=%s where type='%s'") % (left_num, table)
        self.cursor.execute(_sql)
        self.conn.commit()

    def select_left_num(self, table):
        _sql = "select left_num from statistics where type='%s'" % table
        self.cursor.execute(_sql)
        return self.cursor.fetchone()[0]

    def md5_exist(self, _md5_value):
        _sql = "select md5_value from file_md5 where md5_value='%s'" % _md5_value
        self.cursor.execute(_sql)
        if self.cursor.fetchone():
            return 1
        else:
            return 0

    def insert_md5(self, _md5):
        _sql = "insert into file_md5(md5_value) values('%s')" % _md5
        self.cursor.execute(_sql)
        self.conn.commit()

    def select_key(self, table, id):
        _sql = "select * from %s where id=%s" % (table, id)
        self.cursor.execute(_sql)
        select_result = self.cursor.fetchone()
        print select_result
        self.conn.commit()

class HdcpTool(MysqlTool):
    def __init__(self):
        print "hdcp_tool start"
        self.key_type = "2x_rx"
        super(HdcpTool, self).__init__()

    def import_bin(self, path):
        bin_size = os.path.getsize(path)
        with open(path, "rb") as f:
            bin_all = f.read()
            md5_sum = self.md5_lib(bin_all)
            _md5_exist = self.md5_exist(md5_sum)
            print _md5_exist
            if _md5_exist:
                print "the bin file has been imported"
                return
            # seek to 0
            f.seek(0)
            if self.key_type == "1x_tx" or self.key_type == "1x_rx":
                if (bin_size-4) % 308 != 0:
                    print "the file size is wrong,please check"
                    return
                head_1x = f.read(4)
                tag_1x = bytearray(head_1x)[0]
                if tag_1x == 1:
                    table = "1x_tx"
                else:
                    table = "1x_rx"
                left_num = self.select_left_num(table)
                while 1:
                    _hash = f.read(20)
                    _key = f.read(288)
                    if not _hash:
                        print "the key hash is not right"
                        break
                    key_value = binascii.hexlify(_key)
                    self.insert_key(table, key_value)
                    left_num = left_num + 1
                    # print struct.unpack('i',_file)
                    # break
                self.update_statistic(table, left_num)
            if self.key_type == "2x_rx" or self.key_type == "2x_tx":
                if (bin_size-40) % 862 != 0:
                    print "the file size is wrong,please check"
                    print (bin_size-40) % 862
                    return
                head_2x = f.read(40)
                tag_2x = bytearray(head_2x)[3]
                if tag_2x == 1:
                    table = "2x_tx"
                else:
                    table = "2x_rx"
                left_num = self.select_left_num(table)
                while 1:
                    _key = f.read(862)
                    if not _key:
                        break
                    key_value = binascii.hexlify(_key)
                    self.insert_key(table, key_value)
                    left_num = left_num + 1
                self.update_statistic(table, left_num)
            self.insert_md5(md5_sum)

    def hash_lib(self, data):
        hash_obj = hashlib.sha1()
        hash_obj.update(data)
        return hash_obj.hexdigest()

    def md5_lib(self, data):
        md5_obj = hashlib.md5()
        md5_obj.update(data)
        return md5_obj.hexdigest()
    
    def export(self):
         table = "1x_rx"
         for i in range(3,10):
             self.select_key(table, i)
        
        
        
        
    def load_excel_form(self, file_name):
        try:
            data = xlrd.open_workbook(file_name)
        except:
            print "打开文件格式不对!"
            return
        table = data.sheets()[0]
        apply_date = (xlrd.xldate.xldate_as_datetime(table.cell(1,2).value, 0)).strftime( '%Y-%m-%d')
        print apply_date
        department = table.cell(1,7).value
        print department
        apply_person = table.cell(2,2).value
        print apply_person
        review_person = table.cell(2,7).value
        print review_person
        usage = table.cell(3,4).value
        print usage
        key_source = table.cell(5,4).value
        print key_source
        key_content = table.cell(7,4).value
        print key_content
        tx = table.cell(9,5).value
        print tx
        rx = table.cell(9,8).value
        print rx
        inner_model = table.cell(11,4).value
        print inner_model
        chip_num = table.cell(12,4).value
        print chip_num
        test_engineer = table.cell(14,4).value
        print test_engineer
        No = table.cell(16,0).value
        print No
        contractor = table.cell(16,1).value
        print contractor
        lot_id = table.cell(16,3).value
        print lot_id
        wafers = table.cell(16,5).value
        if type(wafers)==float:
            wafers = str(int(wafers))
        print wafers


if __name__ == "__main__":
    # new = MysqlTool()
    new_tool = HdcpTool()
    #new_tool.import_bin("2x_rx.bin")
    #new_tool.load_excel_form("Hdcp_key_SFH820.xlsx")
    new_tool.export()
    