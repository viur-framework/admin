# -*- coding: utf-8 -*-
from viur_admin.event import event
from viur_admin.bones.relational import RelationalViewBoneDelegate, RelationalEditBone, RelationalBoneSelector
from viur_admin.widgets.hierarchy import HierarchyWidget
from viur_admin.priorityqueue import editBoneSelector


class HierarchyItemViewBoneDelegate(RelationalViewBoneDelegate):
	pass


class HierarchyItemBone(RelationalEditBone):
	def onAddBtnReleased(self, *args, **kwargs):
		editWidget = HierarchyBoneSelector(self.modulName, self.boneName, self.multiple, self.toModul, self.selection)
		editWidget.selectionChanged.connect(self.setSelection)

	def installAutoCompletion(self):
		"""
			Prevent installing an autoCompletion for this modul (not implementet yet)
		"""
		if not self.multiple:
			self.entry.setReadOnly(True)


class HierarchyBoneSelector(RelationalBoneSelector):
	displaySourceWidget = HierarchyWidget

	def onSourceItemDoubleClicked(self, item):
		"""
			An item has been doubleClicked in our listWidget.
			Read its properties and add them to our selection.
		"""
		data = item.entryData
		if self.multiple:
			self.selection.extend([data])
		else:
			self.selectionChanged.emit([data])
			event.emit("popWidget", self)


def CheckForHierarchyItemBone(modulName, boneName, skelStucture):
	return (skelStucture[boneName]["type"].startswith("hierarchy."))


editBoneSelector.insert(1, CheckForHierarchyItemBone, HierarchyItemBone)
