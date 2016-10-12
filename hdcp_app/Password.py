# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'password.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_DialogPassword(object):
    def setupUi(self, DialogPassword):
        DialogPassword.setObjectName(_fromUtf8("DialogPassword"))
        DialogPassword.resize(240, 223)
        self.buttonBox = QtGui.QDialogButtonBox(DialogPassword)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 170, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget_2 = QtGui.QWidget(DialogPassword)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 10, 177, 171))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_5 = QtGui.QLabel(self.layoutWidget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.lineEdit_5 = QtGui.QLineEdit(self.layoutWidget_2)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.gridLayout_3.addWidget(self.lineEdit_5, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.lineEdit_6 = QtGui.QLineEdit(self.layoutWidget_2)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.gridLayout_3.addWidget(self.lineEdit_6, 1, 1, 1, 1)

        self.retranslateUi(DialogPassword)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogPassword.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogPassword.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogPassword)

    def retranslateUi(self, DialogPassword):
        DialogPassword.setWindowTitle(_translate("DialogPassword", "Dialog", None))
        self.label_5.setText(_translate("DialogPassword", "新密码", None))
        self.label_6.setText(_translate("DialogPassword", "旧密码", None))

