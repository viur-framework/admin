# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from viur_admin.utils import Overlay
from viur_admin.network import NetworkService
from viur_admin.event import event
import viur_admin.utils
from viur_admin.config import conf
from viur_admin.widgets.edit import EditWidget
from viur_admin.priorityqueue import protocolWrapperInstanceSelector, actionDelegateSelector
from viur_admin.ui.hierarchyUI import Ui_Hierarchy
from viur_admin.utils import WidgetHandler


class HierarchyAddAction(QtWidgets.QAction):
    def __init__(self, parent, *args, **kwargs):
        super(HierarchyAddAction, self).__init__(QtGui.QIcon(":icons/actions/add.svg"),
                                                 QtCore.QCoreApplication.translate("Hierarchy", "Add entry"), parent)
        self.triggered.connect(self.onTriggered)
        self.setShortcut(QtGui.QKeySequence.New)
        self.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)

    def onTriggered(self):
        # config = conf.serverConfig["modules"][ self.parent().modul ]
        modul = self.parent().getModul()
        node = self.parent().hierarchy.rootNode
        widget = lambda: EditWidget(modul, EditWidget.appHierarchy, 0, node=node)
        handler = WidgetHandler(widget, descr=QtCore.QCoreApplication.translate("Hierarchy", "Add entry"),
                                icon=QtGui.QIcon(":icons/actions/add.svg"))
        handler.stackHandler()

    # event.emit( QtCore.SIGNAL('stackHandler(PyQt_PyObject)'), handler )

    @staticmethod
    def isSuitableFor(modul, actionName):
        return ( (modul == "hierarchy" or modul.startswith("hierarchy.")) and actionName == "add")


actionDelegateSelector.insert(1, HierarchyAddAction.isSuitableFor, HierarchyAddAction)


class HierarchyEditAction(QtWidgets.QAction):
    def __init__(self, parent, *args, **kwargs):
        super(HierarchyEditAction, self).__init__(QtGui.QIcon(":icons/actions/edit.svg"),
                                                  QtCore.QCoreApplication.translate("Hierarchy", "Edit entry"), parent)
        self.triggered.connect(self.onTriggered)
        self.setShortcut(QtGui.QKeySequence.Open)
        self.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)

    def onTriggered(self):
        parent = self.parent()
        for item in parent.hierarchy.selectedItems():
            modul = self.parent().getModul()
            key = item.entryData["id"]
            widget = lambda: EditWidget(modul, EditWidget.appHierarchy, key)
            handler = WidgetHandler(widget, descr=QtCore.QCoreApplication.translate("Hierarchy", "Edit entry"),
                                    icon=QtGui.QIcon(":icons/actions/edit.svg"))
            handler.stackHandler()
        # event.emit( QtCore.SIGNAL('stackHandler(PyQt_PyObject)'), handler )

    @staticmethod
    def isSuitableFor(modul, actionName):
        return ( (modul == "hierarchy" or modul.startswith("hierarchy.")) and actionName == "edit")


actionDelegateSelector.insert(1, HierarchyEditAction.isSuitableFor, HierarchyEditAction)


class HierarchyDeleteAction(QtWidgets.QAction):
    def __init__(self, parent, *args, **kwargs):
        super(HierarchyDeleteAction, self).__init__(QtGui.QIcon(":icons/actions/delete.svg"),
                                                    QtCore.QCoreApplication.translate("Hierarchy", "Delete entry"),
                                                    parent)
        self.triggered.connect(self.onTriggered)
        self.setShortcut(QtGui.QKeySequence.Delete)
        self.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)


    def onTriggered(self):
        parent = self.parent()
        for item in parent.hierarchy.selectedItems():
            self.parent().hierarchy.requestDelete(item.entryData["id"])

    @staticmethod
    def isSuitableFor(modul, actionName):
        return ( (modul == "hierarchy" or modul.startswith("hierarchy.")) and actionName == "delete")


actionDelegateSelector.insert(1, HierarchyDeleteAction.isSuitableFor, HierarchyDeleteAction)