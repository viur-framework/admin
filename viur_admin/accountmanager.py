from PyQt5 import QtCore, QtGui, QtWidgets

from viur_admin.log import getLogger

logger = getLogger(__name__)
from viur_admin.config import conf
from viur_admin.event import event
from viur_admin.ui.accountmanagerUI import Ui_MainWindow

"""
	Allows editing the local accountlist.
"""


class AccountItem(QtWidgets.QListWidgetItem):
	def __init__(self, account, *args, **kwargs):
		super(AccountItem, self).__init__(QtGui.QIcon(":icons/profile.png"), account["name"], *args, **kwargs)
		self.account = account

	def update(self, accountData):
		self.account = accountData
		self.setText(self.account["name"])


class Accountmanager(QtWidgets.QMainWindow):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.loadAccountList()
		self.oldAccountName = None
		self.ui.addAccBTN.released.connect(self.onAddAccBTNReleased)
		self.ui.acclistWidget.itemClicked.connect(self.onAcclistWidgetItemClicked)
		self.ui.delAccBTN.released.connect(self.onDelAccBTNReleased)
		self.ui.editAccountName.textChanged.connect(self.onEditAccountNameTextChanged)
		self.ui.editUserName.textChanged.connect(self.onEditUserNameTextChanged)
		self.ui.editPassword.textChanged.connect(self.onEditPasswordTextChanged)
		self.ui.editUrl.textChanged.connect(self.onEditUrlTextChanged)
		self.ui.FinishedBTN.released.connect(self.onFinishedBTNReleased)
		if len(conf.accounts) == 0:
			self.onAddAccBTNReleased()

	def loadAccountList(self):
		guiList = self.ui.acclistWidget
		guiList.setIconSize(QtCore.QSize(128, 128))
		guiList.clear()
		currentPortalName = conf.adminConfig.get("currentPortalName")
		logger.debug("currentPortalName %r", currentPortalName)
		currentIndex = 0
		for ix, account in enumerate(conf.accounts):
			if account["name"] == currentPortalName:
				currentIndex = ix
			item = AccountItem(account)
			guiList.addItem(item)
		if len(conf.accounts) > 0:
			guiList.setCurrentRow(ix)
			self.onAcclistWidgetItemClicked(None)

	def closeEvent(self, e):
		conf.accounts = []
		for itemIndex in range(0, self.ui.acclistWidget.count()):
			conf.accounts.append(self.ui.acclistWidget.item(itemIndex).account)
		conf.saveConfig()
		event.emit("accountListChanged()")
		self.close()

	def onAddAccBTNReleased(self):
		guiList = self.ui.acclistWidget
		item = AccountItem(
				{
					"name": QtCore.QCoreApplication.translate("Accountmanager", "New"),
					"user": "", "password": "",
					"url": ""
				}
		)
		guiList.addItem(item)
		guiList.setCurrentItem(item)
		self.updateUI()

	def onAcclistWidgetItemClicked(self, clickeditem):
		self.updateUI()

	def onDelAccBTNReleased(self):
		item = self.ui.acclistWidget.currentItem()
		if not item:
			return
		reply = QtWidgets.QMessageBox.question(
				self,
				QtCore.QCoreApplication.translate("Accountmanager", "Account deletion"),
				QtCore.QCoreApplication.translate("Accountmanager",
				                                  "Really delete the account \"%s\"?") %
				item.account["name"],
				QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
				QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.No:
			return
		self.ui.acclistWidget.takeItem(self.ui.acclistWidget.row(item))
		self.updateUI()

	def updateUI(self):
		item = self.ui.acclistWidget.currentItem()
		self.ui.acclistWidget.sortItems()
		if not item:
			self.ui.editAccountName.setText("")
			self.ui.editUrl.setText("")
			self.ui.editUserName.setText("")
			self.ui.editPassword.setText("")
			self.ui.editAccountName.setEnabled(False)
			self.ui.editUrl.setEnabled(False)
			self.ui.editUserName.setEnabled(False)
			self.ui.editPassword.setEnabled(False)
			self.ui.delAccBTN.setEnabled(False)
		else:
			self.ui.editAccountName.blockSignals(True)
			self.ui.editUrl.blockSignals(True)
			self.ui.editUserName.blockSignals(True)
			self.ui.editPassword.blockSignals(True)
			self.ui.editAccountName.setText(item.account["name"])
			self.oldAccountName = item.account["name"]
			self.ui.editUrl.setText(item.account["url"])
			self.ui.editUserName.setText(item.account["user"])
			self.ui.editPassword.setText(item.account["password"])
			self.ui.editAccountName.setEnabled(True)
			self.ui.editUrl.setEnabled(True)
			self.ui.editUserName.setEnabled(True)
			self.ui.editPassword.setEnabled(True)
			self.ui.delAccBTN.setEnabled(True)
			self.ui.editAccountName.blockSignals(False)
			self.ui.editUrl.blockSignals(False)
			self.ui.editUserName.blockSignals(False)
			self.ui.editPassword.blockSignals(False)
			if item.account["password"] != "":
				self.ui.accSavePWcheckBox.setCheckState(QtCore.Qt.Checked)

	def onAccSavePWcheckBoxStateChanged(self, state):
		self.ui.editPassword.setEnabled(state)
		if state == 0:
			self.ui.editPassword.setText("")

	def saveAccount(self):
		item = self.ui.acclistWidget.currentItem()
		if not item:
			return
		url = self.ui.editUrl.text()
		url = url.rstrip("/")
		if url.find("http") == -1:
			url = "https://" + url
		if url.find("/admin") == -1:
			url += "/admin"
		account = {
			"name": self.ui.editAccountName.text(),
			"user": self.ui.editUserName.text(),
			"password": self.ui.editPassword.text(),
			"url": url
		}
		cpn = conf.adminConfig.get("currentPortalName")
		name = account["name"]
		if cpn == self.oldAccountName:
			self.oldAccountName = conf.adminConfig["currentPortalName"] = name
			conf.saveConfig()
		item.update(account)

	def onEditAccountNameTextChanged(self):
		self.saveAccount()

	def onEditUserNameTextChanged(self):
		self.saveAccount()

	def onEditPasswordTextChanged(self):
		self.saveAccount()

	def onEditUrlTextChanged(self):
		self.saveAccount()

	def onFinishedBTNReleased(self):
		conf.accounts = []
		for itemIndex in range(0, self.ui.acclistWidget.count()):
			conf.accounts.append(self.ui.acclistWidget.item(itemIndex).account)
		event.emit("accountListChanged")
		self.close()
