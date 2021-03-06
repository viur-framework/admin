#!/usr/bin/env python3
import hashlib
import os
import shutil
import sys
import zipfile
from tempfile import NamedTemporaryFile
from typing import Any, List

from PyQt5 import QtCore, QtWidgets

from network import NetworkService
from ui.updaterUI import Ui_Updater
from utils import Overlay

# Fixing the path
cwd = os.getcwd()
prgc = sys.argv[0]

if prgc.startswith("/") or prgc[1] == ":":
	path = os.path.dirname(prgc)
else:
	path = os.path.abspath(os.path.dirname(os.path.join(cwd, prgc)))
os.chdir(path)

"""
ViUR Admin Updater

Copyright 2012 Mausbrand Informationssysteme GmbH
Licensed under GPL Version 3.
http://www.gnu.org/licenses/gpl-3.0

http://www.viur.is

Note:	Wherever the underlying OS provides an updatemechanism,
		it should be preferred instead of this script.
"""


class Updater(QtWidgets.QMainWindow):
	baseURL = "https://viur-site.appspot.com"

	def __init__(self, *args: Any, **kwargs: Any):
		super(Updater, self).__init__(*args, **kwargs)
		self.log: List[str] = list()
		self.targetVersion: float = 0.0  # Version, to witch can be upgraded
		self.targetDL = None  # Download-Key of the file for our OS-Arch
		self.ui = Ui_Updater()
		self.ui.setupUi(self)
		self.ui.btnUpdate.hide()
		self.ui.btnExit.hide()
		self.ui.progressBar.setValue(0)
		self.overlay = Overlay(self.ui.label)
		if os.path.isdir(os.path.join(os.getcwd(), "oldData")):
			shutil.rmtree(os.path.join(os.getcwd(), "oldData"))
		os.mkdir(os.path.join(os.getcwd(), "oldData"))

	def on_btnCheck_released(self) -> None:
		self.ui.btnCheck.setEnabled(False)
		self.checkUpdate()

	def on_btnUpdate_released(self) -> None:
		self.ui.btnUpdate.setEnabled(False)
		self.update()

	def on_btnExit_released(self) -> None:
		sys.exit(0)

	def onDownloadProgress(self, recv: Any, total: Any) -> None:
		self.ui.progressBar.setRange(0, total)
		self.ui.progressBar.setValue(recv)

	def getPlattform(self) -> str:
		isSourceDistribution = False
		try:
			open("admin.py", "r").read()
			isSourceDistribution = True
		except:
			pass
		if isSourceDistribution:
			return "source"
		pf = sys.platform
		if pf.startswith("linux"):
			pf = "linux"
		elif pf.startswith("darwin"):
			pf = "darwin"
		elif pf.startswith("win32"):
			pf = "win32"
		return pf

	def checkUpdate(self) -> None:
		self.overlay.inform(self.overlay.BUSY, "Prüfe")
		self.addLog(QtCore.QCoreApplication.translate("Updater", "Searching for updates"))
		self.req = NetworkService.request(self.baseURL + "/json/adminversion/list?orderby=version&orderdir=1&limit=5")
		self.req.finished.connect(self.onCheckUpdate)

	def onCheckUpdate(self) -> None:
		data = NetworkService.decode(self.req)
		self.req.deleteLater()
		try:
			currentVersion = float(open("version.dat", "r").read())
		except:
			currentVersion = 0.0
		needsUpdate = False
		for skel in data["skellist"]:
			rev = float(skel["version"])
			if rev > currentVersion:
				if not self.targetVersion or self.targetVersion < rev:
					fn = "%sfile" % self.getPlattform()
					if fn in skel and skel[fn]:
						self.targetVersion = rev
						self.targetDL = skel[fn]["dlkey"]
						self.addLog("%s: %s" % (rev, skel["changelog"]))
						needsUpdate = True
		if needsUpdate:
			self.showUpdateBtn()
			self.addLog(QtCore.QCoreApplication.translate("Updater", "Updates avaiable. Ready to upgrade."))
		else:
			self.showExitBtn()
			self.addLog(QtCore.QCoreApplication.translate("Updater", "There is no new version avaiable."))
		self.overlay.clear()

	def update(self) -> None:
		self.overlay.inform(self.overlay.BUSY, "Prüfe")
		self.addLog("Download...")
		self.req = NetworkService.request(self.baseURL + "/file/view/%s/admin.update" % (self.targetDL))
		self.req.downloadProgress.connect(self.onDownloadProgress)
		self.req.finished.connect(self.onDownloadComplete)

	def onDownloadComplete(self) -> None:
		tempfile = NamedTemporaryFile()
		tempfile.write(self.req.readAll())
		self.req.deleteLater()
		tempfile.seek(0)
		zipFile = zipfile.ZipFile(tempfile)
		for name in zipFile.namelist():
			if not os.path.abspath(os.path.join(os.getcwd(), name)).startswith(os.getcwd()):
				self.addLog(QtCore.QCoreApplication.translate("Updater",
				                                              "Securityviolation inside the update!!! Update aborted!"))
				return
			self.addLog(QtCore.QCoreApplication.translate("Updater", "Extracting: %s") % name)
		zipFile.extractall(os.path.join(os.getcwd(), "currUpdate"))
		for (dirName, dirs, files) in os.walk(os.path.join(os.getcwd(), "currUpdate")):
			currSubDir = dirName.replace(os.path.join(os.getcwd(), "currUpdate"), ".")
			for subDir in dirs:
				s = os.path.join(os.getcwd(), currSubDir, subDir)
				if not os.path.isdir(s):
					os.mkdir(s)
			for file in files:
				targetFile = os.path.join(os.getcwd(), currSubDir, file)
				srcFile = os.path.join(dirName, file)
				if self.getPlattform() == "win32":  # Fu...
					# Its impossible on Windows to delete a file currently in use
					# What we can is renameing (moving the file out of the way)
					if os.path.isfile(targetFile):
						idx = 0
						tmpFname = hashlib.md5((srcFile + str(idx)).encode("UTF-8")).hexdigest()
						while (os.path.isfile(os.path.join(os.getcwd(), "oldData", tmpFname))):
							idx += 1
							tmpFname = hashlib.md5((srcFile + str(idx)).encode("UTF-8")).hexdigest()
						os.rename(targetFile, os.path.join(os.getcwd(), "oldData", tmpFname))
					shutil.move(srcFile, targetFile)
				else:
					if os.path.isfile(targetFile):
						os.remove(targetFile)
					shutil.move(srcFile, targetFile)
		self.addLog(QtCore.QCoreApplication.translate("Updater", "Update successful"))
		open("version.dat", "w+").write(str(self.targetVersion))
		self.showExitBtn()
		self.overlay.clear()

	def showExitBtn(self) -> None:
		self.ui.btnCheck.hide()
		self.ui.btnUpdate.hide()
		self.ui.btnExit.show()

	def showUpdateBtn(self) -> None:
		self.ui.btnCheck.hide()
		self.ui.btnExit.hide()
		self.ui.btnUpdate.show()

	def addLog(self, message: str) -> None:
		self.log.append(message)
		self.ui.textLog.setPlainText("\n".join(self.log))
		self.ui.textLog.verticalScrollBar().setValue(self.ui.textLog.verticalScrollBar().maximum())


app = QtCore.QApplication(sys.argv)
updater = Updater()
updater.show()
app.exec_()
