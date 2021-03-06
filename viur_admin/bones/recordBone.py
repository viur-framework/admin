# -*- coding: utf-8 -*-                                                                                                                                                                                                                                                        

import sys
from typing import Any, Dict, List, Union

from viur_admin.log import getLogger

logger = getLogger(__name__)

from collections import OrderedDict

from PyQt5 import QtCore, QtGui, QtWidgets
from viur_admin.bones.bone_interface import BoneEditInterface

from viur_admin.utils import formatString, Overlay
from viur_admin.priorityqueue import editBoneSelector, viewDelegateSelector
from viur_admin.bones.base import BaseViewBoneDelegate, LanguageContainer, MultiContainer
from viur_admin import config
from viur_admin.widgets.edit import collectBoneErrors
from viur_admin.bones.relational import InternalEdit


class BaseBone:
	pass


class RecordViewBoneDelegate(BaseViewBoneDelegate):
	cantSort = True

	def __init__(
			self,
			module: str,
			boneName: str,
			structure: Dict[str, Any]):
		super(RecordViewBoneDelegate, self).__init__(module, boneName, structure)
		logger.debug("RecordViewBoneDelegate.init: %r, %r, %r", module, boneName, structure[self.boneName])
		self.format = "$(name)"
		if "format" in structure[boneName]:
			self.format = structure[boneName]["format"]
		self.module = module
		self.structure = structure
		self.boneName = boneName

	def displayText(self, value: str, locale: QtCore.QLocale) -> str:
		logger.debug("RecordViewBoneDeleaget - value: %r, structure: %r", value, self.structure[self.boneName])
		relStructList = self.structure[self.boneName]["using"]
		try:
			if isinstance(value, list):
				if relStructList:
					# logger.debug("RecordViewBoneDelegate.displayText: %r, %r, %r", self.boneName, self.format, self.structure)
					value = "\n".join([(formatString(
						formatString(
							self.format,
							x, self.structure[self.boneName],
							language=config.conf.adminConfig["language"]),
						x, x, language=config.conf.adminConfig["language"]) or x[
						                    "key"]) for x in value])
				else:
					value = ", ".join([formatString(self.format, x, self.structure,
					                                language=config.conf.adminConfig["language"]) for x in value])
			elif isinstance(value, dict):
				value = formatString(
					formatString(self.format, value["dest"], self.structure[self.boneName]["relskel"], prefix=["dest"],
					             language=config.conf.adminConfig["language"]),
					value, value, language=config.conf.adminConfig["language"]) or value[
					        "key"]
		except Exception as err:
			logger.exception(err)
			# We probably received some garbage
			value = ""
		return value



class RecordEditBone(BoneEditInterface):
	GarbageTypeName = "RecordEditBone"
	skelType = None

	def __init__(
			self,
			moduleName: str,
			boneName: str,
			readOnly: bool,
			required: bool,
			multiple: bool,
			using: Dict[str, Any] = None,
			format: str="$(name)",
			*args: Any,
			**kwargs: Any):
		super(RecordEditBone, self).__init__(moduleName, boneName, readOnly, required, *args, **kwargs)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.setLayout(self.layout)
		logger.debug("RecordEditBone: %r, %r, %r", moduleName, boneName, readOnly)
		self.multiple = multiple
		self.using = using
		self.format = format
		self.overlay = Overlay(self)
		outerLayout = QtWidgets.QVBoxLayout(self.editWidget)
		self.internalEdit = InternalEdit(self.editWidget, self.using, "FIXME", {}, [])
		outerLayout.addWidget(self.internalEdit)


	@classmethod
	def fromSkelStructure(
			cls,
			moduleName: str,
			boneName: str,
			skelStructure: dict,
			**kwargs: Any) -> Any:
		#logger.debug("Recordbone.fromSkelStructure: %r, %r, %r", moduleName, boneName, skelStructure)
		myStruct = skelStructure[boneName]
		readOnly = "readonly" in skelStructure[boneName] and skelStructure[boneName]["readonly"]
		required = "required" in skelStructure[boneName] and skelStructure[boneName]["required"]
		widgetGen = lambda: cls(
			moduleName,
			boneName,
			readOnly,
			required,
			skelStructure[boneName]["multiple"],
			using=skelStructure[boneName]["using"],
			format=skelStructure[boneName].get("format", "$(name)")
		)
		if myStruct.get("multiple"):
			preMultiWidgetGen = widgetGen
			widgetGen = lambda: MultiContainer(preMultiWidgetGen)
		if myStruct.get("languages"):
			preLangWidgetGen = widgetGen
			widgetGen = lambda: LanguageContainer(myStruct["languages"], preLangWidgetGen)
		return widgetGen()


	def unserialize(self, data: Dict[str, Any], errors: List[Dict]) -> None:
		self.setErrors(errors)
		return self.internalEdit.unserialize(data, errors)

	def serializeForPost(self) -> dict:
		return self.internalEdit.serializeForPost()


def CheckForRecordBoneBone(
		moduleName: str,
		boneName: str,
		skelStucture: Dict[str, Any]) -> bool:
	return skelStucture[boneName]["type"] == "record" or skelStucture[boneName]["type"].startswith("record.")


# Register this Bone in the global queue
editBoneSelector.insert(2, CheckForRecordBoneBone, RecordEditBone)
viewDelegateSelector.insert(2, CheckForRecordBoneBone, RecordViewBoneDelegate)
