# -*- coding: utf-8 -*-

from typing import List, Dict, Any

from PyQt5 import QtWidgets

from viur_admin.log import getLogger

logger = getLogger(__name__)

from viur_admin.bones.relational import RelationalViewBoneDelegate, RelationalEditBone, RelationalBoneSelector
from viur_admin.event import event
from viur_admin.priorityqueue import editBoneSelector, viewDelegateSelector
from viur_admin.widgets.selectedEntities import SelectedEntitiesWidget
from viur_admin.widgets.tree import TreeWidget


class TreeItemViewBoneDelegate(RelationalViewBoneDelegate):
	pass


class TreeItemBone(RelationalEditBone):
	skelType = "leaf"

	def onAddBtnReleased(self, *args: Any, **kwargs: Any) -> None:
		editWidget = TreeBoneSelector(
			self.moduleName, self.boneName, self.multiple, self.toModule, self.selection)
		editWidget.selectionChanged.connect(self.setSelection)

	def installAutoCompletion(self) -> None:
		"""
			Prevent installing an autoCompletion for this module (not implementet yet)
		"""
		if not self.multiple:
			self.entry.setReadOnly(True)


class TreeSelectedEntities(SelectedEntitiesWidget):
	skelType = "leaf"


class TreeBoneSelector(RelationalBoneSelector):
	displaySourceWidget = TreeWidget
	displaySelectionWidget = TreeSelectedEntities

	def onSourceItemDoubleClicked(self, item: QtWidgets.QListWidgetItem) -> None:
		"""
			An item has been doubleClicked in our listWidget.
			Read its properties and add them to our selection.
		"""
		if not isinstance(item, self.list.getLeafItemClass()):
			return
		data = item.entryData
		if self.multiple:
			self.selection.extend([data])
		else:
			self.selectionChanged.emit([data])
			event.emit("popWidget", self)


def CheckForTreeItemBone(
		moduleName: str,
		boneName: str,
		skelStucture: Dict[str, Any]) -> bool:
	return skelStucture[boneName]["type"].startswith("relational.treeitem.")


editBoneSelector.insert(2, CheckForTreeItemBone, TreeItemBone)
viewDelegateSelector.insert(2, CheckForTreeItemBone, TreeItemViewBoneDelegate)
