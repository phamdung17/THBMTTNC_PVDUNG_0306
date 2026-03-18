# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file './ui/rsa.ui'
# Created by: PyQt5 UI code generator 5.15.11

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1128, 513)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(480, 10, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # txt_plain_text: user nhập vào -> setReadOnly(False)
        self.txt_plain_text = QtWidgets.QTextBrowser(Dialog)
        self.txt_plain_text.setGeometry(QtCore.QRect(100, 170, 421, 101))
        self.txt_plain_text.setObjectName("txt_plain_text")
        self.txt_plain_text.setReadOnly(False)

        # txt_cipher_text: hiển thị kết quả mã hóa -> read-only
        self.txt_cipher_text = QtWidgets.QTextBrowser(Dialog)
        self.txt_cipher_text.setGeometry(QtCore.QRect(100, 300, 421, 101))
        self.txt_cipher_text.setObjectName("txt_cipher_text")

        # txt_info: user nhập vào -> setReadOnly(False)
        self.txt_info = QtWidgets.QTextBrowser(Dialog)
        self.txt_info.setGeometry(QtCore.QRect(660, 170, 421, 101))
        self.txt_info.setObjectName("txt_info")
        self.txt_info.setReadOnly(False)

        # txt_sign: hiển thị chữ ký -> read-only
        self.txt_sign = QtWidgets.QTextBrowser(Dialog)
        self.txt_sign.setGeometry(QtCore.QRect(660, 300, 421, 101))
        self.txt_sign.setObjectName("txt_sign")

        self.btn_encrypt = QtWidgets.QPushButton(Dialog)
        self.btn_encrypt.setGeometry(QtCore.QRect(110, 430, 75, 23))
        self.btn_encrypt.setObjectName("btn_encrypt")
        self.btn_decrypt = QtWidgets.QPushButton(Dialog)
        self.btn_decrypt.setGeometry(QtCore.QRect(390, 430, 75, 23))
        self.btn_decrypt.setObjectName("btn_decrypt")
        self.btn_sign = QtWidgets.QPushButton(Dialog)
        self.btn_sign.setGeometry(QtCore.QRect(720, 430, 75, 23))
        self.btn_sign.setObjectName("btn_sign")
        self.btn_verify = QtWidgets.QPushButton(Dialog)
        self.btn_verify.setGeometry(QtCore.QRect(940, 430, 75, 23))
        self.btn_verify.setObjectName("btn_verify")
        self.btn_gen_keys = QtWidgets.QPushButton(Dialog)
        self.btn_gen_keys.setGeometry(QtCore.QRect(720, 30, 75, 23))
        self.btn_gen_keys.setObjectName("btn_gen_keys")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 310, 60, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 180, 60, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(600, 180, 60, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(600, 300, 60, 13))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RSA Cipher"))
        self.label.setText(_translate("Dialog", "RSA Cipher"))
        self.btn_encrypt.setText(_translate("Dialog", "Encrypt"))
        self.btn_decrypt.setText(_translate("Dialog", "Decrypt"))
        self.btn_sign.setText(_translate("Dialog", "Sign"))
        self.btn_verify.setText(_translate("Dialog", "Verify"))
        self.btn_gen_keys.setText(_translate("Dialog", "Generate Keys"))
        self.label_2.setText(_translate("Dialog", "Cipher Text"))
        self.label_3.setText(_translate("Dialog", "Plain Text"))
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
