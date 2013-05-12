# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'accountmanager.ui'
#
# Created: Sat May 11 13:48:23 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 680)
        MainWindow.setMinimumSize(QtCore.QSize(480, 0))
        MainWindow.setMaximumSize(QtCore.QSize(480, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/viur_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.acclistWidget = QtGui.QListWidget(self.centralwidget)
        self.acclistWidget.setMinimumSize(QtCore.QSize(450, 250))
        self.acclistWidget.setObjectName("acclistWidget")
        self.verticalLayout.addWidget(self.acclistWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addAccBTN = QtGui.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/actions/add_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addAccBTN.setIcon(icon1)
        self.addAccBTN.setObjectName("addAccBTN")
        self.horizontalLayout_3.addWidget(self.addAccBTN)
        self.delAccBTN = QtGui.QPushButton(self.centralwidget)
        self.delAccBTN.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/actions/delete_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delAccBTN.setIcon(icon2)
        self.delAccBTN.setObjectName("delAccBTN")
        self.horizontalLayout_3.addWidget(self.delAccBTN)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label)
        self.editAccountName = QtGui.QLineEdit(self.centralwidget)
        self.editAccountName.setObjectName("editAccountName")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.editAccountName)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_2)
        self.editUrl = QtGui.QLineEdit(self.centralwidget)
        self.editUrl.setObjectName("editUrl")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.editUrl)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_5)
        self.editUserName = QtGui.QLineEdit(self.centralwidget)
        self.editUserName.setObjectName("editUserName")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.editUserName)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout.setLayout(10, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout.setLayout(16, QtGui.QFormLayout.LabelRole, self.horizontalLayout)
        self.editPassword = QtGui.QLineEdit(self.centralwidget)
        self.editPassword.setEnabled(True)
        self.editPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.editPassword.setObjectName("editPassword")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.editPassword)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_3)
        self.accSavePWcheckBox = QtGui.QCheckBox(self.centralwidget)
        self.accSavePWcheckBox.setObjectName("accSavePWcheckBox")
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.accSavePWcheckBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.FinishedBTN = QtGui.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/success_transparent.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FinishedBTN.setIcon(icon3)
        self.FinishedBTN.setObjectName("FinishedBTN")
        self.verticalLayout_3.addWidget(self.FinishedBTN)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Viur Accountmanager", None, QtGui.QApplication.UnicodeUTF8))
        self.addAccBTN.setText(QtGui.QApplication.translate("MainWindow", "New Account", None, QtGui.QApplication.UnicodeUTF8))
        self.delAccBTN.setText(QtGui.QApplication.translate("MainWindow", "Delete Account", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Account Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Serveradress", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Userpassword", None, QtGui.QApplication.UnicodeUTF8))
        self.accSavePWcheckBox.setText(QtGui.QApplication.translate("MainWindow", "Save Password", None, QtGui.QApplication.UnicodeUTF8))
        self.FinishedBTN.setText(QtGui.QApplication.translate("MainWindow", "Back to Loginscreen", None, QtGui.QApplication.UnicodeUTF8))

