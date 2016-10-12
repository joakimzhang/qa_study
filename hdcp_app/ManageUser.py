# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_del_user.ui'
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

class Ui_DialogManageUser(object):
    def setupUi(self, DialogManageUser):
        DialogManageUser.setObjectName(_fromUtf8("DialogManageUser"))
        DialogManageUser.resize(240, 320)
        self.buttonBox = QtGui.QDialogButtonBox(DialogManageUser)
        self.buttonBox.setGeometry(QtCore.QRect(150, 50, 81, 301))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textEdit = QtGui.QTextEdit(DialogManageUser)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 121, 271))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(DialogManageUser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogManageUser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogManageUser.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogManageUser)

    def retranslateUi(self, DialogManageUser):
        DialogManageUser.setWindowTitle(_translate("DialogManageUser", "Dialog", None))

