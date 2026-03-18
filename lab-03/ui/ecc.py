# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file './ui/ecc.ui'
# Created by: PyQt5 UI code generator 5.15.11

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(705, 513)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(270, 40, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # txt_info: user nhập vào -> setReadOnly(False)
        self.txt_info = QtWidgets.QTextBrowser(Dialog)
        self.txt_info.setGeometry(QtCore.QRect(210, 170, 421, 101))
        self.txt_info.setObjectName("txt_info")
        self.txt_info.setReadOnly(False)

        # txt_sign: hiển thị chữ ký -> read-only
        self.txt_sign = QtWidgets.QTextBrowser(Dialog)
        self.txt_sign.setGeometry(QtCore.QRect(210, 300, 421, 91))
        self.txt_sign.setObjectName("txt_sign")

        self.btn_sign = QtWidgets.QPushButton(Dialog)
        self.btn_sign.setGeometry(QtCore.QRect(270, 430, 75, 23))
        self.btn_sign.setObjectName("btn_sign")
        self.btn_verify = QtWidgets.QPushButton(Dialog)
        self.btn_verify.setGeometry(QtCore.QRect(490, 430, 75, 23))
        self.btn_verify.setObjectName("btn_verify")
        self.btn_gen_keys = QtWidgets.QPushButton(Dialog)
        self.btn_gen_keys.setGeometry(QtCore.QRect(510, 60, 75, 23))
        self.btn_gen_keys.setObjectName("btn_gen_keys")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(66, 180, 121, 20))
        font2 = QtGui.QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_4.setFont(font2)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(86, 300, 101, 20))
        self.label_5.setFont(font2)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ECC Cipher"))
        self.label.setText(_translate("Dialog", "ECC Cipher"))
        self.btn_sign.setText(_translate("Dialog", "Sign"))
        self.btn_verify.setText(_translate("Dialog", "Verify"))
        self.btn_gen_keys.setText(_translate("Dialog", "Generate Keys"))
        self.label_4.setText(_translate("Dialog", "Information"))
        self.label_5.setText(_translate("Dialog", "Signature"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
