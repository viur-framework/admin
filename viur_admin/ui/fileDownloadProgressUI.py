# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileDownloadProgress.ui'
#
# Created by: PyQt5 UI code generator 5.12.dev1812231618
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileDownloadProgress(object):
    def setupUi(self, FileDownloadProgress):
        FileDownloadProgress.setObjectName("FileDownloadProgress")
        FileDownloadProgress.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FileDownloadProgress)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(FileDownloadProgress)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.pbarTotal = QtWidgets.QProgressBar(FileDownloadProgress)
        self.pbarTotal.setProperty("value", 24)
        self.pbarTotal.setObjectName("pbarTotal")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pbarTotal)
        self.verticalLayout.addLayout(self.formLayout)
        self.lblProgress = QtWidgets.QLabel(FileDownloadProgress)
        self.lblProgress.setObjectName("lblProgress")
        self.verticalLayout.addWidget(self.lblProgress)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(124, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnCancel = QtWidgets.QPushButton(FileDownloadProgress)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)

        self.retranslateUi(FileDownloadProgress)
        QtCore.QMetaObject.connectSlotsByName(FileDownloadProgress)

    def retranslateUi(self, FileDownloadProgress):
        _translate = QtCore.QCoreApplication.translate
        FileDownloadProgress.setWindowTitle(_translate("FileDownloadProgress", "Form"))
        self.label.setText(_translate("FileDownloadProgress", "ProgressTotal"))
        self.lblProgress.setText(_translate("FileDownloadProgress", "Progress"))
        self.btnCancel.setText(_translate("FileDownloadProgress", "Cancel"))

