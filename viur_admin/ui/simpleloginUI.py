# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simplelogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_simpleLogin(object):
    def setupUi(self, simpleLogin):
        simpleLogin.setObjectName("simpleLogin")
        simpleLogin.resize(501, 319)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":icons/viur_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        simpleLogin.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(simpleLogin)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":icons/login.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.statusLbl = QtWidgets.QLabel(self.centralwidget)
        self.statusLbl.setObjectName("statusLbl")
        self.verticalLayout.addWidget(self.statusLbl)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.usernameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.usernameEdit.setObjectName("usernameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.usernameEdit)
        self.passwordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.googleLoginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.googleLoginBtn.setObjectName("googleLoginBtn")
        self.horizontalLayout.addWidget(self.googleLoginBtn)
        self.loginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBtn.setObjectName("loginBtn")
        self.horizontalLayout.addWidget(self.loginBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        simpleLogin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(simpleLogin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 501, 29))
        self.menubar.setObjectName("menubar")
        simpleLogin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(simpleLogin)
        self.statusbar.setObjectName("statusbar")
        simpleLogin.setStatusBar(self.statusbar)

        self.retranslateUi(simpleLogin)
        QtCore.QMetaObject.connectSlotsByName(simpleLogin)

    def retranslateUi(self, simpleLogin):
        _translate = QtCore.QCoreApplication.translate
        simpleLogin.setWindowTitle(_translate("simpleLogin", "ViUR Admin Updater"))
        self.statusLbl.setText(_translate("simpleLogin", "Login2 :)"))
        self.label.setText(_translate("simpleLogin", "Username"))
        self.label_2.setText(_translate("simpleLogin", "Password"))
        self.googleLoginBtn.setText(_translate("simpleLogin", "Login with Google"))
        self.loginBtn.setText(_translate("simpleLogin", "Login with Password"))
