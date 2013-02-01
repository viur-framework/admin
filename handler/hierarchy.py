# -*- coding: utf-8 -*-
from ui.hierarchyUI import Ui_Hierarchy
from PyQt4 import QtCore, QtGui
from network import NetworkService
from event import event
from config import conf
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
from time import sleep, time
import sys, os, os.path
from utils import RegisterQueue, Overlay,  formatString
from mainwindow import EntryHandler, WidgetHandler
from widgets.hierarchy import HierarchyWidget
from widgets.edit import EditWidget

class HierarchyItem(QtGui.QTreeWidgetItem):
	def __init__( self, data ):
		if "name" in data.keys():
			name = data["name"]
		else:
			name = "---"
		super( HierarchyItem, self ).__init__( [str( name )] )
		self.loaded = False
		self.data = data
		self.setChildIndicatorPolicy( QtGui.QTreeWidgetItem.ShowIndicator )

	def __gt__( self, other ):
		if isinstance( other, HierarchyItem ) and "sortindex" in self.data.keys() and "sortindex" in other.data.keys():
			return( self.data["sortindex"] > other.data["sortindex"] )
		else:
			return( super( HierarchyItem, self ).__gt__( other ) )

	def __lt__( self, other ):
		if isinstance( other, HierarchyItem ) and "sortindex" in self.data.keys() and "sortindex" in other.data.keys():
			return( self.data["sortindex"] < other.data["sortindex"] )
		else:
			return( super( HierarchyItem, self ).__lt__( other ) )


class HierarchyList( QtGui.QWidget ):
	
	def __init__(self, modul, repoID=None, *args, **kwargs ):
		self.modul = modul
		self.page = 0
		self.rootNodes = {}
		config = conf.serverConfig["modules"][ modul ]
		self.currentRootNode = None
		self.isSorting=False
		self.path = []
		self.request = None
		if not "ui" in dir( self ):
			QtGui.QWidget.__init__( self, *args, **kwargs )
			self.ui = Ui_Hierarchy()
			self.ui.setupUi( self )
			layout = QtGui.QHBoxLayout( self.ui.treeWidget )
			self.ui.treeWidget.setLayout( layout )
			self.hierarchy = HierarchyWidget( self.ui.treeWidget, self.modul )
			layout.addWidget( self.hierarchy )
			#self.ui.treeWidget.addChild( self.hierarchy )
			self.hierarchy.show()
			self.toolBar = QtGui.QToolBar( self )
			self.toolBar.setIconSize( QtCore.QSize( 32, 32 ) )
			queue = RegisterQueue()
			event.emit( QtCore.SIGNAL('requestHierarchyListActions(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), queue, self.modul, self )
			for item in queue.getAll():
				i = item( self )
				if isinstance( i, QtGui.QAction ):
					self.toolBar.addAction( i )
				else:
					self.toolBar.addWidget( i )
			self.ui.boxActions.addWidget( self.toolBar )
		self.overlay = Overlay( self )
		#event.emit( QtCore.SIGNAL('addHandlerWidget(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), self, config["name"], None )
		#if not repoID:
		#	self.loadRootNodes()
		#else:
		#	self.setRootNode( repoID )
		self.setAcceptDrops( True )
		#self.connect( event, QtCore.SIGNAL('dataChanged(PyQt_PyObject,PyQt_PyObject)'),self.doReloadData )
		self.ui.webView.hide()
		self.connect( self.hierarchy, QtCore.SIGNAL("onItemClicked(PyQt_PyObject)"), self.onItemClicked )
		self.connect( self.hierarchy, QtCore.SIGNAL("onItemDoubleClicked(PyQt_PyObject)"), self.onItemDoubleClicked )


	def onItemClicked( self, item ):
		"""
			A item has been selected. If we have a previewURL -> show it
		"""
		config = conf.serverConfig["modules"][ self.modul ]
		if "previewURL" in config.keys():
			previewURL = config["previewURL"].replace("{{id}}",item["id"])
			if not previewURL.lower().startswith("http"):
				previewURL = NetworkService.url.replace("/admin","")+previewURL
			self.loadPreview( previewURL )

	def onItemDoubleClicked(self, item ):
		"""
			Open a editor for this entry.
		"""
		widget = EditWidget(self.modul, EditWidget.appHierarchy, item["id"] )
		handler = WidgetHandler( self.modul, widget )
		event.emit( QtCore.SIGNAL('addHandler(PyQt_PyObject)'), handler )

	def loadPreview( self, url ):
		self.request = NetworkService.request( url )
		self.connect(self.request, QtCore.SIGNAL("finished()"), self.setHTML )
	
	def setHTML( self ):
		try: #This request might got canceled meanwhile..
			html = bytes( self.request.readAll() )
		except:
			return
		self.request.deleteLater()
		self.request= None
		self.ui.webView.setHtml( html.decode("UTF-8"), QtCore.QUrl( NetworkService.url.replace("/admin","") ) )
		self.ui.webView.show()


class HierarchyAddAction( QtGui.QAction ):
	def __init__(self, parent, *args, **kwargs ):
		super( HierarchyAddAction, self ).__init__(  QtGui.QIcon("icons/actions/add_small.png"), "Eintrag hinzufügen", parent )
		self.connect( self, QtCore.SIGNAL( "triggered(bool)"), self.onTriggered )
		self.setShortcut( QtGui.QKeySequence.New )
	
	def onTriggered( self, e ):
		config = conf.serverConfig["modules"][ self.parent().modul ]
		widget = EditWidget(self.parent().modul, EditWidget.appHierarchy, 0, rootNode=self.parent().hierarchy.currentRootNode)
		handler = WidgetHandler( self.parentWidget().modul, widget )
		event.emit( QtCore.SIGNAL('addHandler(PyQt_PyObject)'), handler )
		

class HierarchyDeleteAction( QtGui.QAction ):
	def __init__(self, parent, *args, **kwargs ):
		super( HierarchyDeleteAction, self ).__init__(  QtGui.QIcon("icons/actions/delete_small.png"), "Eintrag Löschen", parent )
		self.connect( self, QtCore.SIGNAL( "triggered(bool)"), self.onTriggered )
		self.setShortcut( QtGui.QKeySequence.Delete )
	
	def onTriggered( self, e ):
		parent = self.parent()
		for item in parent.hierarchy.selectedItems():
			config = conf.serverConfig["modules"][ self.parentWidget().modul ]
			if "formatstring" in config.keys():
				question = QtCore.QCoreApplication.translate("HierarchyHandler", "Delete entry %s and everything beneath?") % formatString( config["formatstring"],  item.data )
			else:
				question = QtCore.QCoreApplication.translate("HierarchyHandler", "Delete this entry and everything beneath?")
			res = QtGui.QMessageBox.question(	self.parentWidget(),
											QtCore.QCoreApplication.translate("HierarchyHandler", "Confirm delete"),
											question,
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No
										)
			if res == QtGui.QMessageBox.Yes:
				parent.hierarchy.delete( item.data["id"] )
			
class HierarchyEditAction( QtGui.QAction ):
	def __init__(self, parent, *args, **kwargs ):
		super( HierarchyEditAction, self ).__init__(  QtGui.QIcon("icons/actions/edit_small.png"), QtCore.QCoreApplication.translate("HierarchyHandler", "Edit entry"), parent )
		self.connect( self, QtCore.SIGNAL( "triggered(bool)"), self.onTriggered )
		self.setShortcut( "Return" )
	
	def onTriggered( self, e ):
		parent = self.parent()
		for item in parent.hierarchy.selectedItems():
			widget = EditWidget(parent.modul, EditWidget.appHierarchy, item.data["id"] )
			handler = WidgetHandler( parent.modul, widget  )
			event.emit( QtCore.SIGNAL('addHandler(PyQt_PyObject)'), handler )


class HierarchyRepoHandler( EntryHandler ):
	"""Class for holding one Repo-Entry within the modules-list"""
	def __init__( self, modul, repo, *args, **kwargs ):
		super( HierarchyRepoHandler, self ).__init__( modul, *args, **kwargs )	
		self.repo = repo
		self.setText(0, repo["name"] )

	def clicked( self ):
		if not self.widgets:
			self.addWidget( HierarchyList( self.modul, self.repo["key"]  ) )
		else:
			self.focus()


class HierarchyCoreHandler( EntryHandler ):
	"""Class for holding the main (module) Entry within the modules-list"""
	
	def __init__( self, modul,  *args, **kwargs ):
		super( HierarchyCoreHandler, self ).__init__( modul, *args, **kwargs )
		config = conf.serverConfig["modules"][ modul ]
		if config["icon"]:
			lastDot = config["icon"].rfind(".")
			smallIcon = config["icon"][ : lastDot ]+"_small"+config["icon"][ lastDot: ]
			if os.path.isfile( os.path.join( os.getcwd(), smallIcon ) ):
				self.setIcon( 0, QtGui.QIcon( smallIcon ) )
			else:
				self.setIcon( 0, QtGui.QIcon( config["icon"] ) )
		self.setText( 0, config["name"] )
		self.repos = []
		self.tmpObj = QtGui.QWidget()
		self.fetchTask = NetworkService.request("/%s/listRootNodes" % self.modul )
		self.tmpObj.connect(self.fetchTask, QtCore.SIGNAL("finished()"), self.setRepos) 

	def setRepos( self ):
		data = NetworkService.decode( self.fetchTask )
		self.fetchTask.deleteLater()
		self.fetchTask = None
		self.tmpObj.deleteLater()
		self.tmpObj = None
		self.repos = data
		if len( self.repos ) > 1:
			for repo in self.repos:
				d = HierarchyRepoHandler( self.modul, repo )
				self.addChild( d )

	def clicked( self ):
		if not self.widgets:
			self.addWidget( HierarchyList( self.modul ) )
		else:
			self.focus()


class HierarchyHandler( QtCore.QObject ):
	def __init__(self, *args, **kwargs ):
		QtCore.QObject.__init__( self, *args, **kwargs )
		self.connect( event, QtCore.SIGNAL('modulHandlerInitializion(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), self.initWidgetItem )
		self.connect( event, QtCore.SIGNAL('requestHierarchyListActions(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)') ,  self.requestHierarchyListActions )
		self.connect( event, QtCore.SIGNAL('requestModulHandler(PyQt_PyObject,PyQt_PyObject)'), self.requestModulHandler )

	def requestHierarchyListActions(self, queue, modul, parent ):
		config = conf.serverConfig["modules"][ modul ]
		if config and config["handler"]=="hierarchy":
			queue.registerHandler( 2, HierarchyAddAction )
			queue.registerHandler( 3, HierarchyEditAction )
			queue.registerHandler( 4, HierarchyDeleteAction )

	def requestModulHandler(self, queue, modul ):
		config = conf.serverConfig["modules"][ modul ]
		if( config["handler"]=="hierarchy" ):
			f = lambda: HierarchyCoreHandler( modul )
			queue.registerHandler( 5, f )

	def initWidgetItem(self, queue, modulName, config ):
		if( config["handler"]!="hierarchy"):
			return
		listOpener = lambda *args, **kwargs: self.openList( modulName, config )
		contextHandler = lambda *args, **kwargs: None 
		if not "icon" in config.keys():
			config["icon"]="icons/conesofticons/ihre_idee.png"
		res= {"name":config["name"], "icon":config["icon"], "functions":[
				{"name":"Alle Einträge", "icon":config["icon"],  "handler":listOpener, "contextHandler":contextHandler }
			], "defaulthandler":listOpener }
		queue.registerHandler(15,res)
	
	def openList(self, modulName, config ):
		if "name" in config.keys():
			name = config["name"]
		else:
			name = "Liste"
		if "icon" in config.keys():
			icon = config["icon"]
		else:
			icon = None
		event.emit( QtCore.SIGNAL('addHandlerWidget(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), HierarchyList( modulName, config ), name, icon )

_hierarchyHandler = HierarchyHandler()

