# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hierarchySelector.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HierarchySelector(object):
    def setupUi(self, HierarchySelector):
        HierarchySelector.setObjectName("HierarchySelector")
        HierarchySelector.resize(1041, 599)
        self.verticalLayout = QtWidgets.QVBoxLayout(HierarchySelector)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hierarchyWidget = QtWidgets.QWidget(HierarchySelector)
        self.hierarchyWidget.setObjectName("hierarchyWidget")
        self.verticalLayout.addWidget(self.hierarchyWidget)
        self.lblSelected = QtWidgets.QLabel(HierarchySelector)
        self.lblSelected.setObjectName("lblSelected")
        self.verticalLayout.addWidget(self.lblSelected)
        self.listSelected = QtWidgets.QWidget(HierarchySelector)
        self.listSelected.setObjectName("listSelected")
        self.verticalLayout.addWidget(self.listSelected)
        self.btnSelect = QtWidgets.QPushButton(HierarchySelector)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":icons/actions/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSelect.setIcon(icon)
        self.btnSelect.setObjectName("btnSelect")
        self.verticalLayout.addWidget(self.btnSelect)

        self.retranslateUi(HierarchySelector)
        QtCore.QMetaObject.connectSlotsByName(HierarchySelector)

    def retranslateUi(self, HierarchySelector):
        _translate = QtCore.QCoreApplication.translate
        HierarchySelector.setWindowTitle(_translate("HierarchySelector", "Form"))
        self.lblSelected.setText(_translate("HierarchySelector", "Selected:"))
        self.btnSelect.setText(_translate("HierarchySelector", "Apply"))

import viur_admin.ui.icons_rc
