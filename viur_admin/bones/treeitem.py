# -*- coding: utf-8 -*-

from viur_admin.event import event
from viur_admin.bones.relational import RelationalViewBoneDelegate, RelationalEditBone, RelationalBoneSelector
from viur_admin.widgets.tree import TreeWidget
from viur_admin.widgets.selectedEntities import SelectedEntitiesWidget
from viur_admin.priorityqueue import editBoneSelector
from viur_admin.bones.bone_interface import BoneEditInterface


class TreeItemViewBoneDelegate(RelationalViewBoneDelegate):
	pass


class TreeItemBone(RelationalEditBone):
	skelType = "leaf"

	def onAddBtnReleased(self, *args, **kwargs):
		editWidget = TreeBoneSelector(self.moduleName, self.boneName, self.multiple, self.toModul, self.selection)
		editWidget.selectionChanged.connect(self.setSelection)

	def installAutoCompletion(self):
		"""
			Prevent installing an autoCompletion for this modul (not implementet yet)
		"""
		if not self.multiple:
			self.entry.setReadOnly(True)


class TreeSelectedEntities(SelectedEntitiesWidget):
	skelType = "leaf"


class TreeBoneSelector(RelationalBoneSelector):
	displaySourceWidget = TreeWidget
	displaySelectionWidget = TreeSelectedEntities

	def onSourceItemDoubleClicked(self, item):
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


def CheckForTreeItemBone(moduleName, boneName, skelStucture):
	return (skelStucture[boneName]["type"].startswith("treeitem."))


editBoneSelector.insert(1, CheckForTreeItemBone, TreeItemBone)
