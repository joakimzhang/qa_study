# -*- coding: utf-8 -*-
import os
import sys
import hashlib
import re
import redis
import MySQLdb
import chardet
import ConfigParser
import subprocess
import shlex
import binascii
import xlrd
#import datetime
#from dateutil.parser import parse
from PyQt4 import QtGui, QtCore
from hashlib import sha256
from hmac import HMAC
import time
import threading
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def encrypt_password(password, salt=None):
    """Hash password on the fly."""
    if salt is None:
        salt = os.urandom(8) # 64 bits.

    assert 8 == len(salt)
    assert isinstance(salt, str)

    if isinstance(password, unicode):
        password = password.encode('UTF-8')

    assert isinstance(password, str)

    result = password
    for _ in xrange(10):
        result = HMAC(result, salt, sha256).digest()

    return salt + result

def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password, salt=hashed[:8])

def execCLI(cmd_line, shell=True):
        cmd_args = shlex.split(cmd_line, posix=False)
        cmd_exec =  subprocess.Popen(cmd_args,bufsize=0,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=shell)
        output,strrout= cmd_exec.communicate()
        cmd_exec.wait()
        return (cmd_exec.returncode, output, strrout)

class Ui_Register(QtGui.QDialog):
    def __init__(self, db, parent=None):
        self.db = db
        QtGui.QDialog.__init__(self, parent)
        self.resize(429, 253)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(60, 60, 261, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(60, 90, 231, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_2 = QtGui.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(60, 120, 231, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 150, 231, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(140, 200, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 200, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.reject)
        
        self.retranslateUi()
#         QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", u"注册管理员密码", None))
        self.label.setText(_translate("Dialog", u"初次使用，请注册管理员(admin)密码:", None))
        self.label_2.setText(_translate("Dialog", u"请再次输入:", None))
        self.pushButton.setText(_translate("Dialog", u"确定", None))
        self.pushButton_2.setText(_translate("Dialog", u"取消", None))
    
    def login(self):
        password_1 = str(self.lineEdit.text())
        password_2 = str(self.lineEdit_2.text())
        
        if not password_1 and not password_2:
            QtGui.QMessageBox.critical(self, 'Error', u'密码不能为空!')
            return
        if password_1 != password_2:
            QtGui.QMessageBox.critical(self, 'Error', u'两次输入密码不一致， 请重新输入!')
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        else:
            print 'write into db'
#             encr_pwd = encrypt_password(password_1)
            self.db.add_user('admin', password_1)
            self.accept()

class Ui_Login(QtGui.QDialog):
    def __init__(self, db, parent=None):
        self.db = db
        QtGui.QDialog.__init__(self, parent)
        self.resize(432, 257)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(60, 80, 61, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox = QtGui.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 361, 181))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(130, 130, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 130, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.reject)
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(90, 40, 191, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 80, 191, 21))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit.setPlaceholderText('username')
        self.lineEdit_2.setPlaceholderText('password')
        self.label_3 = QtGui.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(60, 120, 61, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        
        self.retranslateUi()
#         QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", u"HDCP Key 管理工具", None))
        self.label.setText(_translate("Dialog", u"用户名:", None))
        self.groupBox.setTitle(_translate("Dialog", u"登录", None))
        self.label_3.setText(_translate("Dialog", u"密码:", None))
        self.pushButton.setText(_translate("Dialog", u"确定", None))
        self.pushButton_2.setText(_translate("Dialog", u"取消", None))
    
    def login(self):
        try:
            password = self.db.get_ps(self.lineEdit.text())
        except redis.exceptions.ConnectionError:
            QtGui.QMessageBox.critical(self, 'Error', u'Redis server 没有运行!')
            return
        if password == None:
            QtGui.QMessageBox.critical(self, 'Error', u'用户名: "%s" 不存在!'%self.lineEdit.text())
        elif password == self.lineEdit_2.text():
            self.current_user = self.lineEdit.text()
            self.accept()
        else:
            QtGui.QMessageBox.critical(self, 'Error', u'密码不正确!')
            
#class WorkThread(QtCore.QThread):
 #   def __init__(self, parent = None, _func):
  #      super(WorkThread, self).__init__(parent)
   #     self.func = _func(
    #def run(self):
     #   _func()

        

class Ui_MainWindow(QtGui.QMainWindow):
    sinOut_err = QtCore.pyqtSignal(str) 
    sinOut_progress_bar = QtCore.pyqtSignal(int) 
    sinOut_info = QtCore.pyqtSignal(str, str)
    sinOut_enable = QtCore.pyqtSignal(bool) 
    sinOut_status = QtCore.pyqtSignal() 
    def __init__(self, redis, db, user, parent = None):
        self.redis_inst = redis
        self.db = db
        self.user = user
        QtGui.QMainWindow.__init__(self, parent)
        self.setObjectName(_fromUtf8("Dialog"))
        self.resize(942, 712)
        self.tabWidget = QtGui.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 30, 931, 661))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
  
        self.mac_pre = QtGui.QLineEdit(self.tab)
        self.mac_pre.setGeometry(QtCore.QRect(250, 110, 311, 23))
        self.mac_pre.setObjectName(_fromUtf8("mac_pre"))
        self.mac_button = QtGui.QPushButton(self.tab)
        self.mac_button.setGeometry(QtCore.QRect(630, 110, 75, 23))
        self.mac_button.setObjectName(_fromUtf8("mac_button"))
        self.mac_button.clicked.connect(self.mac_import)
        self.mac_label = QtGui.QLabel(self.tab)
        self.mac_label.setGeometry(QtCore.QRect(160, 110, 85, 23))
        self.mac_label.setObjectName(_fromUtf8("mac_label"))
        
        self.file_edit = QtGui.QLineEdit(self.tab)
        self.file_edit.setGeometry(QtCore.QRect(250, 150, 311, 23))
        self.file_edit.setObjectName(_fromUtf8("file_edit"))
        self.import_button = QtGui.QPushButton(self.tab)
        self.import_button.setGeometry(QtCore.QRect(630, 150, 75, 23))
        self.import_button.setObjectName(_fromUtf8("import_button"))
        self.import_button.clicked.connect(self.import_)
        
        
        #self.sinOut.connect(self.outText)
        self.sinOut_err.connect(self.warning)
        self.sinOut_progress_bar.connect(self.progress_bar)
        self.sinOut_info.connect(self.info)
        self.sinOut_enable.connect(self.enable)
        self.sinOut_status.connect(self.display_status)
        
        self.file_import = QtGui.QPushButton(self.tab)
        self.file_import.setGeometry(QtCore.QRect(160, 150, 90, 23))
        self.file_import.setObjectName(_fromUtf8("file_import"))
        self.file_import.clicked.connect(lambda: self.chose_file(1))
        
        self.key_version = QtGui.QLabel(self.tab)
        self.key_version.setGeometry(QtCore.QRect(160, 200, 71, 16))
        self.key_version.setObjectName(_fromUtf8("key_version"))
        self.x1 = QtGui.QRadioButton(self.tab)
        self.x1.setGeometry(QtCore.QRect(260, 200, 89, 16))
        self.x1.setObjectName(_fromUtf8("x1"))
        self.x2 = QtGui.QRadioButton(self.tab)
        self.x2.setGeometry(QtCore.QRect(400, 200, 89, 16))
        self.x2.setObjectName(_fromUtf8("x2"))
        
        self.key_version_group = QtGui.QButtonGroup()
        self.key_version_group.addButton(self.x1)
        self.key_version_group.addButton(self.x2)
        self.x1.setChecked(True)
        
        self.title_1x_tx_total = QtGui.QLabel(self.tab)
        self.title_1x_tx_total.setGeometry(QtCore.QRect(160, 260, 124, 16))
        self.title_1x_tx_total.setObjectName(_fromUtf8("title_1x_tx_total"))
        self.num_1x_tx_left = QtGui.QLabel(self.tab)
        self.num_1x_tx_left.setGeometry(QtCore.QRect(560, 260, 54, 16))
        self.num_1x_tx_left.setObjectName(_fromUtf8("num_1x_tx_left"))
        self.num_1x_rx_left = QtGui.QLabel(self.tab)
        self.num_1x_rx_left.setGeometry(QtCore.QRect(560, 300, 80, 16))
        self.num_1x_rx_left.setObjectName(_fromUtf8("num_1x_rx_left"))
        self.title_1x_tx_left = QtGui.QLabel(self.tab)
        self.title_1x_tx_left.setGeometry(QtCore.QRect(500, 260, 80, 16))
        self.title_1x_tx_left.setObjectName(_fromUtf8("title_1x_tx_left"))
        self.num_1x_tx_total = QtGui.QLabel(self.tab)
        self.num_1x_tx_total.setGeometry(QtCore.QRect(330, 260, 100, 16))
        self.num_1x_tx_total.setObjectName(_fromUtf8("num_1x_tx_total"))
        self.num_1x_rx_total = QtGui.QLabel(self.tab)
        self.num_1x_rx_total.setGeometry(QtCore.QRect(330, 300, 54, 16))
        self.num_1x_rx_total.setObjectName(_fromUtf8("num_1x_rx_total"))
        self.title_1x_rx_left = QtGui.QLabel(self.tab)
        self.title_1x_rx_left.setGeometry(QtCore.QRect(500, 300, 51, 16))
        self.title_1x_rx_left.setObjectName(_fromUtf8("title_1x_rx_left"))
        self.title_1x_rx_total = QtGui.QLabel(self.tab)
        self.title_1x_rx_total.setGeometry(QtCore.QRect(160, 300, 124, 16))
        self.title_1x_rx_total.setObjectName(_fromUtf8("title_1x_rx_total"))
        
        self.title_2x_tx_total = QtGui.QLabel(self.tab)
        self.title_2x_tx_total.setGeometry(QtCore.QRect(160, 340, 124, 16))
        self.title_2x_tx_total.setObjectName(_fromUtf8("title_2x_tx_total"))
        self.num_2x_tx_left = QtGui.QLabel(self.tab)
        self.num_2x_tx_left.setGeometry(QtCore.QRect(560, 340, 80, 16))
        self.num_2x_tx_left.setObjectName(_fromUtf8("num_2x_tx_left"))
        self.num_2x_rx_left = QtGui.QLabel(self.tab)
        self.num_2x_rx_left.setGeometry(QtCore.QRect(560, 380, 80, 16))
        self.num_2x_rx_left.setObjectName(_fromUtf8("num_2x_rx_left"))
        self.title_2x_tx_left = QtGui.QLabel(self.tab)
        self.title_2x_tx_left.setGeometry(QtCore.QRect(500, 340, 51, 16))
        self.title_2x_tx_left.setObjectName(_fromUtf8("title_2x_tx_left"))
        self.num_2x_tx_total = QtGui.QLabel(self.tab)
        self.num_2x_tx_total.setGeometry(QtCore.QRect(330, 340, 54, 16))
        self.num_2x_tx_total.setObjectName(_fromUtf8("num_2x_tx_total"))
        self.num_2x_rx_total = QtGui.QLabel(self.tab)
        self.num_2x_rx_total.setGeometry(QtCore.QRect(330, 380, 54, 16))
        self.num_2x_rx_total.setObjectName(_fromUtf8("num_2x_rx_total"))
        self.title_2x_rx_left = QtGui.QLabel(self.tab)
        self.title_2x_rx_left.setGeometry(QtCore.QRect(500, 380, 51, 16))
        self.title_2x_rx_left.setObjectName(_fromUtf8("title_2x_rx_left"))
        self.title_2x_rx_total = QtGui.QLabel(self.tab)
        self.title_2x_rx_total.setGeometry(QtCore.QRect(160, 380, 124, 16))
        self.title_2x_rx_total.setObjectName(_fromUtf8("title_2x_rx_total"))
        
        
        self.title_mac_total = QtGui.QLabel(self.tab)
        self.title_mac_total.setGeometry(QtCore.QRect(160, 420, 124, 16))
        self.title_mac_total.setObjectName(_fromUtf8("title_mac_total"))
        self.num_mac_left = QtGui.QLabel(self.tab)
        self.num_mac_left.setGeometry(QtCore.QRect(560, 420, 80, 16))
        self.num_mac_left.setObjectName(_fromUtf8("num_mac_left"))
        self.title_mac_left = QtGui.QLabel(self.tab)
        self.title_mac_left.setGeometry(QtCore.QRect(500, 420, 51, 16))
        self.title_mac_left.setObjectName(_fromUtf8("title_mac_left"))
        self.num_mac_total = QtGui.QLabel(self.tab)
        self.num_mac_total.setGeometry(QtCore.QRect(330, 420, 54, 16))
        self.num_mac_total.setObjectName(_fromUtf8("num_mac_total"))       
        
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        
        
        '''tab 2'''
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tableWidget = QtGui.QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 870, 60))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
#         self.tableWidget.itemClicked.connect(self.get_item_text)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget.setItem(1, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(1, 3, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(180)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0,175)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,175)
        self.tableWidget.setColumnWidth(3,268)
        self.tableWidget.setRowHeight(1, 28)
        
        '''tableWidget_2'''
        self.tableWidget_2 = QtGui.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(20, 80, 870, 390))
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_2.setRowCount(13)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
#         self.tableWidget_2.itemClicked.connect(self.get_item_text)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(0, 0, item)
        self.radio = QtGui.QRadioButton()        
        self.tableWidget_2.setCellWidget(0, 1, self.radio)
        self.radio_1 = QtGui.QRadioButton()      
        self.tableWidget_2.setCellWidget(0, 2, self.radio_1)
        self.radio_2 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(0, 3, self.radio_2)
        self.radio_1.setChecked(True)
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.radio)
        self.buttonGroup.addButton(self.radio_1)
        self.buttonGroup.addButton(self.radio_2)
        
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(2, 0, item)
        self.radio_3 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(1, 1, self.radio_3)
        self.radio_4 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(1, 2, self.radio_4)
        self.radio_3.setChecked(True)
        self.buttonGroup_1 = QtGui.QButtonGroup()
        self.buttonGroup_1.addButton(self.radio_3)
        self.buttonGroup_1.addButton(self.radio_4)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(3, 0, item)
        self.radio_5 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(3, 2, self.radio_5)
        self.radio_6 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(4, 2, self.radio_6)
        
        self.radio_20 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(5, 2, self.radio_20)
        self.radio_21 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(6, 2, self.radio_21)
        
        self.radio_5.setChecked(True)
        self.buttonGroup_2 = QtGui.QButtonGroup()
        self.buttonGroup_2.addButton(self.radio_5)
        self.buttonGroup_2.addButton(self.radio_6)
        self.buttonGroup_2.addButton(self.radio_20)
        self.buttonGroup_2.addButton(self.radio_21)
        
        
        self.radio_22 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(3, 4, self.radio_22)
        self.radio_23 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(4, 4, self.radio_23)
        
        self.radio_24 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(5, 4, self.radio_24)
        self.radio_25 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(6, 4, self.radio_25)
        
        self.radio_22.setChecked(True)
        self.buttonGroup_6 = QtGui.QButtonGroup()
        self.buttonGroup_6.addButton(self.radio_22)
        self.buttonGroup_6.addButton(self.radio_23)
        self.buttonGroup_6.addButton(self.radio_24)
        self.buttonGroup_6.addButton(self.radio_25)
        
        
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(4, 0, item)
        self.radio_7 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(2, 1, self.radio_7)
        self.radio_8 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(2, 2, self.radio_8)
        self.radio_9 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(2, 3, self.radio_9)
        self.radio_7.setChecked(True)
        self.buttonGroup_3 = QtGui.QButtonGroup()
        self.buttonGroup_3.addButton(self.radio_7)
        self.buttonGroup_3.addButton(self.radio_8)
        self.buttonGroup_3.addButton(self.radio_9)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(5, 0, item)
        
        
#         self.radio_10 = QtGui.QRadioButton()  
#         self.radio_11 = QtGui.QRadioButton()  
#         self.radio_10.setChecked(True)
# 
#         
#         self.buttonGroup_4 = QtGui.QButtonGroup()
#         self.buttonGroup_4.addButton(self.radio_10)
#         self.buttonGroup_4.addButton(self.radio_11)
#         self.buttonGroup_2.addButton(self.radio_15)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(6, 0, item)
        self.radio_12 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(7, 1, self.radio_12)
        self.radio_12.setChecked(True)
        self.radio_13 = QtGui.QRadioButton()  
        self.tableWidget_2.setCellWidget(7, 2, self.radio_13)
        self.buttonGroup_5 = QtGui.QButtonGroup()
        self.buttonGroup_5.addButton(self.radio_12)
        self.buttonGroup_5.addButton(self.radio_13)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(7, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(8, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_2.setItem(8, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(9, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_2.setItem(9, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(10, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_2.setItem(10, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(11, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_2.setItem(11, 1, item)
        
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(12, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget_2.setItem(12, 1, item)
        
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(3, 1, item)
        
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.tableWidget_2.setItem(3, 3, item)
        
        self.comboBox_3 = QtGui.QComboBox()
# #         self.comboBox.setGeometry(QtCore.QRect(130, 60, 101, 22))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_3.setEditable(True)
        self.tableWidget_2.setCellWidget(8, 1, self.comboBox_3)
        
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(170)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.setWordWrap(True)
        self.tableWidget_2.setSpan(0,3,1,2)
        self.tableWidget_2.setSpan(1,2,1,3)
        self.tableWidget_2.setSpan(2,3,1,2)
#         self.tableWidget_2.setSpan(7,2,1,2)
        self.tableWidget_2.setSpan(3,3,4,1)
        self.tableWidget_2.setSpan(3,1,4,1)
        self.tableWidget_2.setSpan(3,0,4,1)
        self.tableWidget_2.setSpan(7,0,2,1)
        self.tableWidget_2.setSpan(7,2,1,3)
        self.tableWidget_2.setSpan(8,2,1,3)
        
        for i in range(9, 13):
            self.tableWidget_2.setSpan(i,1,1,4)
            
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tableWidget_2.setColumnWidth(0,188)
        self.tableWidget_2.setRowHeight(11, 28)
        
        self.tableWidget_3 = QtGui.QTableWidget(self.tab_2)
        self.tableWidget_3.setGeometry(QtCore.QRect(20, 468, 870, 60))
        self.tableWidget_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_3.setRowCount(2)
        self.tableWidget_3.setColumnCount(4)
        self.tableWidget_3.horizontalHeader().setVisible(False)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(223)
        self.tableWidget_3.verticalHeader().setVisible(False)
        self.tableWidget_3.setWordWrap(True)
        self.tableWidget_3.setColumnWidth(0,50)
        self.tableWidget_3.setColumnWidth(1,110)
        self.tableWidget_3.setColumnWidth(2,110)
        self.tableWidget_3.setColumnWidth(3,598)
        self.tableWidget_3.setRowHeight(1,28)
        
        for i in range(0, 4):
            item = QtGui.QTableWidgetItem()
            item.setFlags(QtCore.Qt.NoItemFlags)
            self.tableWidget_3.setItem(0, i, item)
            item = QtGui.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
            self.tableWidget_3.setItem(1, i, item)
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.NoItemFlags)
#         self.tableWidget_3.setItem(0, 1, item)
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.NoItemFlags)
#         self.tableWidget_3.setItem(0, 2, item)
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.NoItemFlags)
#         self.tableWidget_3.setItem(0, 3, item)
        
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
#         self.tableWidget_3.setItem(1, 0, item)
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
#         self.tableWidget_3.setItem(1, 1, item)
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
#         self.tableWidget_3.setItem(1, 2, item)
#         item = QtGui.QTableWidgetItem()
#         item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
#         self.tableWidget_3.setItem(1, 3, item)
        
        self.file_edit_2 = QtGui.QLineEdit(self.tab_2)
        self.file_edit_2.setGeometry(QtCore.QRect(100, 555, 400, 25))
        self.file_edit_2.setObjectName(_fromUtf8("file_edit_2"))
        self.load_table = QtGui.QPushButton(self.tab_2)
        self.load_table.setGeometry(QtCore.QRect(17, 555, 75, 23))
        self.load_table.setObjectName(_fromUtf8("load_table"))
        self.load_table.clicked.connect(lambda: self.chose_file(2))
        
        self.file_edit_3 = QtGui.QLineEdit(self.tab_2)
        self.file_edit_3.setGeometry(QtCore.QRect(100, 585, 400, 25))
        self.file_edit_3.setObjectName(_fromUtf8("file_edit_3"))
        self.export_dir = QtGui.QPushButton(self.tab_2)
        self.export_dir.setGeometry(QtCore.QRect(17, 585, 75, 23))
        self.export_dir.setObjectName(_fromUtf8("export_dir"))
        self.export_dir.clicked.connect(lambda: self.chose_file(3))
        
        self.start_export = QtGui.QPushButton(self.tab_2)
        self.start_export.setGeometry(QtCore.QRect(780, 560, 75, 41))
        self.start_export.setObjectName(_fromUtf8("start_export"))
        self.start_export.clicked.connect(self.export)
        
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))     
        
        self.lot_id_label = QtGui.QLabel(self.tab_3)
        self.lot_id_label.setGeometry(QtCore.QRect(40, 60, 81, 21))
        self.lot_id_label.setObjectName(_fromUtf8("lot_id_label"))
        self.comboBox = QtGui.QComboBox(self.tab_3)
        self.comboBox.setGeometry(QtCore.QRect(130, 60, 101, 22))
        self.comboBox.setEditable(True)
        #         self.display_lot()
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.wafer_id = QtGui.QLabel(self.tab_3)
        self.wafer_id.setGeometry(QtCore.QRect(40, 100, 81, 21))
        self.wafer_id.setObjectName(_fromUtf8("wafer_id"))
        self.comboBox_2 = QtGui.QComboBox(self.tab_3)
        self.comboBox_2.setGeometry(QtCore.QRect(130, 100, 101, 22))
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.x_cor = QtGui.QLabel(self.tab_3)
        self.x_cor.setGeometry(QtCore.QRect(40, 140, 81, 21))
        self.x_cor.setObjectName(_fromUtf8("x_cor"))
        self.y_cor = QtGui.QLabel(self.tab_3)
        self.y_cor.setGeometry(QtCore.QRect(40, 180, 81, 21))
        self.y_cor.setObjectName(_fromUtf8("y_cor"))
        self.lineEdit_4 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(130, 140, 51, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.search_result = QtGui.QLabel(self.tab_3)
        self.search_result.setGeometry(QtCore.QRect(40, 235, 91, 16))
        self.search_result.setObjectName(_fromUtf8("search_result"))
        self.textBrowser = QtGui.QTextBrowser(self.tab_3)
        self.textBrowser.setGeometry(QtCore.QRect(40, 265, 390, 320))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.search_key = QtGui.QPushButton(self.tab_3)
        self.search_key.setGeometry(QtCore.QRect(320, 180, 75, 23))
        self.search_key.setObjectName(_fromUtf8("search_key"))
        self.search_key.clicked.connect(self.key_search)
        self.label_18 = QtGui.QLabel(self.tab_3)
        self.label_18.setGeometry(QtCore.QRect(190, 140, 16, 16))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.lineEdit_6 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(210, 140, 51, 20))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.lineEdit_5 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(130, 180, 51, 20))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_7 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_7.setGeometry(QtCore.QRect(210, 180, 51, 20))
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.label_19 = QtGui.QLabel(self.tab_3)
        self.label_19.setGeometry(QtCore.QRect(190, 180, 16, 16))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        
        self.search_lot = QtGui.QPushButton(self.tab_3)
        self.search_lot.setGeometry(QtCore.QRect(320, 60, 75, 23))
        self.search_lot.setObjectName(_fromUtf8("search_lot"))
        self.search_lot.clicked.connect(self.lot_search)
        
        self.line_2 = QtGui.QFrame(self.tab_3)
        self.line_2.setGeometry(QtCore.QRect(450, 0, 20, 650))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        
        #回收
        
        self.op_type = QtGui.QLabel(self.tab_3)
        self.op_type.setGeometry(QtCore.QRect(500, 90, 81, 20))
        self.op_type.setObjectName(_fromUtf8("op_type"))
        self.statis_search = QtGui.QPushButton(self.tab_3)
        self.statis_search.setGeometry(QtCore.QRect(780, 230, 75, 23))
        self.statis_search.setObjectName(_fromUtf8("statis_search"))
        self.statis_search.clicked.connect(self.op_record_search)
        self.user_ = QtGui.QLabel(self.tab_3)
        self.user_.setGeometry(QtCore.QRect(500, 50, 71, 20))
        self.user_.setObjectName(_fromUtf8("user_"))
        self.lineEdit_2 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(600, 50, 121, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.comboBox_4 = QtGui.QComboBox(self.tab_3)
        self.comboBox_4.setGeometry(QtCore.QRect(600, 90, 121, 22))
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_5 = QtGui.QComboBox(self.tab_3)
        self.comboBox_5.setGeometry(QtCore.QRect(600, 130, 121, 22))
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.comboBox_5.setEditable(True)
        self.inner_type = QtGui.QLabel(self.tab_3)
        self.inner_type.setGeometry(QtCore.QRect(500, 130, 91, 20))
        self.inner_type.setObjectName(_fromUtf8("inner_type"))
        self.date_ = QtGui.QLabel(self.tab_3)
        self.date_.setGeometry(QtCore.QRect(500, 170, 91, 20))
        self.date_.setObjectName(_fromUtf8("date_"))
        self.dateEdit = QtGui.QDateEdit(self.tab_3)
        self.dateEdit.setGeometry(QtCore.QRect(600, 170, 121, 22))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.dateEdit.setDateTime(self.dateEdit.dateTimeFromText('2015/3/1'))
        self.dateEdit_2 = QtGui.QDateEdit(self.tab_3)
        self.dateEdit_2.setGeometry(QtCore.QRect(740, 170, 121, 22))
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.dateEdit_2.setDateTime(self.dateEdit.dateTimeFromText(time.strftime('%Y/%m/%d',time.localtime())))
        self.label_49 = QtGui.QLabel(self.tab_3)
        self.label_49.setGeometry(QtCore.QRect(725, 170, 16, 20))
        self.label_49.setObjectName(_fromUtf8("label_49"))
        self.textBrowser_2 = QtGui.QTextBrowser(self.tab_3)
        self.textBrowser_2.setGeometry(QtCore.QRect(495, 265, 390, 320))
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.search_result_2 = QtGui.QLabel(self.tab_3)
        self.search_result_2.setGeometry(QtCore.QRect(500, 235, 91, 16))
        self.search_result_2.setObjectName(_fromUtf8("search_result_2"))
        
        #tab_4
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        
        
        self.line_3 = QtGui.QFrame(self.tab_4)
        self.line_3.setGeometry(QtCore.QRect(450, 0, 20, 650))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        
        self.op_history = QtGui.QLabel(self.tab_4)
        self.op_history.setGeometry(QtCore.QRect(40, 30, 91, 16))
        self.op_history.setObjectName(_fromUtf8("op_history"))
        self.textBrowser_3 = QtGui.QTextBrowser(self.tab_4)
        self.textBrowser_3.setGeometry(QtCore.QRect(40, 50, 390, 580))
        self.textBrowser_3.setObjectName(_fromUtf8("textBrowser_3"))
        
        self.admin_password = QtGui.QLabel(self.tab_4)
        self.admin_password.setGeometry(QtCore.QRect(520, 140, 65, 16))
        self.admin_password.setObjectName(_fromUtf8("admin_password"))
        self.lineEdit_10 = QtGui.QLineEdit(self.tab_4)
        self.lineEdit_10.setGeometry(QtCore.QRect(600, 140, 111, 20))
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.lineEdit_10.setEchoMode(QtGui.QLineEdit.Password)
        
        self.lot_id_2 = QtGui.QLabel(self.tab_4)
        self.lot_id_2.setGeometry(QtCore.QRect(520, 180, 61, 16))
        self.lot_id_2.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.tab_4)
        self.lineEdit.setGeometry(QtCore.QRect(600, 180, 111, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        
        self.input_again = QtGui.QLabel(self.tab_4)
        self.input_again.setGeometry(QtCore.QRect(520, 220, 65, 16))
        self.input_again.setObjectName(_fromUtf8("input_again"))
        self.lineEdit_11 = QtGui.QLineEdit(self.tab_4)
        self.lineEdit_11.setGeometry(QtCore.QRect(600, 220, 111, 20))
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))
        
        self.retrieve = QtGui.QPushButton(self.tab_4)
        self.retrieve.setGeometry(QtCore.QRect(770, 220, 75, 23))
        self.retrieve.setObjectName(_fromUtf8("retrieve"))
        self.retrieve.clicked.connect(self.retrieve_key)
        
        
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 887, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        User = self.menuBar.addMenu(u'&用户管理')
        add_delete = User.addAction(u'添加/删除用户')
        password = User.addAction(u'修改密码')
        if self.user != 'admin':
            add_delete.setDisabled(True) 
        self.menuBar.connect(add_delete, QtCore.SIGNAL('triggered()'), self.add_delete)
        self.menuBar.connect(password, QtCore.SIGNAL('triggered()'), self.change_password)
        self.setMenuBar(self.menuBar)
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(0, 690, 940, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        
        self.retranslateUi()
        self.display_status()
        self.combox_init()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", u"HDCP Key 管理工具", None))
        self.mac_label.setText(_translate("Dialog", u" 输入mac前缀：", None))
        self.file_import.setText(_translate("Dialog", u"导入bin文件：", None))
        self.mac_button.setText(_translate("Dialog", u"开始导入", None))
        self.import_button.setText(_translate("Dialog", u"开始导入", None))
        self.title_1x_tx_total.setText(_translate("Dialog", u"1.x Transmitter 总数：", None))
        self.num_1x_tx_left.setText(_translate("Dialog", "0", None))
        self.num_1x_rx_left.setText(_translate("Dialog", "0", None))
        self.title_1x_tx_left.setText(_translate("Dialog", u"剩余：", None))
        self.num_1x_tx_total.setText(_translate("Dialog", "0", None))
        self.num_1x_rx_total.setText(_translate("Dialog", "0", None))
        self.title_1x_rx_left.setText(_translate("Dialog", u"剩余：", None))
        self.title_1x_rx_total.setText(_translate("Dialog", u"1.x Receiver 总数:", None))
        self.key_version.setText(_translate("Dialog", u"key 版本：", None))
        
        self.title_2x_tx_total.setText(_translate("Dialog", u"2.x Transmitter 总数：", None))
        self.num_2x_tx_left.setText(_translate("Dialog", u"0", None))
        self.num_2x_rx_left.setText(_translate("Dialog", u"0", None))
        self.title_2x_tx_left.setText(_translate("Dialog", u"剩余", None))
        self.num_2x_tx_total.setText(_translate("Dialog", u"0", None))
        self.num_2x_rx_total.setText(_translate("Dialog", u"0", None))
        self.title_2x_rx_left.setText(_translate("Dialog", u"剩余", None))
        self.title_2x_rx_total.setText(_translate("Dialog", u"2.x Receiver 总数:", None))
        
        self.title_mac_total.setText(_translate("Dialog", u"Mac 总数：", None))
        self.title_mac_left.setText(_translate("Dialog", u"剩余：", None))
        self.num_mac_total.setText(_translate("Dialog", u"0", None))
        self.num_mac_left.setText(_translate("Dialog", u"0", None))
        
        self.x1.setText(_translate("Dialog", u"1.X", None))
        self.x2.setText(_translate("Dialog", u"2.X", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", u"导入Key", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Dialog", u"申请日期", None))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Dialog", u"所属部门", None))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("Dialog", u"申请人员", None))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("Dialog", u"此处待定", None))
        item = self.tableWidget_2.item(0, 0)
        item.setText(_translate("Dialog", u"领用类型", None))
        item = self.tableWidget_2.item(1, 0)
        item.setText(_translate("Dialog", u"KEY来源", None))  
        item = self.tableWidget_2.item(2, 0)
        item.setText(_translate("Dialog", u"KEY内容", None))
#         item = self.tableWidget_2.item(4, 0)
#         item.setText(_translate("Dialog", u"KEY版本", None))
        item = self.tableWidget_2.item(3, 0)
        item.setText(_translate("Dialog", u"KEY版本/类型", None))
        item = self.tableWidget_2.item(6, 0)
        item.setText(_translate("Dialog", u"", None))
        item = self.tableWidget_2.item(7, 0)
        item.setText(_translate("Dialog", u"有无内部型号", None))
        item = self.tableWidget_2.item(9, 0)
        item.setText(_translate("Dialog", u"需求片数", None))
        item = self.tableWidget_2.item(10, 0)
        item.setText(_translate("Dialog", u"需求key数", None))
        item = self.tableWidget_2.item(11, 0)
        item.setText(_translate("Dialog", u"单位", None))
        item = self.tableWidget_2.item(12, 0)
        item.setText(_translate("Dialog", u"测试工程师", None))
        
        item = self.tableWidget_3.item(0, 0)
        item.setText(_translate("Dialog", u"序号", None))
        item = self.tableWidget_3.item(0, 1)
        item.setText(_translate("Dialog", u"外包商", None))
        item = self.tableWidget_3.item(0, 2)
        item.setText(_translate("Dialog", u"批号", None))
        item = self.tableWidget_3.item(0, 3)
        item.setText(_translate("Dialog", u"片号", None))
        
        item = self.tableWidget_2.item(3, 1)
        item.setText(_translate("Dialog", u"TX", None))
        
        item = self.tableWidget_2.item(3, 3)
        item.setText(_translate("Dialog", u"RX", None))
        
        self.load_table.setText(_translate("Dialog", u"载入表格：", None))
        self.export_dir.setText(_translate("Dialog", u"导出目录：", None))
        self.start_export.setText(_translate("Dialog", u"开始导出", None))
        
        self.radio.setText(u'工程')
        self.radio_1.setText(u'量产')
        self.radio_2.setText(u'pilot run')
        self.radio_3.setText(u'Availink')
        self.radio_4.setText(u'Customer')
        self.radio_5.setText(u'1.X')
        self.radio_6.setText(u'2.X')
        self.radio_7.setText(u'16进制')
        self.radio_8.setText(u'8进制')
        self.radio_9.setText(u'2进制')
        self.radio_12.setText(u'有内部型号')
        self.radio_13.setText(u'无内部型号')
        self.radio_20.setText(u'Both')
        self.radio_21.setText(u'None')
        self.radio_22.setText(u'1.X')
        self.radio_23.setText(u'2.X')
        self.radio_24.setText(u'Both')
        self.radio_25.setText(u'None')
        
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", u"导出Key", None))
        
        
        self.lot_id_label.setText(_translate("Dialog", "Lot ID：", None))
        self.wafer_id.setText(_translate("Dialog", "Wafer ID：", None))
        self.x_cor.setText(_translate("Dialog", u"X 坐标：", None))
        self.y_cor.setText(_translate("Dialog", u"Y 坐标：", None))
        self.search_result.setText(_translate("Dialog", u"查询结果：", None))
        self.label_18.setText(_translate("Dialog", "-", None))
        self.label_19.setText(_translate("Dialog", "-", None))
        self.search_key.setText(_translate("Dialog", "查询key", None))
        self.search_lot.setText(_translate("Dialog", "查询lot", None))
        
        self.op_type.setText(_translate("Dialog", "操作类型：", None))
        self.user_.setText(_translate("Dialog", "用户：", None))
        self.inner_type.setText(_translate("Dialog", "内部型号：", None))
        self.date_.setText(_translate("Dialog", "日期：", None))
        self.statis_search.setText(_translate("Dialog", "查询", None))
        self.label_49.setText(_translate("Dialog", "-", None))
        self.search_result_2.setText(_translate("Dialog", "查询结果：", None))
        
        self.lot_id_2.setText(_translate("Dialog", "LotID:", None))
        self.input_again.setText(_translate("Dialog", u"再输入一次：", None))
        self.retrieve.setText(_translate("Dialog", "回收", None))
        self.admin_password.setText(_translate("Dialog", u"管理员密码：", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", u"查询", None))
        self.op_history.setText(_translate("Dialog", "操作历史：", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", u"历史/回收", None))
        
    def add_delete(self):
        ui = UserDialog(self.db, self)
        ui.exec_()

    def change_password(self):
        '''change password'''
        dialog = PasswordDialog(self.db, self.user, parent = self)
        if dialog.exec_():
#             new_password = QtGui.QStandardItem(dialog.newPassword())
            new_password = dialog.new_password()
#             encr_pwd = encrypt_password(str(new_password))
            self.db.update_ps(str(self.user), new_password)
        dialog.destroy()
    
    def import_(self):
        
        self.file_path = self.file_edit.text()
        if not self.file_path:
            QtGui.QMessageBox.critical(self.tab, 'Error', u'You have not chose any file!')
            return
        if not os.path.exists(self.file_path):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'This file is not exist!')
        self.tabWidget.setEnabled(False)
        thread_obj = threading.Thread(target=self.parse_key_file)
        thread_obj.start()
        #self.display_status()
           
    def md5_calc(self, data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()
    
    def sha1_calc(self, data):
        sha1obj = hashlib.sha1()
        sha1obj.update(data)
        return sha1obj.hexdigest()
    
    def mac_import(self):
        mac_pre = str(self.mac_pre.text()).strip()
        if not mac_pre:
            QtGui.QMessageBox.critical(self.tab, 'Error', u'Mac 前缀不能为空!')
        if self.redis_inst.val_is_exist(mac_pre, 'mac'):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'Mac 前缀已经被导入过!')
            return
        mac_total = 256*256*256
        for i in range(0, mac_total):
            val = int((i + 1)*100/mac_total)
            self.progressBar.setValue(val)
            self.db.insert_mac( "0000" + mac_pre + "{0:0>6}".format(hex(i)[2:]))
            if i % 100 == 0:
                print i 
            
        self.db.update_status('mac', 'import', total = mac_total, left = mac_total)
        self.redis_inst.add_val(mac_pre)
        self.redis_inst.add_history('%s import %s mac address at %s' % (self.user, mac_total, time.strftime('%Y/%m/%d',time.localtime())))
        QtGui.QMessageBox.information(self, u'提示', u'Mac导入已完成，共导入%s个Mac!'%mac_total)
        self.progressBar.setValue(0)

    def warning(self, str):
        QtGui.QMessageBox.critical(self.tab, 'Error', str)
    def progress_bar(self, val):
        self.progressBar.setValue(val)
    def info(self,str1, str2):
        QtGui.QMessageBox.information(self, str1, str2)
    def enable(self, bool):
        self.tabWidget.setEnabled(bool)
        
    def parse_key_file(self):
        start_time = time.time()
        bin_size = os.path.getsize(self.file_path)
        with open(self.file_path, 'rb') as f:
            data = f.read()
            md5_val = self.md5_calc(data)
            if self.redis_inst.val_is_exist(md5_val):
                #QtGui.QMessageBox.critical(self.tab, 'Error', u'文件数据已经被导入过!')
                self.sinOut_err.emit(u'文件数据已经被导入过!')
                self.sinOut_enable.emit(True)
                return
            order_format = bytearray(data)
            f.seek(0)
        
        key_type = self.checked_radio(self.key_version_group).text()
        if key_type == '1.X':
            table_pre = '1X'
            if (bin_size - 4)%308 != 0:
                #QtGui.QMessageBox.critical(self, 'Error', u'bin文件大小不对，请确认是否导入了正确的文件!')
                self.sinOut_err.emit(u'bin文件大小不对，请确认是否导入了正确的文件!')
                self.sinOut_enable.emit(True)
                return
            if order_format[0] == 1:
                table_suff = 'TX'
            else:
                table_suff = 'RX'
        elif key_type == '2.X':
            table_pre = '2X'
            if (bin_size - 40)%862 != 0:
                #QtGui.QMessageBox.critical(self, 'Error', u'bin文件大小不对，请确认是否导入了正确的文件!')
                self.sinOut_err.emit(u'bin文件大小不对，请确认是否导入了正确的文件!')
                self.sinOut_enable.emit(True)
                return
            if order_format[3] == 1:
                table_suff = 'TX'
            else:
                table_suff = 'RX'
               
        db_table = table_pre + '_' + table_suff
        print db_table
        #self.tabWidget.setEnabled(False)
        #self.sinOut_enable.emit(False)
        if table_pre == '1X':
            with open(self.file_path, 'rb') as f:
                f.read(4)
                key_total = (bin_size - 4)/308
                key_imported = 0
                for i in range(0, key_total):
                    key_bin = f.read(288)
                    sha = f.read(20)
                    if self.sha1_calc(key_bin) == binascii.hexlify(sha):
                        key_hex = binascii.hexlify(key_bin)
                        if i % ((key_total/1000)+1) == 0:
                            print i
                            val = int((i + 1)*100/key_total)
                            self.sinOut_progress_bar.emit(val)
                        self.db.insert_key(db_table, key_hex)
                        key_imported += 1
                    
                    else:
                        print "error occured!"
                        self.sinOut_err.emit(u'bin文件checksum不对，请确认是否导入了正确的文件!')
                        self.sinOut_enable.emit(True)
                        return

        elif db_table == '2X_RX':
            with open(self.file_path, 'rb') as f:
                f.read(40)
                data = f.read(862)
                key_total = (bin_size - 40)/862
                key_imported = 0
                while data:
                    key_hex = binascii.hexlify(data)
                    if key_imported % ((key_total/1000)+1) == 0:
                        print key_imported 
                        val = int((key_imported + 1)*100/key_total)
                        self.sinOut_progress_bar.emit(val)
                    self.db.insert_key(db_table, key_hex)
                    key_imported += 1
                    data = f.read(862)
        elif db_table == '2X_TX':
            self.sinOut_err.emit(u'暂时不支持2X_TX类型!')
            self.sinOut_enable.emit(True)
            return 0
        self.db.update_status(db_table.lower(), 'import', total = key_imported, left = key_imported)
        self.redis_inst.add_val(md5_val)
        today = time.strftime('%Y-%m-%d',time.localtime())
        sql = "insert into op_record(user,operate_type,%s,day) values('%s','storage',%s,'%s')" % (db_table.lower(), self.user, key_imported, today)
        self.db.set_op_record(sql)
        self.redis_inst.add_history('%s import %s keys: %s at %s' % (self.user, db_table, key_imported, today))
#         print 'history: ', '%s import %s keys: %s at %s' % (self.user, db_table, key_imported, time.strftime('%Y/%m/%d',time.localtime()))
        #QtGui.QMessageBox.information(self, u'提示', u'导入已完成，共导入%s个key!'%key_imported)
        self.sinOut_info.emit(u'提示',u'导入已完成，共导入%s个key!'%key_imported)
        self.sinOut_progress_bar.emit(0)
        end_time = time.time()
        print "spend time:%d second"%(end_time-start_time)
        #self.progressBar.setValue(0)
        #self.tabWidget.setEnabled(True)   
        self.sinOut_enable.emit(True)
        self.sinOut_status.emit()
    def chose_file(self, n):
        if n == 1:
            filename = QtGui.QFileDialog.getOpenFileName(self,'Open file','./') 
            self.file_edit.setText(filename)
        elif n == 2:
            filename = str(QtGui.QFileDialog.getOpenFileName(self,'Open file','./'))
            self.load_excel_form(filename)
            self.file_edit_2.setText(filename)
        elif n == 3:
            dir_name = QtGui.QFileDialog.getExistingDirectory(self,'Open directory','./')
            self.file_edit_3.setText(dir_name)
    
    def load_excel_form(self, file_name):
        try:
            data = xlrd.open_workbook(file_name)
        except:
            QtGui.QMessageBox.critical(self, 'Error', u'打开文件格式不对!')
            return
        self.get_form_detail()
        
        table = data.sheets()[0]
        apply_date = (xlrd.xldate.xldate_as_datetime(table.cell(1,2).value, 0)).strftime( '%Y-%m-%d')
        print apply_date
        self.apply_date_p.setText(apply_date)
        department = table.cell(1,7).value
        self.department_p.setText(department)
        apply_person = table.cell(2,2).value
        self.apply_person_p.setText(apply_person)
        review_person = table.cell(2,7).value
        self.review_person_p.setText(review_person)
        usage = table.cell(3,4).value
        self.chose_radio(self.buttonGroup, usage)
        key_source = table.cell(5,4).value
        self.chose_radio(self.buttonGroup_1, key_source)
        key_content = table.cell(7,4).value
        self.chose_radio(self.buttonGroup_3, key_content)
        tx = table.cell(9,5).value
        self.chose_radio(self.buttonGroup_2, tx)
        rx = table.cell(9,8).value
        self.chose_radio(self.buttonGroup_6, rx)
        inner_model = table.cell(11,4).value
        self.inner_model_p.setEditText(inner_model)
        chip_num = table.cell(12,4).value
        self.chip_num_p.setText(str(int(chip_num)))
        test_engineer = table.cell(14,4).value
        self.test_engineer_p.setText(test_engineer)
        No = table.cell(16,0).value
        self.No_p.setText(str(int(No)))
        contractor = table.cell(16,1).value
        self.contractor_p.setText(contractor)
        lot_id = table.cell(16,3).value
        self.lot_id_p.setText(lot_id)
        wafers = table.cell(16,5).value
        if type(wafers)==float:
            wafers = str(int(wafers))
        self.wafers_p.setText(wafers)
    
    def get_form_detail(self):
        self.dir_path = self.file_edit_3.text()
        self.apply_date_p = self.tableWidget.item(0, 1)
        self.apply_date = self.apply_date_p.text()
        self.department_p = self.tableWidget.item(0, 3)
        self.department = self.department_p.text()
        self.apply_person_p = self.tableWidget.item(1, 1)
        self.apply_person = self.apply_person_p.text()
        self.review_person_p = self.tableWidget.item(1, 3)
        self.review_person = self.review_person_p.text() 
        
        self.usage = self.checked_radio(self.buttonGroup)
        self.key_source = self.checked_radio(self.buttonGroup_1)
        self.tx = self.checked_radio(self.buttonGroup_2).text()
        self.rx = self.checked_radio(self.buttonGroup_6).text()
        self.key_content = self.checked_radio(self.buttonGroup_3)
#         self.inner_model_radio = self.checked_radio(self.buttonGroup_5).text()
        self.inner_model_p = self.comboBox_3
        self.inner_model = self.inner_model_p.currentText()
        self.chip_num_p = self.tableWidget_2.item(9, 1)
        self.chip_num = self.chip_num_p.text()
        self.key_num_p = self.tableWidget_2.item(10, 1)
        self.key_num = self.key_num_p.text()
        self.unit_p = self.tableWidget_2.item(11, 1)
        self.unit = self.unit_p.text()
        self.test_engineer_p = self.tableWidget_2.item(12, 1)
        self.test_engineer = self.test_engineer_p.text() 
        self.No_p = self.tableWidget_3.item(1,0)
        self.No = self.No_p.text()
        self.contractor_p = self.tableWidget_3.item(1,1)
        self.contractor = self.contractor_p.text()
        self.lot_id_p = self.tableWidget_3.item(1, 2)
        self.lot_id = self.lot_id_p.text()
        self.wafers_p = self.tableWidget_3.item(1, 3)
        self.wafers = self.wafers_p.text()
        
    def chose_radio(self, group, name):
        for radio in group.buttons():
            if radio.text() == name:
                radio.setChecked(True)
    
    def checked_radio(self, group_button):
        for radio in group_button.buttons():
            if radio.isChecked():
                return radio
    
    def get_statis(self):
        statis = self.db.get_statistics()
        X1_TX_total, X1_TX_left = statis['1X_TX'][0], statis['1X_TX'][1]
        X1_RX_total, X1_RX_left = statis['1X_RX'][0], statis['1X_RX'][1]
        X2_TX_total, X2_TX_left = statis['2X_TX'][0], statis['2X_TX'][1]
        X2_RX_total, X2_RX_left = statis['2X_RX'][0], statis['2X_RX'][1]
        mac_total, mac_left = statis['mac'][0], statis['mac'][1]
        return X1_TX_total, X1_TX_left, X1_RX_total, X1_RX_left, X2_TX_total, X2_TX_left, X2_RX_total, X2_RX_left, mac_total, mac_left
        
    def display_status(self):
        X1_TX_total, X1_TX_left, X1_RX_total, X1_RX_left, X2_TX_total, X2_TX_left, X2_RX_total, X2_RX_left, mac_total, mac_left = self.get_statis()
        self.num_1x_tx_total.setText(str(X1_TX_total))
        self.num_1x_rx_total.setText(str(X1_RX_total))
        self.num_1x_tx_left.setText(str(X1_TX_left))
        self.num_1x_rx_left.setText(str(X1_RX_left))
        
        self.num_2x_tx_left.setText(str(X2_TX_left))
        self.num_2x_rx_left.setText(str(X2_RX_left))
        self.num_2x_tx_total.setText(str(X2_TX_total))
        self.num_2x_rx_total.setText(str(X2_RX_total))
        self.num_mac_total.setText(str(mac_total))
        self.num_mac_left.setText(str(mac_left))
        
        history = self.redis_inst.get_history()
        for item in history:
            self.textBrowser_3.append(item)

    
                
    def get_item_text(self):
#         item = self.tableWidget_2.currentItem()
        test_zh = self.tableWidget.currentItem().text()
        print 'out of db:'
        print test_zh, type(test_zh)
        self.db.add_user(test_zh, '123')
        users = self.db.get_users()
        print 'in db：'
        print users[-1], type(users[-1])
        print chardet.detect(users[-1])
#         print new.decode('gbk'), type(new)
        item = self.tableWidget.item(1,0)
        item.setText(users[-1].decode('utf8'))
     
    def export(self):

    
        self.get_form_detail()
        key_table = []
        if self.tx == "1.X":
            key_table.append("1X_TX")
        elif self.tx == "2.X":
            key_table.append("2X_TX")
        elif self.tx == "Both":
            key_table.extend(["1X_TX", "2X_TX"])
        
        if self.rx == "1.X":
            key_table.append("1X_RX")
        elif self.rx == "2.X":
            key_table.append("2X_RX")
        elif self.rx == "Both":
            key_table.extend(["1X_RX", "2X_RX"])
        
        if not self.lot_id:
            QtGui.QMessageBox.critical(self.tab, 'Error', u'批号不能为空!')
            return
        elif self.redis_inst.val_is_exist(str(self.lot_id), 'lot_id'):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'批号：%s 已经被导出过!' % str(self.lot_id))
            return
        
        if not self.inner_model:
            QtGui.QMessageBox.critical(self.tab, 'Error', u'内部型号不能为空!')
            return
        elif str(self.chip_num).strip() != str(len(self.wafers.split(','))):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'wafer片号与总数不匹配!')
            return
        elif not str(self.dir_path).strip():
            QtGui.QMessageBox.critical(self.tab, 'Error', u'你还没有选择导出目录!')
            return
        elif not os.path.isdir(str(self.dir_path)):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'输入的不是目录名!')
            return

        self.parse_cfg()#解析 conf文件
        self.create_target_dir()
        
        export_thread_obj = threading.Thread(target = self._export)
        export_thread_obj.start()

    def _export(self):
        #self.tabWidget.setEnabled(False)
        self.sinOut_enable.emit(False)
        #解析txt文件，获得wafer上的每个芯片的位置      
        keys_in_one_wafer = len(self.wafer_map)
        self.lot_id_str = str(self.lot_id).replace('.', '_')
        #创建lotid这个表，用于通过lotid查询
        self.db.create_table_by_lot(self.lot_id_str)
        self.mac_start_id = self.mac_end_id = self.db.get_start_id('mac')       
        exported_keys = 0
        if len(self.key_type) == 1:
            total_keys = keys_in_one_wafer*(int(str(self.chip_num)))
            for tb in self.key_type:
                #start id是上一次取key结束的位置，end id是这次取key结束的位置              
                key_start_id = key_end_id = self.db.get_start_id(tb)
                
                #self.wafers代表“片号”
                for wafer_id in self.wafers.split(','):
                    i = 0
                    while i < keys_in_one_wafer:
                        x, y = self.wafer_map[i]
                        print "lot_id: %s, wafer_id: %s, key_type: %s, x: %s, y: %s, id: %s"%(self.lot_id_str, wafer_id, tb, x, y, key_end_id)
                        #根据key id查tb表获取key值
                        key = self.db.get_key(tb, key_end_id)
                        #将key生成key文件
                        self.gen_key_file(tb, wafer_id, x, y, key)
                        #往lot_id_str这个表里插入信息，用于通过lotid查询导出的key的
                        self.db.insert_value_by_lot(self.lot_id_str, wafer_id, tb, x, y, key_end_id)
                        i += 1
                        key_end_id += 1
                        exported_keys += 1
                        val = int((exported_keys + 1)*100/total_keys)
                        #self.progressBar.setValue(val)
                        self.sinOut_progress_bar.emit(val)
                        #print exported_keys
                    wafer_dir = os.path.join(self.output_dir, str("%02d" % int(wafer_id)))
                    self.clean_file(wafer_dir)
                    
                today = time.strftime('%Y-%m-%d',time.localtime())
                self.db.update_status(tb.lower(), 'export', left = key_end_id - key_start_id, start_id = key_end_id)
                sql = "insert into op_record(user,inner_model,operate_type,%s,day) values('%s','%s','fetch',%s,'%s')" % (tb.lower(), self.user, str(self.inner_model), key_end_id - key_start_id, today)
                self.db.set_op_record(sql)
        elif len(self.key_type) == 2:
            assert '1X_TX' == self.key_type[0] and '2X_RX' == self.key_type[1]
            x1 = '1X_TX'
            x2 = '2X_RX'
            x1_tx_start_id = x1_tx_end_id = self.db.get_start_id(x1)
            x2_rx_start_id = x2_rx_end_id = self.db.get_start_id(x2)
            total_keys = keys_in_one_wafer*(int(str(self.chip_num)))
            for wafer_id in self.wafers.split(','):
                i = 0
                while i < keys_in_one_wafer:
                    x, y = self.wafer_map[i]
                    x1_key = self.db.get_key(x1, x1_tx_end_id)
                    x2_key = self.db.get_key(x2, x2_rx_end_id)
                    self.gen_key_file(x1, wafer_id, x, y, x1_key, x2_key)
                    self.db.insert_value_by_lot(self.lot_id_str, wafer_id, x1, x, y, x1_tx_end_id)
                    self.db.insert_value_by_lot(self.lot_id_str, wafer_id, x2, x, y, x2_rx_end_id)
                    i += 1
                    x1_tx_end_id += 1
                    x2_rx_end_id += 1
                    exported_keys += 1
                    val = int((exported_keys + 1)*100/total_keys)
                    #self.progressBar.setValue(val)
                    self.sinOut_progress_bar.emit(val)
#                     print exported_keys
                wafer_dir = os.path.join(self.output_dir, str("%02d" % int(wafer_id)))
                self.clean_file(wafer_dir)
            
            today = time.strftime('%Y-%m-%d',time.localtime())
            self.db.update_status(x1.lower(), 'export', left = x1_tx_end_id - x1_tx_start_id, start_id = x1_tx_end_id)
            self.db.update_status(x2.lower(), 'export', left = x2_rx_end_id - x2_rx_start_id, start_id = x2_rx_end_id)
            sql = "insert into op_record(user,inner_model,operate_type,%s,day) values('%s','%s','fetch',%s,'%s')" % (x1, self.user, str(self.inner_model), x1_tx_end_id - x1_tx_start_id, today)
            self.db.set_op_record(sql)
            sql = "insert into op_record(user,inner_model,operate_type,%s,day) values('%s','%s','fetch',%s,'%s')" % (x2, self.user, str(self.inner_model), x1_tx_end_id - x1_tx_start_id, today)
            self.db.set_op_record(sql)
            
#                     print "lot_id: %s, wafer_id: %s, key_type: %s, x: %s, y: %s, id: %s"%(self.lot_id_str, wafer_id, self.key_type, x, y, x1_tx_end_id)
        self.db.update_status('mac', 'export', left = self.mac_end_id - self.mac_start_id, start_id = self.mac_end_id)
        self.redis_inst.add_val(str(self.lot_id), 'lot_id')
        for type_ in self.key_type:
            self.redis_inst.add_history('%s export %s keys: %s at %s' % (self.user, type_, total_keys, time.strftime('%Y/%m/%d',time.localtime())))
        #QtGui.QMessageBox.information(self, u'提示', u'导出已完成，共导出%s个key!' % total_keys)
        self.sinOut_info.emit(u'提示', u'导出已完成，共导出%s个key!' % total_keys)
        #self.display_status()
        #self.progressBar.setValue(0)
        self.sinOut_progress_bar.emit(0)
        #self.tabWidget.setEnabled(True)
        self.sinOut_enable.emit(True)
        self.sinOut_status.emit()
    def create_target_dir(self):
        main_dir = os.getcwd()
        self.output_dir = os.path.join(main_dir, "Output", str(self.lot_id))
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
    
    def gen_key_file(self, tb, wafer_id, x, y, key_1, key_2 = None):               
        wafer_dir = os.path.join(self.output_dir, str("%02d" % int(wafer_id)))
        print wafer_dir
        if not os.path.exists(wafer_dir):
            os.mkdir(wafer_dir)
        work_dir = os.getcwd()
        os.chdir(wafer_dir)
        name_base = "%s_%s_%s_%s" % (str(self.lot_id), str("%02d" % int(wafer_id)), x, y)
        print name_base
        key_name = "%s.key_source" % name_base
        key2_name = "%s.txt" % name_base
        key_name_abs = os.path.join(wafer_dir, key_name)
        key2_name_abs =  os.path.join(wafer_dir, key2_name)

        if "TX" in tb:
            type_ = '1'
        else:
            type_ = '2'
        if "1X" in tb:
            bytes_ = '288'
        with open(key_name_abs, 'a+') as f:
            f.write("==PAR_START==" + "\n")
            f.write(str(self.lot_id) + "\n")
            f.write(str(wafer_id) + '\n')
            f.write(str(x) + '\n')
            f.write(str(y) + '\n')
            f.write(type_ + '\n')
            f.write(bytes_ + '\n')
            f.write("==KEY_START==" + '\n')
            length = len(zip(key_1[0::2], key_1[1::2]))
            for index, item in enumerate(zip(key_1[0::2], key_1[1::2])):
                if index != length - 1:
                    f.write(''.join(item) + '\n')
                else:
                    f.write(''.join(item))

        if self.bind_mac == 'yes':                
            mac_value = self.db.get_mac(self.mac_end_id)
            self.mac_end_id += 1
        else:
            mac_value = 1234567890123456
            
        if len(self.key_type) == 1: 
            cmd_str = '%s %s %d' % (self.rom_gen_exe, key_name_abs, 1)
            execCLI(cmd_str)
            with open("%s.rom"%key_name_abs, 'a+') as f:
                f.write('\n')                
                
            cmd_final = '%s %s %s %s' % (self.final_exe[0], "%s.rom"%key_name_abs, "%s.key"%name_base, mac_value)
            execCLI(cmd_final)
            print 'key: %s, mac: %s' % (name_base, mac_value)
            
        elif len(self.key_type) == 2:
            with open(key2_name_abs, 'a+') as f:
                length = len(zip(key_2[0::2], key_2[1::2]))
                for index, item in enumerate(zip(key_2[0::2], key_2[1::2])):
                        f.write((''.join(item) + '\n'))
                        
            cmd_str = '%s %s %d' % (self.rom_gen_exe, key_name_abs, 1)
            execCLI(cmd_str)
            with open("%s.rom"%key_name_abs, 'a+') as f:
                    f.write('\n')
                
            cmd_final_1 = '%s %s %s %s' % (self.final_exe[0], "%s.rom"%key_name_abs, "%s.out"%key_name_abs, mac_value)
            execCLI(cmd_final_1)
            cmd_final_2 = '%s %s %s %s' % (self.final_exe[1], "%s.out"%key_name_abs, key2_name_abs, "%s.key"%name_base)
            execCLI(cmd_final_2)
            print 'key: %s, mac: %s' % (name_base, mac_value)            
                      
        os.chdir(work_dir)
    
    def clean_file(self, clean_dir, reserved = 'key'):
        work_dir = os.getcwd()
        os.chdir(clean_dir)
        for f in os.listdir('.'):
            if not f.endswith(reserved):
                os.remove(f)
        os.chdir(work_dir)
                
    def parse_cfg(self):
        target_dir = os.path.join(os.getcwd(),'Input', str(self.inner_model))
        if not os.path.exists(target_dir):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'目标目录不存在!')
            return
        for f in os.listdir(target_dir):
            if f.endswith("cfg"):
                cfg_file = f
                break
            
        cfg_file_abs = os.path.join(target_dir, cfg_file)
        config = ConfigParser.ConfigParser()
        try:
            cfg_fp = open(cfg_file_abs,"r")
            config.readfp(cfg_fp)
        except Exception,e:
            print e
        
        self.chip_name = config.get('Chip name', 'chip_name').strip()
        self.map_file = os.path.join(target_dir, config.get('Map file', 'file').strip())
        self.rom_gen_exe = os.path.join(target_dir, config.get('HDCP_ROM_GEN', 'rom_gen_exe').strip())
        print self.rom_gen_exe
#         self.final_exe = os.path.join(target_dir, config.get('FINAL_ROM_GEN', 'final_exe').strip())
        self.final_exe = [os.path.join(target_dir, config.get('FINAL_ROM_GEN', item).strip()) for item in config.options('FINAL_ROM_GEN')]
        print self.final_exe
        self.bind_mac = config.get('MAC', 'bind_mac').strip()
        self.key_type = [config.get('Key type', item).strip() for item in config.options('Key type')]
#         print self.chip_name
#         print self.map_file
#         print self.rom_gen_exe
#         print self.final_exe
#         print self.key_type
        self.wafer_map = self.parse_map(self.map_file)       
#         print self.wafer_map
        
        
    def parse_map(self, file_name):

        with open(file_name, 'r') as f:
            data = f.readlines()
        
        start_x = int(data[7].split('=')[1].split(',')[0])
        start_y = int(data[7].split('=')[1].split(',')[1])
        
        length = len(data)
        #解析出出wafer圆的第一行
        for i in range(0, length):
            if '=' not in data[i] and data[i].strip():
                circle_start = i
                break
        #解析出出wafer圆的最后一行，如果最后一行后面不是空格怎么办呢？感觉会有问题
        for i in range(circle_start, length):
            if not data[i].strip():
                circle_end = i - 1
        
        a = re.compile(r"\s*[MSms]*([^MmSs\s]+?).*")
        for i in range(circle_start, circle_end + 1):
            match = a.search(data[i])
            if match:
                #x_base 是第一行的最左边一个字符的坐标，start(1)函数是指group(1)匹配的字符(括号里面匹配的部分)在整个字符串里面的位置 
                x_base = start_x - match.start(1)
                break
        
        wafer_map = []
        for i in range(circle_start, circle_end + 1):
            match = a.search(data[i]) 
            if match:
                first_index = match.start(1)
                incr = 0
                for j in data[i][first_index:].strip():
                    if j not in "MmSs":
                        x = x_base + first_index + incr
                        y = start_y
                        wafer_map.append((x, y))
                    incr += 1
                start_y -= 1
              
        return wafer_map    
    
    def key_search(self):
        lot_id = str(self.comboBox.currentText()).replace('.', '_')
        wafer_id = self.comboBox_2.currentText()
        x_start = str(self.lineEdit_4.text()).strip()
        y_start = str(self.lineEdit_5.text()).strip()
        x_end = str(self.lineEdit_6.text()).strip()
        y_end = str(self.lineEdit_7.text()).strip()
        self.textBrowser.clear()
        
        if not lot_id:
            QtGui.QMessageBox.critical(self.tab_3, 'Error', u'Lot ID 不能为空!')
            return
        sql = "select id, x_coordinate, y_coordinate from %s where 1=1 " % lot_id
        
        if not wafer_id:
            QtGui.QMessageBox.critical(self.tab_3, 'Error', u'Wafer ID 不能为空!')
            return
        sql += "and waferID=%s " % wafer_id
        
        if not x_start and not x_end:
            QtGui.QMessageBox.critical(self.tab_3, 'Error', u'至少应输入一个 X坐标!')
            return
        elif not x_start.isdigit() and not x_end.isdigit():
            QtGui.QMessageBox.critical(self.tab_3, 'Error', u'坐标应该输入数字!')
            return
        elif x_start and not x_end:
            sql += "and x_coordinate=%s " % x_start
        elif x_end and not x_start:
            sql += "and x_coordinate=%s " % x_end
        elif x_start and x_end:
            sql += "and x_coordinate>=%s and x_coordinate<=%s " % (x_start, x_end)
            
        if not y_start and not y_end:
            QtGui.QMessageBox.critical(self.tab_3, 'Error', u'至少应输入一个 Y坐标!')
            return
        elif not y_start.isdigit() and not y_end.isdigit():
            QtGui.QMessageBox.critical(self.tab_3, 'Error', u'坐标应该输入数字!')
            return
        elif y_start and not y_end:
            sql += "and y_coordinate=%s " % y_start
        elif y_end and not y_start:
            sql += "and y_coordinate=%s " % y_end
        elif x_start and x_end:
            sql += "and y_coordinate>=%s and y_coordinate<=%s " % (y_start, y_end)
        
        key_types = self.db.get_key_types(lot_id)
        
        for item in key_types:
            cur_sql = sql + "and key_type='%s' " % item
            print cur_sql
            cors = self.db.get_key_id(cur_sql)
            if cors:
                self.textBrowser.append("[key_type: %s]" % item)
                for cor in cors:
                    self.textBrowser.append("X Coordinate: %s, Y Coordinate: %s\n" % (cor[1], cor[2]))
                    self.textBrowser.append(self.db.get_key_info(item, cor[0]) + '\n')
                     
        
    def lot_search(self):
        self.textBrowser.setText("hello sky")
    
    def display_lot(self):
        if self.redis_inst.is_exist('lot_id'):
            for item in self.redis_inst.r.smembers('lot_id'):
                self.comboBox.addItem(QtCore.QString(item))        
  
    def combox_init(self):
        if self.redis_inst.is_exist('lot_id'):
            for item in self.redis_inst.r.smembers('lot_id'):
                self.comboBox.addItem(QtCore.QString(item))
        for i in range(1,26):
            self.comboBox_2.addItem(QtCore.QString(str(i)))
        self.comboBox_4.addItem(QtCore.QString(u'storage'))
        self.comboBox_4.addItem(QtCore.QString(u'fetch'))
    
    def op_record_search(self):
        sql = "select sum(1x_tx), sum(1x_rx), sum(2x_tx), sum(2x_rx) from op_record where 1=1 "
        html = "<p><b>Date:</b> %s -- %s</p><p><b>Operate type:</b> %s</p>"
        
        from_date = self.dateEdit.textFromDateTime(self.dateEdit.dateTime())     
        if from_date:
            sql += "and day >= '%s' " % from_date
            real_para = [from_date,]
            
        end_date = self.dateEdit_2.textFromDateTime(self.dateEdit_2.dateTime()) 
        if end_date:
            sql += "and day <= '%s' " % end_date
            real_para.append(end_date)
        
        operate_type = self.comboBox_4.currentText() 
        if operate_type:
            sql += "and operate_type='%s' " % operate_type
            real_para.append(operate_type)
             
        user = self.lineEdit_2.text()
        if user:
            sql += "and user='%s' " % user
            html += "<p><b>User:</b> %s</p>"
            real_para.append(user)
            
        inner_model = self.comboBox_5.currentText()    
        if inner_model:
            sql += "and inner_model='%s' " % inner_model
            html += "<p><b>Inner model:</b> %s</p>"
            real_para.append(inner_model)
        
        x1_tx, x1_rx, x2_tx, x2_rx = self.db.get_op_record(sql)
        html += "<p><b>1X_TX:</b> %s</p><p><b>1X_RX:</b> %s</p><p><b>2X_TX:</b> %s</p><p><b>2X_RX:</b> %s</p>"
        x1_tx = 0 if not x1_tx else x1_tx
        x1_rx = 0 if not x1_rx else x1_rx
        x2_tx = 0 if not x2_tx else x2_tx
        x2_rx = 0 if not x2_rx else x2_rx
        real_para.extend([x1_tx, x1_rx, x2_tx, x2_rx])
        self.textBrowser_2.setText(html%tuple(real_para))
        
    def retrieve_key(self):
        
        lot_id_1 = str(self.lineEdit.text()).replace('.', '_')
        lot_id_2 = str(self.lineEdit_11.text()).replace('.', '_')  
        if not self.lineEdit_10.text() == self.db.get_ps('admin'):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'输入的管理员密码错误!')
            return
        if lot_id_1 != lot_id_2:
            QtGui.QMessageBox.critical(self.tab, 'Error', u'两次输入的lot id 不一致!')
            return
        if not self.redis_inst.val_is_exist(lot_id_1.replace('_', '.'),'lot_id'):
            QtGui.QMessageBox.critical(self.tab, 'Error', u'输入的lot id在数据库中不存在!')
            return
        
        key_types = self.db.get_key_types(lot_id_1)
        if not key_types:
            QtGui.QMessageBox.critical(self.tab, 'Error', u'lot id 对应的表类型为空!')
            return
        for type_ in key_types:
            new_id = int(mysql_inst.get_new_id(type_)) + 1
            del_ids = self.db.get_del_ids(lot_id_1, type_)
            id_num = len(del_ids)
        #update id
            for id_ in del_ids:
                self.db.update_key_id(type_, id_, str(new_id))
                new_id += 1
                print new_id
        #update statistics table
            self.db.update_status(type_, 'retrieve', left = id_num)
            
        #should insert code here of update op_record
            self.redis_inst.add_history('%s retrieve %s keys: %s at %s' % (self.user, type_, id_num, time.strftime('%Y/%m/%d',time.localtime())))
        #drop table
        self.db.drop_table(lot_id_1)
        self.redis_inst.del_val(lot_id_1.replace('_', '.'), 'lot_id')
        self.display_status()
        QtGui.QMessageBox.information(self, u'提示', u'回收操作已完成!')
    
class UserDialog(QtGui.QDialog):
    def __init__(self, db, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.db = db
        self.resize(400, 300)
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(300, 80, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.delete)
        self.pushButton_4 = QtGui.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(300, 40, 75, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.add)
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(20, 30, 256, 201))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        
        items =  [QtGui.QListWidgetItem(item) for item in self.db.get_users()]
        for i in range(len(items)):
            if items[i].text() != 'admin':
                self.listWidget.insertItem(i+1,items[i])
        self.listWidget.itemClicked.connect(self.cur_item)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", u"添加/删除用户", None))
        self.pushButton.setText(_translate("Dialog", u"删除", None))
        self.pushButton_4.setText(_translate("Dialog", u"添加", None))
    
    def cur_item(self):
        self.current_item = self.listWidget.currentItem().text()
        
    def add(self):
        ui = AddDialog(self.db, self)
        if ui.exec_():
            self.listWidget.addItem(QtGui.QListWidgetItem(ui.addUser))
    
    def delete(self):
        if not hasattr(self, 'current_item'):
            QtGui.QMessageBox.critical(self, 'Error', u'请选择要删除的用户!')
            return
        reply = QtGui.QMessageBox.question(self, 'Warning', u'你确定要删除用户: %s 吗？'%self.current_item, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.listWidget.setItemHidden(self.listWidget.currentItem(), True)
            self.db.del_user(self.current_item)
        
class AddDialog(QtGui.QDialog):
    def __init__(self, db, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.db = db
        self.setObjectName(_fromUtf8("Dialog"))
        self.resize(345, 208)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(40, 160, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 40, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(40, 60, 221, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 110, 221, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.retranslateUi()
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.add_user)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", u"添加用户", None))
        self.label.setText(_translate("Dialog", u"请输入用户名:", None))
        self.label_2.setText(_translate("Dialog", u"请输入密码:", None))
    
    def add_user(self):
        username = self.lineEdit.text()
        password = str(self.lineEdit_2.text())
        if not username:
            QtGui.QMessageBox.warning(self, 'Warning', u'用户名不能为空!', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            return
        if not password:
            QtGui.QMessageBox.warning(self, 'Warning', u'密码不能为空!', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            return
        if username in self.db.get_users():
            QtGui.QMessageBox.warning(self, 'Warning', u'用户: %s 已经存在，请更换其他的用户名!'%username, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        else:
            self.db.add_user(str(username), password)
            if username in self.db.get_users():
                self.addUser = username
            self.accept()

class PasswordDialog(QtGui.QDialog):
    def __init__(self, db, user, parent=None):
        self.db = db
        self.user = user
        QtGui.QDialog.__init__(self, parent)
        self.resize(240, 200)
        self.setWindowTitle(u'修改密码')
        grid = QtGui.QGridLayout()
 
        grid.addWidget(QtGui.QLabel(u'旧密码:', parent=self), 0, 0, 1, 1)
 
        self.oldPassword = QtGui.QLineEdit(parent=self)
        grid.addWidget(self.oldPassword, 0, 1, 1, 1)
 
        grid.addWidget(QtGui.QLabel(u'新密码:', parent=self), 1, 0, 1, 1)
 
        self.newPassword = QtGui.QLineEdit(parent=self)
        grid.addWidget(self.newPassword, 1, 1, 1, 1)
 
        buttonBox = QtGui.QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.judge)
        buttonBox.rejected.connect(self.reject)
 
        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid)
 
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacerItem)
 
        layout.addWidget(buttonBox)
        self.setLayout(layout)
    
    def judge(self):
        if self.db.get_ps(self.user) == self.old_password():
#         if self.old_password() == self.db.get_ps(self.user):
            self.accept()
        else:
            QtGui.QMessageBox.critical(self, 'Error', u'旧密码不正确!')
    
    def old_password(self):
        return self.oldPassword.text()
    
    def new_password(self):
        return self.newPassword.text()

class RedisOperate(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='127.0.0.1', port = 6379, password = 'AvL_1108')
        self.r = redis.StrictRedis(connection_pool=pool)
    
    def get_ps(self, name):
        return self.r.hget('user_management', name)
            
    def set_ps(self, name, value):
        self.r.hset('user_management', name, value)
    
    def is_hexist(self, name):
        return self.r.hexists('user_management', name)
    
    def is_exist(self, name):
        return self.r.exists(name)
    
    def add_val(self, val, set_type = 'file_md5'):
        self.r.sadd(set_type, val)
    
    def del_val(self, val, set_type):
        self.r.srem(set_type, val)
    
    def val_is_exist(self, val, set_type = 'file_md5'):
        return self.r.sismember(set_type, val)
    
    def add_history(self, action):
        self.r.lpush('history', action)
    
    def get_history(self):
        return self.r.lrange('history', 0, -1)
    
    def set(self, name, value):
        self.r.set(name, value)
    
    def get(self, name):
        return self.r.get(name)
    
    def delete_user(self, name):
        self.r.hdel('user_management', name)
    
    def dump_users(self):
        return self.r.hkeys('user_management')

class MysqlOperate(object):
    def __init__(self, host, user, passwd, db):
        self.conn = MySQLdb.connect(host, user, passwd, db)
        self.cur = self.conn.cursor()
        
        self.conn.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8;') 
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        
        if not self.table_is_exist():
            self.create_tables()
        
            
    def create_tables(self):
        #username management table
        self.cur.execute("create table user(name varchar(20), password varchar(50))")
        #key table
        self.cur.execute("create table 1X_TX(id int not null auto_increment, value varchar(2000), is_use enum('yes', 'no'), primary key(id))")
        self.cur.execute("create table 1X_RX(id int not null auto_increment, value varchar(2000), is_use enum('yes', 'no'), primary key(id))")
        self.cur.execute("create table 2X_TX(id int not null auto_increment, value varchar(2000), is_use enum('yes', 'no'), primary key(id))")
        self.cur.execute("create table 2X_RX(id int not null auto_increment, value varchar(2000), is_use enum('yes', 'no'), primary key(id))")
        #lot table, to be finish
        self.cur.execute("create table lot(lotID varchar(20), department varchar(20), applyPerson varchar(20), \
                        applyType enum('project', 'batch', 'pilot'), keySource enum('availink', 'customer'), \
                        keyContent enum('16', '8', '2'), TX enum('1X','2X','Both','None'), RX enum('1X','2X','Both','None'), \
                        innerType varchar(30), sliceNumber tinyint, keyNumber int, testEngineer varchar(20), slices varchar(80))")
        #key record
        self.cur.execute("create table op_record(user char(20), inner_model char(30), operate_type enum('fetch','storage'), 1x_tx int, 1x_rx int, 2x_tx int, 2x_rx int, day date)")
        #Statistics table
        self.cur.execute("create table Statistics(type enum('1X_TX','1X_RX','2X_TX','2X_RX','mac'), total int, left_num int, start_id int)")
        sql = "insert into Statistics values(%s,%s,%s,%s)"
        self.cur.executemany(sql,[('1X_TX', '0', '0', '1'), ('1X_RX', '0', '0', '1'), ('2X_TX', '0', '0', '1'), ('2X_RX', '0', '0', '1'), ('mac', '0', '0', '1')])
        #mac info
        self.cur.execute("create table mac_addr(id int not null auto_increment,mac_value char(16),primary key(id))")
        self.conn.commit()
    
    def insert_key(self, table_name, value):
#         print "insert into %s(value, is_use) values('%s', 'no')"%(table_name, value)
        self.cur.execute("insert into %s(value, is_use) values('%s', 'no')"%(table_name, value))
        #self.conn.commit()
    
    def insert_mac(self, value):
        self.cur.execute("insert into mac_addr(mac_value) values('%s')" % value)
        self.conn.commit()
    
    def update_status(self, key_type, op_type, total = None, left = None, start_id = None):
        
        if op_type == 'import':
            sql = "update statistics set total=total+%s,left_num=left_num+%s where type='%s'"%(total, left, key_type)
        elif op_type == 'export':
            sql = "update statistics set left_num=left_num-%s,start_id=%s where type='%s'"%(left, start_id, key_type)
        elif op_type == 'retrieve':
            sql = "update statistics set left_num=left_num+%s where type='%s'"%(left, key_type)
        
        self.cur.execute(sql)
        self.conn.commit()
    
    def update_start_id(self, tb, start_id):
        sql = "update statistics set start_id=%s where type='%s'" %(start_id, tb)
        self.cur.execute(sql)
        self.conn.commit()
    
    def table_is_exist(self):
        self.cur.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'hdcp' AND table_name ='user'")
        return self.cur.fetchone()[0] == 1
        
    def create_table_by_lot(self, lotID):
        self.cur.execute("create table %s(waferID tinyint, key_type enum('1X_RX', '1X_TX', '2X_RX', '2X_TX'), x_coordinate smallint, y_coordinate smallint, id int)"%lotID)
        
    def insert_value_by_lot(self, lotID, waferID, key_type, x, y, id_):
        self.cur.execute("insert into %s values(%s,'%s',%s,%s,%s)"%(lotID, waferID, key_type, x, y, id_))
        self.conn.commit()
    
    def get_start_id(self, tb):
        sql = "select start_id from statistics where type='%s'" % tb
        self.cur.execute(sql)
        return self.cur.fetchone()[0]
    
    def get_new_id(self, tb):
        sql = "select id from %s order by id desc limit 1" % tb
        self.cur.execute(sql)
        return self.cur.fetchone()[0]
    
    def get_key_id(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()
    
    def get_key(self, tb, id_):
        self.cur.execute("select value from %s where id='%s'" % (tb, id_))
        key_value = self.cur.fetchone()[0]
#         self.cur.execute("update %s set is_use='yes' where id='%s'" % (tb, id))
        return key_value
    
    def get_mac(self, id_):
        self.cur.execute("select mac_value from mac_addr where id='%s'" % id_)
        mac_value = self.cur.fetchone()[0]
        return mac_value
    
    def get_key_info(self, target_table, id_):
        self.cur.execute("select value from %s where id=%s" % (target_table, id_))
        return self.cur.fetchone()[0]
    
    def get_key_types(self, tb):
        self.cur.execute("select distinct key_type from %s" % tb)
        types_ = [item[0] for item in self.cur.fetchall()]
        return types_
    
    def get_del_ids(self, tb, key_type):
        self.cur.execute("select id from %s where key_type='%s'" % (tb, key_type))
        ids = [item[0] for item in self.cur.fetchall()]
        return ids
    
    def update_key_id(self, tb, cur_id, new_id):
        self.cur.execute("update %s set id=%s where id=%s" % (tb, new_id, cur_id))
        self.conn.commit()
    
    def drop_table(self,tb):
        self.cur.execute("drop table %s" % tb)
        self.conn.commit()
        
    def set_op_record(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        
    def get_op_record(self, sql):
        self.cur.execute(sql)
        x1_tx, x1_rx, x2_tx, x2_rx = self.cur.fetchall()[0]
        
        return x1_tx, x1_rx, x2_tx, x2_rx
    
    def get_lot_info(self, lotID):
        self.cur.execute("select * from lot where lotID='%s'" % lotID)
        print self.cur.fetchall()
        return self.cur.fetchall()[0]
       
    def add_user(self, name, passwd):
        self.cur.execute("insert into user values('%s','%s')"%(name, passwd))
        self.conn.commit()
        
    def get_ps(self, name):
        self.cur.execute("select password from user where name='%s'"%name)
        return self.cur.fetchone()[0]
    
    def update_ps(self, name, ps):
        self.cur.execute("update user set password='%s' where name='%s'"%(ps, name))
        self.conn.commit()
        
    def del_user(self, name):
        self.cur.execute("delete from user where name='%s'"%name)
        self.conn.commit()
        
    def get_users(self):
        self.cur.execute("select name from user")
        users = []
        for item in self.cur.fetchall():
            users.extend(item)
        return users
    
    def get_statistics(self):
        self.cur.execute("select type, total, left_num from statistics")
        statis = {}
        for item in self.cur.fetchall():
            statis[item[0]] = (item[1], item[2])
        return statis
            
    def close(self):
        self.cur.close()
        self.conn.close()
    

if __name__ == '__main__':
    redis_inst = RedisOperate()
    mysql_inst = MysqlOperate(host='127.0.0.1', user='root', passwd='Avl1108', db ='hdcp')

            
    app = QtGui.QApplication(sys.argv)
    if 'admin' not in mysql_inst.get_users():
        reg = Ui_Register(mysql_inst)
        if reg.exec_():      
            login = Ui_Login(mysql_inst)
            if login.exec_():
                ui = Ui_MainWindow(redis_inst, mysql_inst, login.current_user)
                ui.show()
                sys.exit(app.exec_())
    else:
        login = Ui_Login(mysql_inst)
        if login.exec_(): 
            ui = Ui_MainWindow(redis_inst, mysql_inst, login.current_user)
            ui.show()
            sys.exit(app.exec_())
        
#     ui = Ui_MainWindow(redis_inst, mysql_inst, 'admin')
#     ui.show()
#     sys.exit(app.exec_())
    mysql_inst.close()
    redis_inst.r.save()
