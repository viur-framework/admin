#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from time import time
from typing import Sequence, Union, Dict, List, Tuple, Any

from PyQt5 import QtCore, QtGui

from viur_admin.network import NetworkService, RequestGroup, RequestWrapper
from viur_admin.priorityqueue import protocolWrapperClassSelector, protocolWrapperInstanceSelector


class HierarchyWrapper(QtCore.QObject):
	maxCacheTime = 60  # Cache results for max. 60 Seconds
	updateDelay = 0  # 1,5 Seconds gracetime before reloading

	entitiesChanged = QtCore.pyqtSignal()
	childrenAvailable = QtCore.pyqtSignal((object,))  # A recently queried entity was fetched and is now avaiable
	entityAvailable = QtCore.pyqtSignal((object,))  # We recieved informations about that entry
	busyStateChanged = QtCore.pyqtSignal((bool,))  # If true, im busy right now
	updatingSucceeded = QtCore.pyqtSignal((str,))  # Adding/Editing an entry succeeded
	updatingFailedError = QtCore.pyqtSignal((str,))  # Adding/Editing an entry failed due to network/server error
	updatingDataAvailable = QtCore.pyqtSignal((str, dict, bool))  # Adding/Editing an entry failed due to missing fields
	modulStructureAvailable = QtCore.pyqtSignal()  # We fetched the structure for this module and that data is now
	# available
	rootNodesAvailable = QtCore.pyqtSignal()  # We fetched the list of rootNodes for this module and that data is now

	# avaiable

	def __init__(
			self,
			module: str,
			*args: Any,
			**kwargs: Any):
		super(HierarchyWrapper, self).__init__()
		self.module = module
		self.dataCache: Dict[str, Any] = {}
		self.rootNodes = None
		self.viewStructure = None
		self.addStructure = None
		self.editStructure = None
		self.busy = True
		self.deferredTaskQueue: Sequence[Tuple[str, str]] = []
		NetworkService.request("/%s/listRootNodes" % self.module, successHandler=self.onRootNodesAvailable)
		req = NetworkService.request("/getStructure/%s" % self.module, successHandler=self.onStructureAvailable)
		protocolWrapperInstanceSelector.insert(1, self.checkForOurModul, self)
		self.checkBusyStatus()

	def checkBusyStatus(self) -> None:
		QtGui.QGuiApplication.processEvents()
		QtCore.QCoreApplication.processEvents()
		busy = False
		for child in self.children():
			if (isinstance(child, RequestWrapper) or isinstance(child, RequestGroup)) and not child.hasFinished:
				busy = True
				break
		if busy != self.busy:
			self.busy = busy
			self.busyStateChanged.emit(busy)
		QtGui.QGuiApplication.processEvents()
		QtCore.QCoreApplication.processEvents()

	def checkForOurModul(self, moduleName: str) -> bool:
		return self.module == moduleName

	def onStructureAvailable(self, req: RequestWrapper) -> None:
		tmp = NetworkService.decode(req)
		if tmp is None:
			self.checkBusyStatus()
			return
		for stype, structlist in tmp.items():
			structure: OrderedDict = OrderedDict()
			for k, v in structlist:
				structure[k] = v
			if stype == "viewSkel":
				self.viewStructure = structure
			elif stype == "editSkel":
				self.editStructure = structure
			elif stype == "addSkel":
				self.addStructure = structure
		self.modulStructureAvailable.emit()
		self.checkBusyStatus()

	def onRootNodesAvailable(self, req: RequestWrapper) -> None:
		tmp = NetworkService.decode(req)
		if isinstance(tmp, list):
			self.rootNodes = tmp
		else:
			self.rootNodes = []
		self.rootNodesAvailable.emit()
		self.checkBusyStatus()

	def cacheKeyFromFilter(self, node: str, filters: dict) -> str:
		tmpList = list(filters.items())
		tmpList.append(("node", node))
		tmpList.sort(key=lambda x: x[0])
		return "&".join(["%s=%s" % (k, v) for (k, v) in tmpList])

	def queryData(self, node: str, **kwargs: Any) -> str:
		""" Fetches the *children* of that node
		:param node: the node id we should fetch childs from
		:type node: str
		:param kwargs: the filter parameters we use for that query
		:return: the cache key we use
		:rtype: str
		"""
		key = self.cacheKeyFromFilter(node, kwargs)
		if key in self.dataCache:
			self.deferredTaskQueue.append(("childrenAvailable", node))
			QtCore.QTimer.singleShot(25, self.execDeferred)
			return key
		# It's a cache-miss or cache too old
		r = NetworkService.request("/%s/list?skelType=node&parententry=%s" % (self.module, node), kwargs, successHandler=self.addCacheData)
		r.wrapperCbCacheKey = key
		r.node = node
		self.checkBusyStatus()
		return key

	def queryEntry(self, key: str) -> str:
		""" Fetches *that* specific entry, not its children
		:param key: the node id we should fetch
		:type key: str
		:return: the cache key we use - in this case it's the same as input arg 'key'
		:rtype: str
		"""
		if key in self.dataCache:
			QtCore.QTimer.singleShot(25, lambda *args, **kwargs: self.entityAvailable.emit(self.dataCache[key]))
			return key
		r = NetworkService.request("/%s/view/%s" % (self.module, key), successHandler=self.addCacheData)
		return key

	def execDeferred(self, *args: Any, **kwargs: Any) -> None:
		action, node = self.deferredTaskQueue.pop(0)
		if action == "childrenAvailable":
			self.childrenAvailable.emit(node)

	def doCallDeferred(self, *args: Any, **kwargs: Any) -> None:
		weakSelf, callName, fargs, fkwargs = self.deferredTaskQueue.pop(0)
		callFunc = weakSelf()
		if callFunc is not None:
			targetFunc = getattr(callFunc, callName)
			targetFunc(*fargs, **fkwargs)
		self.checkBusyStatus()

	def addCacheData(self, req: RequestWrapper) -> None:
		data = NetworkService.decode(req)
		cursor = None
		if "cursor" in data:
			cursor = data["cursor"]
		if data["action"] == "list":
			self.dataCache[req.wrapperCbCacheKey] = (time(), data["skellist"], cursor)
			for skel in data["skellist"]:
				self.dataCache[skel["key"]] = skel
			self.childrenAvailable.emit(req.node)
		elif data["action"] == "view":
			self.dataCache[data["values"]["key"]] = data["values"]
			self.entityAvailable.emit(data["values"])
		self.checkBusyStatus()

	def childrenForNode(self, node: str) -> str:
		assert isinstance(node, str)
		res = []
		for item in self.dataCache.values():
			if isinstance(item, dict):  # Its a "normal" item, not a customQuery result
				if item["parententry"] == node:
					res.append(item)
		return res

	def add(self, parent: QtCore.QObject = None, **kwargs: Any) -> str:
		tmp = {k: v for k, v in kwargs.items()}
		tmp["node"] = parent
		tmp["skelType"] = "node"
		req = NetworkService.request(
			"/%s/add/" % self.module, tmp, secure=(len(kwargs) > 0),
			finishedHandler=self.onSaveResult)
		if not kwargs:
			# This is our first request to fetch the data, dont show a missing hint
			req.wasInitial = True
		else:
			req.wasInitial = False
		self.checkBusyStatus()
		return str(id(req))

	def edit(self, key: str, **kwargs: Any) -> str:
		req = NetworkService.request(
			"/%s/edit?skelType=node&key=%s" % (self.module, key), kwargs, secure=(len(kwargs) > 0),
			finishedHandler=self.onSaveResult)
		if not kwargs:
			# This is our first request to fetch the data, don't show a missing hint
			req.wasInitial = True
		else:
			req.wasInitial = False
		self.checkBusyStatus()
		return str(id(req))

	def delete(self, keys: Union[Sequence[str], str]) -> None:
		if isinstance(keys, list):
			req = RequestGroup(finishedHandler=self.delayEmitEntriesChanged)
			for key in keys:
				r = NetworkService.request("/%s/delete?skelType=node&key=%s" % (self.module, key), secure=True)
				req.addQuery(r)
		else:  # We just delete one
			NetworkService.request(
				"/%s/delete?skelType=node&key=%s" % (self.module, keys), secure=True,
				finishedHandler=self.delayEmitEntriesChanged)
		self.checkBusyStatus()

	#def updateSortIndex(self, itemKey: str, newIndex: float) -> None:
	#	#self.request = NetworkService.request(
	#	#	"/%s/edit" % self.module, {"key": itemKey, "sortindex": newIndex, "skelType": "node"}, True,
	#	#	finishedHandler=self.delayEmitEntriesChanged)
	#	self.checkBusyStatus()

	def reparent(self, itemKey: str, destParent: str, sortIndex: int = None) -> None:
		data = {"key": itemKey, "parentNode": destParent, "skelType": "node"}
		if sortIndex is not None:
			data["sortindex"] = sortIndex
		NetworkService.request(
			"/%s/move" % self.module, data, True,
			finishedHandler=self.delayEmitEntriesChanged, parent=self)
		self.checkBusyStatus()

	def delayEmitEntriesChanged(self, *args: Any, **kwargs: Any) -> None:
		"""
			Give the GAE a chance to apply recent changes and then
			force all open views of that module to reload its data
		"""
		QtCore.QTimer.singleShot(self.updateDelay, self.emitEntriesChanged)
		self.checkBusyStatus()

	def onSaveResult(self, req: RequestWrapper) -> None:
		try:
			data = NetworkService.decode(req)
		except:  # Something went wrong, call ErrorHandler
			self.updatingFailedError.emit(str(id(req)))
			return
		if data["action"] in ["addSuccess", "editSuccess", "deleteSuccess"]:  # Saving succeeded
			QtCore.QTimer.singleShot(self.updateDelay, self.emitEntriesChanged)
			self.updatingSucceeded.emit(str(id(req)))
		else:  # There were missing fields
			self.updatingDataAvailable.emit(str(id(req)), data, req.wasInitial)
		self.checkBusyStatus()

	def emitEntriesChanged(self, *args: Any, **kwargs: Any) -> None:
		self.dataCache = {}
		# for k,v in self.dataCache.items():
		# Invalidate the cache. We don't clear that dict so that execDeferred calls don't fail
		# ctime, data, cursor = v
		# self.dataCache[ k ] = (1, data, cursor )
		self.entitiesChanged.emit()
		self.checkBusyStatus()


def CheckForHierarchyModul(moduleName: str, moduleList: dict) -> bool:
	modulData = moduleList[moduleName]
	if "handler" in modulData and (
			modulData["handler"] == "tree.nodeonly" or modulData["handler"].startswith("tree.nodeonly.")):
		return True
	return False


protocolWrapperClassSelector.insert(3, CheckForHierarchyModul, HierarchyWrapper)
