# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extendedStringSearchPlugin.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.value1Label = QtWidgets.QLabel(Form)
        self.value1Label.setObjectName("value1Label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.value1Label)
        self.value1 = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value1.sizePolicy().hasHeightForWidth())
        self.value1.setSizePolicy(sizePolicy)
        self.value1.setObjectName("value1")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.value1)
        self.value2Label = QtWidgets.QLabel(Form)
        self.value2Label.setObjectName("value2Label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.value2Label)
        self.value2 = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value2.sizePolicy().hasHeightForWidth())
        self.value2.setSizePolicy(sizePolicy)
        self.value2.setObjectName("value2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.value2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        Form.setTitle(_translate("Form", "Filter Name"))
        self.value1Label.setText(_translate("Form", "Value 1"))
        self.value2Label.setText(_translate("Form", "Value 2"))
